arr = list()
exp_num = 0
product_num = 0

exp_num = int(input('Введите количество экспертов'))
product_num = int(input('Введите количество видов ассортимента'))
rate = 0
buffer = list()
arr_str=0
arr_clm=list()
rate_mass=0
for i in range (exp_num):
    buffer.clear()
    sum=0
    for g in range(product_num):
        rate=float(input("Введите оценку "))
        buffer.append(rate)
        sum= sum+rate
    arr_str= arr_str+sum
    q = buffer.copy()
    arr.append(q)

for i in range (product_num):
    sum=0
    for g in range(exp_num):
        sum = sum+arr[g][i]
    rate_mass=float(sum/arr_str)

    arr_clm.append(rate_mass)
product_arr=list()
for g in range(product_num):
    product_arr.append(g+1)

for i in range(product_num-1):
        for j in range(product_num-i-1):
            if arr_clm[j] < arr_clm[j+1]:
                arr_clm[j], arr_clm[j+1] = arr_clm[j+1], arr_clm[j]
                supbuf =product_arr[j]
                product_arr[j] = product_arr[j+1]
                product_arr[j+1] = supbuf
print (arr_clm,product_arr)
