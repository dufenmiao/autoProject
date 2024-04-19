import requests
from bs4 import BeautifulSoup
from wechatpy import WeChatClient
from wechatpy.exceptions import WeChatClientException
from wechatpy.replies import TextReply

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

# 使用 requests 库获取网页内容
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 使用 BeautifulSoup 库解析网页内容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 查找包含燃油价格的列表
    fuel_prices_list = soup.find('ul', class_='single-city-prices')
    
    if fuel_prices_list:
        # 查找最新一天的 <li> 元素
        latest_day_li = fuel_prices_list.find('li')
        
        if latest_day_li:
            # 查找日期
            day_text = latest_day_li.find('span', class_='daytext').string.strip()
            date_text = latest_day_li.find('span', class_='datetext').string.strip()
            
            # 查找 Regular fuel price
            regular_fuel = latest_day_li.find('div', class_='fueltitle', string='Regular')
            if regular_fuel:
                regular_fuel_price_div = regular_fuel.find_next_sibling('div', class_='fuelprice')
                if regular_fuel_price_div:
                    regular_fuel_price = regular_fuel_price_div.text.strip()
                    
                    # 将日期和常规燃油价格组合成消息
                    message = f"{regular_fuel_price}"
                    send_wechat(message)
        else:
            print("Could not find information for the latest day.")
    else:
        print("Could not find the single-city-prices list.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

