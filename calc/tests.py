from django.test import TestCase
from calc.rpn import Calculator

class CalculatorTest(TestCase):
    """This class tested module rpn.py"""

    def setUp(self):
        self.__Calculator = Calculator('')
        self.__testExpressions = [ 
            '3+4*2/(1-5)^2', 
            '(8+2*5)/(1+3*2-4)', 
            '(1+2*4)/2', 
            '((3-5)*(-2+2)+4*(7+2))', 
            '-1+2*3!^2',
            '11.1+-1.1+2!',
            '((-1.234+.234)*-1)-1',
            '3!^2!',
            '-.12+((.08+.2*5)/3^2)+14/10',
            '-----2-----5!'
        ]
        self.__testReversePolishNotations = [ 
            '342*15-2^/+', 
            '825*+132*+4-/', 
            '124*+2/', 
            '35-_22+*472+*+', 
            '_123!2^*+',
            '11.1_1.1+2!+',
            '_1.234.234+_1*1-',
            '3!2!^',
            '_.12.08.25*+32^/+1410/+',
            '_____2____5!-'
        ]
        self.__testResult = [ 
            3.5, 
            6, 
            4.5, 
            36, 
            71,
            12,
            0,
            36,
            1.4,
            -122
        ]
        self.__testErrors = {
            'invalidDelimeterError' : 'Invalid delimeter expression',
            'invalidPosfixFunctionError' : 'Invalid expression with posfix function',
            'invalidBracketsError' : 'Invalid expression with brackets',
            'invalidLengthError' : 'Length of input expression = 0',
            'invalidDivisionError' : 'Division by zero',
            'invalidExpressionError' : 'Invalid expression'
        }
        self.__testFailedExpressions = {
            'invalidDelimeterError' : [ '.+1', '1+2+.', '(1+2)/3.' ],#
            'invalidPosfixFunctionError' : [ '!5', '1+!', '5!3' ],
            'invalidBracketsError' : [ '1+2)', '(1+2' ],
            'invalidLengthError' : [ '' ],
            'invalidDivisionError' : [ '1/0', '1/(1-1)' ],
            'invalidExpressionError' : [ '(1(-2))', '1++2', '1+2+' ]
        }


    def testRPNstrings(self):
        """This function tested reverse polish notation strings"""
        for i in range(len(self.__testExpressions)):
            self.__Calculator.setExpression(self.__testExpressions[i])
            self.__Calculator.reverseInfixEntry()
            self.assertEqual(self.__Calculator.getReversePolishNotation(), self.__testReversePolishNotations[i])


    def testCalculate(self):
        """This function tested result"""
        for i in range(len(self.__testExpressions)):
            self.__Calculator.setExpression(self.__testExpressions[i])
            self.__Calculator.calculateResult()
            self.assertEqual(self.__Calculator.getResult(), self.__testResult[i])


    def testFailed(self):
        """This function tested fails"""
        failedExprKeys = list(self.__testFailedExpressions.keys())
        for i in range(len(failedExprKeys)):
            for expr in self.__testFailedExpressions[failedExprKeys[i]]:
                self.__Calculator.setExpression(expr)
                self.__Calculator.calculateResult()
                self.assertEqual(self.__testErrors[failedExprKeys[i]], self.__Calculator.getError())