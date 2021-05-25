class AnalisiSintactico():
    def __init__(self, tokens, noterminales, terminales, firsts):
        self.tokens = tokens
        self.noTerminales = noterminales
        self.terminales = terminales
        self.firsts = firsts
        self.pos = 0
        self.currentToken = None
        self.nextToken = None

    def coincidir(self, terminal):
        if self.currentToken == terminal:
            self.currentToken = self.nextToken
            self.next()
        else:
            self.reportar('Error de sintaxis')

    def next(self):
        self.pos += 1
        self.nextToken = self.tokens[self.pos]

    def reportar(self, msg):
        print(msg)

    def First(self, token):
        if token in self.noTerminales:
            return self.firsts[token]
        elif token in self.terminales:
            return token
        else:
            return []

    def Expr(self):
        while self.currentToken in self.First(self.currentToken):
            self.Stat()
            if self.currentToken == ';':
                self.coincidir(';') # o el token de ;

            while self.currentToken in self.First(self.currentToken):
                self.coincidir('white')

        while self.currentToken in self.First(self.currentToken):
            self.coincidir('white')

        self.coincidir('.') # o el token de .

    def Stat(self):
        print()