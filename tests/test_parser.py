import unittest
from dsl.parser import Parser
from dsl.lexer import Lexer

class TestParser(unittest.TestCase):

    # 测试缺少INIT模式的代码
    def test_no_init_mode(self):
        code = '''
        start
        end
        '''
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)

        # 应该抛出SyntaxError，因为没有提供INIT模式
        with self.assertRaises(SyntaxError):
            parser.parse()

    # 测试缺少end关键字的代码
    def test_no_end(self):
        code = '''
        start
        '''
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)

        # 应该抛出TypeError，因为缺少end语句
        with self.assertRaises(TypeError):
            parser.parse()

    # 测试包含无效标记的代码
    def test_invalid_token(self):
        code = '''
        start
        INIT
            sfdsa
        end
        '''
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)

        # 应该抛出SyntaxError，因为遇到无效的标记"sfdsa"
        with self.assertRaises(SyntaxError):
            parser.parse()

    # 测试多次出现INIT模式的代码
    def test_multi_init(self):
        code = '''
        start
        INIT
        INIT
        end
        '''
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)

        # 应该抛出SyntaxError，因为INIT模式重复出现
        with self.assertRaises(SyntaxError):
            parser.parse()

    # 测试解析if语句
    def test_parse_if_statement(self):
        code = """
        start
        INIT
            if "hello" in user_input then
                response "hello"
        end
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        # 验证AST的结构是否正确
        expected_ast = {
            'type': 'program',
            'statements': [
                {'type': 'mode', 'mode': 'INIT'},
                {'type': 'if', 'condition': ['hello'], 'response': 'hello', 'next_statements': []}
            ]
        }

        # 断言实际解析结果和预期的AST结构相等
        self.assertEqual(expected_ast, ast)

    # 测试解析elif语句
    def test_parse_elif_statement(self):
        code = """
        start
        INIT
            if "hello" in user_input then
                response "hello"
            elif "hi" in user_input then
                response "hi"
        end
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        # 验证AST的结构是否正确
        expected_ast = {
            'type': 'program',
            'statements': [
                {'type': 'mode', 'mode': 'INIT'},
                {'type': 'if', 'condition': ['hello'], 'response': 'hello', 'next_statements': []},
                {'type': 'elif', 'condition': ['hi'], 'response': 'hi', 'next_statements': []}
            ]
        }

        self.assertEqual(expected_ast, ast)

    # 测试解析if-else语句
    def test_parse_if_else_statement(self):
        code = """
        start
        INIT
            if "hello" in user_input then
                response "hello"
            else
                response "What can I say?"
        end
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        # 验证AST的结构是否正确
        expected_ast = {
            'type': 'program',
            'statements': [
                {'type': 'mode', 'mode': 'INIT'},
                {'type': 'if', 'condition': ['hello'], 'response': 'hello', 'next_statements': []},
                {'type': 'else', 'response': 'What can I say?', 'next_statements': []}
            ]
        }

        self.assertEqual(expected_ast, ast)

    # 测试解析if-elif-else语句
    def test_parse_if_elif_else_statement(self):
        code = """
        start
        INIT
            if "hello" in user_input then
                response "hello"
            elif "hi" in user_input then
                response "hi"
            else
                response "What can I say?"
        end
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        # 验证AST的结构是否正确
        expected_ast = {
            'type': 'program',
            'statements': [
                {'type': 'mode', 'mode': 'INIT'},
                {'type': 'if', 'condition': ['hello'], 'response': 'hello', 'next_statements': []},
                {'type': 'elif', 'condition': ['hi'], 'response': 'hi', 'next_statements': []},
                {'type': 'else', 'response': 'What can I say?', 'next_statements': []}
            ]
        }

        self.assertEqual(expected_ast, ast)

    # 测试解析赋值语句
    def test_parse_assignment_statement(self):
        code = '''
        start
        INIT
            if "set" in user_input then
                response "set"
                set val = 10
        end
        '''
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        # 验证AST的结构是否正确
        expected_ast = {
            'type': 'program',
            'statements': [
                {'type': 'mode', 'mode': 'INIT'},
                {'type': 'if', 'condition': ['set'], 'response': 'set', 'next_statements': [
                    {'type': 'set', 'variable': 'val', 'expression': {'type': 'number', 'value': '10'}}
                ]}
            ]
        }

        self.assertEqual(expected_ast, ast)

    # 测试解析go语句
    def test_parse_go_statement(self):
        code = '''
        start
        INIT
            if "set" in user_input then
                response "set"
                set val = 24
                go TEMP
        TEMP
            if "hello" in user_input then
                response "hello"
            elif "hi" in user_input then
                response "hi"
            else
                response "What can I say? Mamba out!"
                set val = 8
                go INIT
        end
        '''
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        # 验证AST的结构是否正确
        expected_ast = {
            'type': 'program',
            'statements': [
                {'type': 'mode', 'mode': 'INIT'},
                {'type': 'if', 'condition': ['set'], 'response': 'set', 'next_statements': [
                    {'type': 'set', 'variable': 'val', 'expression': {'type': 'number', 'value': '24'}},
                    {'type': 'go', 'mode': 'TEMP'}
                ]},
                {'type': 'mode', 'mode': 'TEMP'},
                {'type': 'if', 'condition': ['hello'], 'response': 'hello', 'next_statements': []},
                {'type': 'elif', 'condition': ['hi'], 'response': 'hi', 'next_statements': []},
                {'type': 'else', 'response': 'What can I say? Mamba out!', 'next_statements': [
                    {'type': 'set', 'variable': 'val', 'expression': {'type': 'number', 'value': '8'}},
                    {'type': 'go', 'mode': 'INIT'}
                ]}
            ]
        }

        self.assertEqual(expected_ast, ast)

if __name__ == '__main__':
    unittest.main()
