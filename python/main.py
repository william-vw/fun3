import sys, os, argparse
from pathlib import Path
from n3.to_py import run_py

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run test manifest.")
    parser.add_argument('--query', help="Query.", required=True)
    parser.add_argument('--rules', help="Rules.", required=True)
    parser.add_argument('--data', help="Data.", required=True)

    args = parser.parse_args()
    query = args.query
    rules = args.rules
    data = args.data

    run_py(Path(query), Path(rules), Path(data), all_stdout=True)     
