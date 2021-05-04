from lark import Lark

grammar =  r"""
    programme: txt | txt programme | dumbo_bloc | dumbo_bloc programme
    txt: /[a-zA-Z0-9;&<>"_\=\-\.\/\n\s:,]+/
    dumbo_bloc: "{{" expression_list "}}" | "{{" "}}"
    expression_list: expression ";" expression_list | expression ";"
    expression: "print" string_expression
               |for_loop
               |if_exp
               |variable ":=" integer
               |variable ":=" string_expression
               |variable ":=" string_list
    string_expression: string | variable | string_expression "." string_expression
    string_list: "(" string_list_interior ")"
    string_list_interior: string | string "," string_list_interior
    variable: /[a-zA-Z0-9_]+/
    string: "'" txt "'"

    for_loop: "for" variable "in" string_list "do" expression_list "endfor"
             |"for" variable "in" variable "do" expression_list "endfor"
    if_exp: "if" bool "do" expression_list "endif"

    add: "+"
    dif: "-"
    mul: "*"
    div: "/"

    gt: ">"
    lt: "<"
    eq: "="
    neq:"!="
    
    int: /[0-9]+/ | "-" int

    op: add|dif|mul|div

    integer:  integer op integer 
    | variable op integer
    | integer op variable
    | int

    var: int | variable
    cmp: gt | lt | eq | neq
    bool_exp: or | and
    true : "true"
    false: "false"
    bool: true | false | bool_exp | var cmp var

    or: "(" bool "or" bool ")"
    and: "(" bool "and" bool ")"

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
        elif (root.children[0].data == "for_loop"):
            print("for")
        elif (root.children[0].data == "if_exp"):
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



