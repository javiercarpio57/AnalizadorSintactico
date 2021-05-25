

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
        self.IdentList()

    def IdentList(self):
        if self.currentToken == "ident":
        	self.coincidir("ident")
        	n = 1
        	print(f"Ident found: {self.lastvalue}")
        	while self.currentToken in ['nuevo1']:
        		if self.currentToken == "nuevo1":
        			self.coincidir("nuevo1")
        			if self.currentToken == "ident":
        				self.coincidir("ident")
        				n += 1
        				print(f"Ident found: {self.lastvalue}")
        	print(f"Hay {n} elementos en la lista.")