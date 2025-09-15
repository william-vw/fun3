
// Generated from ../../grammar/n3.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "n3Listener.h"


/**
 * This class provides an empty implementation of n3Listener,
 * which can be extended to create a listener which only needs to handle a subset
 * of the available methods.
 */
class  n3BaseListener : public n3Listener {
public:

  virtual void enterN3Doc(n3Parser::N3DocContext * /*ctx*/) override { }
  virtual void exitN3Doc(n3Parser::N3DocContext * /*ctx*/) override { }

  virtual void enterN3Statement(n3Parser::N3StatementContext * /*ctx*/) override { }
  virtual void exitN3Statement(n3Parser::N3StatementContext * /*ctx*/) override { }

  virtual void enterN3Directive(n3Parser::N3DirectiveContext * /*ctx*/) override { }
  virtual void exitN3Directive(n3Parser::N3DirectiveContext * /*ctx*/) override { }

  virtual void enterSparqlDirective(n3Parser::SparqlDirectiveContext * /*ctx*/) override { }
  virtual void exitSparqlDirective(n3Parser::SparqlDirectiveContext * /*ctx*/) override { }

  virtual void enterSparqlBase(n3Parser::SparqlBaseContext * /*ctx*/) override { }
  virtual void exitSparqlBase(n3Parser::SparqlBaseContext * /*ctx*/) override { }

  virtual void enterSparqlPrefix(n3Parser::SparqlPrefixContext * /*ctx*/) override { }
  virtual void exitSparqlPrefix(n3Parser::SparqlPrefixContext * /*ctx*/) override { }

  virtual void enterPrefixID(n3Parser::PrefixIDContext * /*ctx*/) override { }
  virtual void exitPrefixID(n3Parser::PrefixIDContext * /*ctx*/) override { }

  virtual void enterBase(n3Parser::BaseContext * /*ctx*/) override { }
  virtual void exitBase(n3Parser::BaseContext * /*ctx*/) override { }

  virtual void enterTriples(n3Parser::TriplesContext * /*ctx*/) override { }
  virtual void exitTriples(n3Parser::TriplesContext * /*ctx*/) override { }

  virtual void enterPredicateObjectList(n3Parser::PredicateObjectListContext * /*ctx*/) override { }
  virtual void exitPredicateObjectList(n3Parser::PredicateObjectListContext * /*ctx*/) override { }

  virtual void enterObjectList(n3Parser::ObjectListContext * /*ctx*/) override { }
  virtual void exitObjectList(n3Parser::ObjectListContext * /*ctx*/) override { }

  virtual void enterVerb(n3Parser::VerbContext * /*ctx*/) override { }
  virtual void exitVerb(n3Parser::VerbContext * /*ctx*/) override { }

  virtual void enterSubject(n3Parser::SubjectContext * /*ctx*/) override { }
  virtual void exitSubject(n3Parser::SubjectContext * /*ctx*/) override { }

  virtual void enterPredicate(n3Parser::PredicateContext * /*ctx*/) override { }
  virtual void exitPredicate(n3Parser::PredicateContext * /*ctx*/) override { }

  virtual void enterObject(n3Parser::ObjectContext * /*ctx*/) override { }
  virtual void exitObject(n3Parser::ObjectContext * /*ctx*/) override { }

  virtual void enterExpression(n3Parser::ExpressionContext * /*ctx*/) override { }
  virtual void exitExpression(n3Parser::ExpressionContext * /*ctx*/) override { }

  virtual void enterPath(n3Parser::PathContext * /*ctx*/) override { }
  virtual void exitPath(n3Parser::PathContext * /*ctx*/) override { }

  virtual void enterPathItem(n3Parser::PathItemContext * /*ctx*/) override { }
  virtual void exitPathItem(n3Parser::PathItemContext * /*ctx*/) override { }

  virtual void enterLiteral(n3Parser::LiteralContext * /*ctx*/) override { }
  virtual void exitLiteral(n3Parser::LiteralContext * /*ctx*/) override { }

  virtual void enterBlankNodePropertyList(n3Parser::BlankNodePropertyListContext * /*ctx*/) override { }
  virtual void exitBlankNodePropertyList(n3Parser::BlankNodePropertyListContext * /*ctx*/) override { }

  virtual void enterIriPropertyList(n3Parser::IriPropertyListContext * /*ctx*/) override { }
  virtual void exitIriPropertyList(n3Parser::IriPropertyListContext * /*ctx*/) override { }

  virtual void enterCollection(n3Parser::CollectionContext * /*ctx*/) override { }
  virtual void exitCollection(n3Parser::CollectionContext * /*ctx*/) override { }

  virtual void enterFormula(n3Parser::FormulaContext * /*ctx*/) override { }
  virtual void exitFormula(n3Parser::FormulaContext * /*ctx*/) override { }

  virtual void enterFormulaContent(n3Parser::FormulaContentContext * /*ctx*/) override { }
  virtual void exitFormulaContent(n3Parser::FormulaContentContext * /*ctx*/) override { }

  virtual void enterNumericLiteral(n3Parser::NumericLiteralContext * /*ctx*/) override { }
  virtual void exitNumericLiteral(n3Parser::NumericLiteralContext * /*ctx*/) override { }

  virtual void enterRdfLiteral(n3Parser::RdfLiteralContext * /*ctx*/) override { }
  virtual void exitRdfLiteral(n3Parser::RdfLiteralContext * /*ctx*/) override { }

  virtual void enterIri(n3Parser::IriContext * /*ctx*/) override { }
  virtual void exitIri(n3Parser::IriContext * /*ctx*/) override { }

  virtual void enterPrefixedName(n3Parser::PrefixedNameContext * /*ctx*/) override { }
  virtual void exitPrefixedName(n3Parser::PrefixedNameContext * /*ctx*/) override { }

  virtual void enterBlankNode(n3Parser::BlankNodeContext * /*ctx*/) override { }
  virtual void exitBlankNode(n3Parser::BlankNodeContext * /*ctx*/) override { }

  virtual void enterQuickVar(n3Parser::QuickVarContext * /*ctx*/) override { }
  virtual void exitQuickVar(n3Parser::QuickVarContext * /*ctx*/) override { }


  virtual void enterEveryRule(antlr4::ParserRuleContext * /*ctx*/) override { }
  virtual void exitEveryRule(antlr4::ParserRuleContext * /*ctx*/) override { }
  virtual void visitTerminal(antlr4::tree::TerminalNode * /*node*/) override { }
  virtual void visitErrorNode(antlr4::tree::ErrorNode * /*node*/) override { }

};

