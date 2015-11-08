import os
import sys

def _boot():
    main(list(sys.argv[1:]), os.environ)

def main(args, env):
    print("HERE!")

if __name__ == '__main__':
    _boot()

