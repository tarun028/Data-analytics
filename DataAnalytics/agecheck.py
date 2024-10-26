name= input("What is your name? ")
age = int(input("your age? "))

yearsTo50 = 50 - age

if yearsTo50>0:
    print("Hello "+name+" you will be 50 in "+str(yearsTo50)+" years") 
else:
        print("Hello "+name+" your were "+age+str(-yearsTo50)) 
print("bye")