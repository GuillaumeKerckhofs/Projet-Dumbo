import sys
from lark import Lark

grammar = r"""
programme: txt | txt programme |dumbo_bloc | dumbo_bloc programme
txt: /[a-zA-Z0-9;&<>"_\=\-\.\/\n\s:,]+/
dumbo_bloc: "{{" "}}" | "{{" expression_list "}}" 
expression_list: expression ";" expression_list  |  expression ";" 

expression: "print" string_expression | for | variable ":=" integer | variable ":=" string_expression | variable ":=" string_list | if

if: "if"  boolean "do" expression_list "endif"
for: for_string | for_var
for_string: variable "in" string_list "do" expression_list "endfor" 
for_var: "for" variable "in" variable "do" expression_list "endfor"

string_expression: string | variable | string_expression "." string_expression
string_list: "(" string_list_interior ")"
string_list_interior: string | string "," string_list_interior

int: /[0-9]+/ | "-" int
variable: /[a-zA-Z0-9_]+/
string: "'" txt "'"

integer:  integer op integer | variable op integer | integer op variable | int

add: "+"
dif: "-"
mul: "*"
div: "/"

op : add | dif | mul | div 
comp : bigger | lower | eq | neq

bigger: ">"
lower: "<"
eq: "="
neq:"!="

or: boolean ("or" boolean)*
and: boolean ("and" boolean)*

boolean: true | false | or | and | var comp var
true: "true"
false: "false"

var: int | variable

%import common.WS
%ignore WS
"""

parser = Lark(grammar, start='programme')
parse = parser.parse

variables = {}

output=sys.stdout

def interpreter(root):
    if(root.data=="programme" or root.data == "dumbo_bloc" or root.data == "expression_list"):
        for object in root.children:
            interpreter(object)
    elif (root.data == "txt"):
        output.write(root.children[0])
    elif (root.data == "expression"):
        if (root.children[0].data == "string_expression"):
            string_expression(root.children[0])
        elif (root.children[0].data == "variable"):
            output.write("variable")
        elif (root.children[0].data == "for"):
            output.write("for")
        elif (root.children[0].data == "if"):
            output.write("if")

def string_expression(root):

    if (root.children[0].data=="string"):
        output.write(str(root.children[0].children[0].children[0]))
    elif (root.children[0].data=="variable"):
        output.write(str(root.children[0])) #mapping?
    else:
        string_expression(root.children[0])
        string_expression(root.children[1])

def initializeVariable(root):
    if(root.children[1].data=="string_expression"):
        variables[root.children[0].children[0]]=string_expression(root.children[1])
    elif(root.children[1].data=="integer"):
        variables[root.children[0].children[0]]=integer(root.children[1])
    elif(root.children[1].data=="string_list"):
        tmp = []
        listCreation(tmp,root.children[1].children[0])
        variables[root.children[0].children[0]]=tuple(tmp)

def integer(root):


def listCreation(list,root):
    if (len(root.children) > 1):
        list.append(str(root.children[0].children[0].children[0]))
        listCreation(list,root.children[1])
    else:
        list.append(str(root.children[0].children[0].children[0]))
        return list


if  __name__ == '__main__':

    if len(sys.argv)!=3:
        print ("erreur, 2 arguments attendus")
    else:
        dataf = sys.argv[1]
        templatef = sys.argv[2]


        with open(dataf,'r') as f1:
            if (f1 != None):
                data = parse(f1.read())


        with open(templatef, 'r') as f2:
            if (f2 != None):
                template = parse(f2.read())

        interpreter(data)
        interpreter(template)

