
// Generated from ../../grammar/n3.g4 by ANTLR 4.13.2


#include "n3Listener.h"

#include "n3Parser.h"


using namespace antlrcpp;

using namespace antlr4;

namespace {

struct N3ParserStaticData final {
  N3ParserStaticData(std::vector<std::string> ruleNames,
                        std::vector<std::string> literalNames,
                        std::vector<std::string> symbolicNames)
      : ruleNames(std::move(ruleNames)), literalNames(std::move(literalNames)),
        symbolicNames(std::move(symbolicNames)),
        vocabulary(this->literalNames, this->symbolicNames) {}

  N3ParserStaticData(const N3ParserStaticData&) = delete;
  N3ParserStaticData(N3ParserStaticData&&) = delete;
  N3ParserStaticData& operator=(const N3ParserStaticData&) = delete;
  N3ParserStaticData& operator=(N3ParserStaticData&&) = delete;

  std::vector<antlr4::dfa::DFA> decisionToDFA;
  antlr4::atn::PredictionContextCache sharedContextCache;
  const std::vector<std::string> ruleNames;
  const std::vector<std::string> literalNames;
  const std::vector<std::string> symbolicNames;
  const antlr4::dfa::Vocabulary vocabulary;
  antlr4::atn::SerializedATNView serializedATN;
  std::unique_ptr<antlr4::atn::ATN> atn;
};

::antlr4::internal::OnceFlag n3ParserOnceFlag;
#if ANTLR4_USE_THREAD_LOCAL_CACHE
static thread_local
#endif
std::unique_ptr<N3ParserStaticData> n3ParserStaticData = nullptr;

void n3ParserInitialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  if (n3ParserStaticData != nullptr) {
    return;
  }
#else
  assert(n3ParserStaticData == nullptr);
#endif
  auto staticData = std::make_unique<N3ParserStaticData>(
    std::vector<std::string>{
      "n3Doc", "n3Statement", "n3Directive", "sparqlDirective", "sparqlBase", 
      "sparqlPrefix", "prefixID", "base", "triples", "predicateObjectList", 
      "objectList", "verb", "subject", "predicate", "object", "expression", 
      "path", "pathItem", "literal", "blankNodePropertyList", "iriPropertyList", 
      "collection", "formula", "formulaContent", "numericLiteral", "rdfLiteral", 
      "iri", "prefixedName", "blankNode", "quickVar"
    },
    std::vector<std::string>{
      "", "'.'", "'@prefix'", "'@base'", "';'", "','", "'a'", "'has'", "'is'", 
      "'of'", "'='", "'<='", "'=>'", "'<-'", "'!'", "'^'", "'['", "']'", 
      "'('", "')'", "'{'", "'}'", "'^^'"
    },
    std::vector<std::string>{
      "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", 
      "", "", "", "", "", "", "COMMENT", "BooleanLiteral", "String", "IRIREF", 
      "PNAME_NS", "PNAME_LN", "BLANK_NODE_LABEL", "LANGTAG", "INTEGER", 
      "DECIMAL", "DOUBLE", "EXPONENT", "STRING_LITERAL_LONG_SINGLE_QUOTE", 
      "STRING_LITERAL_LONG_QUOTE", "STRING_LITERAL_QUOTE", "STRING_LITERAL_SINGLE_QUOTE", 
      "UCHAR", "ECHAR", "WS", "IPLSTART", "ANON", "QuickVarName", "PN_CHARS_U", 
      "PN_CHARS_BASE", "PN_CHARS", "BASE", "PREFIX", "PN_PREFIX", "PN_LOCAL", 
      "PLX", "PERCENT", "HEX", "PN_LOCAL_ESC"
    }
  );
  static const int32_t serializedATNSegment[] = {
  	4,1,55,224,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,6,2,
  	7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,2,14,7,
  	14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,7,20,2,21,7,
  	21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,2,27,7,27,2,28,7,
  	28,2,29,7,29,1,0,1,0,1,0,1,0,5,0,65,8,0,10,0,12,0,68,9,0,1,0,1,0,1,1,
  	1,1,3,1,74,8,1,1,2,1,2,3,2,78,8,2,1,3,1,3,3,3,82,8,3,1,4,1,4,1,4,1,5,
  	1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,8,1,8,3,8,100,8,8,1,9,1,9,1,
  	9,1,9,1,9,1,9,3,9,108,8,9,5,9,110,8,9,10,9,12,9,113,9,9,1,10,1,10,1,10,
  	5,10,118,8,10,10,10,12,10,121,9,10,1,11,1,11,1,11,1,11,1,11,1,11,1,11,
  	1,11,1,11,1,11,1,11,3,11,134,8,11,1,12,1,12,1,13,1,13,1,13,3,13,141,8,
  	13,1,14,1,14,1,15,1,15,1,16,1,16,1,16,1,16,1,16,3,16,152,8,16,1,17,1,
  	17,1,17,1,17,1,17,1,17,1,17,1,17,3,17,162,8,17,1,18,1,18,1,18,3,18,167,
  	8,18,1,19,1,19,1,19,1,19,1,20,1,20,1,20,1,20,1,20,1,21,1,21,5,21,180,
  	8,21,10,21,12,21,183,9,21,1,21,1,21,1,22,1,22,3,22,189,8,22,1,22,1,22,
  	1,23,1,23,1,23,3,23,196,8,23,3,23,198,8,23,1,23,1,23,3,23,202,8,23,3,
  	23,204,8,23,1,24,1,24,1,25,1,25,1,25,1,25,3,25,212,8,25,1,26,1,26,3,26,
  	216,8,26,1,27,1,27,1,28,1,28,1,29,1,29,1,29,0,0,30,0,2,4,6,8,10,12,14,
  	16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,0,3,
  	1,0,31,33,1,0,27,28,2,0,29,29,43,43,229,0,66,1,0,0,0,2,73,1,0,0,0,4,77,
  	1,0,0,0,6,81,1,0,0,0,8,83,1,0,0,0,10,86,1,0,0,0,12,90,1,0,0,0,14,94,1,
  	0,0,0,16,97,1,0,0,0,18,101,1,0,0,0,20,114,1,0,0,0,22,133,1,0,0,0,24,135,
  	1,0,0,0,26,140,1,0,0,0,28,142,1,0,0,0,30,144,1,0,0,0,32,146,1,0,0,0,34,
  	161,1,0,0,0,36,166,1,0,0,0,38,168,1,0,0,0,40,172,1,0,0,0,42,177,1,0,0,
  	0,44,186,1,0,0,0,46,203,1,0,0,0,48,205,1,0,0,0,50,207,1,0,0,0,52,215,
  	1,0,0,0,54,217,1,0,0,0,56,219,1,0,0,0,58,221,1,0,0,0,60,61,3,2,1,0,61,
  	62,5,1,0,0,62,65,1,0,0,0,63,65,3,6,3,0,64,60,1,0,0,0,64,63,1,0,0,0,65,
  	68,1,0,0,0,66,64,1,0,0,0,66,67,1,0,0,0,67,69,1,0,0,0,68,66,1,0,0,0,69,
  	70,5,0,0,1,70,1,1,0,0,0,71,74,3,4,2,0,72,74,3,16,8,0,73,71,1,0,0,0,73,
  	72,1,0,0,0,74,3,1,0,0,0,75,78,3,12,6,0,76,78,3,14,7,0,77,75,1,0,0,0,77,
  	76,1,0,0,0,78,5,1,0,0,0,79,82,3,8,4,0,80,82,3,10,5,0,81,79,1,0,0,0,81,
  	80,1,0,0,0,82,7,1,0,0,0,83,84,5,48,0,0,84,85,5,26,0,0,85,9,1,0,0,0,86,
  	87,5,49,0,0,87,88,5,27,0,0,88,89,5,26,0,0,89,11,1,0,0,0,90,91,5,2,0,0,
  	91,92,5,27,0,0,92,93,5,26,0,0,93,13,1,0,0,0,94,95,5,3,0,0,95,96,5,26,
  	0,0,96,15,1,0,0,0,97,99,3,24,12,0,98,100,3,18,9,0,99,98,1,0,0,0,99,100,
  	1,0,0,0,100,17,1,0,0,0,101,102,3,22,11,0,102,111,3,20,10,0,103,107,5,
  	4,0,0,104,105,3,22,11,0,105,106,3,20,10,0,106,108,1,0,0,0,107,104,1,0,
  	0,0,107,108,1,0,0,0,108,110,1,0,0,0,109,103,1,0,0,0,110,113,1,0,0,0,111,
  	109,1,0,0,0,111,112,1,0,0,0,112,19,1,0,0,0,113,111,1,0,0,0,114,119,3,
  	28,14,0,115,116,5,5,0,0,116,118,3,28,14,0,117,115,1,0,0,0,118,121,1,0,
  	0,0,119,117,1,0,0,0,119,120,1,0,0,0,120,21,1,0,0,0,121,119,1,0,0,0,122,
  	134,3,26,13,0,123,134,5,6,0,0,124,125,5,7,0,0,125,134,3,30,15,0,126,127,
  	5,8,0,0,127,128,3,30,15,0,128,129,5,9,0,0,129,134,1,0,0,0,130,134,5,10,
  	0,0,131,134,5,11,0,0,132,134,5,12,0,0,133,122,1,0,0,0,133,123,1,0,0,0,
  	133,124,1,0,0,0,133,126,1,0,0,0,133,130,1,0,0,0,133,131,1,0,0,0,133,132,
  	1,0,0,0,134,23,1,0,0,0,135,136,3,30,15,0,136,25,1,0,0,0,137,141,3,30,
  	15,0,138,139,5,13,0,0,139,141,3,30,15,0,140,137,1,0,0,0,140,138,1,0,0,
  	0,141,27,1,0,0,0,142,143,3,30,15,0,143,29,1,0,0,0,144,145,3,32,16,0,145,
  	31,1,0,0,0,146,151,3,34,17,0,147,148,5,14,0,0,148,152,3,32,16,0,149,150,
  	5,15,0,0,150,152,3,32,16,0,151,147,1,0,0,0,151,149,1,0,0,0,151,152,1,
  	0,0,0,152,33,1,0,0,0,153,162,3,52,26,0,154,162,3,56,28,0,155,162,3,58,
  	29,0,156,162,3,42,21,0,157,162,3,38,19,0,158,162,3,40,20,0,159,162,3,
  	36,18,0,160,162,3,44,22,0,161,153,1,0,0,0,161,154,1,0,0,0,161,155,1,0,
  	0,0,161,156,1,0,0,0,161,157,1,0,0,0,161,158,1,0,0,0,161,159,1,0,0,0,161,
  	160,1,0,0,0,162,35,1,0,0,0,163,167,3,50,25,0,164,167,3,48,24,0,165,167,
  	5,24,0,0,166,163,1,0,0,0,166,164,1,0,0,0,166,165,1,0,0,0,167,37,1,0,0,
  	0,168,169,5,16,0,0,169,170,3,18,9,0,170,171,5,17,0,0,171,39,1,0,0,0,172,
  	173,5,42,0,0,173,174,3,52,26,0,174,175,3,18,9,0,175,176,5,17,0,0,176,
  	41,1,0,0,0,177,181,5,18,0,0,178,180,3,28,14,0,179,178,1,0,0,0,180,183,
  	1,0,0,0,181,179,1,0,0,0,181,182,1,0,0,0,182,184,1,0,0,0,183,181,1,0,0,
  	0,184,185,5,19,0,0,185,43,1,0,0,0,186,188,5,20,0,0,187,189,3,46,23,0,
  	188,187,1,0,0,0,188,189,1,0,0,0,189,190,1,0,0,0,190,191,5,21,0,0,191,
  	45,1,0,0,0,192,197,3,2,1,0,193,195,5,1,0,0,194,196,3,46,23,0,195,194,
  	1,0,0,0,195,196,1,0,0,0,196,198,1,0,0,0,197,193,1,0,0,0,197,198,1,0,0,
  	0,198,204,1,0,0,0,199,201,3,6,3,0,200,202,3,46,23,0,201,200,1,0,0,0,201,
  	202,1,0,0,0,202,204,1,0,0,0,203,192,1,0,0,0,203,199,1,0,0,0,204,47,1,
  	0,0,0,205,206,7,0,0,0,206,49,1,0,0,0,207,211,5,25,0,0,208,212,5,30,0,
  	0,209,210,5,22,0,0,210,212,3,52,26,0,211,208,1,0,0,0,211,209,1,0,0,0,
  	211,212,1,0,0,0,212,51,1,0,0,0,213,216,5,26,0,0,214,216,3,54,27,0,215,
  	213,1,0,0,0,215,214,1,0,0,0,216,53,1,0,0,0,217,218,7,1,0,0,218,55,1,0,
  	0,0,219,220,7,2,0,0,220,57,1,0,0,0,221,222,5,44,0,0,222,59,1,0,0,0,22,
  	64,66,73,77,81,99,107,111,119,133,140,151,161,166,181,188,195,197,201,
  	203,211,215
  };
  staticData->serializedATN = antlr4::atn::SerializedATNView(serializedATNSegment, sizeof(serializedATNSegment) / sizeof(serializedATNSegment[0]));

  antlr4::atn::ATNDeserializer deserializer;
  staticData->atn = deserializer.deserialize(staticData->serializedATN);

  const size_t count = staticData->atn->getNumberOfDecisions();
  staticData->decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    staticData->decisionToDFA.emplace_back(staticData->atn->getDecisionState(i), i);
  }
  n3ParserStaticData = std::move(staticData);
}

}

n3Parser::n3Parser(TokenStream *input) : n3Parser(input, antlr4::atn::ParserATNSimulatorOptions()) {}

n3Parser::n3Parser(TokenStream *input, const antlr4::atn::ParserATNSimulatorOptions &options) : Parser(input) {
  n3Parser::initialize();
  _interpreter = new atn::ParserATNSimulator(this, *n3ParserStaticData->atn, n3ParserStaticData->decisionToDFA, n3ParserStaticData->sharedContextCache, options);
}

n3Parser::~n3Parser() {
  delete _interpreter;
}

const atn::ATN& n3Parser::getATN() const {
  return *n3ParserStaticData->atn;
}

std::string n3Parser::getGrammarFileName() const {
  return "n3.g4";
}

const std::vector<std::string>& n3Parser::getRuleNames() const {
  return n3ParserStaticData->ruleNames;
}

const dfa::Vocabulary& n3Parser::getVocabulary() const {
  return n3ParserStaticData->vocabulary;
}

antlr4::atn::SerializedATNView n3Parser::getSerializedATN() const {
  return n3ParserStaticData->serializedATN;
}


//----------------- N3DocContext ------------------------------------------------------------------

n3Parser::N3DocContext::N3DocContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* n3Parser::N3DocContext::EOF() {
  return getToken(n3Parser::EOF, 0);
}

std::vector<n3Parser::N3StatementContext *> n3Parser::N3DocContext::n3Statement() {
  return getRuleContexts<n3Parser::N3StatementContext>();
}

n3Parser::N3StatementContext* n3Parser::N3DocContext::n3Statement(size_t i) {
  return getRuleContext<n3Parser::N3StatementContext>(i);
}

std::vector<n3Parser::SparqlDirectiveContext *> n3Parser::N3DocContext::sparqlDirective() {
  return getRuleContexts<n3Parser::SparqlDirectiveContext>();
}

n3Parser::SparqlDirectiveContext* n3Parser::N3DocContext::sparqlDirective(size_t i) {
  return getRuleContext<n3Parser::SparqlDirectiveContext>(i);
}


size_t n3Parser::N3DocContext::getRuleIndex() const {
  return n3Parser::RuleN3Doc;
}

void n3Parser::N3DocContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterN3Doc(this);
}

void n3Parser::N3DocContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitN3Doc(this);
}

n3Parser::N3DocContext* n3Parser::n3Doc() {
  N3DocContext *_localctx = _tracker.createInstance<N3DocContext>(_ctx, getState());
  enterRule(_localctx, 0, n3Parser::RuleN3Doc);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(66);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 875227346436108) != 0)) {
      setState(64);
      _errHandler->sync(this);
      switch (_input->LA(1)) {
        case n3Parser::T__1:
        case n3Parser::T__2:
        case n3Parser::T__15:
        case n3Parser::T__17:
        case n3Parser::T__19:
        case n3Parser::BooleanLiteral:
        case n3Parser::String:
        case n3Parser::IRIREF:
        case n3Parser::PNAME_NS:
        case n3Parser::PNAME_LN:
        case n3Parser::BLANK_NODE_LABEL:
        case n3Parser::INTEGER:
        case n3Parser::DECIMAL:
        case n3Parser::DOUBLE:
        case n3Parser::IPLSTART:
        case n3Parser::ANON:
        case n3Parser::QuickVarName: {
          setState(60);
          n3Statement();
          setState(61);
          match(n3Parser::T__0);
          break;
        }

        case n3Parser::BASE:
        case n3Parser::PREFIX: {
          setState(63);
          sparqlDirective();
          break;
        }

      default:
        throw NoViableAltException(this);
      }
      setState(68);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(69);
    match(n3Parser::EOF);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- N3StatementContext ------------------------------------------------------------------

n3Parser::N3StatementContext::N3StatementContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::N3DirectiveContext* n3Parser::N3StatementContext::n3Directive() {
  return getRuleContext<n3Parser::N3DirectiveContext>(0);
}

n3Parser::TriplesContext* n3Parser::N3StatementContext::triples() {
  return getRuleContext<n3Parser::TriplesContext>(0);
}


size_t n3Parser::N3StatementContext::getRuleIndex() const {
  return n3Parser::RuleN3Statement;
}

void n3Parser::N3StatementContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterN3Statement(this);
}

void n3Parser::N3StatementContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitN3Statement(this);
}

n3Parser::N3StatementContext* n3Parser::n3Statement() {
  N3StatementContext *_localctx = _tracker.createInstance<N3StatementContext>(_ctx, getState());
  enterRule(_localctx, 2, n3Parser::RuleN3Statement);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(73);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case n3Parser::T__1:
      case n3Parser::T__2: {
        enterOuterAlt(_localctx, 1);
        setState(71);
        n3Directive();
        break;
      }

      case n3Parser::T__15:
      case n3Parser::T__17:
      case n3Parser::T__19:
      case n3Parser::BooleanLiteral:
      case n3Parser::String:
      case n3Parser::IRIREF:
      case n3Parser::PNAME_NS:
      case n3Parser::PNAME_LN:
      case n3Parser::BLANK_NODE_LABEL:
      case n3Parser::INTEGER:
      case n3Parser::DECIMAL:
      case n3Parser::DOUBLE:
      case n3Parser::IPLSTART:
      case n3Parser::ANON:
      case n3Parser::QuickVarName: {
        enterOuterAlt(_localctx, 2);
        setState(72);
        triples();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- N3DirectiveContext ------------------------------------------------------------------

n3Parser::N3DirectiveContext::N3DirectiveContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::PrefixIDContext* n3Parser::N3DirectiveContext::prefixID() {
  return getRuleContext<n3Parser::PrefixIDContext>(0);
}

n3Parser::BaseContext* n3Parser::N3DirectiveContext::base() {
  return getRuleContext<n3Parser::BaseContext>(0);
}


size_t n3Parser::N3DirectiveContext::getRuleIndex() const {
  return n3Parser::RuleN3Directive;
}

void n3Parser::N3DirectiveContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterN3Directive(this);
}

void n3Parser::N3DirectiveContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitN3Directive(this);
}

n3Parser::N3DirectiveContext* n3Parser::n3Directive() {
  N3DirectiveContext *_localctx = _tracker.createInstance<N3DirectiveContext>(_ctx, getState());
  enterRule(_localctx, 4, n3Parser::RuleN3Directive);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(77);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case n3Parser::T__1: {
        enterOuterAlt(_localctx, 1);
        setState(75);
        prefixID();
        break;
      }

      case n3Parser::T__2: {
        enterOuterAlt(_localctx, 2);
        setState(76);
        base();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- SparqlDirectiveContext ------------------------------------------------------------------

n3Parser::SparqlDirectiveContext::SparqlDirectiveContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::SparqlBaseContext* n3Parser::SparqlDirectiveContext::sparqlBase() {
  return getRuleContext<n3Parser::SparqlBaseContext>(0);
}

n3Parser::SparqlPrefixContext* n3Parser::SparqlDirectiveContext::sparqlPrefix() {
  return getRuleContext<n3Parser::SparqlPrefixContext>(0);
}


size_t n3Parser::SparqlDirectiveContext::getRuleIndex() const {
  return n3Parser::RuleSparqlDirective;
}

void n3Parser::SparqlDirectiveContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterSparqlDirective(this);
}

void n3Parser::SparqlDirectiveContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitSparqlDirective(this);
}

n3Parser::SparqlDirectiveContext* n3Parser::sparqlDirective() {
  SparqlDirectiveContext *_localctx = _tracker.createInstance<SparqlDirectiveContext>(_ctx, getState());
  enterRule(_localctx, 6, n3Parser::RuleSparqlDirective);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(81);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case n3Parser::BASE: {
        enterOuterAlt(_localctx, 1);
        setState(79);
        sparqlBase();
        break;
      }

      case n3Parser::PREFIX: {
        enterOuterAlt(_localctx, 2);
        setState(80);
        sparqlPrefix();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- SparqlBaseContext ------------------------------------------------------------------

n3Parser::SparqlBaseContext::SparqlBaseContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* n3Parser::SparqlBaseContext::BASE() {
  return getToken(n3Parser::BASE, 0);
}

tree::TerminalNode* n3Parser::SparqlBaseContext::IRIREF() {
  return getToken(n3Parser::IRIREF, 0);
}


size_t n3Parser::SparqlBaseContext::getRuleIndex() const {
  return n3Parser::RuleSparqlBase;
}

void n3Parser::SparqlBaseContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterSparqlBase(this);
}

void n3Parser::SparqlBaseContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitSparqlBase(this);
}

n3Parser::SparqlBaseContext* n3Parser::sparqlBase() {
  SparqlBaseContext *_localctx = _tracker.createInstance<SparqlBaseContext>(_ctx, getState());
  enterRule(_localctx, 8, n3Parser::RuleSparqlBase);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(83);
    match(n3Parser::BASE);
    setState(84);
    match(n3Parser::IRIREF);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- SparqlPrefixContext ------------------------------------------------------------------

n3Parser::SparqlPrefixContext::SparqlPrefixContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* n3Parser::SparqlPrefixContext::PREFIX() {
  return getToken(n3Parser::PREFIX, 0);
}

tree::TerminalNode* n3Parser::SparqlPrefixContext::PNAME_NS() {
  return getToken(n3Parser::PNAME_NS, 0);
}

tree::TerminalNode* n3Parser::SparqlPrefixContext::IRIREF() {
  return getToken(n3Parser::IRIREF, 0);
}


size_t n3Parser::SparqlPrefixContext::getRuleIndex() const {
  return n3Parser::RuleSparqlPrefix;
}

void n3Parser::SparqlPrefixContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterSparqlPrefix(this);
}

void n3Parser::SparqlPrefixContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitSparqlPrefix(this);
}

n3Parser::SparqlPrefixContext* n3Parser::sparqlPrefix() {
  SparqlPrefixContext *_localctx = _tracker.createInstance<SparqlPrefixContext>(_ctx, getState());
  enterRule(_localctx, 10, n3Parser::RuleSparqlPrefix);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(86);
    match(n3Parser::PREFIX);
    setState(87);
    match(n3Parser::PNAME_NS);
    setState(88);
    match(n3Parser::IRIREF);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- PrefixIDContext ------------------------------------------------------------------

n3Parser::PrefixIDContext::PrefixIDContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* n3Parser::PrefixIDContext::PNAME_NS() {
  return getToken(n3Parser::PNAME_NS, 0);
}

tree::TerminalNode* n3Parser::PrefixIDContext::IRIREF() {
  return getToken(n3Parser::IRIREF, 0);
}


size_t n3Parser::PrefixIDContext::getRuleIndex() const {
  return n3Parser::RulePrefixID;
}

void n3Parser::PrefixIDContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrefixID(this);
}

void n3Parser::PrefixIDContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrefixID(this);
}

n3Parser::PrefixIDContext* n3Parser::prefixID() {
  PrefixIDContext *_localctx = _tracker.createInstance<PrefixIDContext>(_ctx, getState());
  enterRule(_localctx, 12, n3Parser::RulePrefixID);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(90);
    match(n3Parser::T__1);
    setState(91);
    match(n3Parser::PNAME_NS);
    setState(92);
    match(n3Parser::IRIREF);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- BaseContext ------------------------------------------------------------------

n3Parser::BaseContext::BaseContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* n3Parser::BaseContext::IRIREF() {
  return getToken(n3Parser::IRIREF, 0);
}


size_t n3Parser::BaseContext::getRuleIndex() const {
  return n3Parser::RuleBase;
}

void n3Parser::BaseContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterBase(this);
}

void n3Parser::BaseContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitBase(this);
}

n3Parser::BaseContext* n3Parser::base() {
  BaseContext *_localctx = _tracker.createInstance<BaseContext>(_ctx, getState());
  enterRule(_localctx, 14, n3Parser::RuleBase);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(94);
    match(n3Parser::T__2);
    setState(95);
    match(n3Parser::IRIREF);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- TriplesContext ------------------------------------------------------------------

n3Parser::TriplesContext::TriplesContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::SubjectContext* n3Parser::TriplesContext::subject() {
  return getRuleContext<n3Parser::SubjectContext>(0);
}

n3Parser::PredicateObjectListContext* n3Parser::TriplesContext::predicateObjectList() {
  return getRuleContext<n3Parser::PredicateObjectListContext>(0);
}


size_t n3Parser::TriplesContext::getRuleIndex() const {
  return n3Parser::RuleTriples;
}

void n3Parser::TriplesContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterTriples(this);
}

void n3Parser::TriplesContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitTriples(this);
}

n3Parser::TriplesContext* n3Parser::triples() {
  TriplesContext *_localctx = _tracker.createInstance<TriplesContext>(_ctx, getState());
  enterRule(_localctx, 16, n3Parser::RuleTriples);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(97);
    subject();
    setState(99);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 30802416319936) != 0)) {
      setState(98);
      predicateObjectList();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- PredicateObjectListContext ------------------------------------------------------------------

n3Parser::PredicateObjectListContext::PredicateObjectListContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<n3Parser::VerbContext *> n3Parser::PredicateObjectListContext::verb() {
  return getRuleContexts<n3Parser::VerbContext>();
}

n3Parser::VerbContext* n3Parser::PredicateObjectListContext::verb(size_t i) {
  return getRuleContext<n3Parser::VerbContext>(i);
}

std::vector<n3Parser::ObjectListContext *> n3Parser::PredicateObjectListContext::objectList() {
  return getRuleContexts<n3Parser::ObjectListContext>();
}

n3Parser::ObjectListContext* n3Parser::PredicateObjectListContext::objectList(size_t i) {
  return getRuleContext<n3Parser::ObjectListContext>(i);
}


size_t n3Parser::PredicateObjectListContext::getRuleIndex() const {
  return n3Parser::RulePredicateObjectList;
}

void n3Parser::PredicateObjectListContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPredicateObjectList(this);
}

void n3Parser::PredicateObjectListContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPredicateObjectList(this);
}

n3Parser::PredicateObjectListContext* n3Parser::predicateObjectList() {
  PredicateObjectListContext *_localctx = _tracker.createInstance<PredicateObjectListContext>(_ctx, getState());
  enterRule(_localctx, 18, n3Parser::RulePredicateObjectList);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(101);
    verb();
    setState(102);
    objectList();
    setState(111);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == n3Parser::T__3) {
      setState(103);
      match(n3Parser::T__3);
      setState(107);
      _errHandler->sync(this);

      _la = _input->LA(1);
      if ((((_la & ~ 0x3fULL) == 0) &&
        ((1ULL << _la) & 30802416319936) != 0)) {
        setState(104);
        verb();
        setState(105);
        objectList();
      }
      setState(113);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ObjectListContext ------------------------------------------------------------------

n3Parser::ObjectListContext::ObjectListContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<n3Parser::ObjectContext *> n3Parser::ObjectListContext::object() {
  return getRuleContexts<n3Parser::ObjectContext>();
}

n3Parser::ObjectContext* n3Parser::ObjectListContext::object(size_t i) {
  return getRuleContext<n3Parser::ObjectContext>(i);
}


size_t n3Parser::ObjectListContext::getRuleIndex() const {
  return n3Parser::RuleObjectList;
}

void n3Parser::ObjectListContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterObjectList(this);
}

void n3Parser::ObjectListContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitObjectList(this);
}

n3Parser::ObjectListContext* n3Parser::objectList() {
  ObjectListContext *_localctx = _tracker.createInstance<ObjectListContext>(_ctx, getState());
  enterRule(_localctx, 20, n3Parser::RuleObjectList);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(114);
    object();
    setState(119);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == n3Parser::T__4) {
      setState(115);
      match(n3Parser::T__4);
      setState(116);
      object();
      setState(121);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- VerbContext ------------------------------------------------------------------

n3Parser::VerbContext::VerbContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::PredicateContext* n3Parser::VerbContext::predicate() {
  return getRuleContext<n3Parser::PredicateContext>(0);
}

n3Parser::ExpressionContext* n3Parser::VerbContext::expression() {
  return getRuleContext<n3Parser::ExpressionContext>(0);
}


size_t n3Parser::VerbContext::getRuleIndex() const {
  return n3Parser::RuleVerb;
}

void n3Parser::VerbContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterVerb(this);
}

void n3Parser::VerbContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitVerb(this);
}

n3Parser::VerbContext* n3Parser::verb() {
  VerbContext *_localctx = _tracker.createInstance<VerbContext>(_ctx, getState());
  enterRule(_localctx, 22, n3Parser::RuleVerb);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(133);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case n3Parser::T__12:
      case n3Parser::T__15:
      case n3Parser::T__17:
      case n3Parser::T__19:
      case n3Parser::BooleanLiteral:
      case n3Parser::String:
      case n3Parser::IRIREF:
      case n3Parser::PNAME_NS:
      case n3Parser::PNAME_LN:
      case n3Parser::BLANK_NODE_LABEL:
      case n3Parser::INTEGER:
      case n3Parser::DECIMAL:
      case n3Parser::DOUBLE:
      case n3Parser::IPLSTART:
      case n3Parser::ANON:
      case n3Parser::QuickVarName: {
        enterOuterAlt(_localctx, 1);
        setState(122);
        predicate();
        break;
      }

      case n3Parser::T__5: {
        enterOuterAlt(_localctx, 2);
        setState(123);
        match(n3Parser::T__5);
        break;
      }

      case n3Parser::T__6: {
        enterOuterAlt(_localctx, 3);
        setState(124);
        match(n3Parser::T__6);
        setState(125);
        expression();
        break;
      }

      case n3Parser::T__7: {
        enterOuterAlt(_localctx, 4);
        setState(126);
        match(n3Parser::T__7);
        setState(127);
        expression();
        setState(128);
        match(n3Parser::T__8);
        break;
      }

      case n3Parser::T__9: {
        enterOuterAlt(_localctx, 5);
        setState(130);
        match(n3Parser::T__9);
        break;
      }

      case n3Parser::T__10: {
        enterOuterAlt(_localctx, 6);
        setState(131);
        match(n3Parser::T__10);
        break;
      }

      case n3Parser::T__11: {
        enterOuterAlt(_localctx, 7);
        setState(132);
        match(n3Parser::T__11);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- SubjectContext ------------------------------------------------------------------

n3Parser::SubjectContext::SubjectContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::ExpressionContext* n3Parser::SubjectContext::expression() {
  return getRuleContext<n3Parser::ExpressionContext>(0);
}


size_t n3Parser::SubjectContext::getRuleIndex() const {
  return n3Parser::RuleSubject;
}

void n3Parser::SubjectContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterSubject(this);
}

void n3Parser::SubjectContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitSubject(this);
}

n3Parser::SubjectContext* n3Parser::subject() {
  SubjectContext *_localctx = _tracker.createInstance<SubjectContext>(_ctx, getState());
  enterRule(_localctx, 24, n3Parser::RuleSubject);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(135);
    expression();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- PredicateContext ------------------------------------------------------------------

n3Parser::PredicateContext::PredicateContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::ExpressionContext* n3Parser::PredicateContext::expression() {
  return getRuleContext<n3Parser::ExpressionContext>(0);
}


size_t n3Parser::PredicateContext::getRuleIndex() const {
  return n3Parser::RulePredicate;
}

void n3Parser::PredicateContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPredicate(this);
}

void n3Parser::PredicateContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPredicate(this);
}

n3Parser::PredicateContext* n3Parser::predicate() {
  PredicateContext *_localctx = _tracker.createInstance<PredicateContext>(_ctx, getState());
  enterRule(_localctx, 26, n3Parser::RulePredicate);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(140);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case n3Parser::T__15:
      case n3Parser::T__17:
      case n3Parser::T__19:
      case n3Parser::BooleanLiteral:
      case n3Parser::String:
      case n3Parser::IRIREF:
      case n3Parser::PNAME_NS:
      case n3Parser::PNAME_LN:
      case n3Parser::BLANK_NODE_LABEL:
      case n3Parser::INTEGER:
      case n3Parser::DECIMAL:
      case n3Parser::DOUBLE:
      case n3Parser::IPLSTART:
      case n3Parser::ANON:
      case n3Parser::QuickVarName: {
        setState(137);
        expression();
        break;
      }

      case n3Parser::T__12: {
        setState(138);
        match(n3Parser::T__12);
        setState(139);
        expression();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ObjectContext ------------------------------------------------------------------

n3Parser::ObjectContext::ObjectContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::ExpressionContext* n3Parser::ObjectContext::expression() {
  return getRuleContext<n3Parser::ExpressionContext>(0);
}


size_t n3Parser::ObjectContext::getRuleIndex() const {
  return n3Parser::RuleObject;
}

void n3Parser::ObjectContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterObject(this);
}

void n3Parser::ObjectContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitObject(this);
}

n3Parser::ObjectContext* n3Parser::object() {
  ObjectContext *_localctx = _tracker.createInstance<ObjectContext>(_ctx, getState());
  enterRule(_localctx, 28, n3Parser::RuleObject);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(142);
    expression();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ExpressionContext ------------------------------------------------------------------

n3Parser::ExpressionContext::ExpressionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::PathContext* n3Parser::ExpressionContext::path() {
  return getRuleContext<n3Parser::PathContext>(0);
}


size_t n3Parser::ExpressionContext::getRuleIndex() const {
  return n3Parser::RuleExpression;
}

void n3Parser::ExpressionContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression(this);
}

void n3Parser::ExpressionContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression(this);
}

n3Parser::ExpressionContext* n3Parser::expression() {
  ExpressionContext *_localctx = _tracker.createInstance<ExpressionContext>(_ctx, getState());
  enterRule(_localctx, 30, n3Parser::RuleExpression);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(144);
    path();
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- PathContext ------------------------------------------------------------------

n3Parser::PathContext::PathContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::PathItemContext* n3Parser::PathContext::pathItem() {
  return getRuleContext<n3Parser::PathItemContext>(0);
}

n3Parser::PathContext* n3Parser::PathContext::path() {
  return getRuleContext<n3Parser::PathContext>(0);
}


size_t n3Parser::PathContext::getRuleIndex() const {
  return n3Parser::RulePath;
}

void n3Parser::PathContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPath(this);
}

void n3Parser::PathContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPath(this);
}

n3Parser::PathContext* n3Parser::path() {
  PathContext *_localctx = _tracker.createInstance<PathContext>(_ctx, getState());
  enterRule(_localctx, 32, n3Parser::RulePath);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(146);
    pathItem();
    setState(151);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case n3Parser::T__13: {
        setState(147);
        match(n3Parser::T__13);
        setState(148);
        path();
        break;
      }

      case n3Parser::T__14: {
        setState(149);
        match(n3Parser::T__14);
        setState(150);
        path();
        break;
      }

      case n3Parser::T__0:
      case n3Parser::T__3:
      case n3Parser::T__4:
      case n3Parser::T__5:
      case n3Parser::T__6:
      case n3Parser::T__7:
      case n3Parser::T__8:
      case n3Parser::T__9:
      case n3Parser::T__10:
      case n3Parser::T__11:
      case n3Parser::T__12:
      case n3Parser::T__15:
      case n3Parser::T__16:
      case n3Parser::T__17:
      case n3Parser::T__18:
      case n3Parser::T__19:
      case n3Parser::T__20:
      case n3Parser::BooleanLiteral:
      case n3Parser::String:
      case n3Parser::IRIREF:
      case n3Parser::PNAME_NS:
      case n3Parser::PNAME_LN:
      case n3Parser::BLANK_NODE_LABEL:
      case n3Parser::INTEGER:
      case n3Parser::DECIMAL:
      case n3Parser::DOUBLE:
      case n3Parser::IPLSTART:
      case n3Parser::ANON:
      case n3Parser::QuickVarName: {
        break;
      }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- PathItemContext ------------------------------------------------------------------

n3Parser::PathItemContext::PathItemContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::IriContext* n3Parser::PathItemContext::iri() {
  return getRuleContext<n3Parser::IriContext>(0);
}

n3Parser::BlankNodeContext* n3Parser::PathItemContext::blankNode() {
  return getRuleContext<n3Parser::BlankNodeContext>(0);
}

n3Parser::QuickVarContext* n3Parser::PathItemContext::quickVar() {
  return getRuleContext<n3Parser::QuickVarContext>(0);
}

n3Parser::CollectionContext* n3Parser::PathItemContext::collection() {
  return getRuleContext<n3Parser::CollectionContext>(0);
}

n3Parser::BlankNodePropertyListContext* n3Parser::PathItemContext::blankNodePropertyList() {
  return getRuleContext<n3Parser::BlankNodePropertyListContext>(0);
}

n3Parser::IriPropertyListContext* n3Parser::PathItemContext::iriPropertyList() {
  return getRuleContext<n3Parser::IriPropertyListContext>(0);
}

n3Parser::LiteralContext* n3Parser::PathItemContext::literal() {
  return getRuleContext<n3Parser::LiteralContext>(0);
}

n3Parser::FormulaContext* n3Parser::PathItemContext::formula() {
  return getRuleContext<n3Parser::FormulaContext>(0);
}


size_t n3Parser::PathItemContext::getRuleIndex() const {
  return n3Parser::RulePathItem;
}

void n3Parser::PathItemContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPathItem(this);
}

void n3Parser::PathItemContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPathItem(this);
}

n3Parser::PathItemContext* n3Parser::pathItem() {
  PathItemContext *_localctx = _tracker.createInstance<PathItemContext>(_ctx, getState());
  enterRule(_localctx, 34, n3Parser::RulePathItem);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(161);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case n3Parser::IRIREF:
      case n3Parser::PNAME_NS:
      case n3Parser::PNAME_LN: {
        enterOuterAlt(_localctx, 1);
        setState(153);
        iri();
        break;
      }

      case n3Parser::BLANK_NODE_LABEL:
      case n3Parser::ANON: {
        enterOuterAlt(_localctx, 2);
        setState(154);
        blankNode();
        break;
      }

      case n3Parser::QuickVarName: {
        enterOuterAlt(_localctx, 3);
        setState(155);
        quickVar();
        break;
      }

      case n3Parser::T__17: {
        enterOuterAlt(_localctx, 4);
        setState(156);
        collection();
        break;
      }

      case n3Parser::T__15: {
        enterOuterAlt(_localctx, 5);
        setState(157);
        blankNodePropertyList();
        break;
      }

      case n3Parser::IPLSTART: {
        enterOuterAlt(_localctx, 6);
        setState(158);
        iriPropertyList();
        break;
      }

      case n3Parser::BooleanLiteral:
      case n3Parser::String:
      case n3Parser::INTEGER:
      case n3Parser::DECIMAL:
      case n3Parser::DOUBLE: {
        enterOuterAlt(_localctx, 7);
        setState(159);
        literal();
        break;
      }

      case n3Parser::T__19: {
        enterOuterAlt(_localctx, 8);
        setState(160);
        formula();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- LiteralContext ------------------------------------------------------------------

n3Parser::LiteralContext::LiteralContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::RdfLiteralContext* n3Parser::LiteralContext::rdfLiteral() {
  return getRuleContext<n3Parser::RdfLiteralContext>(0);
}

n3Parser::NumericLiteralContext* n3Parser::LiteralContext::numericLiteral() {
  return getRuleContext<n3Parser::NumericLiteralContext>(0);
}

tree::TerminalNode* n3Parser::LiteralContext::BooleanLiteral() {
  return getToken(n3Parser::BooleanLiteral, 0);
}


size_t n3Parser::LiteralContext::getRuleIndex() const {
  return n3Parser::RuleLiteral;
}

void n3Parser::LiteralContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterLiteral(this);
}

void n3Parser::LiteralContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitLiteral(this);
}

n3Parser::LiteralContext* n3Parser::literal() {
  LiteralContext *_localctx = _tracker.createInstance<LiteralContext>(_ctx, getState());
  enterRule(_localctx, 36, n3Parser::RuleLiteral);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(166);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case n3Parser::String: {
        enterOuterAlt(_localctx, 1);
        setState(163);
        rdfLiteral();
        break;
      }

      case n3Parser::INTEGER:
      case n3Parser::DECIMAL:
      case n3Parser::DOUBLE: {
        enterOuterAlt(_localctx, 2);
        setState(164);
        numericLiteral();
        break;
      }

      case n3Parser::BooleanLiteral: {
        enterOuterAlt(_localctx, 3);
        setState(165);
        match(n3Parser::BooleanLiteral);
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- BlankNodePropertyListContext ------------------------------------------------------------------

n3Parser::BlankNodePropertyListContext::BlankNodePropertyListContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::PredicateObjectListContext* n3Parser::BlankNodePropertyListContext::predicateObjectList() {
  return getRuleContext<n3Parser::PredicateObjectListContext>(0);
}


size_t n3Parser::BlankNodePropertyListContext::getRuleIndex() const {
  return n3Parser::RuleBlankNodePropertyList;
}

void n3Parser::BlankNodePropertyListContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterBlankNodePropertyList(this);
}

void n3Parser::BlankNodePropertyListContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitBlankNodePropertyList(this);
}

n3Parser::BlankNodePropertyListContext* n3Parser::blankNodePropertyList() {
  BlankNodePropertyListContext *_localctx = _tracker.createInstance<BlankNodePropertyListContext>(_ctx, getState());
  enterRule(_localctx, 38, n3Parser::RuleBlankNodePropertyList);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(168);
    match(n3Parser::T__15);
    setState(169);
    predicateObjectList();
    setState(170);
    match(n3Parser::T__16);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- IriPropertyListContext ------------------------------------------------------------------

n3Parser::IriPropertyListContext::IriPropertyListContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* n3Parser::IriPropertyListContext::IPLSTART() {
  return getToken(n3Parser::IPLSTART, 0);
}

n3Parser::IriContext* n3Parser::IriPropertyListContext::iri() {
  return getRuleContext<n3Parser::IriContext>(0);
}

n3Parser::PredicateObjectListContext* n3Parser::IriPropertyListContext::predicateObjectList() {
  return getRuleContext<n3Parser::PredicateObjectListContext>(0);
}


size_t n3Parser::IriPropertyListContext::getRuleIndex() const {
  return n3Parser::RuleIriPropertyList;
}

void n3Parser::IriPropertyListContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterIriPropertyList(this);
}

void n3Parser::IriPropertyListContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitIriPropertyList(this);
}

n3Parser::IriPropertyListContext* n3Parser::iriPropertyList() {
  IriPropertyListContext *_localctx = _tracker.createInstance<IriPropertyListContext>(_ctx, getState());
  enterRule(_localctx, 40, n3Parser::RuleIriPropertyList);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(172);
    match(n3Parser::IPLSTART);
    setState(173);
    iri();
    setState(174);
    predicateObjectList();
    setState(175);
    match(n3Parser::T__16);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- CollectionContext ------------------------------------------------------------------

n3Parser::CollectionContext::CollectionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<n3Parser::ObjectContext *> n3Parser::CollectionContext::object() {
  return getRuleContexts<n3Parser::ObjectContext>();
}

n3Parser::ObjectContext* n3Parser::CollectionContext::object(size_t i) {
  return getRuleContext<n3Parser::ObjectContext>(i);
}


size_t n3Parser::CollectionContext::getRuleIndex() const {
  return n3Parser::RuleCollection;
}

void n3Parser::CollectionContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterCollection(this);
}

void n3Parser::CollectionContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitCollection(this);
}

n3Parser::CollectionContext* n3Parser::collection() {
  CollectionContext *_localctx = _tracker.createInstance<CollectionContext>(_ctx, getState());
  enterRule(_localctx, 42, n3Parser::RuleCollection);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(177);
    match(n3Parser::T__17);
    setState(181);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 30802416304128) != 0)) {
      setState(178);
      object();
      setState(183);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
    setState(184);
    match(n3Parser::T__18);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- FormulaContext ------------------------------------------------------------------

n3Parser::FormulaContext::FormulaContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::FormulaContentContext* n3Parser::FormulaContext::formulaContent() {
  return getRuleContext<n3Parser::FormulaContentContext>(0);
}


size_t n3Parser::FormulaContext::getRuleIndex() const {
  return n3Parser::RuleFormula;
}

void n3Parser::FormulaContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFormula(this);
}

void n3Parser::FormulaContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFormula(this);
}

n3Parser::FormulaContext* n3Parser::formula() {
  FormulaContext *_localctx = _tracker.createInstance<FormulaContext>(_ctx, getState());
  enterRule(_localctx, 44, n3Parser::RuleFormula);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(186);
    match(n3Parser::T__19);
    setState(188);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if ((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 875227346436108) != 0)) {
      setState(187);
      formulaContent();
    }
    setState(190);
    match(n3Parser::T__20);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- FormulaContentContext ------------------------------------------------------------------

n3Parser::FormulaContentContext::FormulaContentContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

n3Parser::N3StatementContext* n3Parser::FormulaContentContext::n3Statement() {
  return getRuleContext<n3Parser::N3StatementContext>(0);
}

n3Parser::FormulaContentContext* n3Parser::FormulaContentContext::formulaContent() {
  return getRuleContext<n3Parser::FormulaContentContext>(0);
}

n3Parser::SparqlDirectiveContext* n3Parser::FormulaContentContext::sparqlDirective() {
  return getRuleContext<n3Parser::SparqlDirectiveContext>(0);
}


size_t n3Parser::FormulaContentContext::getRuleIndex() const {
  return n3Parser::RuleFormulaContent;
}

void n3Parser::FormulaContentContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterFormulaContent(this);
}

void n3Parser::FormulaContentContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitFormulaContent(this);
}

n3Parser::FormulaContentContext* n3Parser::formulaContent() {
  FormulaContentContext *_localctx = _tracker.createInstance<FormulaContentContext>(_ctx, getState());
  enterRule(_localctx, 46, n3Parser::RuleFormulaContent);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(203);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case n3Parser::T__1:
      case n3Parser::T__2:
      case n3Parser::T__15:
      case n3Parser::T__17:
      case n3Parser::T__19:
      case n3Parser::BooleanLiteral:
      case n3Parser::String:
      case n3Parser::IRIREF:
      case n3Parser::PNAME_NS:
      case n3Parser::PNAME_LN:
      case n3Parser::BLANK_NODE_LABEL:
      case n3Parser::INTEGER:
      case n3Parser::DECIMAL:
      case n3Parser::DOUBLE:
      case n3Parser::IPLSTART:
      case n3Parser::ANON:
      case n3Parser::QuickVarName: {
        enterOuterAlt(_localctx, 1);
        setState(192);
        n3Statement();
        setState(197);
        _errHandler->sync(this);

        _la = _input->LA(1);
        if (_la == n3Parser::T__0) {
          setState(193);
          match(n3Parser::T__0);
          setState(195);
          _errHandler->sync(this);

          _la = _input->LA(1);
          if ((((_la & ~ 0x3fULL) == 0) &&
            ((1ULL << _la) & 875227346436108) != 0)) {
            setState(194);
            formulaContent();
          }
        }
        break;
      }

      case n3Parser::BASE:
      case n3Parser::PREFIX: {
        enterOuterAlt(_localctx, 2);
        setState(199);
        sparqlDirective();
        setState(201);
        _errHandler->sync(this);

        _la = _input->LA(1);
        if ((((_la & ~ 0x3fULL) == 0) &&
          ((1ULL << _la) & 875227346436108) != 0)) {
          setState(200);
          formulaContent();
        }
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- NumericLiteralContext ------------------------------------------------------------------

n3Parser::NumericLiteralContext::NumericLiteralContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* n3Parser::NumericLiteralContext::INTEGER() {
  return getToken(n3Parser::INTEGER, 0);
}

tree::TerminalNode* n3Parser::NumericLiteralContext::DECIMAL() {
  return getToken(n3Parser::DECIMAL, 0);
}

tree::TerminalNode* n3Parser::NumericLiteralContext::DOUBLE() {
  return getToken(n3Parser::DOUBLE, 0);
}


size_t n3Parser::NumericLiteralContext::getRuleIndex() const {
  return n3Parser::RuleNumericLiteral;
}

void n3Parser::NumericLiteralContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterNumericLiteral(this);
}

void n3Parser::NumericLiteralContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitNumericLiteral(this);
}

n3Parser::NumericLiteralContext* n3Parser::numericLiteral() {
  NumericLiteralContext *_localctx = _tracker.createInstance<NumericLiteralContext>(_ctx, getState());
  enterRule(_localctx, 48, n3Parser::RuleNumericLiteral);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(205);
    _la = _input->LA(1);
    if (!((((_la & ~ 0x3fULL) == 0) &&
      ((1ULL << _la) & 15032385536) != 0))) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- RdfLiteralContext ------------------------------------------------------------------

n3Parser::RdfLiteralContext::RdfLiteralContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* n3Parser::RdfLiteralContext::String() {
  return getToken(n3Parser::String, 0);
}

tree::TerminalNode* n3Parser::RdfLiteralContext::LANGTAG() {
  return getToken(n3Parser::LANGTAG, 0);
}

n3Parser::IriContext* n3Parser::RdfLiteralContext::iri() {
  return getRuleContext<n3Parser::IriContext>(0);
}


size_t n3Parser::RdfLiteralContext::getRuleIndex() const {
  return n3Parser::RuleRdfLiteral;
}

void n3Parser::RdfLiteralContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterRdfLiteral(this);
}

void n3Parser::RdfLiteralContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitRdfLiteral(this);
}

n3Parser::RdfLiteralContext* n3Parser::rdfLiteral() {
  RdfLiteralContext *_localctx = _tracker.createInstance<RdfLiteralContext>(_ctx, getState());
  enterRule(_localctx, 50, n3Parser::RuleRdfLiteral);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(207);
    match(n3Parser::String);
    setState(211);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case n3Parser::LANGTAG: {
        setState(208);
        match(n3Parser::LANGTAG);
        break;
      }

      case n3Parser::T__21: {
        setState(209);
        match(n3Parser::T__21);
        setState(210);
        iri();
        break;
      }

      case n3Parser::T__0:
      case n3Parser::T__3:
      case n3Parser::T__4:
      case n3Parser::T__5:
      case n3Parser::T__6:
      case n3Parser::T__7:
      case n3Parser::T__8:
      case n3Parser::T__9:
      case n3Parser::T__10:
      case n3Parser::T__11:
      case n3Parser::T__12:
      case n3Parser::T__13:
      case n3Parser::T__14:
      case n3Parser::T__15:
      case n3Parser::T__16:
      case n3Parser::T__17:
      case n3Parser::T__18:
      case n3Parser::T__19:
      case n3Parser::T__20:
      case n3Parser::BooleanLiteral:
      case n3Parser::String:
      case n3Parser::IRIREF:
      case n3Parser::PNAME_NS:
      case n3Parser::PNAME_LN:
      case n3Parser::BLANK_NODE_LABEL:
      case n3Parser::INTEGER:
      case n3Parser::DECIMAL:
      case n3Parser::DOUBLE:
      case n3Parser::IPLSTART:
      case n3Parser::ANON:
      case n3Parser::QuickVarName: {
        break;
      }

    default:
      break;
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- IriContext ------------------------------------------------------------------

n3Parser::IriContext::IriContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* n3Parser::IriContext::IRIREF() {
  return getToken(n3Parser::IRIREF, 0);
}

n3Parser::PrefixedNameContext* n3Parser::IriContext::prefixedName() {
  return getRuleContext<n3Parser::PrefixedNameContext>(0);
}


size_t n3Parser::IriContext::getRuleIndex() const {
  return n3Parser::RuleIri;
}

void n3Parser::IriContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterIri(this);
}

void n3Parser::IriContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitIri(this);
}

n3Parser::IriContext* n3Parser::iri() {
  IriContext *_localctx = _tracker.createInstance<IriContext>(_ctx, getState());
  enterRule(_localctx, 52, n3Parser::RuleIri);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(215);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case n3Parser::IRIREF: {
        enterOuterAlt(_localctx, 1);
        setState(213);
        match(n3Parser::IRIREF);
        break;
      }

      case n3Parser::PNAME_NS:
      case n3Parser::PNAME_LN: {
        enterOuterAlt(_localctx, 2);
        setState(214);
        prefixedName();
        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- PrefixedNameContext ------------------------------------------------------------------

n3Parser::PrefixedNameContext::PrefixedNameContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* n3Parser::PrefixedNameContext::PNAME_NS() {
  return getToken(n3Parser::PNAME_NS, 0);
}

tree::TerminalNode* n3Parser::PrefixedNameContext::PNAME_LN() {
  return getToken(n3Parser::PNAME_LN, 0);
}


size_t n3Parser::PrefixedNameContext::getRuleIndex() const {
  return n3Parser::RulePrefixedName;
}

void n3Parser::PrefixedNameContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterPrefixedName(this);
}

void n3Parser::PrefixedNameContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitPrefixedName(this);
}

n3Parser::PrefixedNameContext* n3Parser::prefixedName() {
  PrefixedNameContext *_localctx = _tracker.createInstance<PrefixedNameContext>(_ctx, getState());
  enterRule(_localctx, 54, n3Parser::RulePrefixedName);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(217);
    _la = _input->LA(1);
    if (!(_la == n3Parser::PNAME_NS

    || _la == n3Parser::PNAME_LN)) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- BlankNodeContext ------------------------------------------------------------------

n3Parser::BlankNodeContext::BlankNodeContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* n3Parser::BlankNodeContext::BLANK_NODE_LABEL() {
  return getToken(n3Parser::BLANK_NODE_LABEL, 0);
}

tree::TerminalNode* n3Parser::BlankNodeContext::ANON() {
  return getToken(n3Parser::ANON, 0);
}


size_t n3Parser::BlankNodeContext::getRuleIndex() const {
  return n3Parser::RuleBlankNode;
}

void n3Parser::BlankNodeContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterBlankNode(this);
}

void n3Parser::BlankNodeContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitBlankNode(this);
}

n3Parser::BlankNodeContext* n3Parser::blankNode() {
  BlankNodeContext *_localctx = _tracker.createInstance<BlankNodeContext>(_ctx, getState());
  enterRule(_localctx, 56, n3Parser::RuleBlankNode);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(219);
    _la = _input->LA(1);
    if (!(_la == n3Parser::BLANK_NODE_LABEL

    || _la == n3Parser::ANON)) {
    _errHandler->recoverInline(this);
    }
    else {
      _errHandler->reportMatch(this);
      consume();
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- QuickVarContext ------------------------------------------------------------------

n3Parser::QuickVarContext::QuickVarContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* n3Parser::QuickVarContext::QuickVarName() {
  return getToken(n3Parser::QuickVarName, 0);
}


size_t n3Parser::QuickVarContext::getRuleIndex() const {
  return n3Parser::RuleQuickVar;
}

void n3Parser::QuickVarContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterQuickVar(this);
}

void n3Parser::QuickVarContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<n3Listener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitQuickVar(this);
}

n3Parser::QuickVarContext* n3Parser::quickVar() {
  QuickVarContext *_localctx = _tracker.createInstance<QuickVarContext>(_ctx, getState());
  enterRule(_localctx, 58, n3Parser::RuleQuickVar);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(221);
    match(n3Parser::QuickVarName);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

void n3Parser::initialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  n3ParserInitialize();
#else
  ::antlr4::internal::call_once(n3ParserOnceFlag, n3ParserInitialize);
#endif
}
