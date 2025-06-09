import unittest
from dsl.lexer import Lexer

class TestLexer(unittest.TestCase):

    # 测试数字的词法分析
    def test_tokenize_number(self):
        code = '123'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # 验证数字 "123" 被正确识别为 NUMBER 类型
        self.assertEqual([('NUMBER', '123')], tokens)

    # 测试字符串的词法分析
    def test_tokenize_string(self):
        code = '"hello world"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # 验证字符串 "hello world" 被正确识别为 STRING 类型
        self.assertEqual([('STRING', 'hello world')], tokens)

    # 测试 if 关键字的词法分析
    def test_tokenize_if(self):
        code = 'if'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # 验证 "if" 被正确识别为 IF 类型
        self.assertEqual([('IF', 'if')], tokens)

    # 测试 elif 关键字的词法分析
    def test_tokenize_elif(self):
        code = 'elif'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # 验证 "elif" 被正确识别为 ELIF 类型
        self.assertEqual([('ELIF', 'elif')], tokens)

    # 测试 response 关键字的词法分析
    def test_tokenize_keyword_response(self):
        code = 'response'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # 验证 "response" 被正确识别为 RESPONSE 类型
        self.assertEqual([('RESPONSE', 'response')], tokens)

    # 测试赋值语句的词法分析
    def test_tokenize_assignment(self):
        code = 'set x = 10'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # 验证赋值语句 "set x = 10" 被正确识别为 SET、ID、ASSIGN 和 NUMBER 类型
        self.assertEqual([('SET', 'set'), ('ID', 'x'), ('ASSIGN', '='), ('NUMBER', '10')], tokens)

    # 测试 go 模式的词法分析
    def test_tokenize_go_mode(self):
        code = 'go INIT'  # 以数字开头的标识符是非法的
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # 验证 "go INIT" 被正确识别为 GO 和 MODE 类型
        self.assertEqual([('GO', 'go'), ('MODE', 'INIT')], tokens)

    # 测试多种不同 token 的词法分析
    def test_tokenize_multiple_tokens(self):
        code = 'if x in user_input then response "hello"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # 验证多个 token 被正确识别，包括 IF、ID、IN、USER_INPUT、THEN、RESPONSE 和 STRING 类型
        expected_tokens = [
            ('IF', 'if'),
            ('ID', 'x'),
            ('IN', 'in'),
            ('USER_INPUT', 'user_input'),
            ('THEN', 'then'),
            ('RESPONSE', 'response'),
            ('STRING', 'hello')
        ]
        self.assertEqual(expected_tokens, tokens)

    # 测试换行符和跳过空白字符的词法分析
    def test_tokenize_newline_and_skip(self):
        code = 'if x = 1 then\n response "done"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # 验证换行符和空格被正确跳过，且其余部分被正确识别
        expected_tokens = [
            ('IF', 'if'),
            ('ID', 'x'),
            ('ASSIGN', '='),
            ('NUMBER', '1'),
            ('THEN', 'then'),
            ('RESPONSE', 'response'),
            ('STRING', 'done')
        ]
        self.assertEqual(expected_tokens, tokens)

    # 测试注释的词法分析
    def test_tokenize_comment(self):
        code = '# This is a comment\nif x = 1'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # 验证注释部分被正确跳过，仅处理有效的代码部分
        expected_tokens = [('IF', 'if'), ('ID', 'x'), ('ASSIGN', '='), ('NUMBER', '1')]
        self.assertEqual(expected_tokens, tokens)


# 执行测试
if __name__ == '__main__':
    unittest.main()
