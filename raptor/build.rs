fn main() {
    // `cargo test`'s binary links `libpython` (an extension module doesn't),
    // and `uv`'s Python keeps it outside the loader's search path,
    // so record its directory in the binary.
    pyo3_build_config::add_libpython_rpath_link_args();
}
