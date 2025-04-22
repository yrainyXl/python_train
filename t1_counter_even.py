
# 统计1到10的偶数和
# 知识点：
# range()
# 语法：range(start, stop[, step])，参数说明：
# start: 计数从 start 开始。默认是从 0 开始。例如range（5）等价于range（0， 5）;
# stop: 计数到 stop 结束，但不包括 stop。例如：range（0， 5） 是[0, 1, 2, 3, 4]没有5
def counter_even(num):
    if(num==0):
        return 0
    sum=0
    for i in range(1,num+1):
        if(i%2==0):
            sum+=i
    return sum

if __name__=="__main__":
    print(counter_even(10))

    