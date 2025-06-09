import unittest
from unittest.mock import patch
from dsl.lexer import Lexer
from dsl.parser import Parser
from dsl.interpreter import Interpreter  # 假设你把解释器保存在 interpreter.py 文件中

# 公共DSL脚本，包含了多个状态（INIT、ACCOUNT、GOODS、QUERY等）
common_code = """
start

# 初始状态
INIT
    if "你好" in user_input then
        response "您好，很高兴为您服务，请问您的需要是"
    elif "账户" in user_input then
        response "已转移至账户模式"
        go ACCOUNT
    elif "商品" in user_input then
        response "已转移至商品模式"
        go GOODS
    else
        response "抱歉，我没有理解您的问题"

# 账户
ACCOUNT
    if "余额" in user_input then
        response "您的余额为 "
    elif "充值" in user_input then
        response "请输入您所充值的金额"
        set balance = balance + user_input  # 假设充值金额会被输入
    elif "退出" in user_input then
        response "您已退出账户模式"
        go INIT
    else
        response "抱歉，我没有理解您的问题"

# 商品
GOODS
    if "名称" in user_input then
        response "在售商品的名称为：商品A, 商品B, 商品C"
    elif "查询" in user_input then
        response "已转移至查询模式，输入对应商品名称查询信息"
        go QUERY
    elif "退出" in user_input then
        response "您已退出商品模式"
        go INIT
    else
        response "抱歉，我没有理解您的问题"

# 查询
QUERY
    if "商品A" in user_input then
        response "商品A：价格：100元，库存：50件"
    elif "商品B" in user_input then
        response "商品B：价格：200元，库存：30件"
    elif "商品C" in user_input then
        response "商品C：价格：300元，库存：20件"
    elif "退出" in user_input then
        response "您已退出商品查询模式"
    else
        response "抱歉，我没有理解您的问题"

end
"""


class TestInterpreter(unittest.TestCase):
    # 测试初始状态模式
    @patch('builtins.input', side_effect=['你好', '账户', '商品', 'exit'])
    def test_initial_state(self, mock_input):
        # 词法分析：将DSL脚本转化为token
        lexer = Lexer(common_code)
        tokens = lexer.tokenize()

        # 语法分析：将tokens转化为抽象语法树（AST）
        parser = Parser(tokens)
        ast = parser.parse()

        # 初始化解释器
        interpreter = Interpreter(ast)

        # 模拟用户输入并测试每个阶段的输出
        response = interpreter.process_input('你好')
        self.assertEqual(response, "您好，很高兴为您服务，请问您的需要是")

        response = interpreter.process_input('账户')
        self.assertEqual(response, "已转移至账户模式")

        response = interpreter.process_input('退出')
        self.assertEqual(response, "您已退出账户模式")

        response = interpreter.process_input('商品')
        self.assertEqual(response, "已转移至商品模式")

    # 测试账户模式
    @patch('builtins.input', side_effect=['余额', '充值', '退出', 'exit'])
    def test_account_mode(self, mock_input):
        # 词法分析：将DSL脚本转化为token
        lexer = Lexer(common_code)
        tokens = lexer.tokenize()

        # 语法分析：将tokens转化为抽象语法树（AST）
        parser = Parser(tokens)
        ast = parser.parse()

        # 初始化解释器，并传入初始余额
        interpreter = Interpreter(ast, balance=50)

        # 模拟用户输入并测试每个阶段的输出
        response = interpreter.process_input('账户')
        self.assertEqual(response, "已转移至账户模式")

        response = interpreter.process_input('余额')
        self.assertEqual(response, "您的余额为  50.00")

        response = interpreter.process_input('退出')
        self.assertEqual(response, "您已退出账户模式")

    # 测试商品模式
    @patch('builtins.input', side_effect=['名称', '查询', '退出', 'exit'])
    def test_goods_mode(self, mock_input):
        # 词法分析：将DSL脚本转化为token
        lexer = Lexer(common_code)
        tokens = lexer.tokenize()

        # 语法分析：将tokens转化为抽象语法树（AST）
        parser = Parser(tokens)
        ast = parser.parse()

        # 初始化解释器
        interpreter = Interpreter(ast)

        # 模拟用户输入并测试每个阶段的输出
        response = interpreter.process_input('商品')
        self.assertEqual(response, "已转移至商品模式")

        response = interpreter.process_input('名称')
        self.assertEqual(response, "在售商品的名称为：商品A, 商品B, 商品C")

        response = interpreter.process_input('查询')
        self.assertEqual(response, "已转移至查询模式，输入对应商品名称查询信息")

        response = interpreter.process_input('退出')
        self.assertEqual(response, "您已退出商品查询模式")

    # 测试商品查询模式
    @patch('builtins.input', side_effect=['商品A', '退出', 'exit'])
    def test_query_mode(self, mock_input):
        # 词法分析：将DSL脚本转化为token
        lexer = Lexer(common_code)
        tokens = lexer.tokenize()

        # 语法分析：将tokens转化为抽象语法树（AST）
        parser = Parser(tokens)
        ast = parser.parse()

        # 初始化解释器
        interpreter = Interpreter(ast)

        # 模拟用户输入并测试每个阶段的输出
        response = interpreter.process_input('商品')
        self.assertEqual(response, "已转移至商品模式")

        response = interpreter.process_input('查询')
        self.assertEqual(response, "已转移至查询模式，输入对应商品名称查询信息")

        response = interpreter.process_input('商品A')
        self.assertEqual(response, "商品A：价格：100元，库存：50件")

        response = interpreter.process_input('退出')
        self.assertEqual(response, "您已退出商品查询模式")

    # 测试天气查询模式下的交互
    @patch('builtins.input', side_effect=['天气查询', '北京', '退出', '你好'])
    def test_recharge(self, mock_input):
        # 假设我们有一个简单的DSL脚本
        code = """
        start
        # 初始状态
        INIT
            if "天气查询" in user_input then
                response "您选择了天气查询，请输入城市名称"
                go WEATHER
            else
                response "请输入天气查询来查询天气"

        # 天气查询模块
        WEATHER
            if "退出" in user_input then
                response "您已退出天气查询模式"
                go INIT
            elif "北京" in user_input then
                response "北京的当前天气：晴，温度25°C"
            else
                response "抱歉，我没有找到该城市的天气，请重新输入"

        end
        """
        # 词法分析：将DSL脚本转化为token
        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # 语法分析：将tokens转化为抽象语法树（AST）
        parser = Parser(tokens)
        ast = parser.parse()

        # 初始化解释器，传入初始余额0
        interpreter = Interpreter(ast)

        # 模拟用户输入并测试每个阶段的输出
        response = interpreter.process_input('天气查询')
        self.assertEqual(response, "您选择了天气查询，请输入城市名称")

        response = interpreter.process_input('北京')
        self.assertEqual(response, "北京的当前天气：晴，温度25°C")

        response = interpreter.process_input('退出')
        self.assertEqual(response, "您已退出天气查询模式")

        response = interpreter.process_input('你好')
        self.assertEqual(response, "请输入天气查询来查询天气")


if __name__ == '__main__':
    unittest.main()
