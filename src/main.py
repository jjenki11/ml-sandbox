#!/usr/bin/python3

import sys
import rpy2
rpy2.__path__

def parseArgs(args):
    # skip the first one, its just the file being run
    parsed=[]
    count=0
    for arg in args:
        if(count > 0):
            parsed.append(arg)
        count = count + 1
    return parsed

if __name__ == '__main__':
    print("This is the main entry point!")
    print("You provided some args...")
    the_args = parseArgs(sys.argv)
    print(str(the_args))