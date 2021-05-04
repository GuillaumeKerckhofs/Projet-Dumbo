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

def interpreter(root):
    if(root.data=="programme"):
        for object in root.children:
            interpreter(object)
    elif (root.data == "txt"):
        print("texte")
    elif (root.data == "dumbo_bloc"):
        for object in root.children:
            interpreter(object)
    elif (root.data == "expression_list"):
        for object in root.children:
            interpreter(object)
    elif (root.data == "expression"):
        print("je rentre")
        if (root.children[0].data == "string_expression"):
            print("string_expression")
        elif (root.children[0].data == "variable"):
            print("variable")
        elif (root.children[0].data == "for"):
            print("for")
        elif (root.children[0].data == "if"):
            print("if")


if  __name__ == '__main__':
    import sys
    if len(sys.argv)!=3:
        print ("erreur, 4 argument attendu")
    else:
        dataf = sys.argv[1]
        templatef = sys.argv[2]
        output=sys.stdout


        with open(dataf,'r') as d:
            if (d != None):
                data = parse(d.read())


        with open(templatef, 'r') as t:
            if (t != None):
                template = parse(t.read())

        interpreter(data)
        interpreter(template)



