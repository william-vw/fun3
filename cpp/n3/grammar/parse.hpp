#include <iostream>
#include <pybind11/pybind11.h>

using namespace std;
namespace py = pybind11;

double parse(string path, py::object &func);