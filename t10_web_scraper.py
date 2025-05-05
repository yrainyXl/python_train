'''
题目要求：编写一个基础网络爬虫程序，从指定网页抓取数据并进行简单处理。

要求：
1. 使用requests库发送HTTP请求获取网页内容
2. 使用BeautifulSoup库解析HTML内容
3. 提取网页中的特定信息（如标题、链接、文本等）
4. 对提取的数据进行简单处理（如过滤、排序等）
5. 将处理后的数据保存为结构化的CSV文件
6. 处理可能出现的异常情况（网络错误、解析错误等）

知识点：
1. HTTP请求基础：
   - requests库的基本用法
   - 处理不同的HTTP状态码
   - 设置请求头（User-Agent等）
   - 处理网络超时和连接错误

2. HTML解析：
   - BeautifulSoup库的基本用法
   - 使用选择器（CSS选择器、XPath等）定位元素
   - 提取元素的文本、属性和嵌套内容
   - 处理不同类型的HTML结构

3. 数据处理与存储：
   - 数据清洗（去除空白字符、特殊字符等）
   - 数据结构化（列表、字典等）
   - 使用CSV模块保存数据
   - 文件操作和异常处理
'''

import requests
import csv
import os
from bs4 import BeautifulSoup
import time
import random

# 示例URL（一个稳定的示例网页，用于教学目的）
SAMPLE_URL = "https://quotes.toscrape.com/"

# 请求头，模拟浏览器访问，减少被网站拒绝的可能性
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# 字段映射，用于CSV文件的表头
FIELD_MAPPING = {
    "quote": "名言",
    "author": "作者",
    "tags": "标签"
}


def fetch_webpage(url, max_retries=3):
    """
    获取网页内容，支持重试机制
    
    参数：
    url -- 网页URL
    max_retries -- 最大重试次数
    
    返回：
    str -- 网页HTML内容
    """
    retries = 0
    while retries < max_retries:
        try:
            # 发送HTTP GET请求
            response = requests.get(url, headers=HEADERS, timeout=10)
            
            # 检查HTTP状态码
            if response.status_code == 200:
                return response.text
            else:
                print(f"HTTP错误: {response.status_code}")
                retries += 1
                # 等待一段时间再重试
                time.sleep(2)
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {str(e)}")
            retries += 1
            # 等待一段时间再重试
            time.sleep(2)
    
    # 如果所有重试都失败，抛出异常
    raise Exception(f"无法获取网页内容: {url}，已重试{max_retries}次")


def parse_quotes(html_content):
    """
    解析HTML内容，提取名言、作者和标签信息
    
    参数：
    html_content -- 网页HTML内容
    
    返回：
    list -- 包含名言信息的字典列表
    """
    # 创建BeautifulSoup对象
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 查找所有名言块
    quote_divs = soup.find_all('div', class_='quote')
    
    # 存储结果的列表
    quotes_data = []
    
    # 遍历每个名言块，提取信息
    for quote_div in quote_divs:
        try:
            # 提取名言文本
            quote_text = quote_div.find('span', class_='text').get_text()
            # 去除引号
            quote_text = quote_text.strip('"')
            
            # 提取作者
            author = quote_div.find('small', class_='author').get_text()
            
            # 提取标签
            tags = [tag.get_text() for tag in quote_div.find_all('a', class_='tag')]
            tags_str = ", ".join(tags)
            
            # 将信息添加到结果列表
            quotes_data.append({
                FIELD_MAPPING["quote"]: quote_text,
                FIELD_MAPPING["author"]: author,
                FIELD_MAPPING["tags"]: tags_str
            })
        except AttributeError as e:
            # 如果解析某个元素失败，打印错误并继续
            print(f"解析错误: {str(e)}")
            continue
    
    return quotes_data


def save_to_csv(data, output_file):
    """
    将数据保存为CSV文件
    
    参数：
    data -- 要保存的数据列表
    output_file -- 输出CSV文件路径
    
    返回：
    bool -- 操作成功返回True，否则抛出异常
    """
    # 确保输出目录存在
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 检查数据是否为空
    if not data:
        raise ValueError("没有数据可保存")
    
    try:
        # 打开CSV文件并写入数据
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            # 获取字段名（表头）
            fieldnames = data[0].keys()
            
            # 创建CSV写入器
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            # 写入表头
            writer.writeheader()
            
            # 写入数据行
            writer.writerows(data)
        
        return True
    except Exception as e:
        raise Exception(f"保存CSV文件时发生错误: {str(e)}")


def scrape_quotes(url=SAMPLE_URL, output_file="./output/quotes.csv"):
    """
    主函数：抓取网页数据并保存为CSV
    
    参数：
    url -- 要抓取的网页URL
    output_file -- 输出CSV文件路径
    
    返回：
    bool -- 操作成功返回True
    """
    try:
        # 获取网页内容
        html_content = fetch_webpage(url)
        
        # 解析网页内容
        quotes_data = parse_quotes(html_content)
        
        # 检查是否成功提取数据
        if not quotes_data:
            print("未找到任何名言数据")
            return False
        
        # 保存数据到CSV文件
        if save_to_csv(quotes_data, output_file):
            print(f"成功抓取{len(quotes_data)}条名言并保存到{output_file}")
            return True
    
    except Exception as e:
        print(f"抓取过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# 练习任务：
# 1. 运行基础版爬虫，观察结果
# 2. 修改程序，实现以下功能：
#    a. 抓取多个页面的数据（提示：网站有分页功能）
#    b. 添加更多数据过滤或处理功能（如按作者分组、按标签筛选等）
#    c. 增强错误处理和日志记录
# 3. 尝试抓取不同网站的数据（注意遵守网站的robots.txt规则和使用条款）


if __name__ == "__main__":
    # 测试爬虫功能
    output_file_path = "./output/t10_quotes.csv"
    
    print("开始抓取网页数据...")
    result = scrape_quotes(SAMPLE_URL, output_file_path)
    
    if result:
        print("爬虫任务完成！")
    else:
        print("爬虫任务失败！")