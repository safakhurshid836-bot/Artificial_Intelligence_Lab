var="""!@#$%^&*(){}[]:;\"'|\/-+?_=,<>"""
data= "MYname !$ $@fa"
print(data)

for i in data:
    if i not in var:
        print(i,end="")


print(f'')# to add space

spec_char="""!@#$%^&*(){}[]:;\"'|\/-+?_=,<>"""
user=input("Enter a string to remove special characters:")
for char in spec_char:
    user=user.replace(char,"")
print("String after removing special characters:",user)