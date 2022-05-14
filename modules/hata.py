import math

def get_a(f, mob, mode):

        if(mode == 1):
            return (1.1 * math.log10(f) - 0.7)*mob - (1.56*math.log10(f) - 0.8)

        if(mode == 2):
            if(f < 200):
                return 8.29(math.pow(math.log10(1.54*mob), 2)) - 1.1
            else:
                return 3.2(math.pow(math.log10(11.75*mob), 2)) - 4.97

        return -1

def get_urban(f, d, base, mob):
    return 69.55 + 26.16 * math.log10(f) - get_a(f, mob, mode) - 13.83 * math.log10(base) + (44.9 - 6.55 * math.log10(base))*math.log10(d)

def get_suburban(f, d, base, mob):
    return get_urban(f, d, base, mob) - 2*math.pow( math.log10( f/28 ) , 2) - 5.4

def get_open(f, d, base, mob):
    return get_urban(f, d, base, mob) - 4.78 * math.pow( math.log10(f) , 2) + 18.33 * math.log10(f) - 40.94
