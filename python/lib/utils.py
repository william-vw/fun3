from collections import defaultdict

# TODO improve this code 
# (always use indexing syntax, not own methods)
class Settings():
    
    def __init__(self, dict=None):
        self.dict = dict if dict is not None else {}
    
    def has(self, key):
        return key in self.dict
    
    def enabled(self, key):
        return self.get(key) == True
        
    def get(self, key):
        if self.has(key):
            return self.dict[key]
        else:
            return None
    
    def __getitem__(self, key):
        if key in self.dict:
            return Settings(self.dict[key])
        else:
            return Settings()