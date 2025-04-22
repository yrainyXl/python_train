# 题目要求：找出前n个同时是斐波那契数和质数的数字
# 知识点：
# 1. 斐波那契数列生成（复用3fbi_list.py）
# 2. 质数判断（复用2prime_number.py）
# 3. 结果筛选与性能统计

from t2_prime_number import is_prime

def generate_fib_primes(n):
    """
    生成前n个既是斐波那契数又是质数的数字，因为斐波那契数的增长速度非常快，所以斐波那契数来筛选
    返回：（结果列表，迭代耗时，筛选耗时）
    """
    # 生成斐波那契数列
    fib_list = []
    a, b = 0, 1
    while len(fib_list) < n:
        if(is_prime(a)):
            fib_list.append(a)
        a,b=b,a+b
    return fib_list

if __name__=="__main__":
    n=(int(input("input a number ")))
    try:
        res_list=generate_fib_primes(n)
        print(f"fib primes list : { ', '.join(map(str,res_list)) }")
    except ValueError as e:
        print(f"generate_fib_primes error: {e}",e)