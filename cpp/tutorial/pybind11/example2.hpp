#ifndef PET_CLASS
#define PET_CLASS

#include <string>

struct Pet {
public:
    Pet(const std::string &name);
    void setName(const std::string &name_);
    const std::string &getName();

private:
    std::string name;
};

#endif