#include <pybind11/pybind11.h>
#include "parse.hpp"

namespace py = pybind11;

PYBIND11_MODULE(cppN3Parser, m, py::mod_gil_not_used()) {
    m.doc() = "C++ N3 parser"; // optional module docstring

    m.def("parse", &parse, "A function that parses an n3 file");
}
