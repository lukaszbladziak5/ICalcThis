#Reverse polish notation

ops = {
  "+": (lambda a, b: a + b),
  "-": (lambda a, b: a - b),
  "*": (lambda a, b: a * b),
  "/": (lambda a, b: a / b)
}

def evaluate(expression):
  tokens = expression.split()
  stack = []

  for token in tokens:
    if token in ops:
      arg2 = stack.pop()
      arg1 = stack.pop()
      result = ops[token](arg1, arg2)
      stack.append(result)
    else:
      stack.append(int(token))

  return stack.pop()

#Returns value of RNP equation
#E.g. '1 2 +' returns 3


# Proponuje to, działa z dowolną długością np: "5 6 - 4 * 5 2 2 * - -", wychodzi -5:

#from stack import Stack

def postfix_eval(postfix_expr):  # "2 3 +"
   operand_stack = Stack()

   for token in postfix_expr.split():
     if token in '+-*/':
       b = operand_stack.pop()
       a = operand_stack.pop()
       result = do_math(token, a, b)
       operand_stack.push(result)
     else:
       operand_stack.push(int(token))

   return operand_stack.pop()

def do_math(op, a, b):
   if op == "*":
     return a * b
   elif op == "/":
     return a // b
   elif op == "+":
     return a + b
   else:
     return a - b
