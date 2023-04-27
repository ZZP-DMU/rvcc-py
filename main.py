#!/home/ZZP/workspace/py_vir_env/py_vir_rvcc/bin/python3

import sys
import re
from enum import Enum



##to debug easy ,so i donot use the sys module

if len(sys.argv) != 2:
    sys.stderr.write(sys.argv[0]+"invalid number of argument\n")

argv = sys.argv[1]




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


def token_equal(node=Token,str_obj=str):
    if node.Kind == tok_kind.TK_PUNCT and node.Val==str_obj[0]:
        return True
    else:
        return False
    
def token_skip(node=Token,str_obj=str):
    if node.Kind == tok_kind.TK_PUNCT and node.Val==str_obj[0]:
        return node.Next
    

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
            
            if i == '+' or i == '-' or i == '*' or i == '/' or i == '(' or i == ')':
                linklist.append(tok_kind.TK_PUNCT,i,count)
        count = count+1
    linklist.append(tok_kind.TK_EOF,'eof',count)
    return linklist



#############################################################
class node_kind(Enum):
    ND_ADD = 0
    ND_SUB = 1
    ND_MUL = 2
    ND_DIV = 3
    ND_NUM = 4
    



class BT_Node():
    def __init__(self):
        pass
    def add_bt_node(self,kind,left,right):
        self.Kind = kind
        self.Left = left
        self.Right = right
    def add_num_node(self,val):
        self.Kind = node_kind.ND_NUM
        self.Val = val

def new_bt_node(kind,left,right):
    node = BT_Node()
    node.add_bt_node(kind,left,right)
    return node

def ex_add_sub(link_head=Token):
    link_head,node = ex_mul_div(link_head)
    while True:
        if token_equal(link_head,'+'):
            link_head,return_node = ex_mul_div(link_head.Next)
            node = new_bt_node(node_kind.ND_ADD,node,return_node)
            continue
        if token_equal(link_head,'-'):
            link_head,return_node = ex_mul_div(link_head.Next)
            node = new_bt_node(node_kind.ND_SUB,node,return_node)
            continue

        #link_head = link_head.Next
        return link_head,node
    
def ex_mul_div(link_head=Token):
    link_head,node = ex_num_oth(link_head)
    while True:
        if token_equal(link_head,'*'):
            link_head,return_node = ex_num_oth(link_head.Next)
            node = new_bt_node(node_kind.ND_MUL,node,return_node)
            continue
        if token_equal(link_head,"/"):
            link_head,return_node = ex_num_oth(link_head.Next)
            node = new_bt_node(node_kind.ND_DIV,node,return_node)
            continue

        #link_head = link_head.Next
        return link_head,node
    
def ex_num_oth(link_head=Token):
    if token_equal(link_head,'('):
        link_head,node = ex_add_sub(link_head.Next)
        link_head = token_skip(link_head,')')
        return link_head,node
    if link_head.Kind == tok_kind.TK_NUM:
        node = BT_Node()
        node.add_num_node(link_head.Val)
        link_head = link_head.Next
        return link_head,node
    sys.stderr.write("error token")
    return None



def print_bt(bt=BT_Node):
    if bt.Kind != node_kind.ND_NUM:
        print(bt.Kind)
    else:
        print(bt.Val)
    if bt.Kind != node_kind.ND_NUM:
        tmp = bt.Left
        print_bt(tmp)
        tmp = bt.Right
        print_bt(tmp)


Depth = 0
def stack_push():
    global Depth
    print("    addi sp, sp,-8\n")
    print("    sd a0,0(sp)\n")
    Depth = Depth + 1

def stack_pop(reg=str):
    global Depth
    print("    ld {}, 0(sp)\n".format(reg))
    print("    addi sp, sp, 8\n")
    Depth = Depth - 1

def gener_ex(node=BT_Node):
    if(node.Kind==node_kind.ND_NUM):
        print("    li a0, {}\n".format(node.Val))
        return 0
    
    gener_ex(node.Right)
    stack_push()
    gener_ex(node.Left)
    stack_pop("a1")

    if node.Kind == node_kind.ND_ADD:
        print("    add a0, a0, a1\n")
        return 0
    elif node.Kind == node_kind.ND_SUB:
        print("    sub a0, a0, a1\n")
        return 0
    elif node.Kind == node_kind.ND_MUL:
        print("    mul a0, a0, a1\n")
        return 0
    elif node.Kind == node_kind.ND_DIV:
        print("    div a0, a0, a1\n")
        return 0





    





def verroAt(Loc,estr,errm):
    sys.stderr.write(estr+'\n')
    sys.stderr.write(Loc*'-')
    sys.stderr.write('^')
    sys.stderr.write(errm)



#link format expression
lin = tokenize(argv)
#lin.travel()

#link's head,use to travel the link node
Head = lin._head

#btree format expression to make generating expression easier
btree = ex_add_sub(Head)
#link's end must be TK_EOF,or it is wrong
assert(btree[0].Kind == tok_kind.TK_EOF)

#print_bt(btree[1])

print("    .global main\n")
print("main:\n")
gener_ex(btree[1])
print("    ret\n")

assert(Depth == 0)
