


with open("reading_test_PY.py", "r") as read_file:
    text_content = read_file.read()

print(text_content.find("def myfunc():"))
print(text_content.rfind("#end myfunc():"))


print(text_content[27:99])

#print(text_content)

