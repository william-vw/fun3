#include <iostream>

using namespace std;

class Term {
    public:
        int type;
        string value;
        string tag1;
        string tag2;

        Term(int t, string v, string t1, string t2): type(t), value(v), tag1(t1), tag2(t2) {}
};

class Triple {
    public:
        Term s;
        Term p;
        Term o;

        Triple(Term su, Term pr, Term ob): s(su), p(pr), o(ob) {}
};

vector<Triple> find(int s, int p, int o) {
    vector<Triple> array;
    
    for (int i = 0; i < 100; i++) {
        Triple t = Triple(Term(1, "http://example.org", "", ""), Term(2, "_:b0", "", ""), Term(3, "abc", "string", "en"));
        array.push_back(t);
    }
    
    return array;
}

int main() {
    vector<Triple> array = find(1, 1, 1);

    for (Triple t: array) {
        Term x = t.s;

        for (Triple t2: array) {
            Term y = t.s;
        }
    }
    
    return 0;
}