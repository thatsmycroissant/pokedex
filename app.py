import sqlite3
import csv
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

connection = sqlite3.connect("POKEDEX.db")

statement = """CREATE TABLE IF NOT EXISTS Pokemon(
                    no INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    type_1 TEXT NOT NULL,
                    type_2 TEXT,
                    total INTEGER NOT NULL,
                    hp INTEGER NOT NULL,
                    attack INTEGER NOT NULL,
                    defense INTEGER NOT NULL,
                    sp_atk INTEGER NOT NULL,
                    sp_def INTEGER NOT NULL,
                    speed INTEGER NOT NULL,
                    generation INTEGER NOT NULL,
                    legendary INTEGER NOT NULL
            )"""

connection.execute(statement)



with open("Pokemon.csv") as infile:
    records = csv.reader(infile)
    header = next(records)
    
    connection.execute("DELETE FROM Pokemon")
    
    for record in records:
        statement = """INSERT OR IGNORE INTO Pokemon
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """
        record[-1] = record[-1] == 'TRUE'    
        connection.execute(statement, tuple(record))

    connection.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/option', methods = ['GET', 'POST'])
def option():
    if request.method == 'GET':
        return redirect('/')
    option = int(request.form['option'])
    return render_template(f'option{option}.html')

@app.route('/option1', methods = ['GET', 'POST'])
def option1():
    if request.method == 'GET':
        return render_template('option1.html')
    
    num = request.form['num']
    cursor = connection.execute("SELECT * FROM Pokemon WHERE no <= ?", (num,))
    return render_template('option1.html', header = header, cursor = cursor)

@app.route('/option2', methods = ['GET', 'POST'])
def option2():
    if request.method == 'GET':
        return render_template('option2.html')
    
    pokemon_type = request.form['pokemon_type']
    cursor = connection.execute("SELECT * FROM Pokemon WHERE type_1 = ? OR type_2 = ? LIMIT 1", (pokemon_type, pokemon_type))
    return render_template('option2.html', header = header, cursor = cursor)

@app.route('/option3', methods = ['GET', 'POST'])
def option3():
    if request.method == 'GET':
        return render_template('option3.html')
    
    stat = request.form['stat']
    cursor = connection.execute("SELECT * FROM Pokemon WHERE total = ?", (stat,))
    return render_template('option3.html', header = header, cursor = cursor)

@app.route('/option4', methods = ['GET', 'POST'])
def option4():
    if request.method == 'GET':
        return render_template('option4.html')
    
    atk = request.form['atk']
    deff = request.form['deff']
    speed = request.form['speed']
    cursor = connection.execute("SELECT * FROM Pokemon WHERE sp_atk >= ? AND sp_def >= ? AND speed >= ?", (atk, deff, speed))
    return render_template('option4.html', header = header, cursor = cursor)

@app.route('/option5', methods = ['GET', 'POST'])
def option5():
    exist = 0
    if request.method == 'GET':
        return render_template('option5.html')
    t1 = request.form['t1']
    t2 = request.form['t2']
    exist = 1 #Prevent showing No such Pokemon when first initiate option 5
    cursor = connection.execute("SELECT * FROM Pokemon WHERE type_1 = ? AND type_2 = ? AND legendary = 1", (t1,t2))
    result = cursor.fetchall()
    if result: 
        exist = 2
    return render_template('option5.html', header = header, result = result, exist = exist) #Pass result instead of cursor bc cursor's content is empty after .fetchall()

@app.route('/option6', methods = ['GET', 'POST'])
def option6():
    if request.method == 'GET':
        return render_template('option6.html')

    namee = request.form["namee"]
    type_1 = request.form["type_1"]
    type_2 = request.form["type_2"]
    total = int(request.form["total"])
    hp = int(request.form["hp"])
    attack = int(request.form["attack"])
    defense = int(request.form["defense"])
    sp_atk = int(request.form["sp_atk"])
    sp_def = int(request.form["sp_def"])
    speed = int(request.form["speed"])
    generation = int(request.form["generation"])
    legendary = int(request.form["legendary"])  
    
    info = (namee,type_1,type_2,total,hp,attack,defense,sp_atk,sp_def,speed,generation,legendary)
    query = """INSERT INTO Pokemon(name,type_1,type_2,total,hp,attack,defense,sp_atk,sp_def,speed,generation,legendary)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            """
    connection.execute(query,info)
    statement = 'SELECT Max(no) as no, name, type_1, type_2, total, hp, attack, defense, sp_atk, sp_def, speed, generation, legendary FROM Pokemon'
    cursor = connection.execute(statement)
    connection.commit()
    message = f'{namee} is succesfully added to Pokedex'
    return render_template('option6.html', header = header, cursor = cursor, message = message)

@app.route('/option7', methods = ['GET', 'POST'])
def option7():
    if request.method == 'GET':
        return render_template('option7.html')
    
    min_hp = request.form['min_hp']
    query = 'SELECT COUNT(type_1), type_1, hp FROM Pokemon WHERE hp > ? GROUP BY type_1 ORDER BY hp'
    cursor = connection.execute(query, (min_hp,))
    return render_template('option7.html', cursor = cursor)

if __name__ == '__main__':
    app.run()