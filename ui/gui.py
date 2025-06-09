import os
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from PIL import Image, ImageTk  # 导入Pillow库
from dsl.lexer import Lexer
from dsl.parser import Parser
from dsl.interpreter import Interpreter

class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("在线客服机器人")
        self.root.geometry("500x600")

        self.chat_box = scrolledtext.ScrolledText(self.root, height=25, width=60, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_box.grid(row=0, column=0, padx=10, pady=10)

        # 用户输入框
        self.user_input = tk.Entry(self.root, width=50)
        self.user_input.grid(row=1, column=0, padx=10, pady=10)

        # 发送按钮
        self.send_button = tk.Button(self.root, text="发送", width=10, command=self.send_message)
        self.send_button.grid(row=2, column=0, padx=10, pady=10)

        # 输入脚本文件路径的文本框
        self.script_input = tk.Entry(self.root, width=50)
        self.script_input.grid(row=3, column=0, padx=10, pady=10)
        self.script_input.insert(0, "scripts/example1.dsl")  # 默认文件路径

        # 加载脚本按钮
        self.load_button = tk.Button(self.root, text="加载脚本", width=10, command=self.load_script)
        self.load_button.grid(row=4, column=0, padx=10, pady=10)

        # 初始化解释器
        self.interpreter = None

        # 获取当前目录路径
        current_directory = os.path.dirname(__file__)

        # 获取项目根目录
        project_root = os.path.abspath(os.path.join(current_directory, '..'))

        # 构建图片文件的绝对路径
        user_avatar_path = os.path.join(project_root, 'photos', 'user.png')
        bot_avatar_path = os.path.join(project_root, 'photos', 'bot.png')

        # 加载图片
        self.user_avatar = self.load_image(user_avatar_path)
        self.bot_avatar = self.load_image(bot_avatar_path)

        # 绑定 Enter 键触发发送消息
        self.user_input.bind("<Return>", lambda event: self.send_message())  # 按下 Enter 时触发 send_message

    def load_image(self, image_path):
        """ 加载图片并返回Tkinter可用的PhotoImage对象 """
        try:
            image = Image.open(image_path)
            image = image.resize((30, 30))  # 调整头像大小
            return ImageTk.PhotoImage(image)
        except Exception as e:
            messagebox.showerror("错误", f"加载图片失败: {str(e)}")
            return None

    def send_message(self):
        """ 发送用户输入并获取机器人回应 """
        user_text = self.user_input.get()

        # 如果用户输入 "exit"，退出程序
        if user_text.lower() == "exit":
            self.chat_box.config(state=tk.NORMAL)
            self.chat_box.insert(tk.END, "退出聊天模式\n")
            self.chat_box.config(state=tk.DISABLED)
            self.root.quit()
            return

        if self.interpreter:
            # 在账户模式下输入“充值”时，弹出充值对话框
            if self.interpreter.context['current_mode'] == 'ACCOUNT' and "充值" in user_text:
                self.prompt_for_recharge()  # 弹出充值窗口
                response = None  # 不需要显示机器人回复
            else:
                # 获取机器人的回复
                response = self.interpreter.process_input(user_text)  # 修改为process_input

            # 显示用户输入和机器人回复（如果有）
            if response is not None:
                self.chat_box.config(state=tk.NORMAL)

                # 显示用户消息和头像
                self.chat_box.insert(tk.END, "\n")
                self.create_message_box("您", self.user_avatar, user_text)

                # 显示机器人消息和头像
                self.create_message_box("机器人", self.bot_avatar, response)

                # 强制更新UI并滚动到底部
                self.chat_box.update_idletasks()  # 等待所有UI更新完成
                self.chat_box.config(state=tk.DISABLED)
                self.chat_box.see(tk.END)  # 滚动到底部

        else:
            self.chat_box.config(state=tk.NORMAL)
            self.chat_box.insert(tk.END, "请先加载一个脚本。\n")
            self.chat_box.config(state=tk.DISABLED)

            # 强制更新UI并滚动到底部
            self.chat_box.update_idletasks()
            self.chat_box.see(tk.END)  # 强制滚动到底部

        # 清空输入框
        self.user_input.delete(0, tk.END)

    def create_message_box(self, name, avatar, message):
        """ 创建一个带头像和框框的消息框 """
        # 创建框框容器
        message_frame = tk.Frame(self.chat_box, padx=10, pady=5, relief=tk.RAISED, bd=2, bg='#f0f0f0')

        # 创建一个水平框架来放头像和消息
        message_content_frame = tk.Frame(message_frame, bg='#f0f0f0')

        # 显示头像在左边
        avatar_label = tk.Label(message_content_frame, image=avatar, bg='#f0f0f0')
        avatar_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")  # 头像左对齐

        # 显示消息在头像右边，设置消息框宽度限制
        message_label = tk.Label(message_content_frame, text=message, bg='#f0f0f0', width=40, wraplength=200)  # 限制宽度
        message_label.grid(row=0, column=1, padx=5, pady=5)

        # 把内容框添加到消息框
        message_content_frame.pack(anchor="w", padx=5, pady=2)  # 控制整体对齐和间距

        # 显示用户名在头像下方并左对齐
        name_label = tk.Label(message_frame, text=name, bg='#f0f0f0', font=("Arial", 10, "bold"))
        name_label.pack(anchor="w", padx=5, pady=2)  # 名字左对齐

        # 将消息框插入聊天框
        self.chat_box.window_create(tk.END, window=message_frame)
        self.chat_box.insert(tk.END, "\n")

    def load_script(self):
        """ 加载用户输入的脚本文件 """
        script_file = self.script_input.get().strip()
        if not script_file:
            messagebox.showerror("错误", "脚本文件路径不能为空！")
            return

        # 尝试加载脚本文件
        script_code = self.load_script_from_file(script_file)
        if script_code:
            self.chat_box.config(state=tk.NORMAL)
            self.chat_box.insert(tk.END, f"加载脚本: {script_file}\n")
            self.chat_box.config(state=tk.DISABLED)

            # 从上下文中获取当前余额
            balance = self.interpreter.context.get('balance', 0) if self.interpreter else 0

            # 创建并执行脚本
            self.interpreter = self.execute_script(script_code, balance)

    def load_script_from_file(self, file_path):
        """ 从脚本文件加载代码 """
        if not os.path.exists(file_path):
            messagebox.showerror("错误", f"脚本文件 '{file_path}' 不存在。")
            return None
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def execute_script(self, script_code, balance):
        """ 执行DSL脚本并返回解释器 """
        lexer = Lexer(script_code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        ast = parser.parse()

        # 创建并返回解释器，传递余额
        interpreter = Interpreter(ast, balance)
        return interpreter

    def prompt_for_recharge(self):
        """ 提示用户输入充值金额，并检查其合法性 """

        def submit_recharge():
            try:
                recharge_amount = float(recharge_entry.get())
                if recharge_amount < 0:
                    messagebox.showerror("错误", "金额不能为负！")
                    return
                self.chat_box.config(state=tk.NORMAL)
                self.chat_box.insert(tk.END, f"充值成功！充值金额为: {recharge_amount:.2f} 元\n")
                self.chat_box.config(state=tk.DISABLED)
                self.interpreter.context['balance'] += recharge_amount  # 更新余额
                recharge_window.destroy()
            except ValueError:
                messagebox.showerror("错误", "请输入一个有效的数字！")

        recharge_window = tk.Toplevel(self.root)
        recharge_window.title("充值金额")
        recharge_window.geometry("300x150")

        label = tk.Label(recharge_window, text="请输入充值金额：")
        label.pack(pady=10)

        recharge_entry = tk.Entry(recharge_window, width=20)
        recharge_entry.pack(pady=5)

        submit_button = tk.Button(recharge_window, text="提交", command=submit_recharge)
        submit_button.pack(pady=10)

        cancel_button = tk.Button(recharge_window, text="取消", command=recharge_window.destroy)
        cancel_button.pack(pady=5)


# 创建主程序窗口
def main():
    root = tk.Tk()
    gui = ChatbotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
