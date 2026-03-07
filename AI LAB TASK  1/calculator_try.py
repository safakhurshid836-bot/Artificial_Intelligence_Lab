# caculator try 

user=input('Enter your calculation:')
user_list=list(user)

i = 0
result=0

while i in range(len(user_list)):

    if user_list[i] == '/':
        a=i-1
        b=i+1
        result=float(user_list[a])/float(user_list[b])
        user_list[a]=result
        del user_list[i]
        del user_list[i]
        i=0

    elif user_list[i] == '*':
        a=i-1
        b=i+1
        result=float(user_list[a])*float(user_list[b])
        user_list[a]=result
        del user_list[i]
        del user_list[i]
        i=0
    else:
        i+=1

i=0

while i in range(len(user_list)):

    if user_list[i] == '+':
        a=i-1
        b=i+1
        result=float(user_list[a])+float(user_list[b])
        user_list[a]=result
        del user_list[i]
        del user_list[i]
        i=0

    elif user_list[i] == '-':
        a=i-1
        b=i+1
        result=float(user_list[a])-float(user_list[b])
        user_list[a]=result
        del user_list[i]
        del user_list[i]
        i=0

    else:
         i += 1

print(f'{user}={user_list[0]}')
