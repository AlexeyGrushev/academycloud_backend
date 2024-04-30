import json


with open('app/lessons/templates/test/workpiece/task.json', "r") as f:
    templates = json.load(f)

print(templates)

# for section, commands in templates.items():
#     print(section)
#     print('\n'.join(commands))
