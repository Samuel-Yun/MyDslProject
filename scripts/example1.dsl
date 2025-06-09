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
        set balance = balance + user_input
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
