#!/usr/bin/python

import argparse

__version_info__ = ('2013','03','14')
__version__ = '-'.join(__version_info__)


if __name__ == "__main__":
    
    """
    [CLS]: Normal Usage
    """
    parser = argparse.ArgumentParser()


    """
    [CLS]: a positional argument (no -- option in front of the name) , always requires
    """
    parser.add_argument("square", type=int, help="display a square of a given number")
    #"--verbose",


    """
    [CLS]: argument
    """
    parser.add_argument("-foo", help="info for foo", default="default value")
    parser.add_argument("-bar", help="info for bar", default="default value", required=True)
    parser.add_argument("-boolean",  action="store_true", help="increase output verbosity")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    
    
    
    # This is the correct way to handle accepting multiple arguments.
    # '+' == 1 or more.
    # '*' == 0 or more.
    # '?' == 0 or 1.
    # An int is an explicit number of arguments to accept.
    """
    drawback: eating position arguments. ex. foo.py --nargs 111 222 333 position_args_not work
    """
    parser.add_argument('--nargs', nargs='+')
    
    """
    use append
    mycommand --carpark 17 --carpark 18
    """
    parser.add_argument('--carpark',
                    dest='carpark_ids',
                    type=int,
                    action='append',
                    default=[],
                    help="One carpark ID (can be used multiple times)"
                    )
    
    
    
    """
    [CLS]: if argements are illegal, this "parse_args" will show help and exit program
    """
    args = parser.parse_args()

    print "args = ", args
    
    
    print "Done"