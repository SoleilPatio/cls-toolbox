import argparse
import os

if __name__ == "__main__":

    os.environ["CLS_PYTHON"] = "hihi!bless you!"

    for ii in os.environ.items():
        print ii
    
    print "Done"