from tempfile import mkstemp
import os
import shutil

class TempFile(object):
    def __init__(self, mode="w", debug=False):
        self.fd, self.file_path = mkstemp(suffix=".cls.temp")
        self.file = None
        self.mode = mode
        self.debug = debug
        self.b_is_moved = False 
    
    def __del__(self):
        """
        [CLS]:remember to close file descriptor
        """
        
        if self.fd != None:
            os.close(self.fd)
        
        if self.debug:
            print "[DEBUG]:file not remove:" + self.file_path
            
        #Remove only when temp file not been moved
        elif self.b_is_moved == False:
            os.remove(self.file_path)
        
    
    def open(self):
        self.file = open(self.file_path, self.mode)
        return self.file
    
    def file_obj(self):
        return self.file
    
    def move_to(self, destfile):
        self.file.close()
        os.close(self.fd)
        self.fd = None
        shutil.move(self.file_path, destfile)
        self.file_path = destfile
        self.b_is_moved = True
    
        
    """
    [CLS]:called when "with", return object as "as"
    """
    def __enter__(self):
        self.open()
        return self
        
    """
    [CLS]:called when exit "with"
    """
    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
        
        
    #Debug
    def cat(self):
        import Utils.CLI as cli
        if self.file:
            self.file.flush()
        cli.Run("cat "+ self.file_path)
        






if __name__ == '__main__':
    
    
    with TempFile("a") as f:
        for i in range(10):
            f.file.write(str(i) + "\n")
            f.cat()
            
    temp = TempFile("a")
    with temp as f:
        for i in range(10):
            f.file.write(str(i) + "\n")
            f.cat()
            
            
    
    
    pass