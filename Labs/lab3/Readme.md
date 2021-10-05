### GraphQL Queries
``` javascript

query studentById{
  students(id: "1"){
    name
  }
}

query classById {
  classes(id: "1"){
    name
    students{
      id
      name
    }
  }
}

mutation createStudent{
  create_student(name: "jan"){
    name
  }
}

mutation createClass{
  create_class(name: "CMPE202" ){
    name
  }
}

mutation updateClass{
  update_class(classid: "1", studentid: "2"){
    name
    students{
      id
      name
    }
  }
}
query getAllClasses{
  getAllClasses {
    id
    name
    students{
      id
      name
    }
    
  }
}

query getAllStudents{
  getAllStudents {
    id
    name
  }
}
```
