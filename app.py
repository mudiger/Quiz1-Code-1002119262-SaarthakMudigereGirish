from flask import request
from flask import Flask
from flask import render_template
import pyodbc
import os
#from azure.storage.blob import BlobServiceClient

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

driver = '{ODBC Driver 17 for SQL Server}'
server = 'sqlserver-1002119262-saarthakmudigeregirish.database.windows.net'
database = 'DataBase-1002119262-SaarthakMudigereGirish'
username = 'saarthakmudigeregirish'
password = 'Hello123'

# Establish the connection
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')

# Create a cursor object
cursor = conn.cursor()
print(cursor)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/picture/", methods=['GET', 'POST'])
def picture():
    return render_template("picture.html")


@app.route("/uniqueid/", methods=['GET', 'POST'])
def uniqueid():
    id = ""
    salpics = []
    system = ""
    if request.method == "POST":
        id = request.form.get('id')

        # Execute a simple select query
        query = "SELECT name, seat, pic FROM dbo.q1c WHERE row=?"
        cursor.execute(query, id)

        # Fetch the first row from the result set
        row = cursor.fetchall()
        print(row)
        if not row:
            system = None
        else:
            # Access row values
            for i in range(len(row)):
                # Assuming the table has columns named 'column1', 'column2', and 'column3'
                salpics.append(row[i])
    return render_template("uniqueid.html", id=id, salpics=salpics, system=system)

'''


@app.route("/pic/", methods=['GET', 'POST'])
def pic():
    salpics = []

    # Execute a simple select query
    query = "SELECT * FROM dbo.q0c"
    cursor.execute(query)

    row = cursor.fetchall()
        # Fetch the first row from the result set

    print(row)
    for i in range(len(row)):
        # Assuming the table has columns named 'column1', 'column2', and 'column3'
        salpics.append(row[i])
        print(row[i])
    return render_template("table.html", salpics=salpics)

@app.route("/add/", methods=['GET', 'POST'])
def add():
    name = ""
    add = ""
    picture = ""
    system = ""
    if request.method == "POST":
        name = request.form['addname']
        add = request.files['add']

        query = "SELECT Picture FROM dbo.people WHERE name=?"
        cursor.execute(query, name)

        # Fetch the first row from the result set
        row = cursor.fetchone()
        if row is None:
            system = None
        else:
            url = upload(add, name)
            query = "UPDATE dbo.people SET Picture=? WHERE name = ?"
            cursor.execute(query, url, name)
            conn.commit()

            query = "SELECT Picture FROM dbo.people WHERE name=?"
            cursor.execute(query, name)

            # Fetch the first row from the result set
            row = cursor.fetchone()
            picture = row[0]

    return render_template("add.html", name=name, picture=picture, system=system)


def upload(file, name):
    account_url = "DefaultEndpointsProtocol=https;AccountName=storageaccount1002119262;AccountKey=3g3TqtLPd318jgDhHPM2llwevOb1jNHj3oN0BbaaZXiJk8T8k31aj+JIsPwL0RrPeKy28s2/mCGa+AStbbWoIQ==;EndpointSuffix=core.windows.net"
    blob_account_client = BlobServiceClient.from_connection_string(account_url)
    blob_client = blob_account_client.get_blob_client("assignment1-container-1002119262-saarthakmudigeregirish",name + ".jpg")
    blob_client.upload_blob(file, overwrite=True)
    return "https://storageaccount1002119262.blob.core.windows.net/assignment1-container-1002119262-saarthakmudigeregirish/" + name + ".jpg"


@app.route("/remove/", methods=['GET', 'POST'])
def remove():
    name = ""
    salpics = []
    system = ""
    if request.method == "POST":
        name = request.form.get('name')

        # Execute a query
        query = "SELECT * FROM dbo.people WHERE name=?"
        cursor.execute(query, name)

        # Fetch a single row
        row = cursor.fetchone()
        if row is None:
            system = None
        else:
            # Access row values
            for i in range(len(row)):
                # Assuming the table has columns named 'column1', 'column2', and 'column3'
                salpics.append(row[i])

        query = "DELETE FROM dbo.people WHERE name = ?"
        cursor.execute(query, name)
        conn.commit()

    return render_template("remove.html", name=name, salpics=salpics, system=system)


@app.route("/keyword/", methods=['GET', 'POST'])
def keyword():
    name = ""
    keyword = ""
    system = ""
    if request.method == "POST":
        name = request.form.get('name')
        keyword = request.form.get('keyword')

        query = "UPDATE dbo.people SET keywords=? WHERE name=?"
        cursor.execute(query, keyword, name)
        conn.commit()

        query = "SELECT keywords FROM dbo.people WHERE name=?"
        cursor.execute(query, name)

        # Fetch the first row from the result set
        row = cursor.fetchone()
        if row is not None:
            if row[0] is not None:
                keyword = row[0]
            else:
                keyword = None
        else:
            system = None

    return render_template("keyword.html", name=name, keyword=keyword, system=system)


@app.route("/salary/", methods=['GET', 'POST'])
def salary():
    name = ""
    salary = ""
    system = ""
    if request.method == "POST":
        name = request.form.get('name')
        salary = request.form.get('salary')

        query = "UPDATE dbo.people SET Salary=? WHERE name=?"
        cursor.execute(query, salary, name)
        conn.commit()

        query = "SELECT Salary FROM dbo.people WHERE name=?"
        cursor.execute(query, name)

        # Fetch the first row from the result set
        row = cursor.fetchone()
        if row is not None:
            if row[0] is not None:
                salary = row[0]
            else:
                salary = None
        else:
            system = None

    return render_template("salary.html", name=name, salary=salary, system=system)
'''

if __name__ == "__main__":
    app.run(debug=True)
