import schedule
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def send_wechat(title,msg):
    token = '9b4ab34af3644367b38ffc32a4bfa295'#前边复制到那个token
    # title = 'gas price'
    topic = 'gasPrice'
    content = msg
    template = 'html'
    url = f"https://www.pushplus.plus/send?token={token}&title={title}&content={content}&template={template}&topic={topic}"
    print(url)
    r = requests.get(url=url)

    current_time_time_module = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(current_time_time_module)
    print(r.text)

def send_slack(msg):
    url = "https://hooks.slack.com/services/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"
    payload = {
    "channel": "#gas_price",
    "username": "gas",
    "text": "today => tomorrow:    "+msg,
    "icon_emoji": ":ghost:"
    }
    response = requests.post(url, json=payload)

    current_time_time_module = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(current_time_time_module)
    print(response.text)


# 指定网页的 URL
url = "https://gaswizard.ca/gas-prices/vancouver/"

# 定时任务的逻辑函数
def send_gas_prices():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    # 使用 requests 库获取网页内容
    response = requests.get(url)
    weekdays_cn = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用 BeautifulSoup 库解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找包含燃油价格的列表
        fuel_prices_list = soup.find('ul', class_='single-city-prices')

        if fuel_prices_list:
            # 查找最新两天的 <li> 元素
            latest_two_days = fuel_prices_list.find_all('li', limit=2)[::-1]
            if latest_two_days:
                # 初始化消息列表
                messages = []
                dates = []

                # 循环遍历最近两天
                for day_li in latest_two_days:
                    # 查找日期
                    date_text = day_li.find('span', class_='datetext').string.strip()
                    date_object = datetime.strptime(date_text, "%b %d, %Y")
                    # 提取月和日
                    month = date_object.month
                    day = date_object.day
                    weekday_number = date_object.weekday()
                    weekday_name_cn = weekdays_cn[weekday_number]

                    # 转成字符串并输出
                    #result_date = f"{month:02d}.{day:02d}{weekday_name_cn}"
                    #result_date = f"{day:02d}{weekday_name_cn}"
                    dates.append(weekday_name_cn)

                    # 查找 Regular fuel price
                    regular_fuel = day_li.find('div', class_='fueltitle', string='Regular')
                    if regular_fuel:
                        regular_fuel_price_div = regular_fuel.find_next_sibling('div', class_='fuelprice')
                        if regular_fuel_price_div:
                            regular_fuel_price = regular_fuel_price_div.text.strip()



                            # 将日期、当前时间和常规燃油价格组合成消息
                            message = (f"{regular_fuel_price}")

                            # 添加到消息列表中
                            messages.append(message)

                # 将消息列表组合成一个字符串，并通过微信发送
                final_date = " to ".join(dates)
                final_message = " --> ".join(messages)

                print(final_date)
                print(final_message)

                # 发送文本消息
                send_wechat(final_date, final_message)
                #send_slack(final_message)
            else:
                print("Could not find information for the latest day.")
        else:
            print("Could not find the single-city-prices list.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

#test
send_gas_prices()

# 安排定时任务，每天在特定时间执行一次
schedule.every().day.at("08:00").do(send_gas_prices)  # 您可以根据需要设置执行时间
schedule.every().day.at("17:00").do(send_gas_prices)  # 您可以根据需要设置执行时间
#schedule.every(2).minutes.do(send_gas_prices)
# 不断运行调度器以保持定时任务的运行
while True:
    schedule.run_pending()
    time.sleep(1)
