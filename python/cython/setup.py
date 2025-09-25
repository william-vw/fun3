from setuptools import setup
from Cython.Build import cythonize

setup(
    # ext_modules=cythonize(["primes.py", "primes_python_compiled.py"],
    #                       annotate=True), py_modules=["primes_python.py"]
    ext_modules=cythonize([ "ex1_it_cy.pyx", "ex1_it_py_compile.py" ], annotate=True)
)

# python setup.py build_ext --inplace
