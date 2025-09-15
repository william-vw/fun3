from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        'example',
        ['example.cpp', 'example_bind.cpp'],
    ),
]

setup(
    name='example',
    version='0.1.0',
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)