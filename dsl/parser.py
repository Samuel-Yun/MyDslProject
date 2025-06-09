import re
from dsl.lexer import Lexer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # 存储所有的tokens（词法单元）
        self.position = 0  # 当前token的位置
        self.token = None  # 当前token
        self.advance()  # 读取下一个token
        self.modes = set()  # 用于跟踪已定义的模式
        self.found_init = False  # 用于标记是否已经找到INIT模式

    def advance(self):
        """ 移动到下一个token """
        if self.position < len(self.tokens):
            self.token = self.tokens[self.position]  # 获取当前token
            self.position += 1    # 移动到下一个token
        else:
            self.token = None  # 如果已经到达tokens末尾，设置token为None

    def parse(self):
        """ 解析整个脚本，从顶层开始 """
        return self.program()

    def program(self):
        """ 解析整个程序，程序以 'start' 开头并以 'end' 结束 """
        statements = []   # 用于存储解析出的语句

        # 期望在开始处出现 'start' token
        if self.token[0] == 'START':
            self.advance()  # 跳过 'start' token

            while self.token and self.token[0] != 'END':  # 直到遇到 'end' token
                statement = self.statement()  # 解析单个语句
                statements.append(statement)  # 将解析出来的语句添加到列表

                # 如果是条件语句（if/elif/else），将其后续语句（go/set）也作为一部分加入
                if statement['type'] in ['if', 'elif', 'else']:
                    statements[-1]['next_statements'] = statement.pop('next_statements')

            # 期望最后是 'end' token
            if self.token[0] == 'END':
                self.advance()
            else:
                raise SyntaxError("Expected 'end' but got {}".format(self.token))

            # 确保脚本中包含 INIT 模式
            self.check_init_mode()

        return {'type': 'program', 'statements': statements}

    def statement(self):
        """ 解析单个语句 """
        if self.token[0] == 'IF':
            return self.if_statement()
        elif self.token[0] == 'ELIF':
            return self.elif_statement()
        elif self.token[0] == 'ELSE':
            return self.else_statement()
        elif self.token[0] == 'RESPONSE':
            return self.response_statement()
        elif self.token[0] == 'GO':
            return self.go_statement()
        elif self.token[0] == 'SET':
            return self.set_statement()
        elif self.token[0] == 'MODE':
            return self.mode_statement()
        else:
            raise SyntaxError("Unexpected token: {}".format(self.token))

    def if_statement(self):
        """ Parse an 'if' statement: if <condition> then response <message> """
        self.advance()  # Move past 'if'
        condition = self.condition()

        if self.token[0] == 'THEN':
            self.advance()  # Move past 'then'
        else:
            raise SyntaxError("Expected 'then' but got {}".format(self.token))

        if self.token[0] == 'RESPONSE':
            self.advance()  # Move past 'response'
            response_message = self.response_message()
        else:
            raise SyntaxError("Expected 'response' but got {}".format(self.token))

        # 解析接下来的 go 和 set 语句
        next_statements = []
        while self.token and self.token[0] in ['GO', 'SET']:
            if self.token[0] == 'GO':
                next_statements.append(self.go_statement())
            elif self.token[0] == 'SET':
                next_statements.append(self.set_statement())

        return {
            'type': 'if',
            'condition': condition,
            'response': response_message,
            'next_statements': next_statements  # 包含接下来的 go 和 set 语句
        }

    def elif_statement(self):
        """ Parse an 'elif' statement: elif <condition> then response <message> """
        self.advance()  # Move past 'elif'
        condition = self.condition()

        if self.token[0] == 'THEN':
            self.advance()  # Move past 'then'
        else:
            raise SyntaxError("Expected 'then' but got {}".format(self.token))

        if self.token[0] == 'RESPONSE':
            self.advance()  # Move past 'response'
            response_message = self.response_message()
        else:
            raise SyntaxError("Expected 'response' but got {}".format(self.token))

        # 解析接下来的 go 和 set 语句
        next_statements = []
        while self.token and self.token[0] in ['GO', 'SET']:
            if self.token[0] == 'GO':
                next_statements.append(self.go_statement())
            elif self.token[0] == 'SET':
                next_statements.append(self.set_statement())

        return {
            'type': 'elif',
            'condition': condition,
            'response': response_message,
            'next_statements': next_statements  # 包含接下来的 go 和 set 语句
        }

    def else_statement(self):
        """ Parse an 'else' statement: else response <message> """
        self.advance()  # Move past 'else'

        if self.token[0] == 'RESPONSE':
            self.advance()  # Move past 'response'
            response_message = self.response_message()
        else:
            raise SyntaxError("Expected 'response' but got {}".format(self.token))

        # 解析接下来的 go 和 set 语句
        next_statements = []
        while self.token and self.token[0] in ['GO', 'SET']:
            if self.token[0] == 'GO':
                next_statements.append(self.go_statement())
            elif self.token[0] == 'SET':
                next_statements.append(self.set_statement())

        return {
            'type': 'else',
            'response': response_message,
            'next_statements': next_statements  # 包含接下来的 go 和 set 语句
        }

    def response_statement(self):
        """ Parse a 'response' statement """
        self.advance()  # Move past 'response'
        message = self.response_message()
        return {
            'type': 'response',
            'message': message
        }

    def go_statement(self):
        """ Parse a 'go' statement """
        self.advance()  # Move past 'go'
        mode = self.token[1]  # Mode could be any string (like 'ACCOUNT', 'GOODS', etc.)
        self.advance()  # Move past the mode
        return {
            'type': 'go',
            'mode': mode
        }

    def set_statement(self):
        """ Parse a 'set' statement: set <variable> = <expression> """
        self.advance()  # Move past 'set'
        variable = self.token[1]  # Variable name (e.g., balance)
        self.advance()  # Move past variable

        if self.token[0] == 'ASSIGN':
            self.advance()  # Move past '='
            expression = self.expression()
        else:
            raise SyntaxError("Expected '=' after variable but got {}".format(self.token))

        return {
            'type': 'set',
            'variable': variable,
            'expression': expression
        }

    def expression(self):
        """ Parse an expression (currently supports addition) """
        if self.token[0] == 'ID':
            left = self.token[1]  # Get the variable name
            self.advance()  # Move past the variable

            if self.token[0] == 'PLUS':
                self.advance()  # Move past '+'
                right = self.token[1]  # The right operand can also be an ID (another variable or number)
                self.advance()
                return {'type': 'addition', 'left': left, 'right': right}
            return {'type': 'variable', 'name': left}

        elif self.token[0] == 'NUMBER':
            left = self.token[1]  # Get the number
            self.advance()

            if self.token[0] == 'PLUS':
                self.advance()  # Move past '+'
                right = self.token[1]  # The right operand can also be a number or ID
                self.advance()
                return {'type': 'addition', 'left': left, 'right': right}

            return {'type': 'number', 'value': left}
        else:
            raise SyntaxError("Expected a number or identifier but got {}".format(self.token))

    def mode_statement(self):
        """ Parse a mode definition (like 'INIT', 'ACCOUNT', 'GOODS', etc.) """
        mode = self.token[1]  # Mode is a string, not a keyword
        self.advance()  # Move past the mode

        # Check for duplicate mode
        if mode in self.modes:
            raise SyntaxError(f"Duplicate mode '{mode}' detected.")
        self.modes.add(mode)

        if mode == 'INIT':
            self.found_init = True

        return {
            'type': 'mode',
            'mode': mode
        }

    def condition(self):
        """ Parse a condition: <string> in user_input """
        conditions = []

        # Parse the first condition
        self.parse_condition_part(conditions)

        return conditions

    def parse_condition_part(self, conditions):
        """ Parse individual condition parts: string 'in' user_input """
        if self.token[0] == 'STRING':
            string = self.token[1]  # Get the string part of the condition
            self.advance()  # Move past the string

            if self.token[0] == 'IN':
                self.advance()  # Move past 'in'

                if self.token[0] == 'USER_INPUT':
                    conditions.append(string)
                    self.advance()  # Move past 'user_input'
                else:
                    raise SyntaxError("Expected 'user_input' but got {}".format(self.token))
            else:
                raise SyntaxError("Expected 'in' but got {}".format(self.token))
        else:
            raise SyntaxError("Expected string condition but got {}".format(self.token))

    def response_message(self):
        """ Parse the message in the response statement """
        message = self.token[1]  # 获取信息
        self.advance()  # Move past the message
        return message

    def check_init_mode(self):
        """ 确保初始模块在文本中 """
        if not self.found_init:
            raise SyntaxError("Missing 'INIT' mode in the script.")

# 接口方法
def parse_script(tokens):
    parser = Parser(tokens)
    return parser.parse()