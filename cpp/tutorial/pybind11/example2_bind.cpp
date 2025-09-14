#include <pybind11/pybind11.h>
#include "example2.hpp"

namespace py = pybind11;

PYBIND11_MODULE(example2, m, py::mod_gil_not_used()) {
    py::class_<Pet>(m, "Pet")
        .def(py::init<const std::string &>())
        .def("setName", &Pet::setName)
        .def("getName", &Pet::getName);
}