'''
题目要求：编写一个文本分析程序，处理多个文本文件并生成分析报告。

要求：
1. 从指定目录读取所有.txt文件
2. 对每个文件进行以下分析：
   a. 统计总字数、总行数和总段落数
   b. 计算平均句子长度（按字数）
   c. 识别出现频率最高的前10个单词（排除常见停用词）
   d. 分析文本的情感倾向（正面/负面/中性）
3. 生成分析报告，包含：
   a. 每个文件的基本统计信息
   b. 所有文件的汇总统计
   c. 词频分析结果
   d. 情感分析结果
4. 将分析报告保存为结构化的CSV文件
5. 处理可能出现的异常情况（文件不存在、编码错误等）

问题列表：
1、如何读取指定目录下的所有.txt文件？
2、如何获取文件名，通过路径截取，还是通过file类有getname之类的函数？
3、re如何用来直接获取单词：re.findall(r'\bw+\b', text) ？ \b是什么意思，re除了前面学过的sub替换还有什么常用的功能？

知识点：
1. 读取指定目录下的所有.txt文件可以使用os.listdir()函数获取目录中的所有文件，然后通过文件扩展名筛选.txt文件。也可以使用os.walk()遍历子目录或使用glob模块的glob.glob("*.txt")方法直接匹配文件模式。

2. 获取文件名有两种主要方法：
   - 通过路径截取：使用os.path.basename(file_path)函数，它会返回路径中的文件名部分
   - 文件对象没有直接获取文件名的方法，文件名需要在打开文件前通过路径获取

3. 正则表达式的重要知识点：
   - \\b 是单词边界元字符，用于匹配单词的开始或结束位置，不消耗实际字符
   - re.findall(r\'\\bw+\\b\', text) 中的 \\b 确保只匹配完整单词，w+ 匹配一个或多个字母
   - re模块的常用功能除了sub()替换外，还有：
     * findall(): 返回所有匹配的字符串列表
     * search(): 查找第一个匹配项并返回Match对象
     * match(): 从字符串开头匹配模式
     * split(): 使用正则表达式分割字符串
     * compile(): 编译正则表达式模式以便重复使用

4. 代码中的正则表达式问题：
   - 统计单词字数使用 r\'[a-zA-Z]\' 只会匹配单个字母而非完整单词
   - 应该使用 r\'\\b[a-zA-Z]+\\b\' 来匹配完整单词
   - 段落识别使用 r\'\.\' 只匹配句点，不能准确识别段落，应考虑使用空行或多行模式

5. 数据结构使用：
   - 使用集合(set)存储停用词和情感词汇是高效的，因为查找操作时间复杂度为O(1)
   - 使用字典(dict)存储单词计数和分析结果便于快速访问和更新
   - sorted()函数的key参数使用lambda表达式实现自定义排序逻辑
'''

import os
import re
import csv
import traceback

# 常见英文停用词列表, {}默认是dict，但是像这样写代表只有key没有value，就代表是集合
STOP_WORDS = {
    "the", "and", "a", "to", "of", "in", "is", "that", "it", "with", "for", "as", "on", 
    "was", "be", "by", "at", "this", "an", "are", "not", "from", "but", "or", "have", 
    "had", "has", "i", "you", "he", "she", "they", "we", "it", "its", "my", "their", "our"
}

# 简单情感词典
POSITIVE_WORDS = {
    "good", "great", "excellent", "wonderful", "happy", "positive", "best", "love", 
    "beautiful", "nice", "amazing", "awesome", "fantastic", "perfect", "better"
}

NEGATIVE_WORDS = {
    "bad", "worst", "terrible", "horrible", "sad", "negative", "poor", "hate", 
    "awful", "wrong", "worse", "difficult", "hard", "problem", "fail"
}

#字段映射
FIELD_MAPPING={
    "file_name":"文件名",
    "total_words":"总字数",
    "total_line_counts":"总行数",
    "total_section_counts":"总段落数",
    "avg_line_lne":"平均句子长度",
    "emotion_trend":"情感倾向",
    "commonest_1":"最常见词1",
    "commonest_2":"最常见词2",
    "commonest_3":"最常见词3",
    "commonest_4":"最常见词4",
    "commonest_5":"最常见词5"
}



def analyze_file(file_path):
    """
    分析单个文本文件，返回分析结果
    
    参数：
    file_path -- 文本文件路径
    
    返回：
    dict -- 包含文件分析结果的字典
    """
    if not file_path:
        raise FileNotFoundError("请输入正确的文件路径")
    
    file_analyze_result={}
    line_count=0
    words_count={}
    with open(file_path,'r',encoding='utf-8') as file:
        for line in file:
            if line.strip(): #去除空行
                line_count+=1
                #1、通过正则匹配查询所有单词字数
                word_list = re.findall(r'[a-zA-Z]',line)
                if FIELD_MAPPING['total_words'] not in file_analyze_result.keys():
                    file_analyze_result[FIELD_MAPPING['total_words']]=0
                file_analyze_result[FIELD_MAPPING['total_words']]+=len(word_list)

                #2、通过正则匹配段落标记，计算总段落数
                secton_list = re.findall(r'\.',line)
                if FIELD_MAPPING['total_section_counts'] not in file_analyze_result.keys():
                    file_analyze_result[FIELD_MAPPING['total_section_counts']]=0
                file_analyze_result[FIELD_MAPPING['total_section_counts']]+=len(secton_list)

                #3、按照单词分隔，统计单词频率 ,以一个字母开头，后面跟上0个或多个字母或'或-，*代表0个或多个，+代表至少一个
                words_list = re.findall(r'[a-zA-Z][a-zA-Z\'\-]*',line)
                for words in words_list:
                    words=words.lower()
                    if words not in words_count.keys():
                        words_count[words]=0
                    words_count[words]+=1

        #按照出现频率降序排序,sorted返回的是一个list，如果是对map排序，那么返回的是list[元组]类型
        words_count=sorted(words_count.items(),key=lambda x: (-x[1],x[0]))

        #4、记录行数
        file_analyze_result[FIELD_MAPPING['total_line_counts']]=line_count

        #5、记录平均句子长度 总字数/总段落数
        file_analyze_result[FIELD_MAPPING['avg_line_lne']]=round( file_analyze_result[FIELD_MAPPING['total_words']]/file_analyze_result[FIELD_MAPPING['total_section_counts']] ,2)

        #6、记录最常见的前5个词汇，排除常见停用词
        i=0
        for word,_ in words_count:
            if i >=5:
                break
            if word not in STOP_WORDS:
                common_key=f"commonest_{i+1}"
                file_analyze_result[FIELD_MAPPING[common_key]]=word
                i+=1

        #7、遍历单词，判断情感倾向
        positive_counts=0
        negative_counts=0
        for word,counts in words_count:
            if word in POSITIVE_WORDS:
                positive_counts+=counts
            elif word in NEGATIVE_WORDS:
                negative_counts+=counts
    
        if positive_counts>negative_counts:
            file_analyze_result[FIELD_MAPPING['emotion_trend']]='正面'
        elif positive_counts<negative_counts:
            file_analyze_result[FIELD_MAPPING['emotion_trend']]='负面'
        else:
            file_analyze_result[FIELD_MAPPING['emotion_trend']]='中性'

        return file_analyze_result






def analyze_directory(directory_path):
    """
    分析指定目录中的所有.txt文件，生成分析报告
    
    参数：
    directory_path -- 目录路径
    
    返回：
    dict -- 包含所有文件分析结果和汇总信息的字典
    """
    # 在这里实现文件分析逻辑
    if not directory_path:
        raise FileNotFoundError("请输入正确的文件夹路径")
    
    #先用dict来记录每个文件的每项统计
    analyze_result={}
    file_list = os.listdir(directory_path)
    for file_path in file_list:
        file_name = os.path.basename(file_path)
        analyze_result[file_name]=analyze_file(f'{directory_path}\\\\{file_path}')
    
    return analyze_result
        


def generate_report(analysis_results, output_file):
    """
    将分析结果写入CSV文件
    
    参数：
    analysis_results -- 分析结果字典
    output_file -- 输出CSV文件路径
    
    返回：
    bool -- 操作成功返回True，否则抛出异常
    """
    # 在这里实现报告生成逻辑
    if not output_file:
        raise FileNotFoundError("请输入正确的文件路径")
    if not isinstance(analysis_results,dict):
        raise TypeError("请传入分析结果的字典类型")
    with open(output_file,'w',newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        #写入表头
        writer.writerow(FIELD_MAPPING.values())
        for file_name,results in analysis_results.items():
            rows=[]
            rows.append(file_name)
            for key in FIELD_MAPPING.keys():
                if key!="file_name":
                    rows.append(results[FIELD_MAPPING[key]])
            writer.writerow(rows)
            


if __name__ == "__main__":
    # 测试目录和输出文件路径
    test_directory = ".\\test_file\\text_samples"
    output_file_path = ".\\output\\t8_text_analysis_report.csv"
    
    try:
        # 分析文件
        results = analyze_directory(test_directory)
        
        # 生成报告
        if generate_report(results, output_file_path):
            print(f"成功分析文本文件并生成报告：{output_file_path}")
            
    except FileNotFoundError as e:
        print(f"错误：找不到文件或目录 - {str(e)}")
        traceback.print_exc()
    except UnicodeDecodeError as e:
        print(f"错误：文件编码问题 - {str(e)}")
        traceback.print_exc()
    except Exception as e:
        print(f"发生未预期的错误：{str(e)}")
        import traceback
        traceback.print_exc()
