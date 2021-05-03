from lark import Lark

grammar = """
start: WORD "," WORD " " WORD "!"
%import common.WORD
%ignore " "
"""

parser = Lark(grammar)




if  __name__ == '__main__':
    import sys
    if len(sys.argv)!=4:
        print ("erreur, 4 argument attendu")
    else:
        dataf = sys.argv[1]
        templatef = sys.argv[1]
        outputf = sys.argv[1]

        with open(dataf,'r') as f1:
            if (f1 != None):
                data = grammar.parse(f1.read())

        with open(templatef, 'r') as f2:
            if (f2 != None):
                template = grammar.parse(f2.read())

        with open(outputf, 'w') as f3:
            print("ué")

    print(parser.parse("Hello, oui world!"))
    print(parser.parse("Adios, no amigo!"))