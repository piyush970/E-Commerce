import json
# Key:value mapping
student = {
"Name" : "Peter",
"Roll_no" : "0090014",
"Grade" : "A",
"Age": 20
}
b = json.dumps(student)

print(b)
