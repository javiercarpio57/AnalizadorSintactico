

class AnalisiSintactico():
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.currentToken = None
        self.nextToken = self.tokens[self.pos]
        self.next()
        self.lastvalue = None

        self.main()

    def coincidir(self, terminal):
        if self.currentToken == terminal:
            self.next()
        else:
            self.reportar('Error de sintaxis')

    def next(self):
        if self.pos - 1 < 0:
            self.lastvalue = None
        else:
            self.lastvalue = self.tokens[self.pos - 1][1]

        if self.nextToken == None:
            self.currentToken = None
        else:
            self.currentToken = self.nextToken[0]
        self.pos += 1

        if self.pos >= len(self.tokens):
            self.nextToken = None
        else:
            self.nextToken = self.tokens[self.pos]
        

    def reportar(self, msg):
        print(msg)

    def main(self):
        self.Expr()

    def Expr(self):
        while self.currentToken in ['nuevo4', 'number', 'decnumber', 'nuevo7']:
        	if self.currentToken in ['nuevo4', 'number', 'decnumber', 'nuevo7']:
        		self.Stat()
        		if self.currentToken == "nuevo1":
        			self.coincidir("nuevo1")
        	while self.currentToken in ["white"]:
        		self.coincidir("white")
        while self.currentToken in ["white"]:
        	self.coincidir("white")
        if self.currentToken == "nuevo2":
        	self.coincidir("nuevo2")

    def Stat(self):
        value=0
        value = self.Expression(value)
        print(f"Resultado: {value}")

    def Expression(self, result):
        result1=result2=0
        result1 = self.Term(result1)
        while self.currentToken in ['nuevo3', 'nuevo4']:
        	if self.currentToken == "nuevo3":
        		self.coincidir("nuevo3")
        		result2 = self.Term(result2)
        		result1+=result2
        	else:
        		if self.currentToken == "nuevo4":
        			self.coincidir("nuevo4")
        			result2 = self.Term(result2)
        			result1-=result2
        result=result1
        return result

    def Term(self, result):
        result1=result2=0
        result1 = self.Factor(result1)
        while self.currentToken in ['nuevo5', 'nuevo6']:
        	if self.currentToken == "nuevo5":
        		self.coincidir("nuevo5")
        		result2 = self.Factor(result2)
        		result1*=result2
        	else:
        		if self.currentToken == "nuevo6":
        			self.coincidir("nuevo6")
        			result2 = self.Factor(result2)
        			result1/=result2
        result=result1
        return result

    def Factor(self, result):
        sign=1
        if self.currentToken in ['nuevo4']:
        	if self.currentToken == "nuevo4":
        		self.coincidir("nuevo4")
        		sign = -1
        if self.currentToken in ['number', 'decnumber']:
        	result = self.Number(result)
        else:
        	if self.currentToken == "nuevo7":
        		self.coincidir("nuevo7")
        		result = self.Expression(result)
        		if self.currentToken == "nuevo8":
        			self.coincidir("nuevo8")
        result*=sign
        return result

    def Number(self, result):
        if self.currentToken == "number":
        	self.coincidir("number")
        elif self.currentToken == "decnumber":
        	self.coincidir("decnumber")
        result = float(self.lastvalue)
        return result