from apispec import APISpec
from apispec_fromfile import FromFilePlugin, from_file
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify
from students.model import StudentSchema
from flasgger import Swagger

spec = APISpec(
    title="SJSU student Registration API",
    version="0.0.1",
    openapi_version="3.0.3",
    plugins=[
        # FromFilePlugin("resource"),
        FlaskPlugin(),
        MarshmallowPlugin()
    ],
)

app = Flask(__name__)
swagger = Swagger(app)

# API endpoints
# @from_file("spec/api.yml")
@app.route("/")
def index():
    return jsonify({"foo": "bar"})


with app.test_request_context():
    spec.path(view=index)


@app.route("/spec")
def get_apispec():
    return jsonify(spec.to_dict())


@app.route("/students")
def get_students():
    """
    Get all SJSU students.
    ---
    get:
     description: Get all students
     responses:
       200:
         content:
           application/json:
             schema: StudentSchema
    """
    student = dict(first_name="foo", last_name="Bar", sjsu_id="1234", email="foo@gmail.com")
    return StudentSchema().dump(student)


with app.test_request_context():
    spec.path(view=index)
    spec.path(view=get_students)
