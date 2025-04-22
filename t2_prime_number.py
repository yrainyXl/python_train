# 题目要求：编写一个函数，接受一个正整数n作为参数，
# 返回小于等于n的所有质数的列表，并统计个数。
# 质数是只能被1和自身整除的正整数。

# 知识点：
# 1、质数：只能被1和自身整除的正整数。且1不是质数
# 2、input() 函数： 接受用户输入的内容
# 3、int() 函数： 将字符串转换为整数
# 4、列表用 [] 表示，append() 函数： 向列表末尾添加元素，pop() 函数： 移除列表中的元素，len() 函数： 返回列表的长度
# 5、判断质数优化： 
#    如果一个数不是质数，那么它一定可以被2到它的平方根之间的某个数整除。
#    代码： for j in range(2, int(i**0.5) + 1):
# 6、幂运算： i**0.5 等价于 math.sqrt(i)，i**3 等价于 i * i * i


def prime_numbers(n):
    if(n<1):
        return []
    prime_list = []
    for i in range(2,n+1):
        
        if(is_prime(i)):
            prime_list.append(i)
    return prime_list
def is_prime(n):
    if(n<=1):
        return False
    for i in range(2,n):
        if(n%i==0):
            return False
    return True

if __name__=="__main__":
    n=(int(input("put a number: ")))
    prime_list=prime_numbers(n)
    print(f"prime numbers: {len(prime_list)}")
    for item in prime_list:
        print(f"{item} ")
