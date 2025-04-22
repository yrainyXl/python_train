# 题目要求：编写生成斐波那契数列前n项的函数，实现迭代和递归两种方式，并比较执行效率
# 知识点：
# 1. 迭代与递归的区别
# 2. time模块计算执行时间
# 3. 异常处理try-except
# 4、斐波那契数列从第0项开始：0、1、1、2、3、5、8、13、21、34、……

# 学习到的知识点：
# 1.time函数： 
#    time.time()：返回自纪元以来的秒数（即，自1970年1月1日以来的秒数）。 
#   这里返回的是float类型，输出格式化：print("迭代耗时: %.4f秒" % (time.time() - start_time))
# 2.join函数： 
#    语法： 'sep'.join(list)，参数说明： sep：分隔符，可以为空；list：要连接的元素序列、字符串、元组、字典，且序列类型是字符串类型
#    示例：', '.join(['1','2','3','4'])，输出：'1, 2, 3, 4
# 3.map函数：
#    语法：map(function, iterable, ...)，参数说明：function：函数，iterable：一个或多个序列、字符串等
#    示例：map(str, [1,2,3,4])，输出：['1','2','3','4'] ,解释： 将列表中的元素转换为字符串序列
# 4.lru_cache函数：
#    作用：缓存函数的结果，避免重复计算，提高程序性能
#    导入： from functools import lru_cache
#    语法：@lru_cache(maxsize=None)，参数说明：maxsize：缓存的最大条目数，如果为None，则缓存大小没有限制





import time
from functools import lru_cache

def iterative_fib(num):
    if num < 0:
        raise ValueError("num need greater than 0")
    
    a,b=0,1
    fbi_lis=[]
    for _ in range(num):
        fbi_lis.append(a)
        a,b=b,a+b
    print("fbi list:", ', '.join(map(str,fbi_lis)))


@lru_cache(maxsize=None)
def recursive_fib(num):
    if num < 0:
        raise ValueError("num need greater than 1")
    elif num<=1: # 第0项是0，第1项是1，所以可以这样简写
        return num
    return recursive_fib(num-1) + recursive_fib(num-2)
        

if __name__=="__main__":
    n=(int(input("input a num : ")))
    # 统计迭代耗时
    start_time = time.time()
    iter_result = iterative_fib(n)
    print(f"迭代耗时: {time.time() - start_time:.4f}秒")
    
    # 统计递归耗时
    print("===================")
    try:
        start_time = time.time()
        recur_list = [recursive_fib(i) for i in range(0, n)]
        print(f"递归结果: {', '.join(map(str, recur_list))}")
        print(f"递归耗时: {time.time() - start_time:.4f}秒")
    except ValueError as e:
        print(f"错误: {e}")
    finally:
        recursive_fib.cache_clear()