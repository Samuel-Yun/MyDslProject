import random
import string
import time
import psutil  # 用于获取系统资源占用信息
import os
import subprocess
from dsl.lexer import Lexer
from dsl.parser import Parser
from dsl.interpreter import Interpreter


# 生成一个长度为`length`的随机字符串
def generate_long_string(length=2000):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


# 随机生成全大写字母组成的模块名称
def generate_random_mode_name(length=2000):
    return ''.join(random.choices(string.ascii_uppercase, k=length))


# 随机生成一个以'z'字母开头的变量名
def generate_variable_name(length=1000):
    return 'z' + ''.join(random.choices(string.ascii_letters + string.digits, k=length - 1))


# 随机生成英文用户输入
def generate_random_user_input():
    inputs = [
        "Account Balance", "Recharge", "Order Inquiry", "Shopping", "Payment", "Exit",
        "Insufficient Balance", "Order Details", "Check Account", "Order Payment",
        "View Balance", "Account Info", "Order Status", "Payment Successful", "Confirm Payment"
    ]
    return random.choice(inputs)


# 模拟生成一些随机DSL代码
def generate_dsl():
    second_mode = generate_random_mode_name()

    dsl_code = f"start\n"
    dsl_code += f"    INIT\n"

    # 在INIT模式下，生成if语句
    dsl_code += f"        if \"{generate_long_string()}\" in user_input then\n"
    dsl_code += f"            response \"{generate_long_string()}\"\n"
    dsl_code += f"            set {generate_variable_name()} = {random.randint(1, 10000000000)}\n"
    dsl_code += f"            go {second_mode}\n"

    # 随机生成第二个模式
    dsl_code += f"    {second_mode}\n"
    dsl_code += f"        if \"{generate_long_string()}\" in user_input then\n"
    dsl_code += f"            response \"{generate_long_string()}\"\n"
    dsl_code += f"        elif \"{generate_long_string()}\" in user_input then\n"
    dsl_code += f"            response \"{generate_long_string()}\"\n"
    dsl_code += f"        else\n"
    dsl_code += f"            response \"What{generate_long_string()} can I{generate_long_string()} say? M{generate_long_string()}amba out!\"\n"
    dsl_code += f"            set {generate_variable_name()} = {random.randint(1, 10000000000)}\n"
    dsl_code += f"            go INIT\n"

    dsl_code += "    end\n"
    return dsl_code


# 性能测试和响应时间统计
def performance_test(num_iterations=1000):
    total_time = 0  # 总共耗时
    max_time = 0  # 最大响应时间
    min_time = float('inf')  # 最小响应时间
    successful_requests = 0  # 成功请求数

    for i in range(num_iterations):
        start_time = time.time()  # 记录请求开始时间

        # 每次请求生成新的DSL代码
        dsl_code = generate_dsl()
        lexer = Lexer(dsl_code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        interpreter = Interpreter(ast)

        # 生成随机用户输入
        user_input = generate_random_user_input()
        print(f"Test Iteration {i + 1}: {user_input}")
        response = interpreter.process_input(user_input)

        # 计算每次请求的响应时间
        response_time = time.time() - start_time
        total_time += response_time
        max_time = max(max_time, response_time)
        min_time = min(min_time, response_time)

        # 统计成功请求
        if response is not None:
            successful_requests += 1

        # 每100次打印一次响应和性能数据
        if i % 100 == 0:
            print(f"Iteration {i + 1} Response: {response}")
            print(f"Iteration {i + 1} Response Time: {response_time:.4f} seconds")

    # 计算平均响应时间和吞吐量
    avg_time = total_time / num_iterations
    throughput = successful_requests / total_time if total_time > 0 else 0

    # 打印总结信息
    print("\nPerformance Test Summary:")
    print(f"Total Requests: {num_iterations}")
    print(f"Successful Requests: {successful_requests}")
    print(f"Average Response Time: {avg_time:.4f} seconds")
    print(f"Max Response Time: {max_time:.4f} seconds")
    print(f"Min Response Time: {min_time:.4f} seconds")
    print(f"Throughput: {throughput:.2f} requests/second")


if __name__ == '__main__':
    # 进行性能测试，模拟1000次迭代
    performance_test(num_iterations=1000)
