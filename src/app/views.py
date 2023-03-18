from flask import Flask, request, redirect, send_from_directory, make_response
from app import app
from mysql.connector import connect, Error
import qrcode
import io
import os
import base64
import random

HOST_NAME = app.config['HOST_NAME']
HOST_PORT = '' if app.config['HOST_PORT'] == 80 else f':{app.config["HOST_PORT"]}'

adjs = []
nouns = []
path_to_this_file = os.path.dirname(__file__)
with open(os.path.join(path_to_this_file, 'data', 'adjectives.txt')) as f:
    adjs = f.read().splitlines()

with open(os.path.join(path_to_this_file, 'data', 'nouns.txt')) as f:
    nouns = f.read().splitlines()


#Get
@app.route('/')
def main():
    return send_from_directory('static', 'index.html')


@app.route('/pass')
def acceess():
    return send_from_directory('static', 'accessPage.html')


@app.route("/s/<alias>")
def get_extend(alias):
    select_query = f"""
    SELECT password, url FROM main
    WHERE alias = '{alias}'
    """

    with app.db_connection.cursor() as cursor:
        cursor.execute(select_query)
        fetch = cursor.fetchall()
        if (len(fetch) == 0): return "Нету"
        
        data = fetch[0]
        if len(data[0]) != 0:
            return redirect(f"http://{HOST_NAME}{HOST_PORT}/pass?alias={alias}")
        else:
            url = data[1]
            if url.find("http://") != 0 and url.find("https://") != 0:
                url = "http://" + url
            return redirect(url, code=301)

#Post

#рискованная штука, подвержена sql инъекциям !
@app.route('/extendUrl', methods=["POST"])
def extend():
    url = request.json['url']
    alias = request.json['alias']
    password = request.json['password']

    if alias == "":
        alias = random.choice(nouns)
        while len(f"http://{HOST_NAME}{HOST_PORT}/s/{alias}")<=len(url):
            alias = f"{random.choice(adjs)}_{alias}"
    
    while True:
        quer = f"SELECT COUNT(*) FROM main WHERE alias = '{alias}'"

        with app.db_connection.cursor() as cursor:
            cursor.execute(quer)
            a = int(cursor.fetchall()[0][0])
            if a == 0: 
                break
            else: 
                alias = f"{random.choice(adjs)}_{random.choice(nouns)}"

    insert_query = f"""
    INSERT INTO main (url, alias, password)
    VALUES ('{url}', '{alias}', '{password}')
    """

    with app.db_connection.cursor() as cursor:
        cursor.execute(insert_query)
        app.db_connection.commit()

    code = qrcode.make(f"http://{HOST_NAME}{HOST_PORT}/s/{alias}")
    buffer = io.BytesIO()
    code.save(buffer, format="png")
    qr_code = base64.b64encode(buffer.getvalue()).decode()
    html_img = f"data:image/png;base64,{qr_code}"
    
    return {"alias": f"http://{HOST_NAME}{HOST_PORT}/s/{alias}", "qrCode": html_img}


@app.route("/pass", methods=["POST"])
def submit():
    select_query = f"""
    SELECT password, url FROM main
    WHERE alias = '{request.json['alias']}'
    """

    with app.db_connection.cursor() as cursor:
        cursor.execute(select_query)
        data = cursor.fetchall()[0]

        if request.json['password'] == data[0]:
            return data[1]
        else: 
            return make_response("Wrong password", 418)
            