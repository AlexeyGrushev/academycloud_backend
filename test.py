import json

s = "[1, 2, 3]"
list_s = json.loads(s)

print(type(s))
print(list_s)  # Вывод: [1, 2, 3]
print(type(list_s))  # Вывод: [1, 2, 3]
