# Example usage:

# python run_manifest.py --system eye --manifest tests-manifest/gterm/manifest-gterm.ttl
# python run_manifest.py --system eye --manifest tests-manifest/gterm/manifest-gterm.ttl --test ggraph1

# python run_manifest.py --system fun3 --what run --manifest tests-manifest/manifest.ttl
# python run_manifest.py --system fun3 --what run --manifest tests-manifest/gterm/manifest-gterm.ttl --test ggraph1

# python run_manifest.py --system fun3 --what gen --manifest tests-manifest/gterm/manifest-gterm.ttl
# python run_manifest.py --system fun3 --what gen --manifest tests-manifest/gterm/manifest-gterm.ttl --test ggraph1
#   e.g., python tests-manifest/gterm/ggraph1.py

import sys, os, argparse, logging, subprocess, re
from pathlib import Path
from rdflib import Graph, RDF, Namespace, compare, Literal
from n3.to_py import run_py, save_py
from n3.parse import parse_n3


MF = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#")
QT = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-query#")
N3T = Namespace("https://w3c.github.io/N3/tests/test.n3#")
RDFT = Namespace("http://www.w3.org/ns/rdftest#")

def runNSave(cmd, path, get_times=False):
    # result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, error = [ b.decode('UTF-8') for b in process.communicate() ]
    out = out.rstrip()
    # print("out:", out)
    # print("error:", error)
        
    with open(path, 'w') as fh:
        fh.write(out)
    
    if "** ERROR **" in error:
        print("ERROR:", error)
        
    elif get_times:
        netw_time = int(re.search(r"networking \d+ \[msec cputime\] (\d+) \[msec walltime\]", error).group(1))
        reas_time = int(re.search(r"reasoning \d+ \[msec cputime\] (\d+) \[msec walltime\]", error).group(1))
        return netw_time, reas_time

class Collection:
    def __init__(self, g, list):
        self.g = g
        self.list = list

    def __iter__(self):
        return self

    def __next__(self):
        if self.list == RDF.nil:
            raise StopIteration
        ret = self.g.value(self.list, RDF.first)
        self.list = self.g.value(self.list, RDF.rest)
        return ret;

def to_path(el):
    if el is None:
        return None
    else:
        return str(el)[len("file://"):]

def get_logger():
    logpath = "output.log"
    
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=logpath, filemode='w', encoding='utf-8', level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    
    return logger

def run_manifest(path, test, system, what, logger, trace, verbose, main=False):
    recur_total_num = 0; recur_noncompl_num = 0
    total_num = 0; noncompl_num = 0
    
    logger.info(f">> loading manifest: {path} <<")
    g = Graph()
    g.parse(path, format='turtle')

    # if test is not None:
    #     for t in g.triples((None, MF.name, Literal(test))):
    #         return run_test(g, t[0], system)
    #     logger.info(f"cannot find test with MF.name {test}")
    #     return

    for mf in g.subjects(RDF.type, MF.Manifest):
        # manifest files
        incl = g.value(mf, MF.include)
        if incl is not None:
            for el in Collection(g=g, list=incl):
                path = str(el)
                this_total_num, this_noncompl_num = run_manifest(path, test, system, what, logger, trace, verbose)
                recur_total_num += this_total_num
                recur_noncompl_num += this_noncompl_num
        # test entries
        entr = g.value(mf, MF.entries)
        if entr is not None:
            for el in Collection(g=g, list=entr):
                name = str(g.value(el, MF.name))
                if test is not None:
                    if name != test: continue
                if g.value(el, RDFT.approval) != RDFT.Approved:
                    logger.info(f"skipping unapproved test: {name}")
                    continue
                is_compl = run_test(g, el, system, what, trace, verbose)
                if not is_compl: noncompl_num += 1
                total_num += 1
    
    if what == 'run':
        recur_total_num += total_num
        recur_noncompl_num += noncompl_num
        
        if total_num > 0:
            logger.info(f"# total: {total_num}; # non-compliant: {noncompl_num}\n")
        
        if main:
            logger.info(f"# all total: {recur_total_num}; # all non-compliant: {recur_noncompl_num}\n")
    
    return ( recur_total_num, recur_noncompl_num )

def run_test(g, test, system, what, trace, verbose):    
    name = str(g.value(test, MF.name))
    action = g.value(test, MF.action)
    query = to_path(g.value(action, QT.query))
    rules = to_path(g.value(action, N3T.rules))
    data = to_path(g.value(action, QT.data))
    
    result = g.value(test, MF.result)
    ref = to_path(g.value(result, QT.data))
    
    match (what):
        case 'run':
            logger.info(f">> running test: {name}")
        case 'gen':
            logger.info(f">> generating code: {name}")

    out = do_test(name, query, rules, data, system, what, trace, verbose)
    
    if what == 'run':
        compl = compare_with(out, ref)        
        logger.info("")
    else:
        compl = False
    
    return compl

def do_test(name, query, rules, data, system, what, trace, verbose):
    match(system):
        case 'eye':
            return do_test_eye(query, rules, data, what, verbose)
        case 'fun3':
            return do_test_fun3(name, query, rules, data, what, trace, verbose)

def create_query_eye(query):
    eye_query = os.path.join(Path(query).parent.absolute(), Path(query).stem + "_eye.n3")
    with open(query, 'r') as query_fh, open(eye_query, 'w') as eye_query_fh:
        file_str = query_fh.read()
        tp_str = re.search(r"\n\s*([^@]*?\s+.*?\s+.*?)\s*\.\s*", file_str).group(1) # ugh
        query_str = f"{{ {tp_str} }} => {{ {tp_str} }}"
        file_str = file_str.replace(tp_str, query_str)
        eye_query_fh.write(file_str)
        return eye_query

def do_test_eye(query, rules, data, what, verbose):   
    if what != 'run':
        raise "only supporting 'run' for eye"
     
    query = create_query_eye(query)
    
    out = "tmp/eye.n3"
    cmd = ["eye", rules, data, "--query", query, "--nope"]
    if verbose:
        print(" ".join(cmd))
    runNSave(cmd, out)
    with open(out, 'r') as fh:
        return fh.read()

def do_test_fun3(name, query, rules, data, what, trace, verbose):
    match(what):
        case 'run':
            return run_py(Path(query), Path(rules), Path(data), print_code=verbose)

        case 'gen':
            rules_path = Path(rules)
            out_path = Path(rules_path.parent, f"{name}.py").absolute() #rules_path.stem + ".py").absolute()
            save_py(Path(query), Path(rules), Path(data), out_path, print_code=verbose, code_dir="../..")
            if trace:
                add_tracer(out_path)
            # add_rel_import(out_path)

def compare_with(out_str, ref_path):
    with open(ref_path, 'r') as ref_fh:
        ref_str = ref_fh.read()
        return compare_rdf_graphs(out_str, "out", 'n3', ref_str, "ref", 'n3')

def compare_rdf_graphs(data1, label1, format1, data2, label2, format2):
    model1 = parse_n3(data1).data
    model2 = parse_n3(data2).data
    
    compliant = True
    for t in model1.triples():
        if t not in model2.triples():
            logger.info(f"different in {label1}:")
            logger.info(t)
            compliant = False
            
    for t in model2.triples():
        if t not in model1.triples():
            logger.info(f"different in {label2}:")
            logger.info(t)
            compliant = False
            
    if compliant:
        logger.info("compliant")
        return True
    else:
        logger.info("non compliant")
        return False

def add_tracer(path):
    with open(path, 'r+') as fh:
        code = fh.read()
        # noqa = no quality assurance, makes linters skip that line or something
        # (avoids vscode to move it to wrong place)
        code = """from lib.trace import trace_calls
sys.settrace(trace_calls)
""" + code
        fh.seek(0)
        fh.write(code)
        fh.truncate()

def add_rel_import(path):
    with open(path, 'r+') as fh:
        code = fh.read()
        code = """import sys # noqa
import pathlib # noqa
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent.resolve())) # noqa
""" + code
        fh.seek(0)
        fh.write(code)
        fh.truncate()
    

# unfortunately, does not work for triples with graph terms
# def compare_rdf_graphs(data1, label1, format1, data2, label2, format2):
#         graph1 = Graph()
#         # print(data1)
#         graph1.parse(data=data1, format=format1)

#         graph2 = Graph()
#         # print(data2)
#         graph2.parse(data=data2, format=format2)
        
#         iso1 = compare.to_isomorphic(graph1)
#         iso2 = compare.to_isomorphic(graph2)

#         if iso1 == iso2:
#             logger.info("compliant")
#             return True
#         else:
#             logger.error("non compliant")
#             in_both, in_first, in_second = compare.graph_diff(graph1, graph2)
#             if len(in_both) > 0:
#                 logger.info("same triples in both files:")
#                 logger.info(dump_graph(in_both))
#             if len(in_first) > 0:
#                 logger.info(f"different in {label1}:")
#                 logger.info(dump_graph(in_first))
#             if len(in_second) > 0:
#                 logger.info(f"different in {label2}:")
#                 logger.info(dump_graph(in_second))
#                 return False

# def dump_graph(graph):
#     return graph.serialize(format='n3').strip()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run test manifest.")
    parser.add_argument('--system', help="System to run the tests (fun3|eye).", required=True)
    parser.add_argument('--what', help="What to do (gen|run).", required=False, default="run")
    parser.add_argument('--manifest', help="Path to the test manifest file.", required=True)
    parser.add_argument('--test', help="Label of test to be run", required=False)
    parser.add_argument('--trace', help="Whether to include tracing", required=False, default=False)
    parser.add_argument('--verbose', help="Verbose output", required=False, default=False)

    args = parser.parse_args()
    system = args.system
    what = args.what
    path = args.manifest
    test = args.test
    trace = args.trace
    verbose = args.verbose
    
    logger = get_logger()
    
    run_manifest(path, test, system, what, logger, trace, verbose, main=True)