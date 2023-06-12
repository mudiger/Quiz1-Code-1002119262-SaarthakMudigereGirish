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
        if not row:
            system = None
        else:
            # Access row values
            for i in row:
                # Assuming the table has columns named 'column1', 'column2', and 'column3'
                salpics.append(i)
    return render_template("uniqueid.html", id=id, salpics=salpics, system=system)

@app.route("/range/", methods=['GET', 'POST'])
def range():
    min = ""
    max = ""
    system = ""
    salpics = []
    seat = []
    if request.method == "POST":
        min = request.form['min']
        max = request.form['max']
        seat =  request.form['seat']
        if range is not None:
            # Execute a simple select query
            query = "SELECT name, seat, notes, pic FROM dbo.q1c WHERE row BETWEEN ? AND ? "
            cursor.execute(query, min, max)
        else:
            query = "SELECT name, seat, notes, pic FROM dbo.q1c WHERE seat=?"
            cursor.execute(query, seat)
        # Fetch the first row from the result set
        row = cursor.fetchall()
        print(query, min, max)
        if row is None:
            system = None
        else:
            for i in row:
                salpics.append(i)
    return render_template("range.html", range=range, salpics=salpics, system=system)


@app.route("/remove/", methods=['GET', 'POST'])
def remove():
    name = ""
    salpics = []
    system = ""
    if request.method == "POST":
        name = request.form.get('name')

        # Execute a query
        query = "SELECT * FROM dbo.q1c WHERE name=?"
        cursor.execute(query, name)

        # Fetch a single row
        row = cursor.fetchone()
        print(row)
        if row is None:
            system = None
        else:
            # Access row values
            for i in range(len(row)):
                # Assuming the table has columns named 'column1', 'column2', and 'column3'
                salpics.append(row[i])

        query = "DELETE FROM dbo.q1c WHERE name = ?"
        cursor.execute(query, name)
        conn.commit()

    return render_template("remove.html", name=name, salpics=salpics, system=system)


@app.route("/add/", methods=['GET', 'POST'])
def add():
    name = ""
    salpics = []
    if request.method == "POST":
        name = request.form.get('name')
        row = request.form.get('row')
        seat = request.form.get('seat')
        pic = request.form.get('pic')
        notes = request.form.get('notes')

        # Execute a query
        query = "INSERT INTO dbo.q1c VALUES (?,?,?,?,?)"
        cursor.execute(query, name, row, seat, pic, notes)
        conn.commit()

        query = "SELECT * FROM dbo.q1c WHERE name=?"
        cursor.execute(query, name)

        # Fetch a single row
        row = cursor.fetchone()
        print(row)
        # Access row values
        for i in range(len(row)):
            # Assuming the table has columns named 'column1', 'column2', and 'column3'
            salpics.append(row[i])

    return render_template("add.html", salpics=salpics)


@app.route("/edit/", methods=['GET', 'POST'])
def edit():
    name = ""
    col = ""
    ele = ""
    if request.method == "POST":
        name = request.form.get('name')
        col = request.form.get('col')
        ele = request.form.get('ele')

        # Execute a simple select query
        query = "UPDATE dbo.q1c SET ?=? WHERE name=?"
        cursor.execute(query, col, ele, name)
        conn.commit()

    return render_template("edit.html", name=name, col=col, ele=ele)


if __name__ == "__main__":
    app.run(debug=True)
