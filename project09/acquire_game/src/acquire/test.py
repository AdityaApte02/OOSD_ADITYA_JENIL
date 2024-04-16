letters = "ABCDEFGHI"
numbers = [1,2,3,4,5,6,7,8,9,10,11,12]

for letter in letters:
    for number in numbers:
         print("{\"row\":\""+letter+"\",\"column\":\""+str(number)+"\"},")
        
        