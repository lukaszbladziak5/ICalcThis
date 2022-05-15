from numpy import source

#Value should be string if sourceBase is not decimal
#Conversion like BIN->HEX requires BIN->DEC->HEX
def exec(value, sourceBase = 10, targetBase = 2):
    if( targetBase != 10 and not(isinstance(value, int))):
         raise ValueError("Binary calculator: value is not valid integer")
    if(targetBase==2): return str(bin(value))[2:]
    if(targetBase==8): return str(oct(value))[2:]
    if(targetBase==10): return int(value, sourceBase)
    if(targetBase==16): return str(hex(value))[2:]

def decToZM(value, bitLength):
    if(not(isinstance(value, int))):
         raise ValueError("Binary calculator: value is not valid integer")
    sign = '0'
    if(value < 0): sign = "1"
    value = exec(abs(value))
    if(1 + len(value) != bitLength):
        for i in range(1, bitLength - len(value)): sign += '0'
    return sign + value

def decToU1(value, bitLength):
    if(not(isinstance(value, int))):
         raise ValueError("Binary calculator: value is not valid integer")
    #TD
    return -1

def decToU2(value, bitLength):
    if(not(isinstance(value, int))):
         raise ValueError("Binary calculator: value is not valid integer")
    if(value == 0):
        result = ''
        for i in range(0, bitLength): result += '0'
        return result
    if(value > 0):
        value = exec(value)
        sign = '0'
        if(1 + len(value) == bitLength): return sign + value
        else:
            result = ''
            result += sign
            for i in range(1, bitLength - len(value)): result += '0'
            result += value
            return result
    #Subzero
    return str(bin(value & (2**bitLength - 1)))[2:]