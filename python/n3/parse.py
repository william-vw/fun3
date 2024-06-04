from antlr4 import *
from n3.grammar.parser.n3Lexer import n3Lexer
from n3.grammar.parser.n3Parser import n3Parser
from n3.grammar.parser.n3Listener import n3Listener

from n3.model import Model
from n3.terms import term_types, Iri, var_types, Var, Literal, GraphTerm, Triple

class state:
    
    # path_item
    # triple
    
    # model
    # prefixes
    # rules
    
    # parent
    
    def __init__(self, parent=None):
        self.path_item = None
        self.triple = Triple()
        
        self.model = Model()
        self.prefixes = {}
        self.rules = []
        
        self.parent = parent
        
    def sub(self):
        return state(self)
        

class n3Creator(n3Listener):
    
    def __init__(self):
        self.model = Model()
        self.state = state()
    
    # Enter a parse tree produced by n3Parser#n3Doc.
    def enterN3Doc(self, ctx:n3Parser.N3DocContext):
        pass

    # Exit a parse tree produced by n3Parser#n3Doc.
    def exitN3Doc(self, ctx:n3Parser.N3DocContext):
        pass

    # Enter a parse tree produced by n3Parser#n3Statement.
    def enterN3Statement(self, ctx:n3Parser.N3StatementContext):
        pass

    # Exit a parse tree produced by n3Parser#n3Statement.
    def exitN3Statement(self, ctx:n3Parser.N3StatementContext):
        pass

    # Enter a parse tree produced by n3Parser#n3Directive.
    def enterN3Directive(self, ctx:n3Parser.N3DirectiveContext):
        pass

    # Exit a parse tree produced by n3Parser#n3Directive.
    def exitN3Directive(self, ctx:n3Parser.N3DirectiveContext):
        pass


    # Enter a parse tree produced by n3Parser#sparqlDirective.
    def enterSparqlDirective(self, ctx:n3Parser.SparqlDirectiveContext):
        pass

    # Exit a parse tree produced by n3Parser#sparqlDirective.
    def exitSparqlDirective(self, ctx:n3Parser.SparqlDirectiveContext):
        pass


    # Enter a parse tree produced by n3Parser#sparqlBase.
    def enterSparqlBase(self, ctx:n3Parser.SparqlBaseContext):
        pass

    # Exit a parse tree produced by n3Parser#sparqlBase.
    def exitSparqlBase(self, ctx:n3Parser.SparqlBaseContext):
        pass


    # Enter a parse tree produced by n3Parser#sparqlPrefix.
    def enterSparqlPrefix(self, ctx:n3Parser.SparqlPrefixContext):
        pass

    # Exit a parse tree produced by n3Parser#sparqlPrefix.
    def exitSparqlPrefix(self, ctx:n3Parser.SparqlPrefixContext):
        self.process_prefix(ctx.PNAME_NS(), ctx.IRIREF())


    # Enter a parse tree produced by n3Parser#prefixID.
    def enterPrefixID(self, ctx:n3Parser.PrefixIDContext):
        pass

    # Exit a parse tree produced by n3Parser#prefixID.
    def exitPrefixID(self, ctx:n3Parser.PrefixIDContext):
        self.process_prefix(ctx.PNAME_NS(), ctx.IRIREF())


    # Enter a parse tree produced by n3Parser#base.
    def enterBase(self, ctx:n3Parser.BaseContext):
        pass

    # Exit a parse tree produced by n3Parser#base.
    def exitBase(self, ctx:n3Parser.BaseContext):
        pass


    # Enter a parse tree produced by n3Parser#triples.
    def enterTriples(self, ctx:n3Parser.TriplesContext):
        pass

    # Exit a parse tree produced by n3Parser#triples.
    def exitTriples(self, ctx:n3Parser.TriplesContext):
        pass


    # Enter a parse tree produced by n3Parser#predicateObjectList.
    def enterPredicateObjectList(self, ctx:n3Parser.PredicateObjectListContext):
        pass

    # Exit a parse tree produced by n3Parser#predicateObjectList.
    def exitPredicateObjectList(self, ctx:n3Parser.PredicateObjectListContext):
        pass


    # Enter a parse tree produced by n3Parser#objectList.
    def enterObjectList(self, ctx:n3Parser.ObjectListContext):
        pass

    # Exit a parse tree produced by n3Parser#objectList.
    def exitObjectList(self, ctx:n3Parser.ObjectListContext):
        pass


    # Enter a parse tree produced by n3Parser#verb.
    def enterVerb(self, ctx:n3Parser.VerbContext):
        pass

    # Exit a parse tree produced by n3Parser#verb.
    def exitVerb(self, ctx:n3Parser.VerbContext):
        if ctx.predicate() is None:
            token = ctx.start.text.strip()
            # if token == "a":
            #     predicate = "rdf:type"

            # # has, is
			
            # elif token == "=":
            #     predicate = "owl:sameAs"
                
            # elif token == "=>":
            #     predicate = "log:implies"
            
            # elif token == "<=":
            #     predicate = "log:impliedBy"

            self.state.path_item = Iri(token, True)
            
        self.state.triple.p = self.state.path_item

    # Enter a parse tree produced by n3Parser#subject.
    def enterSubject(self, ctx:n3Parser.SubjectContext):
        pass

    # Exit a parse tree produced by n3Parser#subject.
    def exitSubject(self, ctx:n3Parser.SubjectContext):
        self.state.triple.s = self.state.path_item


    # Enter a parse tree produced by n3Parser#predicate.
    def enterPredicate(self, ctx:n3Parser.PredicateContext):
        pass

    # Exit a parse tree produced by n3Parser#predicate.
    def exitPredicate(self, ctx:n3Parser.PredicateContext):
        pass


    # Enter a parse tree produced by n3Parser#object.
    def enterObject(self, ctx:n3Parser.ObjectContext):
        pass

    # Exit a parse tree produced by n3Parser#object.
    def exitObject(self, ctx:n3Parser.ObjectContext):
        self.state.triple.o = self.state.path_item
        
        self.emitTriple()


    # Enter a parse tree produced by n3Parser#expression.
    def enterExpression(self, ctx:n3Parser.ExpressionContext):
        pass

    # Exit a parse tree produced by n3Parser#expression.
    def exitExpression(self, ctx:n3Parser.ExpressionContext):
        pass


    # Enter a parse tree produced by n3Parser#path.
    def enterPath(self, ctx:n3Parser.PathContext):
        pass

    # Exit a parse tree produced by n3Parser#path.
    def exitPath(self, ctx:n3Parser.PathContext):
        pass


    # Enter a parse tree produced by n3Parser#path_item.
    def enterPathItem(self, ctx:n3Parser.PathItemContext):
        pass

    # Exit a parse tree produced by n3Parser#path_item.
    def exitPathItem(self, ctx:n3Parser.PathItemContext):
        pass


    # Enter a parse tree produced by n3Parser#literal.
    def enterLiteral(self, ctx:n3Parser.LiteralContext):
        pass

    # Exit a parse tree produced by n3Parser#literal.
    def exitLiteral(self, ctx:n3Parser.LiteralContext):
        pass

    # Enter a parse tree produced by n3Parser#blankNodePropertyList.
    def enterBlankNodePropertyList(self, ctx:n3Parser.BlankNodePropertyListContext):
        pass

    # Exit a parse tree produced by n3Parser#blankNodePropertyList.
    def exitBlankNodePropertyList(self, ctx:n3Parser.BlankNodePropertyListContext):
        pass


    # Enter a parse tree produced by n3Parser#iriPropertyList.
    def enterIriPropertyList(self, ctx:n3Parser.IriPropertyListContext):
        pass

    # Exit a parse tree produced by n3Parser#iriPropertyList.
    def exitIriPropertyList(self, ctx:n3Parser.IriPropertyListContext):
        pass


    # Enter a parse tree produced by n3Parser#collection.
    def enterCollection(self, ctx:n3Parser.CollectionContext):
        pass

    # Exit a parse tree produced by n3Parser#collection.
    def exitCollection(self, ctx:n3Parser.CollectionContext):
        pass


    # Enter a parse tree produced by n3Parser#formula.
    def enterFormula(self, ctx:n3Parser.FormulaContext):
        self.state = self.state.sub()

    # Exit a parse tree produced by n3Parser#formula.
    def exitFormula(self, ctx:n3Parser.FormulaContext):
        graph_model = self.state.model
        
        self.state = self.state.parent
        self.state.path_item = GraphTerm(graph_model)
        

    # Enter a parse tree produced by n3Parser#formulaContent.
    def enterFormulaContent(self, ctx:n3Parser.FormulaContentContext):
        pass

    # Exit a parse tree produced by n3Parser#formulaContent.
    def exitFormulaContent(self, ctx:n3Parser.FormulaContentContext):
        pass


    # Enter a parse tree produced by n3Parser#numericLiteral.
    def enterNumericLiteral(self, ctx:n3Parser.NumericLiteralContext):
        pass

    # Exit a parse tree produced by n3Parser#numericLiteral.
    def exitNumericLiteral(self, ctx:n3Parser.NumericLiteralContext):
        n = None
        
        if ctx.INTEGER() is not None:
            n = ctx.INTEGER()
        elif ctx.DOUBLE is not None:
            n = ctx.DOUBLE()
        elif ctx.DECIMAL is not None:
            n = ctx.DECIMAL()
        
        if n is not None:
            self.state.path_item = Literal(self.text(n))

    # Enter a parse tree produced by n3Parser#rdfLiteral.
    def enterRdfLiteral(self, ctx:n3Parser.RdfLiteralContext):
        pass

    # Exit a parse tree produced by n3Parser#rdfLiteral.
    def exitRdfLiteral(self, ctx:n3Parser.RdfLiteralContext):
        # lex = self.text(ctx.String())
        # lng = self.text(ctx.LANGTAG())
        
        self.state.path_item = Literal(self.text(ctx.String()))

    # Enter a parse tree produced by n3Parser#iri.
    def enterIri(self, ctx:n3Parser.IriContext):
        pass

    # Exit a parse tree produced by n3Parser#iri.
    def exitIri(self, ctx:n3Parser.IriContext):
        iri_ref = ctx.IRIREF()
        
        if iri_ref is not None:
            self.state.path_item = Iri(self.text(iri_ref)[1:-1])


    # Enter a parse tree produced by n3Parser#prefixedName.
    def enterPrefixedName(self, ctx:n3Parser.PrefixedNameContext):
        pass

    # Exit a parse tree produced by n3Parser#prefixedName.
    def exitPrefixedName(self, ctx:n3Parser.PrefixedNameContext):
        pname_ln = ctx.PNAME_LN()
        
        if pname_ln is not None:
            pname_ln = pname_ln.getText().strip()
            
            # (prefix, name) = pname_ln.split(":", 1)
            # ns = self.resolve_prefix(prefix)
            # if ns is not None:
            #     ns = self.state.prefixes[prefix]
            #     iri = ns + name
            #     self.state.path_item = Iri(iri)
            self.state.path_item = Iri(pname_ln, True)
                
        else:
            pname_ns = ctx.PNAME_NS().getText().strip()
            
            # prefix = pname_ns[:-1]
            # ns = self.resolve_prefix(prefix)
            # if ns is not None:
            #     ns = self.state.prefixes[prefix]
            #     self.state.path_item = Iri(ns)
            self.state.path_item = Iri(pname_ns, True)
            

    # Enter a parse tree produced by n3Parser#blankNode.
    def enterBlankNode(self, ctx:n3Parser.BlankNodeContext):
        pass

    # Exit a parse tree produced by n3Parser#blankNode.
    def exitBlankNode(self, ctx:n3Parser.BlankNodeContext):
        name = None if ctx.BLANK_NODE_LABEL() is None else self.text(ctx.BLANK_NODE_LABEL())
        
        self.state.path_item = Var(var_types.EXISTENTIAL, name)


    # Enter a parse tree produced by n3Parser#quickVar.
    def enterQuickVar(self, ctx:n3Parser.QuickVarContext):
        pass

    # Exit a parse tree produced by n3Parser#quickVar.
    def exitQuickVar(self, ctx:n3Parser.QuickVarContext):
        name = ctx.QuickVarName()
        
        if name is not None:
            self.state.path_item = Var(var_types.UNIVERSAL, self.text(name)[1:])
    
    # custom methods
    
    def process_prefix(self, prefix, iri_ref):
        prefix = prefix.getText().strip()[:-1]
        iri_ref = self.text(iri_ref)[1:-1]
        
        self.state.prefixes[prefix] = iri_ref
        
    def resolve_prefix(self, prefix):
        if prefix not in self.state.prefixes:
            print(f"ERROR: unknown prefix {prefix}")
            return None
        else:
            return self.state.prefixes[prefix]
    
    def text(self, node):
        return node.getText().strip()
        
    def emitTriple(self):
        triple = self.state.triple
        
        self.state.model.add(triple)
        if triple.p.type() == term_types.IRI and (triple.p.iri == "<=" or triple.p.iri == "=>"):
            self.state.rules.append(triple)
            
        # so predicateLists etc work
        self.state.triple = triple.clone()

class n3ParseResult:
    
    def __init__(self, state):
        self.model = state.model
        self.rules = state.rules

def parse_n3(str):
    creator = n3Creator()
    
    lexer = n3Lexer(InputStream(str))
    stream = CommonTokenStream(lexer)
    parser = n3Parser(stream)
    parser.addParseListener(creator)

    _ = parser.n3Doc()
    # print(tree.toStringTree(recog=parser))
    
    return n3ParseResult(creator.state)