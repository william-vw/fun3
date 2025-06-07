import sys, os, argparse, logging
from rdflib import Graph, RDF, Namespace, compare, Literal
from n3.to_py import run_py, save_py


MF = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#")
QT = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-query#")
N3T = Namespace("https://w3c.github.io/N3/tests/test.n3#")
RDFT = Namespace("http://www.w3.org/ns/rdftest#")

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
    logging.basicConfig(filename=logpath, filemode='w', encoding='utf-8', level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    
    return logger

def run_manifest(path, test, logger, main=False):
    recur_total_num = 0; recur_noncompl_num = 0
    total_num = 0; noncompl_num = 0
    
    logger.info(f">> loading manifest: {path} <<")
    g = Graph()
    g.parse(path, format='turtle')

    if test is not None:
        for t in g.triples((None, MF.name, Literal(test))):
            return run_test(g, t[0])
        logger.info(f"cannot find test with MF.name {test}")
        return

    for mf in g.subjects(RDF.type, MF.Manifest):
        # manifest files
        incl = g.value(mf, MF.include)
        if incl is not None:
            for el in Collection(g=g, list=incl):
                path = str(el)
                this_total_num, this_noncompl_num = run_manifest(path, test, logger)
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
                is_compl = run_test(g, el)
                if not is_compl: noncompl_num += 1
                total_num += 1
    
    recur_total_num += total_num
    recur_noncompl_num += noncompl_num
    
    if total_num > 0:
        logger.info(f"# total: {total_num}; # non-compliant: {noncompl_num}\n")
    
    if main:
        logger.info(f"# all total: {recur_total_num}; # all non-compliant: {recur_noncompl_num}\n")
    else:
        return ( recur_total_num, recur_noncompl_num )

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
        return run_py(query_str, rules_str, data_str)#, print_code=True)

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
    
    logger = get_logger()
    
    run_manifest(path, test, logger, main=True)