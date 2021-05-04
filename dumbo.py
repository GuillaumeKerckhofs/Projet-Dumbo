from lark import Lark

grammar = """
programme: txt | txt programme |dumbo_bloc | dumbo_bloc programme
txt: /[a-zA-Z0-9;&<>"_\=\-\.\/\n\s:,]+/
dumbo_bloc: "{{" "}}" | "{{" expressions_list "}}" 
expressions_list: expression ";" expressions_list  |  expression ";" 

expression: "print" string_expression | for_string | for_var | variable ":=" string_list | variable ":=" string_expression |variable ":=" string_list | if
if: "if"  boolean "do" expressions_list "endif"
for_string: "for" variable "in" string_list "do" expressions_list "endfor"
for_var: "for" variable "in" variable "do" expressions_list "endfor"

string_expression: string | variable | string_expression "." string_expression
string_list: "(" string_list_interior ")"
string_list_interior: string | string "," string_list_interior

variable: /[a-zA-Z0-9_]+/
string: "'" txt "'"

integer:  integer op integer | variable op integer | integer op variable | int

add: "+"
dif: "-"
mul: "*"
div: "/"

op : bigger | lower | eq | neq

bigger: ">"
lower: "<"
eq: "="
neq:"!="

or: boolean ("or" boolean)*
and: boolean ("and" boolean)*

boolean: true | false | or | and | integer op integer


%import common.WORD
%ignore " "
"""

parser = Lark(grammar)




if  __name__ == '__main__':
    import sys
    if len(sys.argv)!=3:
        print ("erreur, 4 argument attendu")
    else:
        dataf = sys.argv[1]
        templatef = sys.argv[2]
        output=sys.stdout


        with open(dataf,'r') as f1:
            if (f1 != None):
                data = grammar.parse(f1.read())

        with open(templatef, 'r') as f2:
            if (f2 != None):
                template = grammar.parse(f2.read())



    print(parser.parse("Hello, oui world!"))
    print(parser.parse("Adios, no amigo!"))
