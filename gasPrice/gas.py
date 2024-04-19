import schedule
import time
import requests
from bs4 import BeautifulSoup

def send_wechat(msg):
    token = '9b4ab34af3644367b38ffc32a4bfa295'#前边复制到那个token
    title = 'gas price'
    content = msg
    template = 'html'
    url = f"https://www.pushplus.plus/send?token={token}&title={title}&content={content}&template={template}"
    print(url)
    r = requests.get(url=url)
    print(r.text)

# 指定网页的 URL
url = "https://gaswizard.ca/gas-prices/vancouver/"

# 定时任务的逻辑函数
def send_gas_prices():
    # 使用 requests 库获取网页内容
    response = requests.get(url)
    
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
                
                # 循环遍历最近两天
                for day_li in latest_two_days:
                    # 查找日期
                    day_text = day_li.find('span', class_='daytext').string.strip()
                    date_text = day_li.find('span', class_='datetext').string.strip()
                    
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
                final_message = " -> ".join(messages)

                print(final_message)

                # 发送文本消息
                send_wechat(final_message)
            else:
                print("Could not find information for the latest day.")
        else:
            print("Could not find the single-city-prices list.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

#test
# send_gas_prices()

# 安排定时任务，每天在特定时间执行一次
schedule.every().day.at("08:00").do(send_gas_prices)  # 您可以根据需要设置执行时间
schedule.every().day.at("17:00").do(send_gas_prices)  # 您可以根据需要设置执行时间
#schedule.every(2).minutes.do(send_gas_prices)
# 不断运行调度器以保持定时任务的运行
while True:
    schedule.run_pending()
    time.sleep(1)
