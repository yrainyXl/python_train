# 题目要求：编写一个函数，从指定的文本文件中读取内容，统计每个单词出现的次数，
# 并按照出现频率从高到低排序输出结果。如果频率相同，则按照字母顺序排序。
# 注意：单词不区分大小写，标点符号和数字应该被忽略。

# 知识点：
# 1. 文件操作：
#    - open() 函数：打开文件，返回文件对象
#      * 常用模式：'r'（只读）, 'w'（写入）, 'a'（追加）, 'b'（二进制）
#      * encoding参数：指定文件编码，如'UTF-8'
#    - with 语句：自动管理文件资源，确保文件正确关闭，避免资源泄露
#    - read() 方法：一次性读取整个文件内容为字符串，适用于小文件
#    - readlines() 方法：一次性读取所有行到列表，每行作为一个元素
#    - for line in file：逐行读取，内存效率更高，适用于大文件
# 
# 2. 字符串处理：
#    - lower() 方法：将字符串转换为小写，用于不区分大小写的比较
#    - split() 方法：将字符串分割成单词列表，默认以空白字符分割
#    - strip() 方法：去除字符串首尾的空白字符（空格、换行、制表符等）
#    - isalpha() 方法：判断字符串是否只包含字母（不含数字和符号）
#    - 正则表达式处理：
#      * re.sub(pattern, repl, string)：替换匹配的文本
#      * r'[^a-zA-Z\s+]'：匹配非字母和非空白字符的正则表达式
#      * 其他方法：str.translate()配合str.maketrans()也可实现字符替换
# 
# 3. 字典操作：
#    - dict[key] = value：直接设置键值对，如果键不存在则新建
#    - dict.get(key, default)：安全获取值，键不存在返回默认值而不是报错
#    - dict.items()：返回可遍历的(键, 值)元组列表，常用于字典遍历
#    - 字典计数：使用get(key,0)+1是统计频率的常用模式
# 
# 4. 排序和多条件排序：
#    - sorted() 函数：返回新的排序列表，原序列不变
#    - key 参数：指定排序依据的函数，会应用到每个元素上
#    - reverse 参数：True为降序，False为升序（默认）
#    - lambda表达式：用于创建简单的匿名函数
#      * 语法：lambda 参数: 返回值
#      * 示例：lambda x: (-x[1], x[0]) 返回包含两个排序键的元组
#    - 多条件排序技巧：
#      * 返回元组实现多条件：(-x[1], x[0])
#      * 负号实现降序：-x[1]
#      * 当第一个条件相等时，按第二个条件排序
# 
# 5. 异常处理：
#    - try-except 结构：捕获和处理特定类型的异常
#    - FileNotFoundError：文件不存在时的异常
#    - with语句：确保文件正确关闭，即使发生异常

import re

def count_words(file_path):
    """
    统计文件中单词出现的次数
    :param file_path: 文件路径
    :return: 按频率降序排序的单词列表，每个元素为(单词, 出现次数)的元组
    """
    # 在这里实现你的代码
    if not file_path:
        raise FileNotFoundError("请传入正确的文件路径")
    
    word_dict={}
    with open(file_path,'r',encoding='UTF-8') as file:
        for line in file: 
            #这里怎么正确的从str中读取出单词，如何忽略掉标点符号？ 这里通过正则替换掉非字母的特殊字符，并保留空格
            str_line = re.sub(r'[^a-zA-Z\s+]',' ',line)
            word_list = str_line.split()
            for word in word_list:
                word = word.lower()
                word_dict[word] = word_dict.get(word,0)+1 #向dict添加词典，并记录频率
    
    # 在map键值对中，实现多条件排序：
    # 1. x[1]表示单词出现的次数（频率），-x[1]实现降序排序
    # 2. x[0]表示单词本身，用于字母顺序排序
    return sorted(word_dict.items(), key=lambda x: (-x[1], x[0]))


if __name__ == "__main__":
    # 测试用例
    
    file_path = ".\\test_file\\test.txt"
    try:
        result = count_words(file_path)
        print("\n单词统计结果：")
        for word, count in result:
            print(f"{word}: {count}次")
    except FileNotFoundError:
        print("错误：找不到指定的文件")
    except Exception as e:
        print(f"错误：{str(e)}")

# 示例文件内容：
# Python is amazing! Python is powerful.
# I love programming in Python.
# Python makes programming fun and easy.

# 预期输出：
# python: 4次
# is: 2次
# programming: 2次
# amazing: 1次
# and: 1次
# easy: 1次
# fun: 1次
# i: 1次
# in: 1次
# love: 1次
# makes: 1次
# powerful: 1次