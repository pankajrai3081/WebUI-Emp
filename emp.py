from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error
import logging

import webbrowser

app = Flask(__name__)

logging.basicConfig(filename='access.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

### DB connection
try:
    connection = mysql.connector.connect(host="localhost",
                                        user="root",
                                        password="rootroot",
                                        database="pankajdb")
    if connection.is_connected():
        cur = connection.cursor(dictionary=True)
        app.logger.info('DB connection success')
except Error as e:
    app.logger.info('DB connection Failed with error: ' + str(e))

#Login form
@app.route("/")
def login_page():
    app.logger.info('Web page opened for user login')
    return render_template("login_page.html")

#New account creation form
@app.route("/register_page",methods=['POST'])
def register_page():
    app.logger.info('Web page opened for new account creation and login for the existing users')
    return render_template("register_page.html")

# New account creation and validation
@app.route("/post_registration",methods=['POST'])
def post_registration():
    try:
        new_user_id = request.form['user_id']
        new_password = request.form['password']

        check_user = (new_user_id,)
        data_exist_sql = "SELECT user_id FROM user_details where user_id = %s"
        cur.execute(data_exist_sql, check_user)
        check_user1 = cur.fetchone()

        if check_user1:
            app.logger.info('Entered userid: ' + new_user_id + ' already present in the system')
            return render_template("back2.html")
        else:
            new_user_data = (new_user_id, new_password)
            new_user_sql_query = "INSERT INTO user_details values(%s,%s)"
            cur.execute(new_user_sql_query, new_user_data)
            connection.commit()
    except Error as e:
        app.logger.info('Error in new account creation and validation: ' + str(e))
    else:
        app.logger.info('New account created for user: ' + new_user_id)
        return render_template("back.html")

 #login validation
@app.route("/", methods=['POST'])
def login_validation():
    try:
        user_id = request.form['user_id']
        password = request.form['password']

        login_data = (user_id,password)

        login_sql_query = "select user_id,password from user_details where user_id = %s and password = %s"
        cur.execute(login_sql_query, login_data)
        cursor_login_set = cur.fetchone()
        if cursor_login_set:
            app.logger.info("User: " + user_id + " logged in successfully")
        else:
            app.logger.info("Login failed due to invalid user_id or password")
    except Error as e:
        app.logger.info('Error in login validation: ' + str(e))
    else:
        app.logger.info("Login successful")
        return render_template("login_result.html", login_result=cursor_login_set)

# Web page to display the result - Getting entered data by user
@app.route("/result_page", methods=['POST'])
def Final_Result():
    try:
        entered_emp_id = request.form['id_entered']
        entered_emp_name = request.form['name_entered']
        entered_emp_name_final = "%" + entered_emp_name + "%"
        entered_dep_id = request.form['dep_entered']

        if (entered_emp_name_final == '%%'):
            entered_emp_name_final = 'no_name_entered'

        user_data = (entered_emp_id, entered_dep_id, entered_emp_name_final)

        sql_query = "SELECT e.name Employee_name," \
                    "d.name Department " \
                    "FROM  employee e, " \
                    "department d " \
                    "WHERE e.department_id = d.department_id " \
                    "AND   ((e.employee_id =%s) OR (e.department_id = %s) OR (lower(e.name) like %s))"
        cur.execute(sql_query, user_data)
        cursor_result_set = cur.fetchall()
    except Error as e:
        app.logger.info("Error while executing the cursor and fetching the data with error: " + str(e))
    finally:
        app.logger.info(f"Employee details fetched successfully for Employee_id:{entered_emp_id}, Department_id:{entered_dep_id} and Employee_name:{entered_emp_name}")
        return render_template("result_page.html", result=cursor_result_set)










