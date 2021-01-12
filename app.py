# -*- coding: utf-8 -*-
######################################################################
#
# flask路由控制
#
# @app.py
#
######################################################################
from flask import Flask, render_template, request, redirect, session, json, url_for
from flask import current_app
import chat_bot

app = Flask(__name__)



@app.route('/')
def index():
    return render_template("index2.html")

handler = chat_bot.ChatBotGraph()
@app.route('/answer',methods=['GET','POST'])#路由
def getdata():
    question = request.form.get("user")
    #handler = chat_bot.ChatBotGraph()
    answer = handler.chat_main(question)
    return answer;





if __name__ == '__main__':
    app.run(debug=True, port=8777)
