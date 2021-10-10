### GraphQL Queries
``` javascript

Query
query studentById{
  students(id: "1"){
    name
  }
}

Output -
{
  "data": {
    "students": {
      "name": "John"
    }
  }
}
Query
query classById {
  classes(id: "1"){
    name
    students{
      id
      name
    }
  }
}

Output -
{
  "data": {
    "classes": {
      "name": "CMPE273",
      "students": []
    }
  }
}
Query
mutation createStudent{
  create_student(name: "jan"){
    name
  }
}

Output - 
{
  "data": {
    "create_student": {
      "name": "jan"
    }
  }
}
Query
mutation createClass{
  create_class(name: "CMPE202" ){
    name
  }
}

Output - 
{
  "data": {
    "create_class": {
      "name": "CMPE202"
    }
  }
}
Query
mutation updateClass{
  update_class(classid: "1", studentid: "2"){
    name
    students{
      id
      name
    }
  }
}

Output - 
{
  "data": {
    "update_class": {
      "name": "CMPE273",
      "students": [
        {
          "id": "2",
          "name": "Pam"
        }
      ]
    }
  }
```
