class Customer:
    def __init__(self,firstName,lastName,cardID):
        self.firstName = firstName
        self.lastName = lastName
        self.cardID = cardID
    
    @property
    def GetFullName(self):
        return '{} {}'.format(self.firstName, self.lastName)
    
    @property
    def GetCardID(self):
        return '{}'.format(self.cardID)
    
    def __repr__(self):
        return "Customer('{}','{}','{}')".format(self.firstName,self.lastName,self.cardID)
        
    
    