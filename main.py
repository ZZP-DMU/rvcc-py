#!/home/ZZP/workspace/py_vir_env/py_vir_rvcc/bin/python3

import sys
import re
from enum import Enum




if len(sys.argv) != 2:
    sys.stderr.write(sys.argv[0]+"invalid number of argument\n")

argv = sys.argv[1]

print(" .global main\n")
print("main:\n")


#num = re.findall(r"\d+",argv)
#
#print(" li a0, {}\n".format(num[0]))
#
#argv_w = argv[len(num[0]):len(argv)]
#
#i = 1
#
#while(len(argv_w)):
#    if argv_w[0] == '+':
#        print(" addi a0, a0, {}\n".format(num[i]))
#        argv_w=argv_w[len(num[i])+1:len(argv)]
#        i = i+1
#        continue
#    if argv_w[0] == '-':
#        print(" addi a0, a0, -{}\n".format(num[i]))
#        argv_w=argv_w[len(num[i])+1:len(argv)]
#        i = i+1
#        continue
#    print("unexpected character: {}\n".format(num[i]))
#    break
class tok_kind(Enum):
    TK_PUNCT = 0
    TK_NUM = 1
    TK_EOF = 2

class Token():
    def __init__(self,kind,val,loc):
        self.Kind = kind
        self.Val = val
        self.Loc = loc
        self.lenth = len(val)
        self.Next = None

class LinkList():
    def __init__(self):
        self._head = None

    def is_empty(self):
        return self._head == None
    
    def travel(self):
        cur = self._head
        while cur != None:
            print(cur.Kind,cur.Val,cur.Loc,'\n')
            cur = cur.Next
        print('')
    
    def append(self,kind,val,loc):
        node = Token(kind,val,loc)
        if self.is_empty():
            self._head = node
        else:
            cur = self._head
            while cur.Next != None:
                cur = cur.Next 
            cur.Next = node

def tokenize(argv=str):
    linklist = LinkList()
    num = str()
    count = 0
    argv = argv+' '
    for i in argv:
        if i.isdigit():
            num = num+i
        else:
            if len(num):
                linklist.append(tok_kind.TK_NUM,num,count-len(num))
                num = ''
            
            if i == '+' or i == '-':
                linklist.append(tok_kind.TK_PUNCT,i,count)
        count = count+1
    linklist.append(tok_kind.TK_EOF,'eof',count)
    return linklist


lin = tokenize(argv)

Head = lin._head

if Head.Kind == tok_kind.TK_NUM:
    print(" li a0, {}\n".format(Head.Val))

while(Head.Kind != tok_kind.TK_EOF):
    Head = Head.Next
    if Head.Val == '+':
        Head = Head.Next
        print(" addi a0, a0, {}\n".format(Head.Val))
    if Head.Val == '-':
        Head = Head.Next
        print(" addi a0, a0, -{}\n".format(Head.Val))

   

#lin.travel()


print(" ret\n")