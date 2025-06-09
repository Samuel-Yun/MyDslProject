start

# 初始状态
INIT
    if "1" in user_input then
        response "您选择了天气查询，请输入城市名称"
        go WEATHER
    elif "2" in user_input then
        response "您选择了快递查询，请输入快递单号"
        go EXPRESS
    elif "3" in user_input then
        response "您选择了客服帮助，请告诉我您遇到的问题"
        go HELP
    elif "4" in user_input then
        response "您选择了投诉，请描述您的问题或投诉内容"
        go COMPLAINT
    else
        response "抱歉，我没有理解您的选择，请输入1、2、3或4：1. 天气查询 2. 快递查询 3. 客服帮助 4. 投诉"

# 天气查询模块
WEATHER
    if "退出" in user_input then
        response "您已退出天气查询模式"
        go INIT
    elif "北京" in user_input then
        response "北京的当前天气为：晴，温度25°C"
    elif "上海" in user_input then
        response "上海的当前天气为：多云，温度22°C"
    elif "广州" in user_input then
        response "广州的当前天气为：阵雨，温度28°C"
    elif "深圳" in user_input then
        response "深圳的当前天气为：雷阵雨，温度30°C"
    elif "成都" in user_input then
        response "成都的当前天气为：阴，温度24°C"
    else
        response "抱歉，我没有找到此城市的天气数据，请重新输入或输入“退出”返回主菜单"

# 快递查询模块
EXPRESS
    if "退出" in user_input then
        response "您已退出快递查询模式"
        go INIT
    elif "12345" in user_input then
        response "快递单号12345的状态为：已发货，预计到达时间：2024年12月5日"
    elif "67890" in user_input then
        response "快递单号67890的状态为：运输中，预计到达时间：2024年12月7日"
    elif "11223" in user_input then
        response "快递单号11223的状态为：已签收，已完成配送"
    else
        response "抱歉，未能找到对应的快递单号，请确认您的单号是否正确"

# 客服帮助模块
HELP
    if "问题" in user_input then
        response "请描述您遇到的问题，我们将尽快为您解答"
    elif "退出" in user_input then
        response "您已退出客服帮助模式"
        go INIT
    else
        response "抱歉，我没有理解您的问题，您可以尝试输入“人工”或“问题”"

# 投诉模块
COMPLAINT
    if "退出" in user_input then
        response "您已退出投诉模式"
        go INIT
    elif "服务差" in user_input then
        response "非常抱歉给您带来不便，我们将尽快处理您的投诉"
    elif "配送慢" in user_input then
        response "感谢您的反馈，我们会加强配送服务的管理"
    elif "态度差" in user_input then
        response "我们对服务态度深感抱歉，已将您的问题反馈给相关部门"
    else
        response "感谢您的投诉，我们将根据您的反馈改进服务"

end
