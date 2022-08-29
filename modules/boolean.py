def truthTable(expression,inputs=2):
  print("Boolean Expression:")
  print("  X = " + expression.upper())
  expression = expression.lower()
  
  #replace Boolean Operators with bitwise operators
  # OR + |, AND * &, NOT ! ~, XOR ^
  expression = expression.replace("*","&")
  expression = expression.replace("+","|")
  expression = expression.replace("!","~")
  
  print("\nTruth Table:")
  if inputs==2:
    print("  -------------")
    print("  | A | B | X |")
    print("  -------------")
    
    for a in range(0,2):
      for b in range(0,2):
        x = eval(expression)
        print("  | " + str(a) + " | " + str(b) + " | " + str(x) + " |" )
        print("  -------------")
        
  elif inputs==3:
    print("  -----------------")
    print("  | A | B | C | X |")
    print("  -----------------")
    
    for a in range(0,2):
      for b in range(0,2):
        for c in range(0,2):
          x = eval(expression)
          print("  | " + str(a) + " | " + str(b) + " | " + str(c) + " | " + str(x) + " |" )
          print("  -----------------")
    
  elif inputs==4:
    print("  ---------------------")
    print("  | A | B | C | D | X |")
    print("  ---------------------")
    
    for a in range(0,2):
      for b in range(0,2):
        for c in range(0,2):
          for d in range(0,2):
            x = eval(expression)
            print("  | " + str(a) + " | " + str(b) + " | " + str(c) + " | " + str(d) + " | " + str(x) + " |" )
            print("  ---------------------")
