from ast import dump, unparse

from n3.parse import parse_n3
from n3.fun.gen import gen_py
from n3.terms import Iri

def main():
    data = """@base <http://base.org/> .
@prefix : <http://example.org/> . 
# # iri
# <http://example.org/wil> a :Person .
# <#dor> a :Person .
# :this :is { @base <http://base2.org> . @prefix : <http://example2.org/> . <wil> a :Person } .
    
# # bnodes, bnode prp lst, iri prp lst
# :wil :address [ :street "street" ; :country "CA" ] ; :age _:b1 .
# :dor :address [ :street "strasse" ; :country "DE" ] ; :age _:b1 .
# :this :has { :will :age _:b1 } .

# :wil [ :street "street" ; :country "CA" ] :address .
# :dor [ :street "strasse" ; :country "DE" ] :address .

# :spiderman 
#   :enemyOf 
#     [ id :green-goblin 
#       :portrayedBy [ id :willem-dafoe
#         a :Actor 
#       ]
#     ] ;
#   :portrayedBy [ id :tobey-maguire
#       a :Actor
#   ] .

# # numeric literals
# :wil :age 40, 40.0 .
# :dor :age 29e2 .

# # string literals
# @prefix xsd: <http://www.w3.org/2001/XMLSchema#> . 
# :wil :name "william"^^xsd:string .
# :dor :name "doerthe"@de .

# # PATHS
# :john^:father!:father^:father a :Person .
# :john :father!:father^:father :Person .
# :john :father :will!:father^:father.
# :john^:father!:father^:father :mother!:mother^:mother :will!:father^:father .
# :a :b :c .

# # invert
# :john <-:father :paul , :victor ; has :grandfather :edward .
# :will is :alias of :edward .
# :a :b :c .

# collections
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> . 
# :will :names ('will' 'edward'^^xsd:string 'elbert') .
#( :x!:y [ :b 1 ; :c 2 ] :d ) . # crazy
{ :will :aliasNames ( ?xn ?yn ) } <= { :wil :alias ( ?x ?y ) . ?x :name ?xn . ?y :name ?yn } .

# """

    # parse
    
    data = parse_n3(data).data
    print("data:\n", data)
    
    print()

if __name__ == "__main__":
    main()