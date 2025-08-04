# fun3
Stands for **fun**ctions implementing **N3**, or, alternatively, **fun** with **N3**.

## Notation3 (N3)
For more on N3, checkout the [W3C Community Group report](https://w3c.github.io/N3/reports/20230703/) or the [N3 primer](https://notation3.org/).

## Implementation
Currently, there is only a Python implementation that also targets Python as the imperative language. This is located in the [`python`](python/) folder. Some very initial experimentation with Rust can be found in the [`rust`](rust/) folder.

[`python/requirements.txt`](python/requirements.txt): use this file to easily install fun3's dependencies.

[`python/n3/fun`](python/n3/fun) folder: contains the implementation of fun3.

- [`gen.py`](python/n3/fun/gen.py) implements the translation process.  
- [`builtins/`](python/n3/fun/builtins/) includes builtin implementations.
- Utility functions:  
  - [`py_build.py`](python/n3/fun/py_build.py) contains convenience methods to programmatically construct Python code.
  - [`utils.py`](python/n3/fun/utils.py) contains miscellaneous utility functions.

[`python/n3/`](python/n3/) folder:

- [`grammar/`](python/n3/grammar/) folder: contains the N3 grammar and an auto-generated parser implementation using [ANTLR4](https://www.antlr.org/). 

- [`model.py`](python/n3/model.py) implements two data stores:  
    - `ListModel`: simply keeps all triples in a list. When searching for matching triples, it simply iterates over this list. Used for debugging.
    - `MultiDictModel`: keeps `spo`, `pos`, and `osp` indicates for indexing triples. When searching for matching triples, it will use one of these indices.

- [`objects.py`](python/n3/objects.py) implements a series of abstractions for working with N3.

- [`parse.py`](python/n3/parse.py) relies on the ANTLR4 parser to parse N3 triples.

- [`to_py.py`](python/n3/to_py.py) will likely be your entry point into using fun3:  
    - The `run_py` function generates and runs Python code given a query, ruleset and dataset, and returns the results.  
    - The `save_py` function generates and saves the generated Python code given a query, ruleset and dataset.

[`lib/`](python/lib): contains utility functions for generated Python code:  
- [`emit.py`](python/lib/emit.py): instantiate and emit an N3 triple returned by the Python code as a query answer.
- [`trace.py`](python/lib/trace.py): a function that can be passed to `sys.settrace()` to print an execution trace of the Python functions.


## Testing

[`tests-bench/`](python/tests-bench/) folder: lists performance benchmarks.  

- [`zika/`](python/tests-bench/zika/) folder: keeps all artifacts related to the "Zika" benchmark. See the [README](python/tests-bench/zika/README.md) there for more.

[`tests-manifest/`](python/tests-manifest/) folder: lists a range of tests for soundness and completeness, grouped by category. It uses the "manifest" test structure described [here](https://www.w3.org/2001/sw/DataAccess/tests/test-manifest#).  

- [`run_manifest.py`](python/run_manifest.py) runs the tests in the above folder.  

The following command runs all tests and checks whether the output is compliant:
```
python run_manifest.py --system fun3 --what run --manifest tests-manifest/manifest.ttl
```

The following command generates and saves the Python code of all tests:
```
python run_manifest.py --system fun3 --what gen --manifest tests-manifest/manifest.ttl
```

(You can substitute `tests-manifest/manifest.ttl` with a manifest file under one of the subfolders.)

To run / generate only a single test:

```
python run_manifest.py --system fun3 --what run --manifest tests-manifest/gterm/manifest-gterm.ttl --test ggraph1
```

- [`test.ipynb`](python/test.ipynb) simply calls the functions from `to_py.py` for a single set of inputs.

[`tests-py/`](python/tests-py/) folder: contains miscellaneous tests.