#!/home/ZZP/workspace/py_vir_env/py_vir_rvcc/bin/python3

import sys
import re




if len(sys.argv) != 2:
    print(sys.argv[0]+"invalid number of argument\n")

argv = sys.argv[1]

print(" .global main\n")
print("main:\n")

num = re.findall(r"\d+",argv)

print(" li a0, {}\n".format(num[0]))

argv_w = argv[len(num[0]):len(argv)]

i = 1

while(len(argv_w)):
    if argv_w[0] == '+':
        print(" addi a0, a0, {}\n".format(num[i]))
        argv_w=argv_w[len(num[i])+1:len(argv)]
        i = i+1
        continue
    if argv_w[0] == '-':
        print(" addi a0, a0, -{}\n".format(num[i]))
        argv_w=argv_w[len(num[i])+1:len(argv)]
        i = i+1
        continue
    print("unexpected character: {}\n".format(num[i]))
    break



print(" ret\n")