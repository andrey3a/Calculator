"""Reverse Polish Notation"""
import operator

class Calculator(object):
    """This class translates infix nitation into reverse polish notation and calculate result"""
    
    def __init__(self, expression):
        """Constructor"""
        self.__expression = expression
        self.__operationPriority = {
            ')' : 0,
            '(' : 0,
            '+' : 1,
            '-' : 1,
            '*' : 2,
            '/' : 2,
            '^' : 3,
            '_' : 3, # unary minus
        }
        self.__operators = {
            '+' : operator.add,
            '-' : operator.sub,
            '*' : operator.mul,
            '/' : operator.truediv,
            '^' : operator.pow
        }
        self.__stack = []
        self.__reversePolishNotation = []
        self.__result = 0
        self.__error = ""
        self.__numbers = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]
        self.__postfixFunctions = [ '!' ]
        self.__delimeter = [ '.' ]


    def reverseInfixEntry(self):
        """This function translates infix notation into reverse polish notation"""
        self.__reversePolishNotation.clear()
        self.__stack.clear()
        if (self.__error):
            return
        lenExpr = len(self.__expression)
        if (lenExpr):
            for i in range(lenExpr):
                symbol = self.__expression[i]
                if (symbol in self.__delimeter):
                    if (i == lenExpr - 1):
                        self.__error = "Invalid delimeter expression"
                        return -1
                    else:
                        if not(self.__expression[i + 1] in self.__numbers):
                            self.__error = "Invalid delimeter expression"
                            return -1
                elif (symbol in self.__postfixFunctions):
                    if (i == 0):
                        self.__error = "Invalid expression with posfix function"
                        return -3 
                    elif not(self.__expression[i - 1] in self.__numbers):
                        self.__error = "Invalid expression with posfix function"
                        return -3
                    elif (i < lenExpr - 1):
                        if (self.__expression[i + 1] in self.__numbers):
                            self.__error = "Invalid expression with posfix function"
                            return -3
                    self.__reversePolishNotation.append(symbol)
                if ((symbol in self.__numbers) or (symbol in self.__delimeter)):
                    if (not(symbol in self.__postfixFunctions) and (i > 0) and not(self.__expression[i - 1] in self.__operationPriority.keys())):
                        prevSymbol = self.__reversePolishNotation.pop()
                        symbol = prevSymbol + symbol
                    self.__reversePolishNotation.append(symbol)
                elif ((symbol == '-') and ((self.__expression[i - 1] in self.__operators.keys()) or (i == 0) or self.__expression[i - 1] == '(')):
                    self.__reversePolishNotation.append('_')
                elif (symbol == '('):
                    self.__stack.append(symbol)
                elif (symbol == ')'):
                    if len(self.__stack) > 0:
                        elemOfStack = self.__stack.pop()
                        while ((elemOfStack != '(') and (len(self.__stack) != 0)):
                            self.__reversePolishNotation.append(elemOfStack)
                            elemOfStack = self.__stack.pop()
                    if ((len(self.__stack) == 0) and (elemOfStack != '(')):
                        self.__error = "Invalid expression with brackets"
                        return -2
                elif (symbol in self.__operationPriority.keys()):
                    if (i == lenExpr - 1):
                        self.__error = "Invalid expression"
                        return -4
                    elif ((self.__expression[i + 1] in self.__operators.keys()) and (self.__expression[i + 1] != '-')):
                        self.__error = "Invalid expression"
                        return -4
                    symbolPriority = self.__operationPriority[symbol]
                    elemOfStack = ''
                    if len(self.__stack) > 0:
                        topStackPriority = self.__operationPriority[self.__stack[-1]]
                        while ((topStackPriority >= symbolPriority) and (len(self.__stack) != 0) and (elemOfStack != '(')):
                            elemOfStack = self.__stack.pop()
                            self.__reversePolishNotation.append(elemOfStack)
                            if (len(self.__stack) > 0):
                                topStackPriority = self.__operationPriority[self.__stack[-1]]
                    self.__stack.append(symbol)
            while (len(self.__stack) > 0):
                self.__reversePolishNotation.append(self.__stack.pop())
        else:
            self.__error = "Length of input expression = 0"
            return -5


    def factorial(self, n):
        """This function calculate factorial"""
        if (n > 0):
            return n * self.factorial(n - 1)
        else:
            return 1


    def calculateResult(self):
        """This function calculate result"""
        self.reverseInfixEntry()
        self.__stack.clear()
        if (self.__error):
            return
        lenExpr = len(self.__reversePolishNotation)
        iterSkipp = 0
        unaryMinus = -1
        for i in range(lenExpr):
            if ((iterSkipp > 0) and (iterSkipp > i)):
                continue
            symbol = self.__reversePolishNotation[i]
            if ((symbol == '(') or (symbol == ')')):
                self.__error = "Invalid expression with brackets"
                return -2
            elif (symbol == '!'):
                number = self.__stack.pop()
                number = self.factorial(number)
                self.__stack.append(number)
            elif (symbol == '_'):
                if (i < lenExpr - 1):
                    if (self.__reversePolishNotation[i + 1] not in self.__operationPriority.keys()):
                        iterSkipp = i + 2
                    elif (self.__reversePolishNotation[i + 1] == symbol):
                        unaryMinus *= -1
                        continue
                else:
                    self.__error = "Invalid expression"
                    return -4
                if (unaryMinus == -1):
                    strNumber = '-' + self.__reversePolishNotation[i + 1]
                elif (unaryMinus == 1):
                    strNumber = self.__reversePolishNotation[i + 1]
                if (strNumber.find('.') > -1):
                    number = float(strNumber)
                else:
                    number = int(strNumber)
                self.__stack.append(number)
                unaryMinus = -1
            elif (symbol in self.__operators.keys()):
                try:
                    number2, number1 = self.__stack.pop(), self.__stack.pop()
                except IndexError:
                    self.__error = "Index error"
                    return -7
                try:
                    self.__stack.append(self.__operators[symbol](number1, number2))
                except ZeroDivisionError:
                    self.__error = "Division by zero"
                    return -6
            elif (symbol not in self.__operationPriority.keys()):
                if (symbol.find('.') > -1):
                    number = float(symbol)
                else:
                    number = int(symbol)
                self.__stack.append(number)
        if (len(self.__stack) == 1):
            self.__result = self.__stack.pop()
            if (int(self.__result) == self.__result):
                self.__result = int(self.__result)
        else:
            self.__error = "Invalid expression"
            return -4

    
    def getExpression(self):
        """This function return string of expression"""
        return self.__expression


    def getResult(self):
        """This function return result"""
        return self.__result

        
    def getReversePolishNotation(self):
        """This function return string of reverse polish notation"""
        return ''.join(self.__reversePolishNotation)


    def getError(self):
        """This function return string of error"""
        return self.__error


    def setExpression(self, expr):
        """This function set string of expression"""
        self.__expression = expr
        self.__error = ''
        self.__result = 0


if __name__ == "__main__" :
    # calc = Calculator("3+4*2/(1-5)^2") # 342*15-2^/+ # 3.5
    # calc = Calculator("(8+2*5)/(1+3*2-4)") # 825*+132*+4-/ # 6
    # calc = Calculator("(1+2*4)/2") # 124*+2/ # 4.5
    # calc = Calculator("((3-5)*(-2+2)+4*(7+2))") # 35-_22+*472+*+ # 36
    # calc = Calculator("-1+2*3!^2") # _123!2^*+ # 71
    # calc = Calculator("11.1+-1.1+2!") # 11.1_1.1+2!+ # 12
    # calc = Calculator("((-1.234+.234)*-1)-1") # _1.234.234+_1*1- # 0
    # calc = Calculator("3!^2!") # 3!2!^ # 36
    # calc = Calculator("-.12+((.08+.2*5)/3^2)+14/10") # _.12.08.25*+32^/+1410/+ # 1.4
    calc = Calculator("-----2-----5!") # _____2____5!- # -122
    print(calc.getExpression())
    calc.calculateResult()
    print(calc.getReversePolishNotation())
    print(calc.getError())
    print(calc.getResult())