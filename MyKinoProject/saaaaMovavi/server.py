
import random
from flask import Flask, request, render_template, redirect, session, jsonify
from flask_cors import CORS, cross_origin
import sqlite3

app = Flask(__name__)
app.secret_key = '%TGHUI8uyFGHI(*&^5rUIO9i*&^TRfvgbHNJKLKJnhgfDE3WedFGhjKOlIuyTRe4567ioP:liuytr56&8()IuGTfrEdsXcghuy6'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def get_rating():
    rating = []
    db = sqlite3.connect(r'/Users/movavi_school/Desktop/MyKinoProject/saaaaMovavi/MyDatabase/KinoProject.db')
    executor = db.cursor()
    executor.execute('SELECT login, sold_places FROM workers ORDER BY sold_places DESC LIMIT 10')
    data = executor.fetchall()
    for i in data:
        rating.append({'name': list(i)[0], 'sold_places': list(i)[1]})
    return rating


def get_films():
    info = []
    names = []
    descs = []
    db = sqlite3.connect(r'/Users/movavi_school/Desktop/MyKinoProject/saaaaMovavi/MyDatabase/KinoProject.db')
    executor = db.cursor()
    executor.execute(f"SELECT name FROM films")
    a = executor.fetchall()
    info.append(a)
    executor.execute(f"SELECT description FROM films")
    a = executor.fetchall()
    info.append(a)
    films = []
    for i in range(len(list(info[0]))):
        names.append(str(list(info[0][i])[0]))
        descs.append(str(list(info[1][i])[0]))
    films = [names, descs, len(names)]
    return films


def sessions():
    result = ''
    session_result = []
    db = sqlite3.connect(r'/Users/movavi_school/Desktop/MyKinoProject/saaaaMovavi/MyDatabase/KinoProject.db')
    executor = db.cursor()
    executor.execute(f"SELECT * FROM filmsession")
    result = executor.fetchall()
    for i in result:
        i = list(i)
        session_result.append({'sessionid': i[0],
                               'filmname': i[1],
                               'hallname': i[2],
                               'sessiontime': i[3]
                               })
    executor.close()
    return session_result


def processing_session_info(result):
    db = sqlite3.connect(r'/Users/movavi_school/Desktop/MyKinoProject/saaaaMovavi/MyDatabase/KinoProject.db')
    executor = db.cursor()
    all_session_info = []
    for i in result:
        session_info = []
        executor.execute(f"SELECT name FROM films WHERE id LIKE '{i['filmname']}'")
        session_info.append(i['sessionid'])
        session_info.append(list(executor.fetchall()[0])[0])
        executor.execute(f"SELECT naming FROM halls WHERE id LIKE '{i['hallname']}'")
        session_info.append(list(executor.fetchall()[0])[0])
        session_info.append(i['sessiontime'])
        executor.execute(f"SELECT description FROM films WHERE name LIKE '{session_info[1]}'")
        session_info.append(list(executor.fetchall()[0])[0])
        all_session_info.append(session_info)
    executor.close()
    return all_session_info


def create_account(data):
    db = sqlite3.connect(r'/Users/movavi_school/Desktop/MyKinoProject/saaaaMovavi/MyDatabase/KinoProject.db')
    executor = db.cursor()
    executor.execute(f'INSERT INTO workers (login, pass) VALUES ("{data[0]}", "{data[1]}")')
    db.commit()
    executor.close()


def create_moviee(data):
    db = sqlite3.connect(r'/Users/movavi_school/Desktop/MyKinoProject/saaaaMovavi/MyDatabase/KinoProject.db')
    executor = db.cursor()
    executor.execute(f'INSERT INTO films (name, description) VALUES ("{data[0]}", "{data[1]}")')
    db.commit()
    executor.close()


def checklap(data):
    conn = sqlite3.connect(r'/Users/movavi_school/Desktop/MyKinoProject/saaaaMovavi/MyDatabase/KinoProject.db')
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM workers WHERE login LIKE '{data[0]}' AND pass LIKE '{data[1]}'")

    a = cur.fetchall()
    if a:
        a = list(list(a)[0])[0]
        cur.close()
        if a:
            session['username'] = data[0]
            return [True, a]
        else:
            return False
    else:
        return False


@app.route('/')
def index():
    return render_template('index.html', data=processing_session_info(sessions()))


@app.route("/getdata", methods=["GET"])
@cross_origin()
def test():
    data = processing_session_info(sessions())
    return jsonify(data)


@app.route("/oplata", methods=["GET"])
def oplata():
    a = request.args.get('session')
    session['pokupai'] = a
    oplata_info = []
    zanatiye_mesta = []

    oplata_info.append(int(a))
    db = sqlite3.connect(
        r'/Users/movavi_school/Desktop/MyKinoProject/saaaaMovavi/MyDatabase/KinoProject.db')
    executor = db.cursor()
    executor.execute(f"SELECT * FROM filmsession WHERE id LIKE '{a}' ")
    s = executor.fetchall()
    s = list(s[0])
    executor.execute(f"SELECT name FROM films WHERE id LIKE '{s[1]}'")
    filmname = str(list(executor.fetchall()[0])[0])
    oplata_info.append(filmname)
    print(filmname)
    executor.execute(f"SELECT сapacity FROM halls WHERE id LIKE '{s[2]}'")
    capacity = int(list(executor.fetchall()[0])[0])
    print(capacity)
    oplata_info.append(capacity)
    oplata_info.append(s[3])
    executor.execute(f"SELECT number_of_place FROM bought_places WHERE idsession LIKE '{a}'")
    promezh = executor.fetchall()
    try:
        promezh = list(promezh[0])
    except Exception as error:
        promezh = []
    if promezh:
        for i in promezh:
            zanatiye_mesta.append(i)
    oplata_info.append(zanatiye_mesta)
    executor.close()
    return render_template('oplata.html', data=oplata_info)


@app.route('/oplatit', methods=['GET'])
def process():
    a = request.args.get("mesta")
    j = session['pokupai']
    print(a)
    data = [int(j), int(a)]
    session['mesto'] = a
    return render_template('oplation.html', data=data)


@app.route('/konec', methods=["POST"])
def konec():
    a = random.randint(0, 1)
    if a:
        db = sqlite3.connect(r'/Users/movavi_school/Desktop/MyKinoProject/saaaaMovavi/MyDatabase/KinoProject.db')
        executor = db.cursor()
        executor.execute(f'INSERT INTO bought_places (idsession, number_of_place, seller_id) VALUES ({session["pokupai"]},{session["mesto"]},{session["id"]})')
        executor.execute(f"UPDATE workers SET sold_places=sold_places+1 WHERE id = {session['id']}")
        db.commit()
        return render_template('otkaz.html')
    else:
        return render_template('uspex.html')


@app.route('/reg', methods=['POST'])
def reg():
    log = dict(request.form)['reglogin']
    passs = dict(request.form)['regpass']
    data = [log, passs]
    create_account(data)
    conn = sqlite3.connect(r'/Users/movavi_school/Desktop/MyKinoProject/saaaaMovavi/MyDatabase/KinoProject.db')
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM workers WHERE login LIKE '{data[0]}' AND pass LIKE '{data[1]}'")
    a = cur.fetchall()
    cur.close()
    if a:
        session['id'] = a
        return redirect('/')
    else:
        return redirect('/registration')


@app.route('/registration')
def regga():
    return render_template('registration.html')


@app.route('/login')
def loggin():
    return render_template('login.html')


@app.route('/rating')
def rating():
    return render_template('rating.html', data=get_rating())


@app.route('/loggin')
def logandpass():
    data = str(request.args['name'])
    passs = str(request.args['passw'])
    lap = [data, passs]
    if checklap(lap):
        session['id'] = checklap(lap)[1]
        return redirect('/')
    else:
        return redirect('/login')


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')


@app.route('/create_movie')
def create_movie():
    return render_template('create_movie.html')


@app.route('/createmovie', methods=["POST"])
def createmovie():
    log = dict(request.form)['moviename']
    passs = dict(request.form)['moviedescription']
    data = [log, passs]
    create_moviee(data)
    return redirect('/create_movie')


@app.route('/create_session')
def create_session():
    return render_template('create_session.html', data=list(get_films()))


@app.route('/createsession', methods=["POST"])
def createsession():
    film_para = dict(request.form)['filmlist']
    date = dict(request.form)['session_date']
    hall = dict(request.form)['hall_id']
    db = sqlite3.connect(r'/Users/movavi_school/Desktop/MyKinoProject/saaaaMovavi/MyDatabase/KinoProject.db')
    executor = db.cursor()
    executor.execute(f"SELECT id FROM films WHERE name LIKE '{film_para}'")
    a = int(list(executor.fetchall()[0])[0])
    executor.execute(f"INSERT INTO filmsession (filmid, hallid, time)  VALUES ('{a}', '{int(hall)}', '{date}')")
    db.commit()
    executor.close()
    return redirect('/create_session')


if __name__ == '__main__':
    app.run(port=3001, debug=True)
