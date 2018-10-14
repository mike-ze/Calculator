import math
class Calculator:
    # use stack to store the position of parentheses
    class stack:
        class node:
            def __init__(self, value, nextNode):
                self.value = value
                self.nextNode = nextNode
                
        def __init__(self):
            self.top = None
            self.last = None
            self.size = 0

        def __len__(self):
            return self.size

        def push(self, value):
            # push a node into the stack
            newNode = self.node(value, None)   # create a new node
            if self.size ==0:
                self.top = newNode
                self.last = newNode
                self.size += 1
            else:
                newNode.nextNode = self.top
                self.top = newNode
                self.size += 1
                         
        def pop(self):
            # pop a node out of the stack
            if self.size ==0:
                return "error"
            elif self.size == 1:
                x = self.top.value
                self.top = None
                self.last = None
                self.size -= 1
                return x
            else:
                x = self.top.value
                self.top = self.top.nextNode
                self.size -= 1
                return x

    def findNextOpr(self, s):        # find the next operator
        #s must be a nonempty string. 
        if len(s)<=0 or not isinstance(s,str):
            print("type mimatch error: findNextOpr")
            return "type mimatch error: findNextOpr"

        offset=0
        for i in range(len(s)):
            if s[0]==" ":
                s=s.strip()
            if self.isNumber(s[:i+1]):
                offset = i
        if offset >= len(s)-1:
            return -1
        a=s.find("+", offset+1)
        b=s.find("-", offset+1)
        c=s.find("*", offset+1)
        d=s.find("/", offset+1)
        e=s.find("^", offset+1)
        oprs=[]
        oprs.append(a)
        oprs.append(b)
        oprs.append(c)
        oprs.append(d)
        oprs.append(e)
        oprs1=oprs[:]
        if oprs==[-1,-1,-1,-1,-1]:
            return -1
        else:
            for i in oprs:
                if i==-1:
                    oprs1.remove(-1)
            return min(oprs1)
        #--- function code ends -----#

    def isNumber(self, s):
        #s must be a non-empty string
        #returns True if it's convertible to float, else False
        if len(s)==0 or not isinstance(s, str):
            print("type mismatch error: isNumber")
            return "type mismatch error: isNumber"
        s=s.strip()
        if True:
            if s[0]=="-":
                s=s[1:]
            try:
                float(s)
                return True
            except ValueError:
                return False
            
    def isVariable(self, s):
        if self.isNumber(str(s)):
            return False
        s = s.strip()
        if isinstance(s, str):
            if s.isalnum() and self.isNumber(s[0])==False:
                return True
            else:
                return False
        else:
            return False
     
    def getNextItem(self, expr, pos):
        #expr is a given arithmetic formula in string
        #pos = start position in expr
        #1st returned value = the next number (None if N/A)
        #2nd returned value = the next operator (None if N/A)
        #3rd retruned value = the next operator position (None if N/A)
        if len(expr)==0 or not isinstance(expr, str) or pos<0 or pos>=len(expr) or not isinstance(pos, int):
            print("type mismatch error: getNextItem")
            return None, None, "type mismatch error: getNextItem"

        #print("expr in getNextItem:", expr)
        expr1 = expr.strip()
        f_expr = expr
        negative_at_the_front = False
        negative_in_the_middle = False
        # f_expr is expr without the first -
        if expr1[0]=="-" and pos==0:
            negative_at_the_front = True
            f_expr = list(expr)
            for i in range(len(expr)):
                if f_expr[i]=="-":
                    f_expr[i]=" "
                    break
            f_expr = "".join(f_expr)
        s = f_expr[pos:]
        # - in the middle, before looking for the position of next operator
        f_s = s
        s_strip = s.strip()
        if s_strip[0]=="-":
            negative_in_the_middle = True
            f_s = list(s)
            for i in range(len(s)):
                if f_s[i]=="-":
                    f_s[i]=" "
            f_s = "".join(f_s)
        # find the position of next operator
        p = self.findNextOpr(f_s)
        if p==-1:
            newOpr=None
            oprPos=None
        else:
            newOpr=f_s[p]
            oprPos=pos+p
        newnum=f_expr[pos:oprPos]
        #print("newnum:",newnum)
        # convert string number to float        
        if self.isNumber(newnum):
            # handle "- 4"
            newnum_strip = newnum.strip()
            if newnum_strip[0]=="-":
                newnum = list(newnum)
                for i in range(len(newnum)):
                    if newnum[i]=="-":
                        newnum[i]=" "
                        newnum = "".join(newnum)
            newNumber=float(newnum)
        else:
            newNumber=None
        # find variable name
        if self.isVariable(newnum):
            newNumber = newnum.strip()
        if negative_at_the_front == True and pos==0:
            newNumber = newNumber*-1
        if negative_in_the_middle == True:
            newNumber = newNumber*-1
        #print(newNumber, newOpr, oprPos)
        return newNumber, newOpr, oprPos


    def __init__(self):
        self.lines = []
        self.varDic = {}
        self.functDef='''
        sqrt x: math.sqrt(x) ;
        exp  x: math.exp(x) ;
        sin  x: math.sin(x) ;
        cos  x: math.cos(x) ;
        tan  x: math.tan(x) ;
        ln   x: math.log(x) ;
        lg   x: math.log(x) / math.log(2) ;
        round x, y: x – y * math.floor(x/y)
        '''
        self.functDic={}
        self.setFunct()

    def setFunct(self):
        # The function refers to self.functDef, 
        #  and set self.functDic to be 
        # {'sqrt': 'x: math.sqrt(x)', 'exp': 'x: math.exp(x)', 'sin': 'x: math.sin(x)',
        #   'cos': 'x: math.cos(x)', 'tan': 'x: math.cos(x)', 'ln': 'x: math.log(x)',
        #   'lg': 'x: math.log(x) / math.log(2)', 'round': 'x, d: round(x, d)'}
        self.functDic = {'sqrt': 'x: math.sqrt(x)', 'exp': 'x: math.exp(x)', 'sin': 'x: math.sin(x)', 'cos': 'x: math.cos(x)', 'tan': 'x: math.cos(x)', 'ln': 'x: math.log(x)', 'lg': 'x: math.log(x) / math.log(2)', 'round': 'x, d: round(x, d)', 'mod': 'mod'}

    def getLines(self, expr):
        expr_split = expr.split()
        for i in range(len(expr_split)):
            # add = after "return"
            if expr_split[i]=="return":
                expr_split.insert(i+1,"=")
        expr = " ".join(expr_split)
        each_expr = expr.split(";")
        for i in each_expr:
            expr_parts = i.split("=")
            for j in range(len(expr_parts)):
                expr_parts[j]=expr_parts[j].strip()
            self.lines.append(expr_parts)

        
    def _calc(self, expr):
        #expr: nonempty string that is an arithmetic expression
        #the fuction returns the calculated result
        if len(expr)<=0 or not isinstance(expr,str):
            print("argument error: line A in eval_expr")        #Line A
            return "argument error: line A in eval_expr"
        #Hold two modes: "addition" and "multiplication"
        #Initializtion: get the first number
        newNumber, newOpr, oprPos = self.getNextItem(expr, 0)
        # get variable's number from dict
        if self.isVariable(newNumber):
            newNumber = self.varDic[newNumber]
        if newNumber is None:
            print("input formula error: line B in eval_expr")   #Line B
            return "input formula error: line B in eval_expr"
        elif newOpr is None:
            return newNumber
        elif newOpr=="+" or newOpr=="-":
            mode="add"
            addResult=newNumber     #value so far in the addition mode
            mulResult=None          #value so far in the mulplication mode
        elif newOpr=="*" or newOpr=="/":
            mode="mul"
            addResult=0
            mulResult=newNumber
        elif newOpr=="^":
            mode="pow"
        pos=oprPos+1                #the new current position
        opr=newOpr                  #the new current operator
        #start the calculation. Use the above functions effectively.
        ladd=[]
        lmul=[]
        #1st loop
        pnum=newNumber
        powdiv=0
        if mode == 'add':
            ladd.append(newNumber)
        elif mode == 'mul':
            lmul.append(newNumber)
            powadd=1
            if newOpr=="/":
                powdiv=1
        elif mode == 'pow':
            if newNumber<0:
                #lmul.append("+")
                pnum=pnum*-1
        while True:
        
            newNumber, newOpr, oprPos = self.getNextItem(expr, pos)
            # get variable's number from dict
            if self.isVariable(newNumber):
                newNumber = self.varDic[newNumber]
            #final loop
            if newNumber==None and newOpr != None:
                return "Error"
            if newOpr== None and oprPos == None:
                if mode == 'add':
                    if opr == '+':
                        ladd.append(newNumber)
                    else:
                        ladd.append(newNumber * -1)
                elif mode == 'mul':
                    if opr == '*':
                        lmul.append(newNumber)
                    else:
                        try:
                            lmul.append(1/newNumber)
                        except:
                            return "Error"
                elif mode == 'pow':
                    if powdiv==1:
                        lmul.append(1/pnum**newNumber)
                    if powdiv==0:
                        lmul.append(pnum**newNumber)
                break
            #listing
            if mode == 'add' and (newOpr =='+' or newOpr == '-'):
                if opr == '+':
                    ladd.append(newNumber)
                else:
                    ladd.append(newNumber * -1)
                powdiv=0
            elif mode == 'add' and (newOpr =='*' or newOpr == '/'):
                mode = 'mul'
                lmul.append(opr)
                lmul.append(newNumber)
                if newOpr=="/":
                    powdiv=1
                if newOpr=="*":
                    powdiv=0
            # +3^3
            elif mode == 'add' and (newOpr =='^'):
                mode = 'pow'
                lmul.append(opr)
                powdiv=0
            elif mode == 'mul' and (newOpr == '+' or newOpr=='-'):
                mode = 'add'
                if opr=='*':
                    lmul.append(newNumber)
                else:
                    try:
                        lmul.append(1/newNumber)
                    except:
                        return "Error"
                powdiv=0
            elif mode == 'mul' and (newOpr == '*' or newOpr == '/'):
                if opr =='*':
                    lmul.append(newNumber)
                elif opr == '/':
                    try:
                        lmul.append(1/newNumber)
                    except:
                        return "Error"
                if newOpr=="/":
                    powdiv=1
                if newOpr=="*":
                    powdiv=0
            # *3^3
            elif mode == 'mul' and (newOpr =='^'):
                mode = 'pow'
                if newOpr=="/":
                    powdiv=1
                if newOpr=="*":
                    powdiv=0
            # ^3+3
            elif mode == 'pow' and (newOpr =='+' or newOpr == '-'):
                mode = 'add'
                if powdiv==1:
                    lmul.append(1/pnum**newNumber)
                else:
                    lmul.append(pnum**newNumber)
                powdiv=0
            # ^3*3
            elif mode == 'pow' and (newOpr =='*' or newOpr == '/'):
                mode = 'mul'
                if powdiv==1:
                    lmul.append(1/pnum**newNumber)
                else:
                    lmul.append(pnum**newNumber)
                if newOpr=="*":
                    powdiv=0
                if newOpr=="/":
                    powdiv=1
            # ^3^3
            elif mode == 'pow' and newOpr == '^':
                return "Error"
            pnum=newNumber
            pos=oprPos+1
            opr=newOpr
        #print(ladd,lmul)
        #calculation
        x = 0
        y = 1
        z = 0
        l = []
        for i in lmul:
            if i == None:
                return "Error. None in lmul"
            if z == 0:
                pass
            else:
                if self.isNumber(str(i)) and self.isNumber(str(lmul[z-1])):
                    y = i*lmul[z-1]
                    lmul[z] = y
                    lmul[z-1] = 0
                elif self.isNumber(str(i)) and (self.isNumber(str(lmul[z-1]))==False):
                    y = 1
            z += 1
        z=0
        for i in lmul:
            if i != 0:
                l.append(i)
        for i in l:
            if i == "-":
                l[z+1] *=-1
            z += 1
        z=0
        fadd=0
        fmul=0
        final=0
        for i in ladd:
            if i == None:
                return "Error. None in ladd"
            fadd += i
        for i in l:
            if self.isNumber(str(i)):
                fmul += i
        if len(l)==0:
            return fadd
        else:
            final = fadd+fmul
            return final
        

    # from the expression tree exercise
    def mask(self, s):
        nestLevel = 0
        masked = list(s)
        for i in range(len(s)):
            if s[i]==")":
                nestLevel -=1
            elif s[i]=="(":
                nestLevel += 1
            if nestLevel>0 and not (s[i]=="(" and nestLevel==1):  # Line A
                masked[i]=" "
        return "".join(masked)
        
    def findFunctParen(self,expr):
        # expr = arithmetic expression without a space
        # Find a minimal substring including a function name
        #   and the matched pair of parentheses
        # Return
        #   1st value = the start position of the substring, or None if N/A
        #   2nd value = the end position of the substring, or None if N/A
        #   3rd value = function name, or None if N/A
        #
        # e.g.
        #   s = "2*sin(2*pi)"  -->  returns 2, 10, “sin”
        #   s = "2*32*(2*pi)"  -->  returns 5, 10, None
        #   s = "2*32/8/4/2"   -->  returns None, None, None
        expr = self.mask(expr)
        # find function name
        start_pos=0
        end_pos=0
        for i in self.functDic:
            if i in expr:
                funct=i
                break
        else:
            funct=None
        # find start position
        if funct!=None:
            start_pos = expr.find(funct)
        elif "(" in expr:
            start_pos = expr.find("(")
        else:
            start_pos=None
        # find end position
        if start_pos == None:
            end_pos=None
        else:
            end_pos=expr[start_pos:].find(")")+start_pos
        return start_pos, end_pos, funct

    def _calcFunctExpr(self, expr):
        #calculate functions inside
        for i in expr:
            if i == " ":
                expr=expr.replace(i,"")
        leftPos, rightPos, f = self.findFunctParen(expr)
        print("leftPos:", leftPos, "rightPos:", rightPos, "function:", f)
        fx = ""
        if f!=None:
            if f=="round":
                insideF = expr[leftPos+len(f)+1:rightPos]
                comma_pos = insideF.find(",")
                var1 = self._calcFunctExpr(insideF[:comma_pos])
                var2 = int(insideF[comma_pos+1:])
                fx = str(round(var1, var2))
            elif f=="mod":
                insideF = expr[leftPos+len(f)+1:rightPos]
                comma_pos = insideF.find(",")
                var1 = self._calcFunctExpr(insideF[:comma_pos])
                var2 = float(insideF[comma_pos+1:])
                fx = str(var1-var2*(var1//var2))
            else:
                insideF = expr[leftPos+len(f)+1:rightPos]
                insideF = self._calcFunctExpr(insideF)
                fBody = self.functDic[f]
                fx = str(eval("("+"lambda "+fBody+")(insideF)"))
            expr=expr.replace(expr[leftPos:rightPos+1], fx)
            print(expr)
            return self._calcFunctExpr(expr)
        print(expr)
        #handle -2^2
        expr_strip = expr.strip()
        if expr_strip[0]=="-":
            expr = "0"+expr_strip
        #try:
        if True:
            s = self.stack()
            for i in range(len(expr)):
                if expr[i] == "(":
                    s.push(i)
                if expr[i] == ")":
                    x=s.pop()
                    expr1_strip=expr[x+1:i].strip()
                    if expr1_strip[0]=="-":
                        result = self._calc("0"+expr[x+1:i])
                        #print("0"+expr[x+1:i]," = ",result)
                    else:
                        result = self._calc(expr[x+1:i])
                        #print(expr[x+1:i]," = ",result)
                    expr = expr[:x]+str(result)+(i-x+1-len(str(result)))*" "+expr[i+1:]
            else:
                return self._calc(expr)

            
    def calc(self, expr):
        if True:
            self.getLines(expr)
            for j in self.lines:
                for i in j:
                    if not self.isVariable(i):
                        self.varDic[j[0]]= self._calcFunctExpr(i)
                    if i=="return":
                        self.varDic["__return__"]= self._calcFunctExpr(j[1])
            return self.varDic["__return__"]


## To debug
c = Calculator()
#s  = "pi =3.1415926; r= 6*(2 - (7-5)/3) ; S =pi * r^2; return S"
#s = "pi =0.00000001; return 2*sin(2*pi)"
#s = "2*32*(2*pi)"
#s = "return 2*-15"
#print(c.calc(s))

#output:
#201.0619264
#To check
s = "  a1 =  - 1 / 2 ; b = exp(- 3 * a1) ; return round(b,3) "
print("input: "+ s + "\n" + "output: " + str(c.calc(s)))
print("****************")
print("input:   ", s)
