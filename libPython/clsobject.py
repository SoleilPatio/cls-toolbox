import cPickle

class clsobject(object):
    def __init__(self):
        pass
    
    def __repr__(self):
        return "%s"%self.__dict__
    
    def obj_store(self, filename):
        with open(filename, "wb") as f:
            cPickle.dump(self.__dict__, f)
        
    def obj_load(self, filename):
        with open(filename, "rb") as f:
            self.__dict__ = cPickle.load(f)
        
