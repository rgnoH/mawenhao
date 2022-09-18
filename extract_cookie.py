import re

f = open('cookies.txt', 'r', encoding='utf-8')
context = f.read()
f.close()

pattern = re.compile(r'([^\t]+?)\t.*?Medium')
keys = pattern.findall(context)
print(keys)
print(len(keys))

result= ""

for key in keys:
    pos = context.find(key) + len(key)
    value = ""
    for i in range(pos + 1, len(context)):
        if context[i] != '\t':
            value += context[i]
        else:
            break
    result += '"' + key + '" : "' + value + '",\n'

f = open('cookies_dict.txt', 'w', encoding='utf-8')
f.write(result)
f.close()