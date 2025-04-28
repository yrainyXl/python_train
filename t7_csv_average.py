# 题目要求：编写一个程序，读取一个CSV文件，统计每列的平均值，并将结果输出到新的CSV文件中。
# 
# 要求：
# 1. 输入文件为CSV格式，第一行为列名，后续行为数值数据
# 2. 计算每一列的平均值（不包括列名行）
# 3. 输出文件应包含两行：第一行为原始列名，第二行为对应的平均值
# 4. 处理可能出现的异常情况（文件不存在、格式错误、非数值数据等）
# 5. 保留平均值到小数点后两位
#
# 知识点：
# 1. CSV文件操作：
#    - csv模块：Python标准库，专门用于处理CSV文件
#      * csv.reader()：创建CSV读取器，返回可迭代对象
#      * csv.writer()：创建CSV写入器，用于写入CSV数据
#      * csv.DictReader()：以字典形式读取CSV，将列名作为键
#      * csv.DictWriter()：以字典形式写入CSV，需指定字段名
# 
# 2. 数据处理与计算：
#    - 类型转换：将CSV中的字符串转换为数值类型(float/int)
#    - 数值计算：求和、计算平均值等基本数学运算
#    - 格式化输出：使用round()或f-string控制小数位数
# 
# 3. 异常处理：
#    - FileNotFoundError：处理文件不存在的情况
#    - ValueError：处理数值转换错误
#    - try-except-else-finally结构：完整的异常处理流程
#    - 自定义异常信息：提供友好的错误提示

import csv


def calculate_average(input_file, output_file):

    
    try:
        num_dict = {}
        count_dict = {}
        avg_dict = {}
        
        # 读取CSV文件并计算每列的总和和计数
        with open(input_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for line in reader:
                for key, value in line.items():  # 修正：使用items()方法
                    try:
                        num_value = float(value)  # 尝试转换为浮点数
                        num_dict[key] = num_dict.setdefault(key, 0) + num_value  # 修正：正确使用setdefault
                        count_dict[key] = count_dict.setdefault(key, 0) + 1
                    except ValueError:
                        raise ValueError(f"列 '{key}' 中包含非数值数据: '{value}'")

        # 计算每列的平均值
        for key, value in num_dict.items():  # 修正：使用items()方法
            count = count_dict[key]
            avg_dict[key] = round(value/count, 2)

        # 将结果写入输出文件
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(num_dict.keys())  # 修正：使用keys()方法
            writer.writerow(avg_dict.values())  # 修正：使用values()方法
        
        return True  # 操作成功完成
        
    except FileNotFoundError:
        raise  # 重新抛出文件不存在异常
    except ValueError as e:
        raise  # 重新抛出值错误异常
    except Exception as e:
        raise Exception(f"处理CSV文件时发生错误: {str(e)}")





if __name__ == "__main__":
    # 测试文件路径
    input_file_path = ".\\test_file\\input.csv"
    output_file_path = ".\\test_file\\output.csv"
    
    try:
        result = calculate_average(input_file_path, output_file_path)
        if result:
            print(f"成功计算平均值并写入到 {output_file_path}")
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_file_path}")
    except ValueError as e:
        print(f"错误：{str(e)}")
    except Exception as e:
        print(f"发生未预期的错误：{str(e)}")


# ====================== 标准答案（参考实现） ======================
"""
以下是CSV平均值计算程序的标准实现方案，仅供参考：

def calculate_average_standard(input_file, output_file):
    标准实现：读取CSV文件，计算每列的平均值，并将结果写入新的CSV文件
    try:
        # 初始化数据结构：列名->总和，列名->计数
        column_sums = {}
        column_counts = {}
        
        # 读取CSV文件
        with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # 检查文件是否为空
            if not reader.fieldnames:
                raise ValueError("CSV文件格式错误：没有列名")
                
            # 遍历每一行数据
            for row in reader:
                for column, value in row.items():
                    try:
                        # 尝试转换为浮点数
                        num_value = float(value)
                        
                        # 累加总和和计数
                        if column not in column_sums:
                            column_sums[column] = 0
                            column_counts[column] = 0
                        
                        column_sums[column] += num_value
                        column_counts[column] += 1
                        
                    except ValueError:
                        raise ValueError(f"列 '{column}' 中包含非数值数据: '{value}'")
        
        # 检查是否有数据被处理
        if not column_sums:
            raise ValueError("CSV文件不包含有效数据行")
            
        # 计算每列的平均值
        averages = {}
        for column in column_sums:
            if column_counts[column] > 0:  # 防止除零错误
                averages[column] = round(column_sums[column] / column_counts[column], 2)
            else:
                averages[column] = 0.0
        
        # 写入结果到输出文件
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # 写入列名和平均值
            writer.writerow(averages.keys())
            writer.writerow(averages.values())
            
        return True
        
    except FileNotFoundError:
        raise  # 重新抛出文件不存在异常
    except ValueError as e:
        raise  # 重新抛出值错误异常
    except Exception as e:
        raise Exception(f"处理CSV文件时发生错误: {str(e)}")
"""

# ====================== 知识点总结 ======================
"""
1. CSV文件处理
   - csv模块是Python标准库，专门用于处理CSV文件
   - csv.DictReader：将CSV文件按行读取为字典，列名作为键
   - csv.reader/writer：按行读取/写入CSV数据
   - 文件操作最佳实践：使用with语句自动关闭文件资源
   - 编码处理：指定encoding='utf-8'确保正确处理中文等字符
   - newline=''参数：确保在不同操作系统下正确处理换行符

2. 字典操作技巧
   - setdefault方法：获取键值，如果键不存在则设置默认值
   - 字典的items()、keys()、values()方法：遍历字典的不同部分
   - 字典作为数据聚合工具：按列名分组统计数据

3. 异常处理机制
   - try-except结构：捕获并处理特定类型的异常
   - 异常传递：使用raise重新抛出异常，保持异常链
   - 异常分类处理：针对不同类型的异常提供不同的处理方式
   - 自定义异常信息：使用f-string提供详细的错误描述

4. 数据验证与转换
   - 类型转换：使用float()将字符串转换为浮点数
   - 数据验证：检查输入是否为有效数值，非数值则抛出异常
   - 防御性编程：检查除数是否为零，文件是否为空等边界情况
   - 数值格式化：使用round()函数控制小数位数

5. 代码结构与设计
   - 函数文档字符串：提供详细的函数说明、参数和返回值描述
   - 模块化设计：将CSV处理逻辑封装在独立函数中
   - 主程序结构：使用if __name__ == "__main__"区分模块导入和直接运行
   - 错误处理与用户反馈：提供友好的错误提示信息
"""