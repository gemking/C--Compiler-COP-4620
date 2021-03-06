# Michael O'Donnell N00939851
# Compiler project 3 - Semantic Analyzer
# Due 1/26/16

import sys
import re

f = open(sys.argv[1], "r")  # open file and read contents into a list (without "\n")
filelines = f.read().splitlines()
f.close()

keywordchecklist = ["else", "if", "int", "return", "void", "while", "float"]  # list of all keywords

# our regular expressions for the lexical analyzer
wordsRegex = "[a-z]+"  # gets all words/ID's
numbersRegex = "[0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?"  # gets all NUM's/float numbers
symRegex = "\/\*|\*\/|\+|-|\*|//|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]"  # gets all special symbols
errorRegex = "\S"

incomment = 0  # check to see if in comment
token = []  # create List to hold all tokens
i = 0  # token counter for parser

# ------------------Begin going through the file and getting tokens----------------------- #
for flines in filelines:
    fline = flines

    if not fline:
        continue
    # print  # extra line to separate input lines
    # if fline:
        # print "INPUT: " + fline  # print the input line, while also getting rid of blank lines

    regex = "(%s)|(%s)|(%s)|(%s)" % (wordsRegex, numbersRegex, symRegex, errorRegex)
    '([a-z]+)|([0-9]+(\.[0-9]+)?(E(\+|-)?[0-9]+)?)|'
    '("\/\*|\*\/|\+|-|\*|/|<=|<|>=|>|==|!=|=|;|,|\(|\)|\{|\}|\[|\]|//")|(\S)'

    for t in re.findall(regex, fline):
        if t[0] and incomment == 0:
            if t[0] in keywordchecklist:
                token.append(t[0])
                # print "keyword:", t[0]
            else:
                # print "ID:", t[0]
                token.append(t[0])
        elif t[1] and incomment == 0:
            if "." in t[1]:
                # print "FLOAT:", t[1]
                token.append(t[1])
            elif "E" in t[1]:
                # print "FLOAT:", t[1]
                token.append(t[1])
            else:
                # print "NUM:", t[1]
                token.append(t[1])
        elif t[5]:
            if t[5] == "/*":
                incomment = incomment + 1
            elif t[5] == "*/" and incomment > 0:
                incomment = incomment - 1
            elif t[5] == "//" and incomment == 0:
                break
            elif incomment == 0:
                if t[5] == "*/":
                    if "*/*" in fline:
                        # print "*"
                        token.append("*")
                        incomment += 1
                        continue
                    else:
                        # print "*"
                        token.append("*")
                        # print "/"
                        token.append("/")
                else:
                    # print t[5]
                    token.append(t[5])
        elif t[6] and incomment == 0:
            # print "ERROR:", t[6]
            token.append(t[6])
# ------------ end of for loop for the file and getting tokens --------------------------- #

token.append("$")  # add to end to check if done parsing
ismain = 0  # check for 1 main function
lastmain = 0  # check if main is last function
done = 0
exc0 = 0
exc1 = 0
excret = 0
parammatch = 0
parm = 0

vardec = []  # list to hold declared variables, type, and scope
vartype = []  # list of type of variables
varop = []  # check for operand and operator agreement, i.e. int x; x = "hi"
vars = []  # list to hold all declared variables
varscope = []  # list of all variable scopes, as in what functions they are in
varscopen = []  # list of all variable scopes, as in block number

fundec = []  # list to hold declared functions with parms/args
fundeci = 0  # index to keep track of parameters/args for a function
funcall = []  # functions called
funcallargs = []  # list of argument types in a function's parameters
funnames = []  # list of all function names
funtypes = []  # list of all function types
funname = 0  # function name, for scope
funtype = 0  # function type, determine if it needs return
curscope = 0  # current scope
funret = 0  # does function have a return
funret = 0  # check if int/float function has return

# ---------------------------------- parsing functions ----------------------------------- #


def hasnum(inputstring):
    return any(char.isdigit() for char in inputstring)


def program():  # 1
    global done
    dl()
    if token[i] == "$":
        done = 1
        # continue outside
    else:
        print "REJECT"


def dl():  # 2
    declaration()
    dlprime()


def dlprime():  # 3
    if token[i] == "int" or token[i] == "void" or token[i] == "float":
        declaration()
        dlprime()
    elif token[i] == "$":
        return
    else:
        return


def declaration():  # 4
    global i, ismain, funname, curscope, funtype, funret, lastmain
    types()
    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        if token[i] == "main":
            ismain += 1
            lastmain = 1
            if token[i-1] != "void" or token[i+2] != "void":
                print "REJECT"
                sys.exit(0)
        else:
            lastmain = 0

        i += 1  # Accept ID
        if token[i] == ";":
            i += 1  # Accept ;
            k = 0
            for v in vars:  # check for duplicate declared variables
                if token[i-2] == v:
                    if vartype[k] == token[i-3]:
                        print "REJECT"
                        sys.exit(0)
                k += 1

            vardec.append(token[i-3] + " " + token[i-2] + " global 0")
            vars.append(token[i-2])
            vartype.append(token[i-3])
            varscope.append("global")
            varscopen.append(0)

            if token[i-3] == "void":
                print "REJECT"
                sys.exit(0)

        elif token[i] == "[":
            i += 1  # Accept [
            k = 0
            for v in vars:  # check for duplicate declared variables
                if token[i-2] == v:
                    if vartype[k] == token[i-3]:
                        print "REJECT"
                        sys.exit(0)
                k += 1

            vardec.append(token[i-3] + " " + token[i-2] + " global 0")
            vars.append(token[i-2])
            vartype.append(token[i-3])
            varscope.append("global")
            varscopen.append(0)

            if token[i-3] == "void":
                print "REJECT"
                sys.exit(0)

            y = hasnum(token[i])
            if y is True:
                i += 1  # Accept NUM/FLOAT
                if token[i] == "]":
                    i += 1  # Accept ]
                    if token[i] == ";":
                        i += 1  # Accept ;
                    else:
                        print "REJECT"
                        sys.exit(0)
                else:
                    print "REJECT"
                    sys.exit(0)
            else:
                print "REJECT"
                sys.exit(0)
        elif token[i] == "(":
            i += 1  # Accept (
            for v in fundec:  # check for duplicate declared functions
                if token[i-2] in v:
                    print "REJECT"
                    sys.exit(0)
            fundec.append(token[i-3] + " " + token[i-2])
            funname = token[i-2]
            funnames.append(token[i-2])
            funtypes.append(token[i-3])
            funtype = token[i-3]
            funret = 0
            curscope = 0

            params()

            if token[i] == ")":
                i += 1  # Accept )
                compoundstmt()

                if funret == 0 and funtype == "int":
                    print "REJECT"
                    sys.exit(0)
                elif funret == 0 and funtype == "float":
                    print "REJECT"
                    sys.exit(0)
                else:
                    funret = 0

            else:
                print "REJECT"
                sys.exit(0)
        else:
            print "REJECT"
            sys.exit(0)
    else:
        print "REJECT"
        sys.exit(0)


def vd():  # 5
    global i, ismain
    types()

    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
        k = 0
        for v in vars:  # check for duplicate declared variables
            if token[i-1] == v:
                if varscope[k] == funname:
                    if varscopen[k] >= curscope:
                        print "REJECT"
                        sys.exit(0)
            k += 1
        vardec.append(token[i-2] + " " + token[i-1] + " " + str(funname) + " " + str(curscope))
        vars.append(token[i-1])
        vartype.append(token[i-2])
        varscope.append(funname)
        varscopen.append(curscope)

        if token[i-2] == "void":  # check if ID is type void
            print "REJECT"
            sys.exit(0)
    else:
        print "REJECT"
        sys.exit(0)

    if token[i] == ";":
        i += 1  # Accept ;
    elif token[i] == "[":
        i += 1  # Accept [
        x = hasnum(token[i])
        if x is True:
            i += 1  # Accept NUM/FLOAT
            if "." in token[i-1]:  # check for float in array declaration
                print "REJECT"
                sys.exit(0)
            if "E" in token[i-1]:  # check for float in array declaration
                print "REJECT"
                sys.exit(0)
            if token[i] == "]":
                i += 1  # Accept ]
                if token[i] == ";":
                    i += 1  # Accept ;
                    return
                else:
                    print "REJECT"
                    sys.exit(0)
            else:
                print "REJECT"
                sys.exit(0)
        else:
            print "REJECT"
            sys.exit(0)
    else:
        print "REJECT"
        sys.exit(0)


def types():  # 6
    global i
    if token[i] == "int" or token[i] == "void" or token[i] == "float":
        i += 1  # Accept int/void/float
    else:
        return


def fd():  # 7
    global i, ismain
    types()

    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        if token[i] == "main":
            ismain += 1
        i += 1  # Accept ID
    else:
        return

    if token[i] == "(":
        i += 1  # Accept (
    else:
        print "REJECT"
        sys.exit(0)

    params()

    if token[i] == ")":
        i += 1  # Accept )
    else:
        print "REJECT"
        sys.exit(0)

    compoundstmt()


def params():  # 8
    global i, fundeci
    if token[i] == "int" or token[i] == "float" or token[i] == "void":
        paramslist()
        fundeci += 1
    else:
        print "REJECT"
        sys.exit(0)


def paramslist():  # 9
    param()
    paramslistprime()


def paramslistprime():  # 10
    global i
    if token[i] == ",":
        i += 1  # Accept ,
        param()
        paramslistprime()
    elif token[i] == ")":
        return
    else:
        return


def param():  # 11
    global i, funname, curscope
    types()
    fundec[fundeci] = fundec[fundeci] + " " + token[i-1]
    funcallargs.append("")
    funcallargs[fundeci] = funcallargs[fundeci] + " " + token[i-1]
    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
        fundec[fundeci] = fundec[fundeci] + " " + token[i-1]

        k = 0
        m = 0
        mc = 0
        ch = 0
        for v in vars:  # check for duplicate declared variables and with scope
            if token[i-1] == v:
                if varscope[k] != "global" and varscope[k] != funname:
                    ch = 1
                    continue
                if varscope[k] == "global":
                    m = k
                    mc = 1
                    break
            k += 1

        curscope = 1
        if not varscope:
            ch = 1
        if ch == 0 and varscope[m] == "global" and mc == 1:
            vardec.append(token[i-2] + " " + token[i-1] + " global 0")
            vars.append(token[i-1])
            vartype.append(token[i-2])
            varscope.append("global")
            varscopen.append(0)

        else:
            vardec.append(token[i-2] + " " + token[i-1] + " " + str(funname) + " " + str(curscope))
            vars.append(token[i-1])
            vartype.append(token[i-2])
            varscope.append(funname)
            varscopen.append(curscope)

        curscope = 0

        if token[i] == "[":
            i += 1  # Accept [
            if token[i] == "]":
                i += 1  # Accept ]
                return
            else:
                print "REJECT"
                sys.exit(0)
        else:
            return
    else:
        if token[i-1] == "void":
            return
        else:
            print "REJECT"
            sys.exit(0)


def compoundstmt():  # 12
    global i, curscope
    if token[i] == "{":
        i += 1  # Accept {
        curscope += 1
    else:
        return

    localdeclarations()
    statementlist()

    if token[i] == "}":
        i += 1  # Accept }
    else:
        print "REJECT"
        sys.exit(0)


def localdeclarations():  # 13
    localdeclarationsprime()


def localdeclarationsprime():  # 14
    if token[i] == "int" or token[i] == "void" or token[i] == "float":
        vd()
        localdeclarationsprime()
    else:
        return


def statementlist():  # 15
    statementlistprime()


def statementlistprime():  # 16
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        statement()
        statementlistprime()
    elif y is True:
        statement()
        statementlistprime()
    elif token[i] == "(" or token[i] == ";" or token[i] == "{" or token[i] == "if" or\
                     token[i] == "while" or token[i] == "return":
        statement()
        statementlistprime()
    elif token[i] == "}":
        return
    else:
        return


def statement():  # 17
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        expstmt()
    elif y is True:
        expstmt()
    elif token[i] == "(" or token[i] == ";":
        expstmt()
    elif token[i] == "{":
        compoundstmt()
    elif token[i] == "if":
        selectionstmt()
    elif token[i] == "while":
        itstmt()
    elif token[i] == "return":
        retstmt()
    else:
        print "REJECT"
        sys.exit(0)


def expstmt():  # 18
    global i
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        exp()
        if token[i] == ";":
            i += 1  # Accept ;
        else:
            print "REJECT"
            sys.exit(0)
    elif y is True:
        exp()
        if token[i] == ";":
            i += 1  # Accept ;
        else:
            print "REJECT"
            sys.exit(0)
    elif token[i] == "(":
        exp()
        if token[i] == ";":
            i += 1  # Accept ;
        else:
            print "REJECT"
            sys.exit(0)
    elif token[i] == ";":
        i += 1  # Accept ;
    else:
        print "REJECT"
        sys.exit(0)


def selectionstmt():  # 19
    global i
    if token[i] == "if":
        i += 1  # Accept if
    else:
        return

    if token[i] == "(":
        i += 1  # Accept (
    else:
        print "REJECT"
        sys.exit(0)

    exp()
    if token[i] == ")":
        i += 1  # Accept )
    else:
        print "REJECT"
        sys.exit(0)
    statement()
    if token[i] == "else":
        i += 1  # Accept else
        statement()
    else:
        return


def itstmt():  # 20
    global i
    if token[i] == "while":
        i += 1  # Accept while
    else:
        return

    if token[i] == "(":
        i += 1  # Accept (
    else:
        print "REJECT"
        sys.exit(0)

    exp()

    if token[i] == ")":
        i += 1  # Accept )
    else:
        print "REJECT"
        sys.exit(0)

    statement()


def retstmt():  # 21
    global i, excret, exptype, funret
    if token[i] == "return":
        i += 1  # Accept return
        if funtype == "int":
            funret = 1
        else:
            funret = 1
    else:
        return
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] == ";":
        i += 1  # Accept ;
        if funtype != "void":  # check if int or float function does not return a value
            print "REJECT"
            sys.exit(0)
        return
    elif token[i] not in keywordchecklist and x is True:
        if funtype == "void":  # check if void has return with value
            print "REJECT"
            sys.exit(0)

        if funtype == "int":
            exptype = "int"
        else:
            exptype = "float"
        excret = 1
        exp()
        excret = 0

        if token[i] == ";":
            i += 1  # Accept ;
            return
        else:
            print "REJECT"
            sys.exit(0)
    elif y is True:
        if funtype == "void":  # check if void has return with value
            print "REJECT"
            sys.exit(0)

        if funtype == "int":
            exptype = "int"
        else:
            exptype = "float"
        excret = 1

        exp()
        excret = 0
        if token[i] == ";":
            i += 1  # Accept ;
            return
        else:
            print "REJECT"
            sys.exit(0)
    elif token[i] == "(":
        exp()
        if token[i] == ";":
            i += 1  # Accept ;
            return
        else:
            print "REJECT"
            sys.exit(0)
    else:
        print "REJECT"
        sys.exit(0)


def exp():  # 22
    global i, exptype, exc1, exc0, excret, parammatch, parm
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
        if parm == 1:
            o = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v == token[i-1]:
                    check = vartype[o]
                o += 1
            parammatch = parammatch + " " + check

        if exc0 == 1 and parm == 0:
            if token[i] == "(":
                o = 0
                check = 0
                for v in funnames:  # get the type of the function for operand/operator checking
                    if v == token[i-1]:
                        check = funtypes[o]
                    o += 1
                if exptype != check:
                    print "REJECT"
                    sys.exit(0)

            else:
                o = 0
                ch = 0
                check = 0
                for v in vars:  # check variable before checking if operator/operand agree
                    if v == token[i-1]:
                        if varscope[o] != "global" and varscope[o] != funname:
                            ch = 1
                        if varscope[o] == funname:
                            ch = 0
                            check = vartype[o]
                            break
                        check = vartype[o]
                    o += 1
                if ch == 1:
                    print "REJECT"
                    sys.exit(0)
                if exptype != check:
                    print "REJECT"
                    sys.exit(0)

        if exc1 == 1:
            o = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v == token[i-1]:
                    check = vartype[o]
                o += 1
            if exptype != check:
                print "REJECT"
                sys.exit(0)

        if excret == 1:
            o = 0
            check = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v == token[i-1]:
                    check = vartype[o]
                o += 1
            if exptype != check:
                print "REJECT"
                sys.exit(0)

        if token[i] == "(" and exc0 == 0 and parm == 0:
            if token[i-1] not in funnames:
                print "REJECT"
                sys.exit(0)

        ch = 0
        k = 0
        for v in vars:  # check for duplicate declared variables
            if token[i-1] == v:
                if varscope[k] != funname and varscope[k] != "global":
                    ch = 1
                if varscope[k] == funname:
                    ch = 0
            k += 1

        if token[i-1] not in vars and token[i] != "(":
            print "REJECT"
            sys.exit(0)

        if ch == 1:
            print "REJECT"
            sys.exit(0)

        ex()

    elif token[i] == "(":
        i += 1  # Accept (
        exp()
        if token[i] == ")":
            i += 1  # Accept )
            termprime()
            addexpprime()
            if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                           token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
            elif token[i] == "+" or token[i] == "-":
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
            elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                             token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
            else:
                return
        else:
            print "REJECT"
            sys.exit(0)
    elif y is True:
        i += 1  # Accept NUM/FLOAT
        if parm == 1:
            if "." in token[i-1]:
                parammatch = parammatch + " float"
            elif "E" in token[i-1]:
                parammatch = parammatch + " float"
            else:
                parammatch = parammatch + " int"

        ch = 0
        if "." in token[i-1]:
            ch = 1
        if "E" in token[i-1]:
            ch = 1

        if excret == 1 and ch == 1:
            if exptype != "float":
                print "REJECT"
                sys.exit(0)

        if excret == 1 and ch == 0:
            if exptype != "int":
                print "REJECT"
                sys.exit(0)

        if exc1 == 1 and "E" in token[i-1]:
            print "REJECT"
            sys.exit(0)
        if exc1 == 1 and "." in token[i-1]:
            print "REJECT"
            sys.exit(0)

        if exc0 == 1:
            if ch != 1 and exptype == "float":
                if "." not in token[i+1] and "E" not in token[i+1]:
                    print "REJECT"
                    sys.exit(0)

        termprime()
        addexpprime()
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                       token[i] == ">=" or token[i] == "==" or token[i] == "!=":
            relop()
            addexp()
        elif token[i] == "+" or token[i] == "-":
            addexpprime()
            if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                           token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
        elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                         token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
        else:
            return
    else:
        print "REJECT"
        sys.exit(0)


def ex():  # 22X
    global i, exptype, exc1, exc0, parm, parammatch
    if token[i] == "=":
        i += 1  # Accept =
        k = 0
        for v in vars:  # find the type of the first ID for the exp
            if token[i-2] == v:
                exptype = vartype[k]
                exc0 = 1
            k += 1
        exp()
        exc0 = 0
    elif token[i] == "[":
        i += 1  # Accept [
        exptype = "int"
        exc1 = 1
        exp()
        exc1 = 0
        if token[i-1] == "[":
            print "REJECT"
            sys.exit(0)
        if token[i] == "]":
            i += 1  # Accept ]
            if token[i] == "=":
                i += 1  # Accept =
                exp()
            elif token[i] == "*" or token[i] == "/":
                termprime()
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
                else:
                    return
            elif token[i] == "+" or token[i] == "-":
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
            elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                             token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
            else:
                return
        else:
            print "REJECT"
            sys.exit(0)
    elif token[i] == "(":
        i += 1  # Accept (
        k = 0
        for v in funnames:
            if v == token[i-2]:
                break
            k += 1
        args()
        parm = 0
        u = 0
        if not parammatch:
            u = 1
        if u == 0 and funcallargs[k] != parammatch:
            print "REJECT"
            sys.exit(0)

        if token[i] == ")":
            i += 1  # Accept )
            if token[i] == "*" or token[i] == "/":
                termprime()
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
                else:
                    return
            elif token[i] == "+" or token[i] == "-":
                addexpprime()
                if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                               token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                    relop()
                    addexp()
            elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                             token[i] == ">=" or token[i] == "==" or token[i] == "!=":
                relop()
                addexp()
            else:
                return
        else:
            print "REJECT"
            sys.exit(0)
    elif token[i] == "*" or token[i] == "/":
        termprime()
        addexpprime()
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                       token[i] == ">=" or token[i] == "==" or token[i] == "!=":
            relop()
            addexp()
        else:
            return
    elif token[i] == "+" or token[i] == "-":
        addexpprime()
        if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                       token[i] == ">=" or token[i] == "==" or token[i] == "!=":
            relop()
            addexp()
        else:
            return
    elif token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                     token[i] == ">=" or token[i] == "==" or token[i] == "!=":
        relop()
        addexp()
    else:
        return


def var():  # 23
    global i
    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
    else:
        return
    if token[i] == "[":
        i += 1  # Accept [
        exp()
        if token[i] == "]":
            i += 1  # Accept ]
        else:
            print "REJECT"
            sys.exit(0)
    else:
        return


def simexp():  # 24
    addexp()
    if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                   token[i] == ">=" or token[i] == "==" or token[i] == "!=":
        relop()
        addexp()
    else:
        return


def relop():  # 25
    global i
    if token[i] == "<=" or token[i] == "<" or token[i] == ">" or\
                   token[i] == ">=" or token[i] == "==" or token[i] == "!=":
        i += 1  # Accept <=, <, >, >=, ==, or !=
    else:
        return


def addexp():  # 26
    term()
    addexpprime()


def addexpprime():  # 27
    if token[i] == "+" or token[i] == "-":
        addop()
        term()
        addexpprime()
    else:
        return


def addop():  # 28
    global i
    if token[i] == "+" or token[i] == "-":
        i += 1  # Accept +, -
    else:
        return


def term():  # 29
    factor()
    termprime()


def termprime():  # 30
    if token[i] == "*" or token[i] == "/":
        mulop()
        factor()
        termprime()
    else:
        return


def mulop():  # 31
    global i
    if token[i] == "*" or token[i] == "/":
        i += 1  # Accept *, /
    else:
        return


def factor():  # 32
    global i, exc0, excret
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID

        if exc0 == 1:
            o = 0
            ch = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v == token[i-1]:
                    if varscope[o] != "global" and varscope[o] != funname:
                        ch = 1
                    if varscope[o] == funname:
                        ch = 0
                        check = vartype[o]
                        break
                    check = vartype[o]
                o += 1
            if exptype != check:
                print "REJECT"
                sys.exit(0)
            if ch == 1:
                print "REJECT"
                sys.exit(0)

        if excret == 1:
            o = 0
            for v in vars:  # get the type of the var for operand/operator checking
                if v == token[i-1]:
                    check = vartype[o]
                o += 1
            if exptype != check:
                print "REJECT"
                sys.exit(0)


        if token[i] == "[":
            i += 1  # Accept [
            exp()
            if token[i] == "]":
                i += 1  # Accept ]
            else:
                return
        elif token[i] == "(":
            i += 1  # Accept (
            args()
            if token[i] == ")":
                i += 1  # Accept )
            else:
                return
        else:
            return
    elif y is True:
        i += 1  # Accept NUM/FLOAT
    elif token[i] == "(":
        i += 1  # Accept (
        exp()
        if token[i] == ")":
            i += 1  # Accept )
        else:
            return
    else:
        print "REJECT"
        sys.exit(0)


def call():  # 33
    global i
    x = token[i].isalpha()
    if token[i] not in keywordchecklist and x is True:
        i += 1  # Accept ID
        if token[i] == "(":
            i += 1  # Accept (
            args()
            if token[i] == ")":
                i += 1  # Accept )
            else:
                print "REJECT"
                sys.exit(0)
        else:
            print "REJECT"
            sys.exit(0)
    else:
        return


def args():  # 34
    global i
    x = token[i].isalpha()
    y = hasnum(token[i])
    if token[i] not in keywordchecklist and x is True:
        arglist()
    elif y is True:
        arglist()
    elif token[i] == "(":
        arglist()
    elif token[i] == ")":
        return
    else:
        return


def arglist():  # 35
    global parammatch, parm
    parm = 1
    parammatch = ""
    exp()
    arglistprime()


def arglistprime():  # 36
    global i
    if token[i] == ",":
        i += 1  # Accept ,
        exp()
        arglistprime()
    elif token[i] == ")":
        return
    else:
        return


# ----------------------------- end of parsing functions --------------------------------- #

# begin parsing
program()

# print vardec
# print fundec

if ismain == 1 and lastmain == 1:  # check if contains 1 main function
    print "ACCEPT"
else:
    print "REJECT"
