from ariadne import ObjectType, QueryType, gql, make_executable_schema, MutationType
from ariadne.asgi import GraphQL
import resolver as resolve


# Define types using Schema Definition Language (https://graphql.org/learn/schema/)
# Wrapping string in gql function provides validation and better error traceback
type_defs = gql("""
type Query {
   students(id: ID!): Student
   classes(id: ID!): Class
   getAllStudents: [Student!]!
   getAllClasses: [Class!]!

}

type Student {
   id:ID!
   name: String!
}

type Class {
   id:ID!
   name: String!
   students: [Student!]
}

type Mutation{
    create_student(name: String!): Student
    create_class(name: String!): Class
    update_class(classid: String!,studentid: String! ): Class
}

input studentNameInput{
    name: String!
}

input classNameInput{
    name: String!
}

input updateClassNameInput{
    classid: ID!
    studentid: ID!
}


""")

# Map resolver functions to Query fields using QueryType
query = QueryType()
query.set_field('students', resolve.get_student)
query.set_field('classes',resolve.get_class)
query.set_field('getAllStudents',resolve.getAllStudents)
query.set_field('getAllClasses',resolve.getAllClasses)

mutation = MutationType()
mutation.set_field('create_student', resolve.create_student)
mutation.set_field('create_class', resolve.create_class)
mutation.set_field('update_class', resolve.update_class)

# Create executable GraphQL schema
schema = make_executable_schema(type_defs, query, mutation)

# Create an ASGI app using the schema, running in debug mode
app = GraphQL(schema, debug=True)