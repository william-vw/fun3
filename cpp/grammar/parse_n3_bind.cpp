#include <pybind11/pybind11.h>
#include "parse_n3.hpp"

namespace py = pybind11;

PYBIND11_MODULE(n3Parser, m, py::mod_gil_not_used()) {
    m.doc() = "n3 parser"; // optional module docstring

    m.def("parse", &parse, "A function that parses an n3 file");
}
