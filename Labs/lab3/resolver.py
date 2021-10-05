import random
from random import randint

students=[]
classes = []
students.append({"id":"1", "name": "John"})
students.append({"id":"2", "name": "Pam"})

classes.append({"id": "1", "name":"CMPE273", "students": []})

RAND_MAX = 1000
RAND_MIN = 3

def generate_id():
    return random.randint(RAND_MIN,RAND_MAX)

def get_student(_, _info, id):
    for student in students:
        if student.get('id')==id:
            return student

def create_student(_, _info,name):
    print(name)
    id=str(generate_id())
    students.append({"id":id, "name":name})
    return {"id":id, "name":name}

def get_class(_, _info, id):
    for cl in classes:
        if cl.get("id")==id:
            return cl

def create_class(_,_info,name):
    id=str(generate_id())
    classes.append({"id":id, "name":name, "students":[]})
    return {"id":id, "name":name, "students":[]}


def update_class(_, _info, classid, studentid):
    studentToAdd={}
    for student in students:
        if student.get('id')==studentid:
            studentToAdd=student
            break
    for i in range(len(classes)):
        if classes[i].get('id')==classid:
            currStudentList = classes[i].get('students')
            currStudentList.append(studentToAdd)
            classes[i].update({"students": currStudentList})          
            return classes[i]

def getAllStudents(_,info):
    return students

def getAllClasses(_, info):
    return classes
