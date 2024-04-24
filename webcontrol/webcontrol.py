from flask import Flask, request, render_template_string
import pymysql.cursors
import datetime

app = Flask(__name__)

## Credential
HOST = 'localhost' # MySQL server host DNS
PORT = 3306 # MySQL server port number
USER = 'greenhope' # MySQL account name
PASSWORD = 'Nahwals1234' # Password of the account
DB = 'greenhope' # DB name
TABLE = 'prototype' # table name
## Credential

def querygen(timestamp, sensor, measurement, value):
    return f"INSERT INTO {TABLE} (timestamp,sensor,measurement,value) VALUE('{timestamp}','{sensor}','{measurement}','{value}');"

# Initialize SQLite database
def post_stuff(inputtype, value):
    connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, port=PORT) # make a connection to MySQL server
    cursor = connection.cursor() 
    cursor.execute(querygen(datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), "user", inputtype, value))
    connection.commit()
    connection.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        field1 = request.form['input type']
        field2 = request.form['value']
        post_stuff(field1, field2)
    return render_template_string('''
        <html>
            <body>
                <form method="post">
                    Input type: <input type="text" name="input type"><br>
                    Value: <input type="text" name="value"><br>
                    <input type="submit" value="Submit">
                </form>
            </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

