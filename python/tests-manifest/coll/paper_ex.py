import sys # noqa
sys.path.insert(0, "../..") # noqa

from n3.parse import parse_n3_file
from n3.objects import ANY, Terms, Iri, Var, Literal, Collection, GraphTerm, Triple
from n3.ns import NS
from lib.emit import emit
data = parse_n3_file('/Users/wvw/git/n3/fun3/python/tests-manifest/coll/paper_ex-data.n3').data

def query(person_0, title_1, final_ctu):
    data.find(person_0, Iri('http://example.org/loves'), title_1, lambda s, p, o: final_ctu(s, o))
    rule_0(person_0, title_1, lambda person_2_m, title_3_m: final_ctu(person_2_m, title_3_m))

def rule_0(person_2, title_3, final_ctu):
    data.find(person_2, Iri('http://example.org/top'), Collection([Var('book1_4'), Var('book2_5'), Var('book3_6')]), lambda s, p, o: rule_0_1(s, title_3, o[0], o[1], o[2], final_ctu))

def rule_0_1(person_2, title_3, book1_4, book2_5, book3_6, final_ctu):
    data.find(book1_4, Iri('http://purl.org/dc/terms/title'), title_3, lambda s, p, o: final_ctu(person_2, o))
query(ANY, ANY, lambda person_0, title_1: emit(Triple(Var('person_0'), Iri('http://example.org/loves'), Var('title_1')), {'person_0': person_0, 'title_1': title_1}))