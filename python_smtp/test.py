import time
a = 1
start = time.time()

for i in range(10000000):
    a += i

print(a)
print(time.time() - start)