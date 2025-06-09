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


# 模拟压力测试和资源占用
def stress_test(num_iterations=1000):
    for i in range(num_iterations):
        # 每次压力测试都生成新的DSL代码
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

        # 每100次打印一次响应
        if i % 100 == 0:
            print(f"Iteration {i + 1} Response: {response}")

        # 模拟资源占用情况
        simulate_cpu_memory_disk_network()

        # 每100次打印一下压力测试状态
        if i % 100 == 0:
            print(f"Iteration {i + 1} resource stress simulated.")

    print("Stress Test completed.")


# 模拟资源占用情况
def simulate_cpu_memory_disk_network():
    # 模拟占用 CPU
    print("Simulating high CPU usage...")
    cpu_usage = psutil.cpu_percent(interval=2)
    print(f"CPU Usage: {cpu_usage}%")

    # 模拟占用内存
    print("Simulating high memory usage...")
    memory_usage = psutil.virtual_memory().percent

    print(f"Memory Usage: {memory_usage}%")

    # 模拟磁盘占用
    print("Simulating high disk usage...")
    disk_usage = psutil.disk_usage('/').percent
    print(f"Disk Usage: {disk_usage}%")

    # 模拟网络带宽占用
    print("Simulating network usage...")
    network_usage = psutil.net_io_counters()
    print(f"Sent: {network_usage.bytes_sent / (1024 ** 2):.2f} MB, Received: {network_usage.bytes_recv / (1024 ** 2):.2f} MB")

    # 模拟一个 CPU 占用高的进程
    print("Launching a high CPU process...")
    subprocess.Popen(["python", "-c", "while True: pass"])  # 启动一个占用 CPU 的进程

    # 模拟一个大内存占用的进程
    print("Launching a high memory process...")
    memory_hog = subprocess.Popen(["python", "-c", "a = ['a' * 10**7 for _ in range(100)]"])  # 启动一个占用内存的进程

    # 模拟磁盘占用接近100%
    print("Simulating disk full condition...")
    with open('large_test_file.txt', 'w') as f:
        f.write('a' * 10**9)  # 写入一个大文件，占用磁盘空间

    # 模拟网络带宽占用的进程（例如，下载一个大文件）
    print("Simulating network bandwidth usage...")
    subprocess.Popen(["curl", "-O", "https://speed.hetzner.de/100MB.bin"])  # 使用curl下载一个大文件

    # 模拟网络断开
    print("Simulating network disconnect...")
    os.system("ifconfig eth0 down")  # 断开网络
    time.sleep(2)
    os.system("ifconfig eth0 up")  # 恢复网络

    # 模拟电源故障
    print("Simulating power failure (mock)...")
    # 这里是模拟一个设备重启的情况
    time.sleep(1)
    print("System rebooted.")  # 模拟系统重启


if __name__ == '__main__':
    # 进行压力测试，模拟10次迭代
    stress_test(num_iterations=10)
