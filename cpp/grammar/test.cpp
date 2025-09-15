#include <iostream>

#include "antlr4-runtime/antlr4-runtime.h"
#include "parser/n3Lexer.h"
#include "parser/n3Parser.h"
#include <chrono>

using namespace std;
using namespace antlr4;

int main(int argc, const char* argv[]) {
    string path = argv[1];
    cout << path << endl;

    auto start = chrono::high_resolution_clock::now();

    ifstream stream;
    stream.open(path);
    
    ANTLRInputStream input(stream);
    n3Lexer lexer(&input);
    CommonTokenStream tokens(&lexer);
    n3Parser parser(&tokens);    

    n3Parser::N3DocContext* tree = parser.n3Doc();

    auto end = chrono::high_resolution_clock::now();
    // auto duration_ms = chrono::duration_cast<chrono::milliseconds>(end - start);
    chrono::duration<double> duration = (end - start);

    cout << duration.count() << endl;

    return 0;
}