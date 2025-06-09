import re

# 定义不同的词法记号（tokens）
TOKEN_SPECIFICATIONS = [
    ('NUMBER', r'\d+'),  # 整数
    ('STRING', r'"([^"]*)"'),  # 双引号中的字符串
    ('IF', r'if'),  # 'if' 关键字
    ('ELIF', r'elif'),  # 'elif' 关键字
    ('THEN', r'then'),  # 'then' 关键字
    ('ELSE', r'else'),  # 'else' 关键字
    ('RESPONSE', r'response'),  # 'response' 关键字
    ('START', r'start'),  # 'start' 关键字
    ('END', r'end'),  # 'end' 关键字
    ('USER_INPUT', r'user_input'),  # 'user_input' 变量
    ('GO', r'go'),  # 'go' 关键字
    ('QUOTE', r'"'),  # 双引号字符
    ('IN', r'in'),  # 'in' 关键字，用于检查是否包含在列表或字符串中
    ('SET', r'set'),  # 'set' 关键字，用于赋值
    ('MODE', r'[A-Z][A-Z]*'),  # 大写字母的单词，作为模式（MODE）
    ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # 标识符（例如：'account'、'payment'）
    ('NEWLINE', r'\n'),  # 换行符
    ('SKIP', r'[ \t]+'),  # 跳过空格和制表符
    ('COMMENT', r'#.*'),  # 注释，单行注释以'#'开头
    ('ASSIGN', r'='),  # 赋值运算符
    ('PLUS', r'\+'),  # 加法运算符
    ('MISMATCH', r'.'),  # 任何其他字符（错误）
]

# 合并所有正则表达式
master_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_SPECIFICATIONS)

class Lexer:
    def __init__(self, code):
        self.code = code
        self.line_number = 1
        self.position = 0
        self.tokens = []

    def tokenize(self):
        line = self.code
        while line:
            match = re.match(master_regex, line)
            if match:
                type_ = match.lastgroup
                value = match.group(type_)

                if type_ == 'NEWLINE':
                    self.line_number += 1
                    self.position = 0
                elif type_ == 'COMMENT':
                    # 忽略注释，不做任何操作，直接跳到下一个
                    line = line[match.end():]
                    continue
                elif type_ == 'STRING':
                    # 如果是字符串，去掉双引号
                    value = value[1:-1]  # 去除双引号
                    self.tokens.append((type_, value))
                elif type_ != 'SKIP':
                    self.tokens.append((type_, value))

                line = line[match.end():]
            else:
                raise ValueError(f'Illegal character at line {self.line_number}, position {self.position}')
        return self.tokens

# 接口方法
def lex_script(code):
    lexer = Lexer(code)
    return lexer.tokenize()