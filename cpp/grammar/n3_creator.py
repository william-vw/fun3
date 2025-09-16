from antlr4 import *
import uritools

import sys
sys.path.insert(0, "../../python")
from n3.parse import state, n3ParseError
from n3.grammar.parser.n3Lexer import n3Lexer
from n3.grammar.parser.n3Parser import n3Parser
from n3.grammar.parser.n3Listener import n3Listener

from n3.model import MultiDictModel, ListModel
from n3.objects import Terms, Iri, Collection, Var, BlankNode, Literal, GraphTerm, Triple
from n3.ns import rdfNs, owlNs, logNs, xsdNs

class n3Creator():
    
    def __init__(self, has_vars=False):
        self.state = state(has_vars=has_vars)
    
    # Exit a parse tree produced by n3Parser#sparqlBase.
    def exitSparqlBase(self, IRIREF):
        self.state.base = IRIREF[1:-1]

    # Exit a parse tree produced by n3Parser#sparqlPrefix.
    def exitSparqlPrefix(self, PNAME_NS, IRIREF):
        self.process_prefix(PNAME_NS, IRIREF)

    # Exit a parse tree produced by n3Parser#prefixID.
    def exitPrefixID(self, PNAME_NS, IRIREF):
        self.process_prefix(PNAME_NS, IRIREF)

    # Exit a parse tree produced by n3Parser#base.
    def exitBase(self, IRIREF):
        self.state.base = IRIREF[1:-1]

    # Exit a parse tree produced by n3Parser#objectList.
    def exitObjectList(self):
        self.state.inv_pred = False

    # Exit a parse tree produced by n3Parser#verb.
    def exitVerb(self, predicateIsNull, token):
        # all these tokens use expression production, not predicate
        if predicateIsNull:
            
            predicate = None
            # 'has' has no side-effects
            match token:
                case 'a': predicate = rdfNs['type']
                case 'is': self.state.inv_pred = True
                case '=': predicate = owlNs['sameAs']
                case '=>': predicate = logNs["implies"]
                case '<=': predicate = logNs["impliedBy"]

            if predicate is not None:
                self.state.path_item = predicate
            
        self.state.triple.p = self.state.path_item

    # Exit a parse tree produced by n3Parser#subject.
    def exitSubject(self):
        self.state.triple.s = self.state.path_item

    # Exit a parse tree produced by n3Parser#predicate.
    def exitPredicate(self, token):
        if token == "<-":
            self.state.inv_pred = True # disabled in exitObjectList

    # Exit a parse tree produced by n3Parser#object.
    def exitObject(self):
        if self.state.is_collecting():
            self.state.collection._parsed_el(self.state.path_item)
        else:
            self.state.triple.o = self.state.path_item
            
            triple = self.state.triple
            self.emit_triple(triple)
            # so predicateLists etc work
            self.state.triple = triple.copy_shallow()

    # Enter a parse tree produced by n3Parser#path.
    def enterPath(self, ctx:n3Parser.PathContext):
        raise "resource paths not yet supported"

        # # print("enterPath", self.state.path_item)
        
        # # in a path, unfortunately
        # if self.state.path_cnt > 0 and self.state.path_item is not None:
            
        #     if self.state.path_cnt == 1: # but, don't have enough yet
        #         # current path_item will be first step
        #         # next path_item (still unknown) will be predicate
        #         self.state.path_step = self.state.path_item
            
        #     else: # have enough now; current path_item will be predicate
        #         # from now on, next step will be blank node object
        #         self.state.path_step = self.emit_path()
                
        # self.state.path_dir = self.text(ctx.parentCtx.getChild(1))
        # self.state.path_cnt += 1

    # Exit a parse tree produced by n3Parser#path.
    def exitPath(self, ctx:n3Parser.PathContext):
        raise "resource paths not yet supported"
        
        # # print("exitPath")
        # # had ourselves a path here
        # if self.state.path_cnt > 1: # complete last path step
        #     # rest will continue from blank node object
        #     self.state.path_item = self.emit_path()
        
        # self.state.path_cnt = 0

    # def emit_path(self):
    #     prior_step = self.state.path_step
    #     pred = self.state.path_item
    #     next_step = BlankNode()
    #     # print(prior_step, pred, next_step)
    #     if self.state.path_dir == "!":
    #         self.emit_triple(Triple(prior_step, pred, next_step))
    #     else:
    #         self.emit_triple(Triple(next_step, pred, prior_step))
    #     return next_step
        
    # Exit a parse tree produced by n3Parser#literal.
    def exitLiteral(self, bool):
        self.state.path_item = Literal(bool, xsdNs['boolean'])

    # Enter a parse tree produced by n3Parser#blankNodePropertyList.
    def enterBlankNodePropertyList(self):
        self.state = self.state.sub()
        
        # use same bnode as subject for properties in list
        self.state.triple[0] = self.state.bnode()

    # Exit a parse tree produced by n3Parser#blankNodePropertyList.
    def exitBlankNodePropertyList(self):
        # bnode for property list
        bnode = self.state.triple[0]
        
        self.state = self.state.parent
        # use bnode as path_item (e.g., object)
        self.state.path_item = bnode


    # Enter a parse tree produced by n3Parser#iriPropertyList.
    def enterIriPropertyList(self):
        self.state = self.state.sub()
        
        # use next iri as subject for properties in ipl
        self.state.iri_mode = 'ipl'

    # Exit a parse tree produced by n3Parser#iriPropertyList.
    def exitIriPropertyList(self):
         # iri for property list
        iri = self.state.triple[0]
        
        self.state = self.state.parent
        # use iri as path_item (e.g., object)
        self.state.path_item = iri


    # Enter a parse tree produced by n3Parser#collection.
    def enterCollection(self):
        self.state = self.state.sub()
        
        self.state.start_collect()

    # Exit a parse tree produced by n3Parser#collection.
    def exitCollection(self):
        collection = self.state.end_collect()
        self.state = self.state.parent
        
        # self.state.parsed_vars(collection._recur_vars())
        
        self.state.path_item = collection


    # Enter a parse tree produced by n3Parser#formula.
    def enterFormula(self):
        self.state = self.state.sub(new_scope=True)
        
        self.state.start_formula()

    # Exit a parse tree produced by n3Parser#formula.
    def exitFormula(self):
        graph_term = self.state.end_formula()
        self.state = self.state.parent
        
        # self.state.parsed_vars(graph_term._recur_vars())
        
        self.state.path_item = graph_term
        
    # Exit a parse tree produced by n3Parser#numericLiteral.
    def exitNumericLiteral(self, num_type, txt):
        n = None; dt = None
        
        match (num_type):
            case 1:
                n = int(txt); dt = xsdNs['int']        
            case 2:
                n = float(txt); dt = xsdNs['double']
            case 3:    
                n = float(txt); dt = xsdNs['decimal']
        
        if n is not None:
            self.state.path_item = Literal(n, dt)

    # Enter a parse tree produced by n3Parser#rdfLiteral.
    def enterRdfLiteral(self):
        self.state.iri_mode = 'rdflit'

    # Exit a parse tree produced by n3Parser#rdfLiteral.
    def exitRdfLiteral(self, lex, lng):
        lex = self.string(lex)
        lng = lng[1:] if lng is not None else None
        
        dt = self.state.dt if self.state.dt is not None else None
        self.state.iri_mode = None; self.state.dt = None
        
        self.state.path_item = Literal(lex, dt, lng)

    # Exit a parse tree produced by n3Parser#iri.
    def exitIri(self, iri_txt):
        iri_ref = Iri(self.iri(iri_txt))
        self.process_iri(iri_ref)

    # Exit a parse tree produced by n3Parser#prefixedName.
    def exitPrefixedName(self, pname_ln, pname_ns):        
        # TODO optimize this code
        
        iri_ref = None
        if pname_ln is not None:
            # iri_ref = Iri(pname_ln)
            
            (prefix, name) = pname_ln.split(":", 1)
            ns = self.resolve_prefix(prefix)
            if ns is not None:
                ns = self.state.prefixes[prefix]
                iri = ns + name
                iri_ref = Iri(iri)
        else:
            # iri_ref = Iri(pname_ns)
            
            prefix = pname_ns[:-1]
            ns = self.resolve_prefix(prefix)
            if ns is not None:
                ns = self.state.prefixes[prefix]
                iri_ref = Iri(ns)
        
        if iri_ref is not None:
            self.process_iri(iri_ref)

    def process_iri(self, iri_ref):
        match self.state.iri_mode:
            case 'ipl': # use iri as subject for properties in ipl
                self.state.triple[0] = iri_ref
                self.state.iri_mode = None
            case 'rdflit': # use iri as datatype
                self.state.dt = iri_ref
                self.state.iri_mode = None
            case None: self.state.path_item = iri_ref

    # Enter a parse tree produced by n3Parser#blankNode.
    def enterBlankNode(self, ctx:n3Parser.BlankNodeContext):
        pass

    # Exit a parse tree produced by n3Parser#blankNode.
    def exitBlankNode(self, bnode_txt):
        if bnode_txt is not None:
            label = bnode_txt
            label = label[2:]
        else:
            label = None
        
        self.state.path_item = self.state.bnode(label)

    # Exit a parse tree produced by n3Parser#quickVar.
    def exitQuickVar(self, qvar_txt):
        if qvar_txt is not None:
            var = Var(qvar_txt[1:])
            self.state.path_item = var
            
            # self.state.parsed_var(var)
    
    # custom methods
    
    def process_prefix(self, prefix, iri_ref):
        prefix = prefix[:-1]
        iri_ref = iri_ref[1:-1]
        
        self.state.prefixes[prefix] = iri_ref
        
    def resolve_prefix(self, prefix):
        if prefix not in self.state.prefixes:
            raise n3ParseError(f"error: unknown prefix '{prefix}'") from None
        else:
            return self.state.prefixes[prefix]
    
    def bool(self, node):
        txt = self.text(node)
        if txt.startswith("@"):
            txt = txt[1:]
        return txt == 'true'
    
    def text(self, node):
        if node is None:
            return None
        return node.getText().strip()
    
    def iri(self, txt):
        txt = txt[1:-1]
        
        # (quick heuristic to avoid expensive checks each time)
        if txt.startswith("http") or txt.startswith("//"):
            return txt
        
        if uritools.isrelpath(txt):
            if self.state.base is None:
                raise n3ParseError("found relative IRI without base IRI set: self.text(node)")
            return uritools.urijoin(self.state.base, txt)
        else:
            return txt
    
    def string(self, text):
        if text is None:
            return ""
        
        if text.startswith("\"\"\""):
            return text[3:-3]
        else:
            return text[1:-1]
        
    def emit_triple(self, triple):
        if self.state.inv_pred:
            triple = Triple(triple.o, triple.p, triple.s)
        
        self.state.data.add(triple)
        
        # something weird going on with imports
        # it doesn't look like logNs[..] Iri type is the same as the Iri type imported here
        if triple.s.type() == Terms.GRAPH and \
            triple.p.type() == Terms.IRI and (triple.p.iri == logNs['implies'].iri or triple.p.iri == logNs['impliedBy'].iri):
            self.state.rules.append(triple)
        
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise n3ParseError(msg) from None

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        pass

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        pass