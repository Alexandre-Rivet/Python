import csv
from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
#import requests
from mysql.connector import Error


app = Flask(__name__)

@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    return response

try:
    connection = mysql.connector.connect(host='AlexR.mysql.eu.pythonanywhere-services.com',
                                         database='AlexR$Gaz',
                                         user='AlexR',
                                         password='Raph&Alex123')
    mycursor = connection.cursor()
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
except Error as e:
    print("Error while connecting to MySQL", e)

mycursor.execute("CREATE TABLE IF NOT EXISTS csvremplace (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(20), message VARCHAR(255))")

@app.route('/')
def home():
    return 'Bienvenue !'

@app.route('/gaz', methods=['GET', 'POST'])
def save_gazouille():
    """page pour envoyer des messages"""
    if request.method == 'POST':
        print (request.form)
        if len(request.form["user-text"]) < 281:
            if request.form["user-text"] not in "barre":
                dump_to_csv(request.form)
                return redirect(url_for('timeline'))
    return render_template('formulaire.html')

@app.route('/timeline', methods= ['GET'])
def timeline():
    gaz = parse_from_db()
    return render_template('timeline.html', gaz= gaz)

@app.route('/timeline/<userName>/', methods=['GET'])
def GazUser(userName):
    newGaz = []
    gaz = parse_from_db()

    for p in gaz:
        if p.get('user') == userName:
            newGaz.append(p)
    return render_template('timeline.html', gaz= newGaz)

def parse_from_db():
    gaz = []
    with open('./gazouilles.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            gaz.append({"user":row[0], "text":row[1]})
    return gaz
#    mycursor.execute("SELECT * FROM csvremplace")
#    myresult = mycursor.fetchone()
#    print(myresult)

def dump_to_csv(d):
    donnees = [d["user-name"],d["user-text"] ]
    with open('./gazouilles.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(donnees)

if (connection.is_connected()):
    cursor.close()
    connection.close()
    print("MySQL connection is closed")