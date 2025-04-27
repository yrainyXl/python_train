# 题目要求：编写一个函数，接收一个字符串作为输入，
# 将字符串中的单词按长度从短到长排序，如果长度相同则按字母顺序排序，
# 最后返回排序后的字符串。

# 知识点：
# 1. split() 方法：
#    - 将字符串按空格分割成单词列表
#    - 不指定分隔符时默认按任意空白字符（空格、制表符、换行符等）分隔
#    - 返回一个字符串列表
# 
# 2. 排序相关：
#    - sort() 方法：在原地对列表进行排序，直接修改原列表
#    - sorted() 函数：返回一个新的已排序列表，不改变原列表
#    - key参数：指定排序依据的函数，该函数会应用到每个元素上
# 
# 3. lambda与多条件排序：
#    - lambda函数：用于创建简单的匿名函数，格式：lambda 参数: 返回值
#    - 多条件排序原理：key函数返回元组(tuple)，Python会按元组元素顺序逐个比较
#    - 示例：key=lambda str: (len(str), str)
#      * 首先按len(str)比较长度
#      * 当长度相同时，按str比较字符串本身
# 
# 4. 元组比较机制：
#    - Python按元组元素从左到右逐个比较
#    - 只有当前一个元素相等时，才会比较下一个元素
#    - 示例：(2, "apple") < (2, "banana") 为True，因为长度相同时比较字符串
#    - 这种机制使得多条件排序非常直观和简洁
# 
# 5. join() 方法：
#    - 用指定的分隔符将字符串列表中的元素连接成一个字符串
#    - 语法：分隔符.join(列表)
#    - 示例：" ".join(["a", "b"]) 返回 "a b"


def sort_words(text):
    if not text.strip():
        return ""
    # 在这里实现你的代码
    words_list = text.split()
    sorted_words =  sorted(words_list,key=lambda str: (len(str),str))
    return " ".join(sorted_words)

if __name__ == "__main__":
    # 测试用例
    test_string = input("请输入一个字符串（单词之间用空格分隔）：")
    result = sort_words(test_string) 
    print(f"排序后的结果：{result}")

# 示例输入："python is an amazing programming language"
# 预期输出："an is python amazing language programming"