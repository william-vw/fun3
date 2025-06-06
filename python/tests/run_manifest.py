import sys, os, argparse, logging
from rdflib import Graph, RDF, Namespace, compare
sys.path.insert(0, os.path.abspath("../"))
from n3.get_py import run_py, save_py
from NTCompare import compare_rdf_graphs

MF = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#")
QT = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-query#")
N3T = Namespace("https://w3c.github.io/N3/tests/test.n3#")

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
    return str(el)[len("file://"):]

def get_logger():
    logpath = "output.log"
    
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=logpath, encoding='utf-8', level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    
    return logger

def run_manifest(path, test):
    total_num = 0; noncompl_num = 0
    global logger; logger = get_logger()
    
    logger.info(f">> loading manifest: {path} <<")
    g = Graph()
    g.parse(path, format='turtle')

    for mf in g.subjects(RDF.type, MF.Manifest):
        # manifest files
        lst = g.value(mf, MF.include)
        if lst is not None:
            for el in Collection(g=g, list=lst):
                path = str(el)
                run_manifest(path, test)
        # test entries
        lst = g.value(mf, MF.entries)
        if lst is not None:
            for el in Collection(g=g, list=lst):
                if test is not None:
                    name = str(g.value(el, MF.name))
                    if name != test: continue
                is_compl = run_test(g, el)
                if not is_compl: noncompl_num += 1
                total_num += 1
    
    logger.info(f"# total: {total_num}; # non-compliant: {noncompl_num}")

def run_test(g, test):    
    name = str(g.value(test, MF.name))
    action = g.value(test, MF.action)
    query = to_path(g.value(action, QT.query))
    rules = to_path(g.value(action, N3T.rules))
    data = to_path(g.value(action, QT.data))
    # ordered = str(g.value(action, QT.ordered))
    
    result = g.value(test, MF.result)
    ref = to_path(g.value(result, QT.data))
    
    # category = get_category(query)
    logger.info(f">> running test: {name}")
    
    out = do_test(query, rules, data)
    compl = compare_with(out, ref)    
    
    logger.info("")
    return compl

def do_test(query, rules, data):
    with open(query, 'r') as query_fh, open(rules, 'r') as rules_fh, open(data, 'r') as data_fh:
        query_str = query_fh.read(); rules_str = rules_fh.read(); data_str = data_fh.read()
        return run_py(query_str, rules_str, data_str)

def compare_with(out_str, ref_path):
    with open(ref_path, 'r') as ref_fh:
        ref_str = ref_fh.read()
        return compare_rdf_graphs(out_str, "out", 'n3', ref_str, "ref", 'n3')
                
def compare_rdf_graphs(data1, label1, format1, data2, label2, format2):
        graph1 = Graph()
        graph1.parse(data=data1, format=format1)

        graph2 = Graph()
        graph2.parse(data=data2, format=format2)
        
        iso1 = compare.to_isomorphic(graph1)
        iso2 = compare.to_isomorphic(graph2)

        if iso1 == iso2:
            logger.info("compliant")
            return True
        else:
            logger.error("non compliant")
            in_both, in_first, in_second = compare.graph_diff(graph1, graph2)
            if len(in_both) > 0:
                logger.info("same triples in both files:")
                logger.info(dump_graph(in_both))
            if len(in_first) > 0:
                logger.info(f"different in {label1}:")
                logger.info(dump_graph(in_first))
            if len(in_second) > 0:
                logger.info(f"different in {label2}:")
                logger.info(dump_graph(in_second))
                return False

def dump_graph(graph):
    return graph.serialize(format='n3').strip()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run test manifest.")
    parser.add_argument('--manifest', help="Path to the test manifest file.", required=True)
    parser.add_argument('--test', help="Label of test to be run", required=False)
    #parser.add_argument('--ordered', help='Consider result ordering during comparison', action="store_true")

    args = parser.parse_args()
    path = args.manifest
    test = args.test
    
    run_manifest(path, test)