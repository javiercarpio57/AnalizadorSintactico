import functools
epsilon = 'ε'

class Token():
    def __init__(self, attr, value):
        self.Atributo = attr
        self.Valor = value


class SyntaxTree():
    def __init__(self, regular_expression, firsts):
        
        self.firsts = firsts
        self.tabs = 0
        self.last_operation = None
        self.simbolos = []
        
        self.nodos = []
        self.root = None
        self.id = 0

        self.follow_pos = {}
        regular_expression = self.concatenation(regular_expression)

        for r in regular_expression:
            print('\t->', r.Atributo, r.Valor)
        self.evaluate(regular_expression)

    def calculate_first(self, ident):
        if ident in self.firsts.keys():
            return self.firsts[ident]
        else:
            return [ident]

    def get_first(self, left, right, operator):
        if operator == 'concat':
            if left.Atributo == 'ident':
                return self.calculate_first(left.Valor)
            elif right.Atributo == 'ident':
                return self.calculate_first(right.Valor)
            else:
                return []
        elif operator == 'union':
            return self.calculate_first(left.Valor) + self.calculate_first(right.Valor)

    # Agrega los operadores concatenacion
    def concatenation(self, expresion):
        new = []
        operators = ['{', '|','(', '[', '}', ']', ')']
        cont = 0

        for cont in range(len(expresion)):
            if cont + 1 >= len(expresion):
                new.append(expresion[-1])
                break

            new.append(expresion[cont])

            if expresion[cont].Valor == '}' and expresion[cont + 1].Valor in '({[]}':
                new.append(Token('concat', '.'))
            elif expresion[cont].Valor not in operators and expresion[cont+1].Valor not in operators:
                new.append(Token('concat', '.'))
            elif expresion[cont].Valor not in operators and expresion[cont+1].Valor in '([':
                new.append(Token('concat', '.'))
            elif expresion[cont].Valor == ')' and expresion[cont+1].Valor not in operators:
                new.append(Token('concat', '.'))
        return new

    # Obtiene el ultimo elemento guardado en el stack
    def peek(self, stack):
        return stack[-1] if stack else None

    # Determina si el token es un simbolo
    def is_symbol(self, s):
        tokens = ['ident', 'attr', 's_action', 'string', 'white']
        if s.Atributo in tokens:
            return True
        return False

    # Obtiene el ID del nodo
    def get_id(self):
        self.id += 1
        return self.id

    # Implementacion de la creacion del arbol sintactico
    def apply_operator(self, operators, values):
        operator = operators.pop()

        if len(values) == 1 and operator.Atributo == 'br_close':
            right = ([], [])
        else:
            right = values.pop()

        if len(values) == 0:
            left = ([], [])
        else:
            left = values.pop()
        
        if operator.Atributo == 'union': return self.operator_or(left, right)
        elif operator.Atributo == 'concat': return self.operator_concat(left, right)
        elif operator.Atributo == 'br_open': return self.operator_kleene(left, right)
        elif operator.Atributo == 'br_close': return self.operator_kleene_close(left, right)
        elif operator.Atributo == 'sq_open': return self.operator_square(left, right)
        elif operator.Atributo == 'sq_close': return self.operator_square_close(left, right)

    # Operacion square
    def operator_square(self, left, right):
        operator = 'square'
        print(operator)
        first = root = []

        if isinstance(left, tuple):
            root = left[0]
        else:
            self.tabs -= 1
            if left.Atributo == 's_action':
                root = ['\t' * self.tabs + left.Valor[2:-2]]
            elif left.Atributo == 'ident' and left.Valor in self.firsts.keys():
                root = ['\t' * self.tabs + 'if self.currentToken in ' + repr(self.firsts[left.Valor]) + ':']
                root += ['\t' * self.tabs + '\tself.' + left.Valor + '()']
                self.tabs += 1
            elif left.Atributo == 'ident' and left.Valor not in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken == "' + left.Valor + '":']
                root += ['\t' * self.tabs + '\tself.coincidir("' + left.Valor + '")']
            # self.tabs += 1

        if isinstance(right, tuple):
            self.tabs -= 1
            root += ['\t' * self.tabs + 'if self.currentToken in ' + repr(right[1]) + ':'] + ['\t' + i for i in right[0]]
            # self.tabs += 1
        else:
            root += ['\t' * self.tabs + 'if self.currentToken in ["' + right.Valor + '"]:'] + ['\t' * self.tabs + '\tself.coincidir("' + right.Valor + '")']
        return (root, first)

    # Operacion square close
    def operator_square_close(self, left, right):
        operator = 'square close'
        print(operator)
        first = []
        self.tabs -= 1

        # RIGHT
        if isinstance(right, tuple):
            root = left[0] + right[0]
        else:
            root = left[0]
            if right.Atributo == 's_action':
                root += ['\t' * self.tabs + right.Valor[2:-2]]
            elif right.Atributo == 'ident' and right.Valor in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken in ' + repr(self.firsts[right.Valor])]
                root += ['\t' * self.tabs +  '\tself.' + right.Valor + '()']
            elif right.Atributo == 'ident' and right.Valor not in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken == "' + right.Valor + '":']
                root += ['\t' * self.tabs + '\tself.coincidir("' + right.Valor + '")']

        return (root, first)

    # Operacion kleene
    def operator_kleene(self, left, right):
        operator = 'kleene'
        print(operator)
        first = []
        root = []

        if isinstance(left, tuple):
            root = left[0]
        else:
            self.tabs -= 1
            if left.Atributo == 's_action':
                root = ['\t' * self.tabs + left.Valor[2:-2]]
            elif left.Atributo == 'ident' and left.Valor in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken in ' + repr(self.firsts[left.Valor]) + ':']
                root = ['\t' * self.tabs + '\tself.' + left.Valor + '()']
                self.tabs += 1
            elif left.Atributo == 'ident' and left.Valor not in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken == "' + left.Valor + '":']
                root += ['\t' * self.tabs + '\tself.coincidir("' + left.Valor + '")']
            self.tabs += 1

        if isinstance(right, tuple):
            self.tabs -= 2
            root += ['\t' * self.tabs + 'while self.currentToken in ' + repr(right[1]) + ':'] + ['\t' + i for i in right[0]]
            self.tabs += 1
        else:
            root += ['\t' * self.tabs + 'while self.currentToken in ["' + right.Valor + '"]:'] + ['\t' * self.tabs + '\tself.coincidir("' + right.Valor + '")']
        return (root, first)

    # Operacion kleene close
    def operator_kleene_close(self, left, right):
        operator = 'kleene close'
        print(operator)
        first = []
        self.tabs -= 1

        # RIGHT
        if isinstance(right, tuple):
            root = left[0] + right[0]
        else:
            root = left[0]
            if right.Atributo == 's_action':
                root += ['\t' * self.tabs + right.Valor[2:-2]]
            elif right.Atributo == 'ident' and right.Valor in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken in ' + repr(self.firsts[right.Valor])]
                root += ['\t' * self.tabs +  '\tself.' + right.Valor + '()']
            elif right.Atributo == 'ident' and right.Valor not in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken == "' + right.Valor + '":']
                root += ['\t' * self.tabs + '\tself.coincidir("' + right.Valor + '")']

        return (root, first)

    # Operacion OR
    def operator_or(self, left, right):
        operator = 'union'
        print(operator)
        
        if isinstance(left, tuple) and isinstance(right, tuple):
            self.tabs -= 1
            root = left[0] + ['else:'] + right[0]
            self.tabs -= 1
            return (root, left[1] + right[1])

        elif not isinstance(left, tuple) and not isinstance(right, tuple):
            root = []
            first = self.get_first(left, right, operator)

            # LEFT
            if left.Atributo == 'ident' and left.Valor in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken in ' + repr(self.firsts[left.Valor])]
                root += ['\t' * self.tabs +  '\tself.' + right.Valor + '()']
            elif left.Atributo == 'ident' and left.Valor not in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken == "' + left.Valor + '":']
                root += ['\t' * self.tabs + '\tself.coincidir("' + left.Valor + '")']

            # RIGHT
            if right.Atributo == 'ident' and right.Valor in self.firsts.keys():
                root += ['\t' * self.tabs + 'elif self.currentToken in ' + repr(self.firsts[right.Valor])]
                root += ['\t' * self.tabs +  '\tself.' + right.Valor + '()']
            elif right.Atributo == 'ident' and right.Valor not in self.firsts.keys():
                root += ['\t' * self.tabs + 'elif self.currentToken == "' + right.Valor + '":']
                root += ['\t' * self.tabs + '\tself.coincidir("' + right.Valor + '")']
                        
            self.tabs -= 1
            return (root, first)

        elif isinstance(left, tuple) and not isinstance(right, tuple):
            root = left[0] + ['else:']
            first = left[1]

            # RIGHT
            if right.Atributo == 'ident' and right.Valor in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken in ' + repr(self.firsts[right.Valor])]
                root += ['\t' * self.tabs +  '\tself.' + right.Valor + '()']
                first += self.firsts[right.Valor]
            elif right.Atributo == 'ident' and right.Valor not in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken == "' + right.Valor + '":']
                root += ['\t' * self.tabs + '\tself.coincidir("' + right.Valor + '")']
                first += [right.Valor]

            self.tabs -= 1
            return (root, first)

        elif not isinstance(left, tuple) and isinstance(right, tuple):
            root = []
            first = right[1]
            self.tabs -= 1

            # LEFT
            if left.Atributo == 'ident' and left.Valor in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken in ' + repr(self.firsts[left.Valor])]
                root += ['\t' * self.tabs +  '\tself.' + right.Valor + '()']
                first += self.firsts[left.Valor]
            elif left.Atributo == 'ident' and left.Valor not in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken == "' + left.Valor + '":']
                root += ['\t' * self.tabs + '\tself.coincidir("' + left.Valor + '")']
                first += [left.Valor]

            root += ['else:'] + ['\t' + r for r in right[0]]

            self.tabs -= 1
            return (root, first)

    # Operacion concatenacion
    def operator_concat(self, left, right):
        operator = 'concat'
        print(operator)
        first = []
        if isinstance(left, tuple) and isinstance(right, tuple):
            root = left[0] + right[0]
            first = left[1]
            return (root, first)

        elif not isinstance(left, tuple) and not isinstance(right, tuple):
            root = []

            first = self.get_first(left, right, operator)
            # LEFT
            if left.Atributo == 's_action':
                root += ['\t' * self.tabs + left.Valor[2:-2]]
            elif left.Atributo == 'ident' and left.Valor in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken in ' + repr(self.firsts[left.Valor]) + ':']
                root += ['\t' * self.tabs + '\tself.' + left.Valor + '()']
                self.tabs += 1
            elif left.Atributo == 'ident' and left.Valor not in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken == "' + left.Valor + '":']
                root += ['\t' * self.tabs + '\tself.coincidir("' + left.Valor + '")']
                self.tabs += 1
            # elif left.Atributo == 'attr':
            #     root[-1] = root[-1][:-2] + '(' + left.Valor[1:-1] + ')'

            # RIGHT
            if right.Atributo == 's_action':
                root += ['\t' * self.tabs + right.Valor[2:-2]]
            elif right.Atributo == 'ident' and right.Valor in self.firsts.keys():
                root += ['\t' * self.tabs + 'self.' + right.Valor + '()']
            elif right.Atributo == 'ident' and right.Valor not in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken == "' + right.Valor + '":']
                root += ['\t' * self.tabs + '\tself.coincidir("' + right.Valor + '")']
                self.tabs += 1
            elif right.Atributo == 'attr':
                x = root[-1][:-2].rfind('\t')
                root[-1] = root[-1][:-2][:x + 1] + right.Valor[1:-1] + ' = ' + root[-1][:-2][x + 1:] + '(' + right.Valor[1:-1] + ')'

            return (root, first)

        elif isinstance(left, tuple) and not isinstance(right, tuple):
            root = left[0]
            first = left[1]

            # RIGHT
            if right.Atributo == 's_action':
                root += ['\t' * self.tabs + right.Valor[2:-2]]
            elif right.Atributo == 'ident' and right.Valor in self.firsts.keys():
                root += ['\t' * self.tabs + 'self.' + right.Valor + '()']
            elif right.Atributo == 'ident' and right.Valor not in self.firsts.keys():
                root += ['\t' * self.tabs + 'if self.currentToken == "' + right.Valor + '":']
                root += ['\t' * self.tabs + '\tself.coincidir("' + right.Valor + '")']
                self.tabs += 1
            elif right.Atributo == 'attr':
                x = root[-1][:-2].rfind('\t')
                root[-1] = root[-1][:-2][:x + 1] + right.Valor[1:-1] + ' = ' + root[-1][:-2][x + 1:] + '(' + right.Valor[1:-1] + ')'
                # root[-1] = right.Valor[1:-1] + ' = ' + root[-1][:-2] + '(' + right.Valor[1:-1] + ')'
            return (root, first)
        
        elif not isinstance(left, tuple) and isinstance(right, tuple):
            root = right[0]

            # LEFT
            if left.Atributo == 's_action':
                root = ['\t' * self.tabs + left.Valor[2:-2]] + root
                first = right[1]
            elif left.Atributo == 'ident' and left.Valor in self.firsts.keys():
                root = ['\t' * self.tabs + 'if self.currentToken in ' + repr(self.firsts[left.Valor]) + ':']
                root += ['\t' * self.tabs + '\tself.' + left.Valor + '()'] + right[0]
                self.tabs += 1
                first = self.calculate_first(left.Valor)
            elif left.Atributo == 'ident' and left.Valor not in self.firsts.keys():
                root = ['\t' * self.tabs + 'if self.currentToken == "' + left.Valor + '":'] + root
                root = ['\t' * self.tabs + '\tself.coincidir("' + left.Valor + '")'] + root
                self.tabs += 1
            # elif left.Atributo == 'attr':
            #     root = root[:-2] + '(' + left.Valor[1:-1] + ')'
            return (root, first)

    # Obtiene la precedencia entre dos operadores
    def greater_precedence(self, op1, op2):
        precedences = {
            'union' : 2,
            'concat' : 3,
            'br_open' : 1,
            'br_close': 0,
            'sq_open' : 1,
            'sq_close': 0
        }
        return precedences[op1] >= precedences[op2]
    
    # Implementacion de la creacion del arbol sintactico
    def evaluate(self, expression):
        values = []
        operators = []
        # raiz = None
        for token in expression:
            # print(raiz)
            if self.is_symbol(token):
                values.append(token)

            elif token.Atributo == 'p_open':
                operators.append(token)

            elif token.Atributo == 'p_close':
                top = self.peek(operators)

                while top is not None and top.Atributo != 'p_open':
                    raiz = self.apply_operator(operators, values)
                    values.append(raiz)
                    top = self.peek(operators)
                operators.pop()
                self.tabs -= 1

            else:
                top = self.peek(operators)

                while top is not None and top.Atributo not in ['p_open', 'p_close'] and self.greater_precedence(top.Atributo, token.Atributo):
                    raiz = self.apply_operator(operators, values)
                    values.append(raiz)
                    top = self.peek(operators)
                operators.append(token)

        while self.peek(operators) is not None:
            raiz = self.apply_operator(operators, values)
            values.append(raiz)

        self.root = values.pop()
        print(self.root, '\n')


# expr = [
#     ('br_open', '{')
#     , ('ident', 'Stat')
#     , ('ident', 'nuevo1')
#     , ('br_open', '{'), ('ident', 'white'), ('br_close', '}')
#     , ('br_close', '}')
#     , ('br_open', '{'), ('ident', 'white'), ('br_close', '}')
#     , ('ident', 'nuevo2')
# ]

# stat = [('s_action', '(.value=0.)'), ('ident', 'Expression'), ('attr', '<value>'), ('s_action', '(.print(f"Resultado: {value}").)')]

# expression = [
#     ('s_action', '(.result1=result2=0.)'), ('ident', 'Term')
#     , ('attr', '<result1>')
#     , ('br_open', '{')
#     ,('ident', 'nuevo3')
#     , ('ident', 'Term'), ('attr', '<result2>'), ('s_action', '(.result1+=result2.)')
#     , ('union', '|')
#     , ('ident', 'nuevo4')
#     , ('ident', 'Term'), ('attr', '<result2>'), ('s_action', '(.result1-=result2.)')
#     , ('br_close', '}')
#     , ('s_action', '(.result=result1.)')
# ]

# term = [
#     ('s_action', '(.result1=result2=0.)'), ('ident', 'Factor'), ('attr', '<result1>')
#     , ('br_open', '{'), ('ident', 'nuevo5'), ('ident', 'Factor'), ('attr', '<result2>'), ('s_action', '(.result1*=result2.)')
#     , ('union', '|')
#     , ('ident', 'nuevo6'), ('ident', 'Factor'), ('attr', '<result2>'), ('s_action', '(.result1/=result2.)')
#     , ('br_close', '}')
#     , ('s_action', '(.result=result1.)')
# ]

# factor = [
#     ('s_action', '(.sign=1.)')
#     , ('sq_open', '['), ('ident', 'nuevo4'), ('s_action', '(.sign = -1.)')
#     , ('sq_close', ']')
#     , ('p_open', '(')
#     , ('ident', 'Number'), ('attr', '<result>')
#     , ('union', '|')
#     , ('ident', 'nuevo7'), ('ident', 'Expression'), ('attr', '<result>'), ('ident', 'nuevo8')
#     , ('p_close', ')')
#     , ('s_action', '(.result*=sign.)')
# ]

# number = [
#     ('p_open', '(')
#     , ('ident', 'number')
#     , ('union', '|')
#     , ('ident', 'decnumber')
#     , ('p_close', ')')
#     , ('s_action', '(.result = float(lastValue).)')
# ]

# {';': 'nuevo1', '.': 'nuevo2', '+': 'nuevo3', '-': 'nuevo4', '*': 'nuevo5', '/': 'nuevo6', '(': 'nuevo7', ')': 'nuevo8'}
# my_tokens = []
# for i in expr:
#     t = Token(i[0], i[1])
#     my_tokens.append(t)

# firsts = {
#     'Number': ['number', 'decnumber'],
#     'Factor': ['nuevo4', 'number', 'decnumber'],
#     'Term': ['nuevo4', 'number', 'decnumber'],
#     'Expression': ['nuevo4', 'number', 'decnumber'],
#     'Stat': ['nuevo4', 'number', 'decnumber']
# }
# lexico = SyntaxTree(my_tokens, firsts)