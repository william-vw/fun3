#include <iostream>

#include "antlr4-runtime/antlr4-runtime.h"
#include "parser/n3Lexer.h"
#include "parser/n3Parser.h"
#include "parser/n3Listener.h"

#include <chrono>
#include <pybind11/pybind11.h>
#include <boost/algorithm/string.hpp>

// #include <pybind11/pybind11.h>
// #include "parse.hpp"

// namespace py = pybind11;

using namespace std;
using namespace antlr4;
namespace py = pybind11;

class  MyN3Listener : public n3Listener {
private:
    py::object &listener;

public:

  MyN3Listener(py::object &listener): listener(listener) {}

  void enterN3Doc(n3Parser::N3DocContext * ctx) override { }
  void exitN3Doc(n3Parser::N3DocContext * ctx) override { }

  void enterN3Statement(n3Parser::N3StatementContext * ctx) override { }
  void exitN3Statement(n3Parser::N3StatementContext * ctx) override { }

  void enterN3Directive(n3Parser::N3DirectiveContext * ctx) override { }
  void exitN3Directive(n3Parser::N3DirectiveContext * ctx) override { }

  void enterSparqlDirective(n3Parser::SparqlDirectiveContext * ctx) override { }
  void exitSparqlDirective(n3Parser::SparqlDirectiveContext * ctx) override { }

  void enterSparqlBase(n3Parser::SparqlBaseContext * ctx) override { }
  void exitSparqlBase(n3Parser::SparqlBaseContext * ctx) override { listener.attr("exitSparqlBase")(to_text(ctx->IRIREF())); }

  void enterSparqlPrefix(n3Parser::SparqlPrefixContext * ctx) override { }
  void exitSparqlPrefix(n3Parser::SparqlPrefixContext * ctx) override { listener.attr("exitSparqlPrefix")(to_text(ctx->PNAME_NS()), to_text(ctx->IRIREF())); }

  void enterPrefixID(n3Parser::PrefixIDContext * ctx) override { }
  void exitPrefixID(n3Parser::PrefixIDContext * ctx) override { listener.attr("exitPrefixID")(to_text(ctx->PNAME_NS()), to_text(ctx->IRIREF())); }

  void enterBase(n3Parser::BaseContext * ctx) override { }
  void exitBase(n3Parser::BaseContext * ctx) override { listener.attr("exitBase")(to_text(ctx->IRIREF())); }

  void enterTriples(n3Parser::TriplesContext * ctx) override { }
  void exitTriples(n3Parser::TriplesContext * ctx) override { }

  void enterPredicateObjectList(n3Parser::PredicateObjectListContext * ctx) override { }
  void exitPredicateObjectList(n3Parser::PredicateObjectListContext * ctx) override { }

  void enterObjectList(n3Parser::ObjectListContext * ctx) override { }
  void exitObjectList(n3Parser::ObjectListContext * ctx) override { listener.attr("exitObjectList")(); }

  void enterVerb(n3Parser::VerbContext * ctx) override { }
  void exitVerb(n3Parser::VerbContext * ctx) override { 
    bool has_predicate = (ctx->predicate() != nullptr);
    
    string token;
    if (!has_predicate) {
        token = ctx->start->getText();
        boost::trim(token);
    }
    
    listener.attr("exitVerb")(has_predicate, token);
  }

  void enterSubject(n3Parser::SubjectContext * ctx) override { }
  void exitSubject(n3Parser::SubjectContext * ctx) override { listener.attr("exitSubject")(); }

  void enterPredicate(n3Parser::PredicateContext * ctx) override { }
  void exitPredicate(n3Parser::PredicateContext * ctx) override { 
    string token = ctx->start->getText();
    boost::trim(token);

    listener.attr("exitPredicate")(token);
  }

  void enterObject(n3Parser::ObjectContext * ctx) override { }
  void exitObject(n3Parser::ObjectContext * ctx) override { listener.attr("exitObject")(); }

  void enterExpression(n3Parser::ExpressionContext *ctx) override { }
  void exitExpression(n3Parser::ExpressionContext *ctx) override { }

  void enterPath(n3Parser::PathContext * ctx) override { /*listener.attr("enterPath")();*/ }
  void exitPath(n3Parser::PathContext * ctx) override { /*listener.attr("exitPath")();*/ }

  void enterPathItem(n3Parser::PathItemContext * ctx) override { }
  void exitPathItem(n3Parser::PathItemContext * ctx) override { }

  void enterLiteral(n3Parser::LiteralContext * ctx) override { }
  void exitLiteral(n3Parser::LiteralContext * ctx) override { 
    auto lit = ctx->BooleanLiteral();
    if (lit != nullptr) {
        bool bl = to_bool(lit);
        listener.attr("exitLiteral")(bl);
    }
  }

  void enterBlankNodePropertyList(n3Parser::BlankNodePropertyListContext * ctx) override { listener.attr("enterBlankNodePropertyList")(); }
  void exitBlankNodePropertyList(n3Parser::BlankNodePropertyListContext * ctx) override { listener.attr("exitBlankNodePropertyList")(); }

  void enterIriPropertyList(n3Parser::IriPropertyListContext * ctx) override { listener.attr("enterIriPropertyList")(); }
  void exitIriPropertyList(n3Parser::IriPropertyListContext * ctx) override { listener.attr("exitIriPropertyList")(); }

  void enterCollection(n3Parser::CollectionContext * ctx) override { listener.attr("enterCollection")(); }
  void exitCollection(n3Parser::CollectionContext * ctx) override { listener.attr("exitCollection")(); }

  void enterFormula(n3Parser::FormulaContext * ctx) override { listener.attr("enterFormula")(); }
  void exitFormula(n3Parser::FormulaContext * ctx) override { listener.attr("exitFormula")(); }

  void enterFormulaContent(n3Parser::FormulaContentContext * ctx) override { }
  void exitFormulaContent(n3Parser::FormulaContentContext * ctx) override { }

  void enterNumericLiteral(n3Parser::NumericLiteralContext * ctx) override { }
  void exitNumericLiteral(n3Parser::NumericLiteralContext * ctx) override { 
    int num_type = -1;
    string num_txt;
    
    if (ctx->INTEGER() != nullptr) {
        num_type = 1;
        num_txt = to_text(ctx->INTEGER());
    } else if (ctx->DECIMAL() != nullptr) {
        num_type = 2;
        num_txt = to_text(ctx->DECIMAL());
    } else if (ctx->DOUBLE() != nullptr) {
        num_type = 3;
        num_txt = to_text(ctx->DOUBLE());
    }

    listener.attr("exitNumericLiteral")(num_type, num_txt);
  }

  void enterRdfLiteral(n3Parser::RdfLiteralContext * ctx) override { listener.attr("enterRdfLiteral")(); }
  void exitRdfLiteral(n3Parser::RdfLiteralContext * ctx) override { 
    string lex_txt = to_text(ctx->String());
    
    auto lng = ctx->LANGTAG();
    // undefined strings are passed as empty strings, not None's
    // so, explicitly pass whether string is None or not
    bool has_lng = (lng != nullptr);
    string lng_txt;
    if (has_lng) {
      lng_txt = to_text(lng);
    }

    listener.attr("exitRdfLiteral")(lex_txt, has_lng, lng_txt);
  }

  void enterIri(n3Parser::IriContext * ctx) override { }
  void exitIri(n3Parser::IriContext * ctx) override { 
    auto iri_ref = ctx->IRIREF();
    if (iri_ref != nullptr) {
        string iri_txt = to_text(iri_ref);
        listener.attr("exitIri")(iri_txt);
    }
  }

  void enterPrefixedName(n3Parser::PrefixedNameContext * ctx) override { }
  void exitPrefixedName(n3Parser::PrefixedNameContext * ctx) override { 
    auto pname_ln = ctx->PNAME_LN();
    bool has_pname_ln = (pname_ln != nullptr);
    string pname_ln_txt;
    if (has_pname_ln) {
        pname_ln_txt = to_text(pname_ln);
    }

    auto pname_ns = ctx->PNAME_NS();
    bool has_pname_ns = (pname_ns != nullptr);
    string pname_ns_txt;
    if (has_pname_ns) {
        pname_ns_txt = to_text(pname_ns);
    }

    listener.attr("exitPrefixedName")(has_pname_ln, pname_ln_txt, has_pname_ns, pname_ns_txt);
  }

  void enterBlankNode(n3Parser::BlankNodeContext * ctx) override { }
  void exitBlankNode(n3Parser::BlankNodeContext * ctx) override { 
    auto bnode = ctx->BLANK_NODE_LABEL();
    bool has_label = (bnode != nullptr);
    string bnode_txt;
    if (has_label) {
      bnode_txt = to_text(bnode);
    }

    listener.attr("exitBlankNode")(has_label, bnode_txt);
  }

  void enterQuickVar(n3Parser::QuickVarContext * ctx) override { }
  void exitQuickVar(n3Parser::QuickVarContext * ctx) override { 
    auto qvar = ctx->QuickVarName();
    if (qvar != nullptr) {
      string qvar_txt = to_text(qvar);
      listener.attr("exitQuickVar")(qvar_txt);
    }
 }

  string to_text(tree::TerminalNode* node) {
    string txt = node->getText();
    boost::trim(txt);
    return txt;
  }

  bool to_bool(tree::TerminalNode* node) {
    string txt = to_text(node);
    if (boost::starts_with(txt, "@")) {
        txt = txt.substr(1);
    }
    return txt == "true";
  }

  void enterEveryRule(antlr4::ParserRuleContext * /*ctx*/) override { }
  void exitEveryRule(antlr4::ParserRuleContext * /*ctx*/) override { }
  void visitTerminal(antlr4::tree::TerminalNode * /*node*/) override { }
  void visitErrorNode(antlr4::tree::ErrorNode * /*node*/) override { }
};

double parse(string path, py::object &listener) {
    auto start = chrono::high_resolution_clock::now();

    ifstream stream;
    stream.open(path);
    
    MyN3Listener myListener(listener);

    ANTLRInputStream input(stream);
    n3Lexer lexer(&input);
    CommonTokenStream tokens(&lexer);
    n3Parser parser(&tokens);
    parser.addParseListener(&myListener);

    n3Parser::N3DocContext* tree = parser.n3Doc();

    auto end = chrono::high_resolution_clock::now();
    // auto duration_ms = chrono::duration_cast<chrono::milliseconds>(end - start);
    chrono::duration<double> duration = (end - start);
    
    return duration.count();
}

PYBIND11_MODULE(cppN3Parser, m, py::mod_gil_not_used()) {
    m.doc() = "C++ N3 parser"; // optional module docstring

    m.def("parse", &parse, "A function that parses an n3 file");
}
