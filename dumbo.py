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
comp : bigger | lower | eq | noteq

bigger: ">"
lower: "<"
eq: "="
noteq:"!="

or: boolean ("or" boolean)*
and: boolean ("and" boolean)*

boolean: true | false | or | and | num comp num
true: "true"
false: "false"

num: int | variable

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
            output.write(string_expression(root.children[0]))
        elif (root.children[0].data == "variable"):
            output.write("variable")
        elif (root.children[0].data == "for"):
            output.write("for")
        elif (root.children[0].data == "if"):
            output.write("if")

def string_expression(root):

    if (root.children[0].data=="string"):
        return(str(root.children[0].children[0].children[0]))
    elif (root.children[0].data=="variable"):
        return (str(root.children[0])) #mapping?
    else:
        return string_expression(root.children[0]) + string_expression(root.children[1])

def initializeVariable(root):
    if(root.children[1].data=="string_expression"):
        variables[root.children[0].children[0]]=string_expression(root.children[1])
    elif(root.children[1].data=="integer"):
        variables[root.children[0].children[0]]=integer(root.children[1])
    elif(root.children[1].data=="string_list"):
        tmp = []
        string_list_interior(tmp,root.children[1].children[0])
        variables[root.children[0].children[0]]=tuple(tmp)

def integer(root):
    if (len(root.children) == 1):
        return int(root.children[0].children[0])
    else:
        if (root.children[0].data == "variable" and root.children[2].data == "integer"):
            return op(root.children[1], variable_value(
                root.children[0]), integer(root.children[2]))
        elif (root.children[0].data == "integer" and root.children[2].data == "variable"):
            return op(root.children[1], integer(root.children[0]),
                      variable_value(root.children[2]))
        elif (root.children[0].data == "integer" and root.children[2].data == "integer"):
            return op(root.children[1], integer(root.children[0]),
                      integer(root.children[2]))

def string_list_interior(list,root):
    if (len(root.children) > 1):
        list.append(str(root.children[0].children[0].children[0]))
        string_list_interior(list,root.children[1])
    else:
        list.append(str(root.children[0].children[0].children[0]))
        return list

def if_exp(root):
    if(boolean(root.children[0])):
        interpreter(root.children[1])


def boolean(root):

    if (root.children[0].data == "true"):
        return True

    elif (root.childre[0].data == "false"):
        return False

    elif(root.children[0].children[0].data == "or"):
        return boolean(root.children[0]) or boolean(root.children[1])

    elif(root.children[0].children[0].data == "and"):
        return boolean(root.children[0]) and boolean(root.children[1])

    elif(root.children[0].data == "num"):
        comp = root.children[1].data
        if (comp == "bigger"):
            return num(root.children[0]) > num(root.children[2])
        elif (comp == "lower"):
            return num(root.children[0]) < num(root.children[2])
        elif(comp == "eq"):
            return num(root.children[0]) == num(root.children[2])
        elif(comp == "noteq"):
            return num(root.children[0]) != num(root.children[2])

def num(root):
    if(root.children[0] == "int"):
        return int(root.children[0].children[0])
    elif(root.children[0] == "variable"):
        return int(root.children[0]) #mapping?




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

