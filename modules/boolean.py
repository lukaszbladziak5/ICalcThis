def truthTable(expression,inputs=2):
  result = ""
  #print("Boolean Expression:")
  #print("  X = " + expression.upper())
  expression = expression.lower()
  
  #replace Boolean Operators with bitwise operators
  # OR + |, AND * &, NOT ! ~, XOR ^
  expression = expression.replace("*","&")
  expression = expression.replace("+","|")
  expression = expression.replace("!","~")
  
  #print("\nTruth Table:")
  if inputs==2:
    #print("  -------------")
    #print("  | A | B | X |")
    #print("  -------------")
    result += "  -------------\n"
    result += "  | A | B | X |\n"
    result += "  -------------\n"
    for a in range(0,2):
      for b in range(0,2):
        x = eval(expression)
        #print("  | " + str(a) + " | " + str(b) + " | " + str(x) + " |" )
        #print("  -------------")
        result += "  | " + str(a) + " | " + str(b) + " | " + str(x) + " |\n"
        result += "  -------------\n"
        
  elif inputs==3:
    #print("  -----------------")
    #print("  | A | B | C | X |")
    #print("  -----------------")
    result += "  -----------------\n"
    result += "  | A | B | C | X |\n"
    result += "  -----------------\n"
    
    for a in range(0,2):
      for b in range(0,2):
        for c in range(0,2):
          x = eval(expression)
          #print("  | " + str(a) + " | " + str(b) + " | " + str(c) + " | " + str(x) + " |" )
          #print("  -----------------")
          result += "  | " + str(a) + " | " + str(b) + " | " + str(c) + " | " + str(x) + " |\n"
          result += "  -----------------\n"
    
  elif inputs==4:
    #print("  ---------------------")
    #print("  | A | B | C | D | X |")
    #print("  ---------------------")
    result += "  ---------------------\n"
    result += "  | A | B | C | D | X |\n"
    result += "  ---------------------\n"
    
    for a in range(0,2):
      for b in range(0,2):
        for c in range(0,2):
          for d in range(0,2):
            x = eval(expression)
            #print("  | " + str(a) + " | " + str(b) + " | " + str(c) + " | " + str(d) + " | " + str(x) + " |" )
            #print("  ---------------------")
            result += "  | " + str(a) + " | " + str(b) + " | " + str(c) + " | " + str(d) + " | " + str(x) + " |\n" 
            result += "  ---------------------\n"
  return result

