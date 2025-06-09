start

# 初始状态
INIT
    if "1" in user_input then
        response "您选择了查询书籍，请输入书名或关键字"
        go QUERY
    elif "2" in user_input then
        response "您选择了借书，请输入要借阅的书名"
        go BORROW
    elif "3" in user_input then
        response "您选择了还书，请输入要归还的书名"
        go RETURN
    elif "4" in user_input then
        response "您选择了联系图书馆客服，请输入您的问题"
        go CONTACT
    else
        response "抱歉，我没有理解您的选择，请请选择操作：1. 查询书籍 2. 借书 3. 还书 4. 联系客服"

# 查询书籍模块
QUERY
    if "退出" in user_input then
        response "您已退出书籍查询模式"
        go INIT
    elif "Python编程" in user_input then
        response "书籍《Python编程》：可借阅，馆藏3本"
    elif "数据结构" in user_input then
        response "书籍《数据结构与算法分析》：已借完，预计归还时间：2024年12月10日"
    elif "机器学习" in user_input then
        response "书籍《机器学习实战》：可借阅，馆藏1本"
    else
        response "未找到相关书籍，请尝试其他关键字或输入“退出”返回主菜单"

# 借书模块
BORROW
    if "退出" in user_input then
        response "您已退出借书模式"
        go INIT
    elif "Python编程" in user_input then
        response "您已成功借阅《Python编程》，请于2025年1月4日归还"
    elif "机器学习" in user_input then
        response "您已成功借阅《机器学习实战》，请于2025年1月4日归还"
    elif "数据结构" in user_input then
        response "抱歉，书籍《数据结构与算法分析》已被借完"
    else
        response "未找到相关书籍，请确认书名是否正确或输入“退出”返回主菜单"

# 还书模块
RETURN
    if "退出" in user_input then
        response "您已退出还书模式"
        go INIT
    elif "Python编程" in user_input then
        response "您已成功归还《Python编程》，欢迎再次借阅"
    elif "机器学习" in user_input then
        response "您已成功归还《机器学习实战》，欢迎再次借阅"
    else
        response "未找到相关归还记录，请确认书名是否正确或输入“退出”返回主菜单"

# 联系客服模块
CONTACT
    if "投诉" in user_input then
        response "您可以发送邮件至support@library.com，我们将尽快处理您的问题"
    elif "帮助" in user_input then
        response "您可以告诉我您的问题，我会尽力帮助您"
    elif "退出" in user_input then
        response "您已退出客服模式"
        go INIT
    else
        response "抱歉，我没有理解您的问题，请尝试输入“投诉”或“帮助”"

end
