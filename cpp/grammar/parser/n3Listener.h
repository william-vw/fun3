
// Generated from ../../grammar/n3.g4 by ANTLR 4.13.2

#pragma once


#include "antlr4-runtime.h"
#include "n3Parser.h"


/**
 * This interface defines an abstract listener for a parse tree produced by n3Parser.
 */
class  n3Listener : public antlr4::tree::ParseTreeListener {
public:

  virtual void enterN3Doc(n3Parser::N3DocContext *ctx) = 0;
  virtual void exitN3Doc(n3Parser::N3DocContext *ctx) = 0;

  virtual void enterN3Statement(n3Parser::N3StatementContext *ctx) = 0;
  virtual void exitN3Statement(n3Parser::N3StatementContext *ctx) = 0;

  virtual void enterN3Directive(n3Parser::N3DirectiveContext *ctx) = 0;
  virtual void exitN3Directive(n3Parser::N3DirectiveContext *ctx) = 0;

  virtual void enterSparqlDirective(n3Parser::SparqlDirectiveContext *ctx) = 0;
  virtual void exitSparqlDirective(n3Parser::SparqlDirectiveContext *ctx) = 0;

  virtual void enterSparqlBase(n3Parser::SparqlBaseContext *ctx) = 0;
  virtual void exitSparqlBase(n3Parser::SparqlBaseContext *ctx) = 0;

  virtual void enterSparqlPrefix(n3Parser::SparqlPrefixContext *ctx) = 0;
  virtual void exitSparqlPrefix(n3Parser::SparqlPrefixContext *ctx) = 0;

  virtual void enterPrefixID(n3Parser::PrefixIDContext *ctx) = 0;
  virtual void exitPrefixID(n3Parser::PrefixIDContext *ctx) = 0;

  virtual void enterBase(n3Parser::BaseContext *ctx) = 0;
  virtual void exitBase(n3Parser::BaseContext *ctx) = 0;

  virtual void enterTriples(n3Parser::TriplesContext *ctx) = 0;
  virtual void exitTriples(n3Parser::TriplesContext *ctx) = 0;

  virtual void enterPredicateObjectList(n3Parser::PredicateObjectListContext *ctx) = 0;
  virtual void exitPredicateObjectList(n3Parser::PredicateObjectListContext *ctx) = 0;

  virtual void enterObjectList(n3Parser::ObjectListContext *ctx) = 0;
  virtual void exitObjectList(n3Parser::ObjectListContext *ctx) = 0;

  virtual void enterVerb(n3Parser::VerbContext *ctx) = 0;
  virtual void exitVerb(n3Parser::VerbContext *ctx) = 0;

  virtual void enterSubject(n3Parser::SubjectContext *ctx) = 0;
  virtual void exitSubject(n3Parser::SubjectContext *ctx) = 0;

  virtual void enterPredicate(n3Parser::PredicateContext *ctx) = 0;
  virtual void exitPredicate(n3Parser::PredicateContext *ctx) = 0;

  virtual void enterObject(n3Parser::ObjectContext *ctx) = 0;
  virtual void exitObject(n3Parser::ObjectContext *ctx) = 0;

  virtual void enterExpression(n3Parser::ExpressionContext *ctx) = 0;
  virtual void exitExpression(n3Parser::ExpressionContext *ctx) = 0;

  virtual void enterPath(n3Parser::PathContext *ctx) = 0;
  virtual void exitPath(n3Parser::PathContext *ctx) = 0;

  virtual void enterPathItem(n3Parser::PathItemContext *ctx) = 0;
  virtual void exitPathItem(n3Parser::PathItemContext *ctx) = 0;

  virtual void enterLiteral(n3Parser::LiteralContext *ctx) = 0;
  virtual void exitLiteral(n3Parser::LiteralContext *ctx) = 0;

  virtual void enterBlankNodePropertyList(n3Parser::BlankNodePropertyListContext *ctx) = 0;
  virtual void exitBlankNodePropertyList(n3Parser::BlankNodePropertyListContext *ctx) = 0;

  virtual void enterIriPropertyList(n3Parser::IriPropertyListContext *ctx) = 0;
  virtual void exitIriPropertyList(n3Parser::IriPropertyListContext *ctx) = 0;

  virtual void enterCollection(n3Parser::CollectionContext *ctx) = 0;
  virtual void exitCollection(n3Parser::CollectionContext *ctx) = 0;

  virtual void enterFormula(n3Parser::FormulaContext *ctx) = 0;
  virtual void exitFormula(n3Parser::FormulaContext *ctx) = 0;

  virtual void enterFormulaContent(n3Parser::FormulaContentContext *ctx) = 0;
  virtual void exitFormulaContent(n3Parser::FormulaContentContext *ctx) = 0;

  virtual void enterNumericLiteral(n3Parser::NumericLiteralContext *ctx) = 0;
  virtual void exitNumericLiteral(n3Parser::NumericLiteralContext *ctx) = 0;

  virtual void enterRdfLiteral(n3Parser::RdfLiteralContext *ctx) = 0;
  virtual void exitRdfLiteral(n3Parser::RdfLiteralContext *ctx) = 0;

  virtual void enterIri(n3Parser::IriContext *ctx) = 0;
  virtual void exitIri(n3Parser::IriContext *ctx) = 0;

  virtual void enterPrefixedName(n3Parser::PrefixedNameContext *ctx) = 0;
  virtual void exitPrefixedName(n3Parser::PrefixedNameContext *ctx) = 0;

  virtual void enterBlankNode(n3Parser::BlankNodeContext *ctx) = 0;
  virtual void exitBlankNode(n3Parser::BlankNodeContext *ctx) = 0;

  virtual void enterQuickVar(n3Parser::QuickVarContext *ctx) = 0;
  virtual void exitQuickVar(n3Parser::QuickVarContext *ctx) = 0;


};

