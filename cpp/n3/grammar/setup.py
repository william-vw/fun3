from glob import glob
from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

src_files = glob("/Users/wvw/git/n3/fun3/cpp/n3/grammar/parser/*.cpp")
src_files.extend(['parse.cpp', 'parse_bind.cpp'])

ext_modules = [
    Pybind11Extension(
        'cppN3Parser',
        src_files,
        include_dirs=[ "/Users/wvw/git/lib/boost_1_89_0", "/Users/wvw/git/n3/fun3/cpp/n3/grammar/antlr4-runtime/" ], 
        library_dirs=[ "/Users/wvw/git/n3/fun3/cpp/n3/grammar/antlr4-cpp-runtime-macos/lib" ],
        libraries=[ "antlr4-runtime" ]
    ),
]

setup(
    name='cppN3Parser',
    version='0.1.0',
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)