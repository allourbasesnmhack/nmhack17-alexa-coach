import logging
import boto3
from modules import goals, tips, user, activities
from boto3.dynamodb.conditions import Key, Attr
#from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


userinfo_item = user.getUser('1');
count = activities.countActivites(userinfo_item['userid'])


@ask.launch
def start_skill():
    #welcome_message = render_template('welcome', first_name=item['first_name'], last_name=item['last_name'], openact=item['openact'], factfind=item['factfind'], suspects=item['suspects'], meals=item['meals'])
    welcome_message = render_template('welcome', first_name=userinfo_item['first_name'], last_name=userinfo_item['last_name'], openact=count)
    welcome_message += goals.generateGoalsMessage(userinfo_item['userid'])
    welcome_message += render_template('tips_question')

    session.attributes['intent']=1

    return question(welcome_message)

@ask.intent("YesIntent")
def yes_intent():
    intent = session.attributes['intent']
    message=''
    if( intent == 1): #tips
        # message = tips.generateTipsMessage(userinfo_item['userid'])
        message = tips.generateTipsMessage("Hello")

        session.attributes['intent']=2
        message+=render_template("question_activites")

    elif(intent == 2): #acitivite
        message+=activities.generateActivitiesMessage(userinfo_item['userid'])
        session.attributes['intent']=3
        message+=render_template("question_oppertunites")

    elif(intent == 3 ): #opertunities

        session.attributes['intent']=4
        message += render_template('good_bye')

    else:
        message = render_template('good_bye')


    return question(message)

@ask.intent("NoIntent")
def no_intent():
    intent = session.attributes['intent']
    message=''
    if( intent == 1): #tips

        session.attributes['intent']=2
        message=render_template("question_activites")

    elif(intent == 2): #acitivite

        session.attributes['intent']=3
        message=render_template("question_oppertunites")

    elif(intent == 3 ): #opertunities

        session.attributes['intent']=4
        message = render_template('good_bye')

    else:
        message = render_template('good_bye')

    return question(message)


@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == '__main__':
    app.run(debug=True)
