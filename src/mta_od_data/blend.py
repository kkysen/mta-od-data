"""A minimal reader for Blender's `.blend` files, enough for `lidar_model`.

Blender's own Python module (`bpy`) has no wheels for every platform this runs on,
so this reads the file format directly: a header,
then blocks of structs, each tagged with its type in the file's own catalog (SDNA),
which names every struct's fields, their types and array sizes.
Only uncompressed files saved by 64-bit little-endian Blender are read,
as Blender 4 saves by default.
"""

import re
import struct
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

# DNA type names to `struct` formats.
FORMATS = {
    "char": "b",
    "uchar": "B",
    "short": "h",
    "ushort": "H",
    "int": "i",
    "uint": "I",
    "float": "f",
    "double": "d",
    "int8_t": "b",
    "uint8_t": "B",
    "int64_t": "q",
    "uint64_t": "Q",
}
POINTER = 8


@dataclass(frozen=True, slots=True)
class Field:
    type: str
    # Its bare name, without `*`, `(*...)` or array sizes.
    name: str
    pointer: bool
    dims: tuple[int, ...]
    offset: int
    size: int


@dataclass(frozen=True, slots=True)
class Struct:
    name: str
    size: int
    fields: dict[str, Field]


@dataclass(frozen=True, slots=True)
class Block:
    code: bytes
    # Where its data starts in the file, and how long it is.
    start: int
    size: int
    # Its address when saved, which pointers to it hold.
    address: int
    struct: Struct
    count: int


@dataclass(frozen=True, slots=True)
class Value:
    """A struct inside another, read further by `Blend.get`."""

    struct: Struct
    start: int


class Blend:
    def __init__(self, path: Path) -> None:
        self.data = path.read_bytes()
        head = self.data[:12]
        if head[:7] != b"BLENDER":
            raise ValueError(f"{path}: not an uncompressed .blend file ({head!r})")
        if head[7:9] != b"-v":
            raise ValueError(f"{path}: not saved by 64-bit little-endian Blender")
        raw: list[tuple[bytes, int, int, int, int, int]] = []
        at = 12
        while at < len(self.data):
            code, size, address, sdna, count = struct.unpack_from(
                "<4siQii", self.data, at
            )
            at += 24
            code = code.rstrip(b"\0")
            if code == b"ENDB":
                break
            raw.append((code, at, size, address, sdna, count))
            if code == b"DNA1":
                self.structs = self._catalog(at)
            at += size
        self.blocks: dict[bytes, list[Block]] = defaultdict(list)
        self.at: dict[int, Block] = {}
        for code, start, size, address, sdna, count in raw:
            b = Block(code, start, size, address, self.structs[sdna], count)
            self.blocks[code].append(b)
            if address:
                self.at[address] = b
        self.by_name = {s.name: s for s in self.structs}

    def _catalog(self, start: int) -> list[Struct]:
        """The file's structs, from its DNA1 block,
        whose sections are aligned to 4 bytes from the block's start."""
        d = self.data
        at = start

        def align() -> None:
            nonlocal at
            at = start + ((at - start + 3) & ~3)

        def strings(tag: bytes) -> list[str]:
            nonlocal at
            assert d[at : at + 4] == tag, (tag, d[at : at + 4])
            (n,) = struct.unpack_from("<i", d, at + 4)
            at += 8
            out = []
            for _ in range(n):
                end = d.index(b"\0", at)
                out.append(d[at:end].decode())
                at = end + 1
            align()
            return out

        assert d[at : at + 4] == b"SDNA"
        at += 4
        names = strings(b"NAME")
        types = strings(b"TYPE")
        assert d[at : at + 4] == b"TLEN"
        lengths = struct.unpack_from(f"<{len(types)}h", d, at + 4)
        at += 4 + 2 * len(types)
        align()
        assert d[at : at + 4] == b"STRC"
        (n,) = struct.unpack_from("<i", d, at + 4)
        at += 8
        out = []
        for _ in range(n):
            t, nfields = struct.unpack_from("<hh", d, at)
            at += 4
            fields = {}
            offset = 0
            for _ in range(nfields):
                ft, fn = struct.unpack_from("<hh", d, at)
                at += 4
                full = names[fn]
                dims = tuple(int(m) for m in re.findall(r"\[(\d+)\]", full))
                pointer = full.startswith(("*", "(*"))
                count = 1
                for x in dims:
                    count *= x
                size = (POINTER if pointer else lengths[ft]) * count
                name = re.sub(r"[*()]|\[.*", "", full)
                fields[name] = Field(types[ft], name, pointer, dims, offset, size)
                offset += size
            out.append(Struct(types[t], lengths[t], fields))
        return out

    def get(
        self, where: Block | Value, path: str, index: int = 0
    ) -> int | float | str | tuple[float, ...] | Value:
        """A field of the `index`th struct in a block, or of a struct inside one,
        by a dotted path through structs inside it.
        Pointers are addresses, for `Blend.at`; char arrays are strings."""
        if isinstance(where, Block):
            s, at = where.struct, where.start + index * where.struct.size
        else:
            s, at = where.struct, where.start
        *outer, last = path.split(".")
        for name in outer:
            f = s.fields[name]
            s, at = self.by_name[f.type], at + f.offset
        f = s.fields[last]
        at += f.offset
        if f.pointer:
            return struct.unpack_from("<Q", self.data, at)[0]
        if f.type == "char" and f.dims:
            return self.data[at : at + f.size].split(b"\0")[0].decode()
        fmt = FORMATS.get(f.type)
        if fmt is None:
            return Value(self.by_name[f.type], at)
        count = f.size // struct.calcsize(fmt)
        values = struct.unpack_from(f"<{count}{fmt}", self.data, at)
        return values if f.dims else values[0]

    def integer(self, where: Block | Value, path: str, index: int = 0) -> int:
        v = self.get(where, path, index)
        assert isinstance(v, int), (path, v)
        return v

    def floats(self, where: Block | Value, path: str, index: int = 0) -> list[float]:
        v = self.get(where, path, index)
        assert isinstance(v, tuple), (path, v)
        return list(v)

    def text(self, where: Block | Value, path: str, index: int = 0) -> str:
        v = self.get(where, path, index)
        assert isinstance(v, str), (path, v)
        return v

    def bytes_at(self, address: int) -> bytes:
        b = self.at[address]
        return self.data[b.start : b.start + b.size]

    def chain(self, first: int, next_: str = "next") -> list[Block]:
        """A linked list's blocks, from its first's address."""
        out = []
        while first:
            b = self.at[first]
            out.append(b)
            first = self.integer(b, next_)
        return out
