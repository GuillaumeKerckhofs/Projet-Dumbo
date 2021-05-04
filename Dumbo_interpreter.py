from lark import Lark

grammar = """
programme: txt | txt programme |dumbo_bloc | dumbo_bloc programme
txt: /[a-zA-Z0-9;&<>"_\=\-\.\/\n\s:,]+/
dumbo_block: "{{" "}}" | "{{" expressions_list "}}" 
expressions_list: expression ";" expressions_list  |  expression ";" 

expression: "print" string_expression | for_string | for_var | variable ":=" string_list | variable ":=" string_expression |variable ":=" string_list | if
if: "if"  boolean "do" expressions_list "endif"
for_string: "for" variable "in" string_list "do" expressions_list "endfor"
for_var: "for" variable "in" variable "do" expressions_list "endfor"

variable: /[a-zA-Z0-9_]+/
string: "'" txt "'"

add: "+"
dif: "-"
mul: "*"
div: "/"

op : bigger | lower | eq | neq

bigger: ">"
lower: "<"
eq: "="
neq:"!="

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


        with open(dataf,'r') as f1:
            if (f1 != None):
                data = grammar.parse(f1.read())

        with open(templatef, 'r') as f2:
            if (f2 != None):
                template = grammar.parse(f2.read())



    print(parser.parse("Hello, oui world!"))
    print(parser.parse("Adios, no amigo!"))
