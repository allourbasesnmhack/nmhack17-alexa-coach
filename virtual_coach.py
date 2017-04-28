import logging
import boto3
from modules import goals, tips, user, activities, opportunities, ssml
from boto3.dynamodb.conditions import Key, Attr
#from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


userinfo_item = user.getUser('1');
count = activities.countactivities(userinfo_item['userid'])


@ask.launch
def start_skill():
    #welcome_message = render_template('welcome', first_name=item['first_name'], last_name=item['last_name'], openact=item['openact'], factfind=item['factfind'], suspects=item['suspects'], meals=item['meals'])
    welcome_message = render_template('welcome', first_name=userinfo_item['first_name'], last_name=userinfo_item['last_name'], openact=count)
    welcome_message += "Would you like to hear your goal progress?..."

    session.attributes['intent']=1

    return question(ssml.prepare(welcome_message))

@ask.intent("YesIntent")
def yes_intent():
    intent = session.attributes['intent']
    message=''
    if(intent == 1):
        message = goals.generateGoalsMessage(userinfo_item['userid'])
        message += render_template('tips_question')
        session.attributes['intent']=2
        card=goals.generateGoalCard(userinfo_item['userid'])
        return question(ssml.prepare(message)).simple_card(title='Goals', content=message)
    elif( intent == 2): #tips
        message = tips.generateTipsMessage(userinfo_item['userid'])
        #message = tips.generateTipsMessage("Hello")

        session.attributes['intent']=3
        message+=render_template("question_activities")

    elif(intent == 3): #activities
        message=activities.generateActivitiesMessage(userinfo_item['userid'])
        session.attributes['intent']=4
        message += render_template('question_opportunities')

    elif(intent == 4 ): #opportunities
        message=opportunities.generateOpportunitiesMessage(userinfo_item['userid'])
        session.attributes['intent']=5
        message+=render_template('good_bye')
        return stop_intent(message)
    else:
        return stop_intent(render_template('good_bye'))


    return question(ssml.prepare(message))

@ask.intent("NoIntent")
def no_intent():
    intent = session.attributes['intent']
    message=''
    if(intent==1):
        #message += render_template('tips_question')
        message=render_template("question_activities")
        session.attributes['intent']=3
    elif( intent == 2): #tips

        session.attributes['intent']=3
        message=render_template("question_activities")

    elif(intent == 3): #acitivite

        session.attributes['intent']=4
        message=render_template("question_opportunities")

    elif(intent == 4 ): #opertunities

        session.attributes['intent']=5
        return stop_intent(render_template('good_bye'))

    else:
        return stop_intent(render_template('good_bye'))

    return question(ssml.prepare(message))


@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
def stop_intent(message):
    if not message:
        message=render_template('good_bye')
    return statement(ssml.prepare(message))

@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    app.run(debug=True)
