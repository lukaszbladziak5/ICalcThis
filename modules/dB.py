import math

def ratioTodB(P1, P2): return 10*math.log10(P1/P2) #dB
def lossTodB(P):
    if(P > 1): raise ValueError("dB calculator: loss cannot be bigger than 1.0")
    return 10*math.log(P) #dB
def voltageTodB(V1, V2): return 20*math.log10(V1/V2) #dB
def WTodBm(P): return 10*math.log10(P/1) #dBW (can be used for mW and uW - same formula, change unit)
def dBWTodBm(dBW): return dBW + 30 #dBm
def dBmTodBW(dBm): return dBm - 30 #dBW
def dBToRatio(dB): return 10**(dB/10) #Ratio
def dBWToW(dBW): return 10**(dBW/10) #W
def dBmToW(dBm): return 10**(dBm/10) / 1000 #W