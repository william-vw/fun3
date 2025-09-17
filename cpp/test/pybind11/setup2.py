from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        'example2',
        ['example2.cpp', 'example_bind2.cpp'],
    ),
]

setup(
    name='example2',
    version='0.1.0',
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)