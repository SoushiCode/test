age=0
max=0
age=int(input())
while (age!=-1) and (10<=age<=90):
    age=int(input())
    if age>max:
        max=age
print(max)