
temparray = [1,2,3]
temparraylen = len(temparray)

for x in range(temparraylen):
    for y in range( x +1, temparraylen):
        print(x,y)