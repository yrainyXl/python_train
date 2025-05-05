# Python网络爬虫基础练习

## 练习内容

这个练习主要帮助你学习使用Python进行网络爬虫的基础知识，包括：

1. 使用`requests`库发送HTTP请求获取网页内容
2. 使用`BeautifulSoup`库解析HTML内容
3. 提取网页中的特定信息（标题、链接、文本等）
4. 对提取的数据进行简单处理（过滤、排序等）
5. 将处理后的数据保存为结构化的CSV文件

## 文件说明

- `t10_web_scraper.py` - 基础网络爬虫程序，从在线网站抓取数据
- `t10_web_scraper_local.py` - 本地版爬虫程序，从本地HTML文件抓取数据
- `test_file/sample_quotes.html` - 用于本地测试的HTML示例文件

## 使用方法

### 安装依赖

在运行程序前，请确保已安装所需的Python库：

```bash
pip install requests beautifulsoup4
```

### 在线爬虫版本

运行在线爬虫程序，从网络抓取名言数据：

```bash
python t10_web_scraper.py
```

程序将从`quotes.toscrape.com`网站抓取名言数据，并保存到`output/t10_quotes.csv`文件中。

### 本地爬虫版本

如果你没有网络连接或想在本地练习，可以运行本地版本：

```bash
python t10_web_scraper_local.py
```

程序将从`test_file/sample_quotes.html`文件中提取数据，并生成三个不同的CSV文件：
- `output/t10_local_quotes.csv` - 按作者排序的所有名言
- `output/t10_wisdom_quotes.csv` - 只包含"智慧"标签的名言
- `output/t10_quotes_by_length.csv` - 按名言长度排序的所有名言

## 练习任务

1. 运行基础版爬虫，观察结果
2. 修改程序，实现以下功能：
   - 抓取多个页面的数据（提示：网站有分页功能）
   - 添加更多数据过滤或处理功能（如按作者分组、按标签筛选等）
   - 增强错误处理和日志记录
3. 尝试解析不同结构的HTML文件或抓取不同网站的数据（注意遵守网站的robots.txt规则和使用条款）

## 知识点

### HTTP请求基础
- requests库的基本用法
- 处理不同的HTTP状态码
- 设置请求头（User-Agent等）
- 处理网络超时和连接错误

### HTML解析
- BeautifulSoup库的基本用法
- 使用选择器（CSS选择器、XPath等）定位元素
- 提取元素的文本、属性和嵌套内容
- 处理不同类型的HTML结构

### 数据处理与存储
- 数据清洗（去除空白字符、特殊字符等）
- 数据结构化（列表、字典等）
- 使用CSV模块保存数据
- 文件操作和异常处理

## 注意事项

- 网络爬虫应当遵守网站的robots.txt规则和使用条款
- 避免频繁请求同一网站，可能会被封IP
- 在实际应用中，应当添加适当的延迟（如使用time.sleep()）
- 处理大量数据时，考虑使用数据库而非CSV文件存储