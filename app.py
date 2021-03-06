from flask import Flask, jsonify, request
from dotenv import load_dotenv
load_dotenv()
import os
# from flaskext.mysql import MySQL
from markupsafe import escape
from config.database import mysql        # config/database.py
from routes.users import app_user        # routes/users.py

app = Flask(__name__)

### MySQL configuration
# mysql = MySQL()
app.config['MYSQL_DATABASE_USER']     = os.getenv("DB_USER")
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("DB_PASS")
app.config['MYSQL_DATABASE_DB']       = os.getenv("DB_NAME")
app.config['MYSQL_DATABASE_HOST']     = os.getenv("DB_HOST")
mysql.init_app(app)

### register blueprints
app.register_blueprint(app_user)

@app.route("/")
def hello_world():
  x = {
    "message" : "Hello World",
    "code" : 200
  }
  return jsonify({"data": x})

@app.route("/api/register", methods = ['POST', "GET"])
def register():
  if request.method == 'GET':
    return jsonify("get register")

  if request.method == 'POST':
    """
    New user will register here
    * submit json data (example) @via CURL
      {
          "firstname" : "John",
          "email"     : "john@email.com"
      }
    """
    regdata   = request.get_json(force=True)
    data      = {
      "data"    : regdata,
      "message" : "New user has been created!",
      "status"  : 200,
    }
    return jsonify(data)

@app.route("/api/login") # this is should POST method
def login():
  return jsonify("login here please!")

@app.route("/api/users")
def show_users():
  try:
    conn  = mysql.connect()
    csr   = conn.cursor()
    query = 'SELECT * FROM customers'  # my own table
    csr.execute(query) 
    ndata  = csr.fetchall()
    data    = {
      "data" : ndata,
      "status" : 200
    }
    return jsonify(data)
  except:
    return jsonify(
      data=[],
      status=404
    )

@app.route("/api/user/<username>")
def show_single_user(username):
  try:
    conn  = mysql.connect()
    csr   = conn.cursor()
    query = f'SELECT * FROM customers WHERE name="{escape(username)}"'
    count = csr.execute(query) # done
    # print(count)    # debug only
    data  = csr.fetchall()
    if count > 0:
      return jsonify(
        data=data,
        status=200
      )
  except:
    return jsonify(
      data=[],
      status=404
    )


@app.route("/api/db-products")
def get_products():
  try:
    conn  = mysql.connect()
    csr   = conn.cursor()
    csr.execute('SELECT * FROM products')
    data  = csr.fetchall()
    return jsonify(
      data=data,
      status=200
    )
    # return jsonify(f"data : {data}")
  except:
    return jsonify(
      data=[],
      status=404
    )