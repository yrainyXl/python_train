'''
题目要求：编写一个基础网络爬虫程序的本地版本，从本地HTML文件抓取数据并进行简单处理。

要求：
1. 读取本地HTML文件内容
2. 使用BeautifulSoup库解析HTML内容
3. 提取HTML中的特定信息（如标题、链接、文本等）
4. 对提取的数据进行简单处理（如过滤、排序等）
5. 将处理后的数据保存为结构化的CSV文件
6. 处理可能出现的异常情况（文件不存在、解析错误等）

知识点：
1. 文件操作基础：
   - 读取本地HTML文件
   - 处理文件编码问题
   - 文件路径处理

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

import csv
import os
from bs4 import BeautifulSoup

# 示例HTML文件路径
SAMPLE_HTML = "./test_file/sample_quotes.html"

# 字段映射，用于CSV文件的表头
FIELD_MAPPING = {
    "quote": "名言",
    "author": "作者",
    "tags": "标签"
}


def read_html_file(file_path):
    """
    读取本地HTML文件内容
    
    参数：
    file_path -- HTML文件路径
    
    返回：
    str -- HTML内容
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return html_content
    except UnicodeDecodeError:
        # 如果UTF-8解码失败，尝试其他编码
        try:
            with open(file_path, 'r', encoding='gbk') as file:
                html_content = file.read()
            return html_content
        except Exception as e:
            raise Exception(f"读取HTML文件时发生错误: {str(e)}")


def parse_quotes(html_content):
    """
    解析HTML内容，提取名言、作者和标签信息
    
    参数：
    html_content -- HTML内容
    
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


def process_quotes_data(quotes_data, sort_by="author", filter_tag=None):
    """
    处理名言数据：排序和过滤
    
    参数：
    quotes_data -- 名言数据列表
    sort_by -- 排序字段（author或quote）
    filter_tag -- 按标签过滤（如果提供）
    
    返回：
    list -- 处理后的数据列表
    """
    # 如果需要按标签过滤
    if filter_tag:
        filtered_data = []
        for quote in quotes_data:
            # 检查标签是否包含过滤条件
            if filter_tag.lower() in quote[FIELD_MAPPING["tags"]].lower():
                filtered_data.append(quote)
        quotes_data = filtered_data
    
    # 排序数据
    if sort_by == "author":
        sorted_data = sorted(quotes_data, key=lambda x: x[FIELD_MAPPING["author"]])
    else:  # 按名言长度排序
        sorted_data = sorted(quotes_data, key=lambda x: len(x[FIELD_MAPPING["quote"]]))
    
    return sorted_data


def scrape_local_html(html_file=SAMPLE_HTML, output_file="./output/local_quotes.csv", sort_by="author", filter_tag=None):
    """
    主函数：从本地HTML文件提取数据并保存为CSV
    
    参数：
    html_file -- 本地HTML文件路径
    output_file -- 输出CSV文件路径
    sort_by -- 排序方式（author或quote）
    filter_tag -- 按标签过滤（可选）
    
    返回：
    bool -- 操作成功返回True
    """
    try:
        # 读取HTML文件
        html_content = read_html_file(html_file)
        
        # 解析HTML内容
        quotes_data = parse_quotes(html_content)
        
        # 检查是否成功提取数据
        if not quotes_data:
            print("未找到任何名言数据")
            return False
        
        # 处理数据（排序和过滤）
        processed_data = process_quotes_data(quotes_data, sort_by, filter_tag)
        
        # 保存数据到CSV文件
        if save_to_csv(processed_data, output_file):
            print(f"成功提取{len(processed_data)}条名言并保存到{output_file}")
            return True
    
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


# 练习任务：
# 1. 运行基础版本，观察结果
# 2. 修改程序，实现以下功能：
#    a. 添加更多数据处理功能（如按作者分组、按名言长度排序等）
#    b. 增强错误处理和日志记录
#    c. 添加命令行参数支持，允许用户指定输入文件、输出文件和处理选项
# 3. 尝试解析不同结构的HTML文件


if __name__ == "__main__":
    # 测试本地HTML解析功能
    output_file_path = "./output/t10_local_quotes.csv"
    
    print("开始解析本地HTML文件...")
    
    # 不带过滤的基本解析
    print("\n1. 基本解析（按作者排序）:")
    result1 = scrape_local_html(SAMPLE_HTML, output_file_path, sort_by="author")
    
    # 带标签过滤的解析
    print("\n2. 带过滤的解析（只包含'智慧'标签）:")
    result2 = scrape_local_html(SAMPLE_HTML, "./output/t10_wisdom_quotes.csv", filter_tag="智慧")
    
    # 按名言长度排序
    print("\n3. 按名言长度排序:")
    result3 = scrape_local_html(SAMPLE_HTML, "./output/t10_quotes_by_length.csv", sort_by="quote")
    
    if result1 and result2 and result3:
        print("\n所有解析任务完成！")
    else:
        print("\n部分解析任务失败！")