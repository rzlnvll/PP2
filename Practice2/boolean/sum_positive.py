n = int(input())
num = list(map(int, input().split()))
count = 0
for i in range(n):
    if num[i] > 0:       #boolean comparison operator
        count += 1
print(count)