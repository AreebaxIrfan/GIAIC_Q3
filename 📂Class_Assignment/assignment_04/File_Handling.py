#file handling in python
#open a file
#read a file(r)
#write a file(w)
#append a file(a)

file = open("file.txt", "w")
file.write("Hello World")
file.close()

lines = ["Areeba\n", "Irfan\n", "Python\n"]
file = open("new_file.txt","a")
file.writelines(lines)
file.close()
##Example

with open ('demo.txt','w') as file:
    file.write('Python File Handling\n')
    file.write('Line 2\n')

with open('demo.txt','r') as file:
    print('Content.')
    print(file.read())
with open ('demo.txt','a')as file:
    file.write('Appended Line\n')
with open('demo.txt','rt')as file:
    file.seek(0)
    print('First line',file.readline())