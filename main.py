#!/home/ZZP/workspace/py_vir_env/py_vir_rvcc/bin/python3

import sys

if len(sys.argv) != 2:
    print(sys.argv[0]+"invalid number of argument\n")

print(" .global main\n")
print("main:\n")
print(" li a0, {}\n".format(sys.argv[1]))
print(" ret\n")