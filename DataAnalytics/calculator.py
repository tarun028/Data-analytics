# exp1=input("What is your expense? ")
# exp2=input("What is your expense? ")
# exp3=input("What is your expense? ")
# exp4=input("What is your expense? ")

# i=1
# while i<=10:
#     print(i)
#     i=i+1

exp=-1
total=0
maxexp=0
minexp=0
while exp!=0:
    exp=int(input("What is your expense? (type 0 to stop)"))
    total=total+exp
    if exp>maxexp:
        maxexp=exp

print("Your total exp is: "+str(total))
print("The maximum you spent is: "+str(maxexp))    

