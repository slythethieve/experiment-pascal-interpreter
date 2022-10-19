# Token types
# EOF stands for (end-of-file) => nothing more to analyse
INTEGER, PLUS, MINUS, EOF, TIMES, DIVIDE = 'INTEGER', 'PLUS', 'MINUS', 'EOF', 'TIMES', 'DIVIDE'

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self): 
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            # if the token is a digit we run the integer 
            # function to check if is multi-digit
            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            if self.current_char == '*':
                self.advance()
                return Token(TIMES, '*')
            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')
            
            self.error()
        return Token(EOF, None)

class Interpreter(object):
    def __init__(self, lexer):

        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')
    
    
    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        # factor: INTEGER
        token = self.current_token
        self.eat(INTEGER)
        return token.value
    
    def term(self):
        # term: factor ((TIMES | DIVIDE) factor)
        result = self.factor()

        while self.current_token.type in (TIMES, DIVIDE):
            token = self.current_token
            if token.type == TIMES:
                self.eat(TIMES)
                result = result * self.factor()
            elif token.type == DIVIDE:
                self.eat(DIVIDE)
                result = result / self.factor()

        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        lexer = Lexer(text)
        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()