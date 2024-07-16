"""
@author: jbrown888
8/6/24
#cwd = D:\\j_Documents\\cliimbing\\climbtracker
"""
# Working on argparse and command line arguments parsing.

# run directly in terminal: 'python testing_argparse.py --sum 5 6'
import argparse

#eg 1

# parser = argparse.ArgumentParser(description="para transfer")
# parser.add_argument("--para", type=str, default="helloWorld", help="para -> str type.")
# args = parser.parse_args()
# print(args)


# eg 2

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
#add_argument() these calls tell the ArgumentParser how to take the strings on the command line and turn them into objects.
# This information is stored and used when parse_args() is called. 
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
# returns a Namespace object with two attributes : integers and accumulate. 
# integers attr is list of one or more integers. accumulate attr is sum() function if --sum called in command line, max() if not.


# general: parse_args(args=None, namespace=None)
# Convert argument strings to objects and assign them as attributes of the namespace. Return the populated namespace
# args: list of strings to parse, taken from sys.argv by default.
# returns Namespace object
# default action is to store the argument value. In this case, if a type is provided, the value is converted to that \
# type before it is stored. If the dest argument is provided, the value is saved to an attribute of that name on the\
#  Namespace object returned when the command line arguments are parsed.
print(args.accumulate(args.integers))



