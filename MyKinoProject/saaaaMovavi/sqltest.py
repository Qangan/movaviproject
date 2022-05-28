import random
from flask import Flask, request, render_template, redirect, session, jsonify
from flask_cors import CORS, cross_origin
import sqlite3


conn = sqlite3.connect(
    r'/Users/movavi_school/Desktop/MyKinoProject/saaaaMovavi/MyDatabase/KinoProject.db')
cur = conn.cursor()
cur.execute(
    f"SELECT id FROM workers WHERE login LIKE '{data[0]}' AND pass LIKE '{data[1]}'")
a = cur.fetchall()
if a
    a = int(list(cur.fetchall()[0])[0])
    cur.close()
    if a:
        session['username'] = data[0]
        s = [True, a]
    else:
        return False
else:
    return False