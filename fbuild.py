#!/usr/bin/python3
import sys,build_parser
if __name__ == '__main__':
    Builder=build_parser.Builder()
    Builder.entry(sys.argv)
