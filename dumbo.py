import sys
from lark import Lark

grammar = r"""
programme: txt | txt programme |dumbo_bloc | dumbo_bloc programme
txt: /[a-zA-Z0-9;&<>"_\=\-\.\/\n\s:,]+/
dumbo_bloc: "{{" "}}" | "{{" expression_list "}}" 
expression_list: expression ";" expression_list  |  expression ";" 

expression: "print" string_expression | for | variable ":=" integer | variable ":=" string_expression | variable ":=" string_list | if

if: "if"  boolean "do" expression_list "endif"
for: "for" variable "in" string_list "do" expression_list "endfor" | "for" variable "in" variable "do" expression_list "endfor"

string_expression: string | variable | string_expression "." string_expression
string_list: "(" string_list_interior ")"
string_list_interior: string | string "," string_list_interior

int: /[0-9]+/ | "-" int
variable: /[a-zA-Z0-9_]+/
string: "'" txt "'"

integer:  integer op integer | variable op integer | integer op variable | int

add: "+"
diff: "-"
mult: "*"
div: "/"

op : add | diff | mult | div 
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
            output.write(str(string_expression(root.children[0])))
        elif (root.children[0].data == "variable"):
            initializeVariable(root)
        elif (root.children[0].data == "for"):
            for_ (root.children[0])
        elif (root.children[0].data == "if"):
            if_ (root.children[0])

def string_expression(root):

    if (root.children[0].data=="string"):
        return(str(root.children[0].children[0].children[0]))
    elif (root.children[0].data=="variable"):
        return(str(variable(root.children[0])))
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
        variables[root.children[0].children[0]]=tmp

def variable(root):
    return variables[root.children[-1]]

def integer(root):
    if (len(root.children) == 1):
        return int(root.children[0].children[0])
    else:
        operator= str(root.children[1].children[0].data)
        if (root.children[0].data == "variable" and root.children[2].data == "integer"):
            return op(variable(root.children[0]), operator, integer(root.children[2]))
        elif (root.children[0].data == "integer" and root.children[2].data == "variable"):
            return op(integer(root.children[0]), operator, variable(root.children[2]))
        elif (root.children[0].data == "integer" and root.children[2].data == "integer"):
            return op(integer(root.children[0]), operator, integer(root.children[2]))

def op(x, operator, y):
    if(operator == "add"):
        return x + y
    elif(operator == "diff"):
        return x - y
    elif(operator == "mult"):
        return x * y
    elif(operator == "div"):
        return x / y

def string_list_interior(list,root):
    if (len(root.children) > 1):
        list.append(str(root.children[0].children[0].children[0]))
        string_list_interior(list,root.children[1])
    else:
        list.append(str(root.children[0].children[0].children[0]))



def if_(root):
    if(boolean(root.children[0])):
        interpreter(root.children[1])


def boolean(root):
    if (root.children[0].data == "true"):
        return True

    elif (root.children[0].data == "false"):
        return False

    elif (root.children[0].children[0].data == "and"):
        return boolean(root.children[0]) and boolean(root.children[1])

    elif(root.children[0].children[0].data == "or"):
        return boolean(root.children[0]) or boolean(root.children[1])

    elif(root.children[0].data == "num"):
        comparator = root.children[1].children[0].data
        if (comparator == "bigger"):
            return num(root.children[0]) > num(root.children[2])
        elif (comparator == "lower"):
            return num(root.children[0]) < num(root.children[2])
        elif(comparator == "eq"):
            return num(root.children[0]) == num(root.children[2])
        elif(comparator == "noteq"):
            return num(root.children[0]) != num(root.children[2])

def num(root):
    if(root.children[0].data == "int"):
        return int(root.children[0].children[0])
    elif(root.children[0].data == "variable"):
        return int(variable(root.children[0]))


def for_(root):
    Key = str(root.children[0].children[0])

    tmp = None

    if(variables.__contains__(Key)):
        tmp = variables.pop(Key)

    if(root.children[1].data == "string_list"):
        list=[]
        string_list_interior(list,root.children[1])
    elif(root.children[1].data == "variable"):
        list = variables[root.children[1].children[0]]
    for element in list:
        variables[Key] = element
        interpreter(root.children[2])
    if(tmp != None):
        variables[Key] = tmp
    else:
        variables.pop(Key)


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

