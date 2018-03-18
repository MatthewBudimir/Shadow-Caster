def reverseInt(x):
    if x>9:
        small = x % 10
        dec = 0;
        while(10**dec<x):
            dec = dec + 1
        print("Size: " + str(dec))
        x = (x-small)/10
        small = small*(10**(dec-1))
        print("Hello! " + str(x))
        return (small + reverseInt(x))
    else:
        return x


print(reverseInt(1234))
