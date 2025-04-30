'''
题目要求：编写一个程序，读取学生信息JSON文件，处理数据并生成统计结果输出到新的JSON文件中。

要求：
1. 从提供的students.json文件中读取学生数据
2. 对数据进行以下处理：
   a. 计算每个学生的平均成绩，并添加到学生信息中
   b. 按平均成绩对学生进行排序（从高到低）
   c. 统计全班的学科平均分
   d. 找出每个学科的最高分和对应的学生
   e. 统计学生的爱好分布情况（每个爱好有多少学生）
3. 将处理后的结果写入新的JSON文件，包含以下内容：
   a. 排序后的学生列表（包含平均成绩）
   b. 全班各学科平均分
   c. 各学科最高分及获得者
   d. 爱好分布统计
4. 处理可能出现的异常情况（文件不存在、格式错误等）
5. JSON输出应当格式化，便于阅读

问题列表：
1、如何加载json文件，和加载json字符串有区别么
2、如何读取json中的数据，对象和列表的读取方式分别是什么
3、如何将列表转成json添加呢，比如这里的每个学科的最高分和学生，即要记录学科最高分，也要记录学生
4、如何将dict合并
5、如何将json类转换成json并输出到文档中 ，这里的indent=2的作用,ensure_ascii=False的作用
6、只有dict需要用items()，列表类型的直接用in即可
7、如何打印堆栈信息

知识点：
1. JSON文件加载：使用json.load()加载文件，使用json.loads()加载字符串。两者的区别在于load()直接从文件对象读取，而loads()从字符串读取。
2. JSON数据读取：对象(字典)通过键值访问如data["key"]或使用items()遍历；列表通过索引访问如data[0]或直接用for循环遍历。
3. 复杂JSON结构：可以通过嵌套字典来表示复杂数据，如subject_max_info[subject]={"score":score,"student":name}创建包含分数和学生名的结构。
4. 字典合并：可以使用{**dict1, **dict2}语法或dict1.update(dict2)方法合并字典。
5. JSON输出：使用json.dump()将数据写入文件，indent=2参数使输出格式化并缩进，ensure_ascii=False允许输出非ASCII字符(如中文)。
6. 集合遍历：字典需要使用items()方法获取键值对，而列表可以直接用for item in list_name遍历。
7. 堆栈信息打印：使用traceback.print_exc()可以打印完整的异常堆栈信息，帮助调试。
'''

import json
import traceback

def put_in_dict(obj, key, value):
    if not isinstance(obj, dict):
        raise TypeError("请传入字典类型数据")
    
    if not key:
        raise KeyError("请传入正确的key")
    
    if key not in obj:
        obj[key] = 0

    obj[key] += value

def process_student_data(input_file, output_file):
    """
    处理学生JSON数据，生成统计结果并输出到新文件
    
    参数：
    input_file -- 输入JSON文件路径
    output_file -- 输出JSON文件路径
    
    返回：
    bool -- 处理成功返回True，否则抛出异常
    """
    try:
        if not input_file:
            raise FileNotFoundError('请输入正确的文件地址')
        with open(input_file, 'r', encoding='utf-8') as file:
            students = json.load(file)

            student_avg = {}  # 统计每个学生的平均成绩
            subject_avg = {}  # 统计每科的平均成绩
            subject_max_info = {} # 统计每科的最高成绩和人
            hobbies_info = {} # 统计每个爱好有多少人
            subject_stedent_count = {}  # 每个科有多少学生，用于计算平均成绩
            student_subject_count = {} # 每个学生有多少门科
            for student in students:
                name = student['name']
                for subject, score in student['scores'].items():
                    if score: # 计算有效的成绩
                        score = int(score)
                        put_in_dict(student_avg, name, score)
                        put_in_dict(student_subject_count, name, 1)
                        put_in_dict(subject_avg, subject, score)
                        put_in_dict(subject_stedent_count, subject, 1)

                        if subject not in subject_max_info or subject_max_info[subject]['score'] < score:
                            subject_max_info[subject] = {'score': score, 'student': name}

                for hobby in student['hobbies']:
                    if hobby:
                        put_in_dict(hobbies_info, hobby, 1)

            # 计算每个人的平均成绩
            for student in students:
                name = student['name']
                if name in student_avg and name in student_subject_count:
                    student['average_score'] = round(student_avg[name] / student_subject_count[name], 2)
            
            # 按照平均分数降序排序
            students = sorted(students, key=lambda x: -(x.get('average_score', 0)))

            # 计算学科平均分
            for subject, score in subject_avg.items():
                subject_avg[subject] = round(score / subject_stedent_count[subject], 2)

            # 组合成最后的json
            merged_dict = {
                "students": students,
                "subject_averages": subject_avg,
                "subject_top_scores": subject_max_info,
                "hobby_distribution": hobbies_info
            }

            if not output_file:
                raise FileNotFoundError('请输入正确的文件地址')
            
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(merged_dict, file, indent=2, ensure_ascii=False)
                        
        return True  # 操作成功完成
        
    except FileNotFoundError:
        raise  # 重新抛出文件不存在异常
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON格式错误: {str(e)}")
    except Exception as e:
        raise Exception(f"处理JSON文件时发生错误: {str(e)}")


if __name__ == "__main__":
    # 测试文件路径
    input_file_path = ".\\test_file\\students.json"
    output_file_path = ".\\test_file\\statistics.json"
    
    try:
        result = process_student_data(input_file_path, output_file_path)
        if result:
            print(f"成功处理学生数据并写入到 {output_file_path}")
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_file_path}")
    except ValueError as e:
        print(f"错误：{str(e)}")
    except Exception as e:
        print(f"发生未预期的错误：{str(e)}")
        traceback.print_exc()