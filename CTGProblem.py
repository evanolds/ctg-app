# Author:
#   Evan Olds
#
# Created:
#   April 7, 2026

import random
import math

# CTGProblem represents an immutable, randomly generated 
# variant of the problem:
#   limit as x -> -1 of (x + 1) / (x^2 + cx + b)
# where c and b are randomly generated integer coefficients.
class CTGProblem:
    def __init__(self, b, c, answer_denominator):
        self._b = b
        self._c = c
        self._answer_denomintor = answer_denominator
    
    def float_answer_equals(self, user_float_answer, tolerance = 0.00001):
        expected_float = 1.0 / math.sqrt(self._answer_denomintor)
        difference = math.fabs(expected_float - user_float_answer)
        return difference <= tolerance
    
    def get_b(self):
        return self._b
    
    def get_c(self):
        return self._c
    
    def get_explanation(self, student_answer_str):
        # Special case for no user input
        if len(student_answer_str) == 0:
            return [{
                "type": "badge",
                "value": "Incorrect"
            },
            {
                "type": "text",
                "value": "Please enter an answer"
            }]
        
        answer = self.get_symbolic_answer()
        
        # Determine if the answer is correct or not
        user_correct = False
        
        if student_answer_str == answer:
            # Exact match for student's answer and expected answer
            user_correct = True
        else:
            user_float = CTGProblem._eval_as_float(student_answer_str)
            if math.isnan(user_float):
                return [{
                    "type": "badge",
                    "value": "Incorrect"
                },
                {
                    "type": "text",
                    "value": ("The entered expression cannot be evaluated. Please " +
                        "enter a fraction or decimal.")                    
                }]
            # If successfully parsed as a float, compared against expected
            user_correct = self.float_answer_equals(user_float)
        
        # Provided one of the cases above is not encountered, the user 
        # always receives the same explanation, minus the minor difference 
        # of the correct vs. incorrect badge.
        parts = []
        if user_correct:
            parts.append({
                "type": "badge",
                "value": "Correct"
            })
        else:
            parts.append({
                "type": "badge",
                "value": "Incorrect"
            })
            parts.append({
                "type": "text",
                "value": f"The correct limit is {answer}."
            })
        
        # Build explanation
        message = ("The expression inside the square root evaluates " +
            "0/0 at x = -1. So direct substitution cannot be used and " + 
            "L'Hôpital's rule must be used.")
        parts.append({
            "type": "text",
            "value": message
        })
        parts.append({
            "type": "text",
            "value": ("Focusing on the fractional part, and taking the "
                "derivative of both numerator and denominator yields:")
        })
        parts.append({
            "type": "latex",
            "value": "\\frac{1}{2x + " + str(self._c) + "}"
        })
        parts.append({
            "type": "text",
            "value": "-1 can then be substituted for x, yielding:"
        })
        latex_str = "\\sqrt{\\frac{1}{"
        latex_str += str(self._c - 2) + "}}"
        parts.append({
            "type": "latex",
            "value": latex_str
        })
        parts.append({
            "type": "text",
            "value": f"So the final answer is {answer}."
        })
        return parts
    
    def get_symbolic_answer(self):
        # Special case if _answer_denomintor is 1
        if self._answer_denomintor == 1:
            return "1"
        return f"1/{math.isqrt(self._answer_denomintor)}"
    
    @staticmethod
    def make_random(max_coefficient = 19):
        # Problem description says that 
        #   x^2 + cx + b
        # must evaluate to 0 when x is -1.
        # When x is -1, the x^2 part is 1. So the following must 
        # be true:
        #     1 + c*(-1) + b = 0
        # =>  1 + b = c
        
        found_randomization = False
        while not found_randomization:
            # L'Hôpital's rule implies that derivatives of the 
            # numerator and denominator in the square root can be 
            # used to calculate the limit.
            # Numerator derivative: 1
            # Denominator derivative: 2x + c
            b = random.randint(1, max_coefficient)
            c = b + 1

            # Solve for the denominator
            denominator = c - 2
            
            # Problem description states that the answer must 
            # simplify to 1/a, where a is an integer. Since the 
            # fractional part is in a square root, the denominator 
            # value determined above must be a perfect square > 0 
            # to satisfy requirements.
            if CTGProblem._is_perfect_square(denominator) and denominator > 0:
                return CTGProblem(b, c, denominator)
    
    @staticmethod
    def _eval_as_float(expression):
        # In a more complete version, this method would use a math library 
        # that could evaluate expressions. Since this project has a 
        # limited implementation time and simplified answer scenarios, the 
        # code that follows only checks for a few simple cases.
        
        # Try parsing a float from the expression
        parsed_float = False
        try:
            user_float = float(expression)
            parsed_float = True
        except ValueError:
            parsed_float = False
        
        if parsed_float:
            return user_float
        
        # Next case: The expression has a single '/' character
        if expression.count("/") == 1:
            parts = expression.split("/")
            if (len(parts) != 2 or not CTGProblem._is_int_str(parts[0]) or
                not CTGProblem._is_int_str(parts[1])):
                return math.nan
            return float(parts[0]) / float(parts[1])
        
        return math.nan
    
    @staticmethod
    def _is_int_str(int_str):
        # Remove leading and/or trailing whitespace
        int_str = int_str.strip()
        
        # Special case for empty string
        if len(int_str) == 0:
            return False
        
        i = 0
        if int_str[0] == "-":
            i += 1
        
        # All remaining characters must be digits
        digits = "0123456789"
        while i < len(int_str):
            if int_str[i] not in digits:
                return False
            i += 1
        return True
    
    @staticmethod
    def _is_perfect_square(integer_value):
        if integer_value < 0:
            return False
        int_square_root = math.isqrt(integer_value)
        return int_square_root * int_square_root == integer_value