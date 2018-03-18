


myList = []
sublist = []
for n in range(3):
    for i in range(5):
        sublist.append(i)
    myList.append(sublist)
    sublist = []
print(myList)
