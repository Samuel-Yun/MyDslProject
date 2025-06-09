from dsl.lexer import Lexer
from dsl.parser import Parser

# 解释器类
class Interpreter:
    def __init__(self, ast, balance=0.0):
        # 初始化状态字典，记录每个模式下的操作
        self.context = {
            'balance': balance,
            'user_input': '',
            'current_mode': 'INIT',
        }
        self.program = self.parse_ast(ast)

    def parse_ast(self, ast):
        # 解析AST，将每个mode的操作存入字典
        modes = {}
        for statement in ast['statements']:
            if statement['type'] == 'mode':
                current_mode = statement['mode']
                modes[current_mode] = {
                    'if_conditions': [],
                    'elif_conditions': [],
                    'else_condition': None
                }
            elif statement['type'] == 'if':
                modes[current_mode]['if_conditions'].append(statement)
            elif statement['type'] == 'elif':
                modes[current_mode]['elif_conditions'].append(statement)
            elif statement['type'] == 'else':
                modes[current_mode]['else_condition'] = statement
        return modes

    def prompt_for_recharge(self):
        """ 提示用户输入充值金额，并检查其合法性 """
        if self.context['current_mode'] != 'ACCOUNT':
            return "无法进行充值操作。请先进入账户模式。"

        while True:
            try:
                recharge_amount = float(input("请输入您所充值的金额（浮动数）："))
                if recharge_amount < 0:
                    print("金额不能为负，请重新输入。")
                    continue
                self.context['balance'] += recharge_amount
                return f"充值成功！您的新余额为 {self.context['balance']:.2f} 元"
            except ValueError:
                print("输入无效，请确保您输入的是一个有效的数字。")

    def process_input(self, user_input):
        # 更新用户输入
        self.context['user_input'] = user_input

        # 获取当前模式下的操作
        current_mode = self.context['current_mode']
        mode_operations = self.program.get(current_mode, {})

        # 处理if/elif/else逻辑
        for condition in mode_operations['if_conditions']:
            if any(cond in user_input for cond in condition['condition']):
                response = condition['response']
                next_statements = condition['next_statements']
                self.handle_next_statements(next_statements)

                # 如果用户输入是 "充值"，跳转到充值处理流程
                if '充值' in user_input:
                    response = self.prompt_for_recharge()  # 处理充值流程
                    return response

                # 处理余额输出时保留2位小数
                if '余额' in response:
                    response = f"{response} {self.context['balance']:.2f}"
                return response

        for condition in mode_operations['elif_conditions']:
            if any(cond in user_input for cond in condition['condition']):
                response = condition['response']
                next_statements = condition['next_statements']
                self.handle_next_statements(next_statements)

                # 如果用户输入是 "充值"，跳转到充值处理流程
                if '充值' in user_input:
                    response = self.prompt_for_recharge()  # 处理充值流程
                    return response

                # 处理余额输出时保留2位小数
                if '余额' in response:
                    response = f"{response} {self.context['balance']:.2f}"
                return response

        if mode_operations['else_condition']:
            response = mode_operations['else_condition']['response']
            next_statements = mode_operations['else_condition']['next_statements']
            self.handle_next_statements(next_statements)

            # 如果用户输入是 "充值"，跳转到充值处理流程
            if '充值' in user_input:
                response = self.prompt_for_recharge()  # 处理充值流程
                return response

            # 处理余额输出时保留2位小数
            if '余额' in response:
                response = f"{response} {self.context['balance']:.2f}"
            return response

    def handle_next_statements(self, next_statements):
        for statement in next_statements:
            if statement['type'] == 'go':
                self.context['current_mode'] = statement['mode']
            elif statement['type'] == 'set':
                var_name = statement['variable']
                expression = statement['expression']

                # 仅当表达式类型为加法运算时才进行处理
                if expression['type'] == 'addition':
                    left = self.context.get(expression['left'], 0)

                    # 确保只有数字才能参与加法运算
                    try:
                        right = float(self.context['user_input'])  # 这里是需要用户输入数字的地方
                        self.context[var_name] = left + right
                    except ValueError:
                        # 如果是充值或其他非数字输入，跳过加法运算
                        if '充值' in self.context['user_input']:
                            print("正在处理充值，请输入金额。")
                        else:
                            print(f"无效输入：'{self.context['user_input']}'，无法进行加法运算。")

    def run(self):
        # 运行与用户交互的循环
        while True:
            user_input = input("请输入您的问题: ")
            if user_input.lower() == "exit":
                break
            print(self.process_input(user_input))

# 接口方法
def run_interpreter(ast, balance=0.0):
    interpreter = Interpreter(ast, balance)
    interpreter.run()