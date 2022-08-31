class Codes:
    #All values are doubled
    #                1       0       1
    #   1|       ____            ____
    #    |  INIT |   |           |   |
    #RZ 0|--------   ------------    ------
    #    |           
    #  -1|           
    #                   INIT 1   0   1
    #is represented by [0,0,1,0,0,0,1,1]
    #
    def __init__(self):
        self.NRZ = [0,0]
        self.RZ = [0,0]
        self.Manchaster = [0,1]
        self.DiffManchaster = [0,1]

    def add(self, value):
        if(value != 1 & value != 0): raise("Invalid bit value")
        length = len(self.NRZ)
        #NRZ
        if(value == 1):
            self.NRZ.append(1)
            self.NRZ.append(1)
        else:
            self.RZ.append(-1)
            self.RZ.append(-1)
        #RZ
        if(value == 1):self.RZ.append(1)
        else: self.RZ.append(-1)
        self.RZ.append(0)
        #Manchaster
        if(value == 1):
            self.Manchaster.append(1)
            self.Manchaster.append(0)
        else:
            self.Manchaster.append(0)
            self.Manchaster.append(1)
        #Differential Manchaster
        if(value == 0):
            self.DiffManchaster.append( self.DiffManchaster[length - 2] )
            self.DiffManchaster.append( self.DiffManchaster[length - 1] )
        else:
            if(self.DiffManchaster[length - 2] == 1):
                self.DiffManchaster.append(0)
                self.DiffManchaster.append(1)
            else:
                self.DiffManchaster.append(1)
                self.DiffManchaster.append(0)
        


#code = Codes()
#code.add(1)
#code.add(1)
#code.add(0)
#print(code.DiffManchaster)