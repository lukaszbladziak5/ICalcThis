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
