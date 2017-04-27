import logging
import boto3
import goals
import tips
from boto3.dynamodb.conditions import Key, Attr
#from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
userinfo_table = dynamodb.Table('userinfo')
response = userinfo_table.get_item(
    Key={
        'userid': '1',
    }
)
userinfo_item = response['Item']


activities_table = dynamodb.Table('activities')
response = activities_table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('userid').eq('1'))
activities_items = response['Items']
# print activities_items
count = 0
for activity_item in activities_items:
    count = count + int(activity_item['count'])

@ask.on_session_started
def new_session():
    log.info('new session started')

@ask.launch
def start_skill():
    #welcome_message = render_template('welcome', first_name=item['first_name'], last_name=item['last_name'], openact=item['openact'], factfind=item['factfind'], suspects=item['suspects'], meals=item['meals'])
    welcome_message = render_template('welcome', first_name=userinfo_item['first_name'], last_name=userinfo_item['last_name'], openact=count)
    welcome_message += goals.generateGoalsMessage(userinfo_item['userid'])
     welcome_message += render_template('tips_question')

    session.attributtes['intent']=1

    return question(welcome_message)

@ask.intent("YesGoalsIntent")
def yes_intent():
    intent = session.attributes['intent']
    if( intent == 1){ #tips

        session.attributtes['intent']=2
        message=render_template("question_tip")
    }
    elif(intent == 2){ #acitivite

        session.attributtes['intent']=3
        message=render_template("question_activites")
    }
    elif(intent == 3 ){ #opertunities

        session.attributtes['intent']=4
        message=render_template("question_oppertunites")
    }
    else{
        message = render_template('good_bye')
    }

    return question(message)

@ask.intent("NoGoalsIntent")
def no_intent():
    intent = session.attributes['intent']
    if( intent == 1){ #tips

        session.attributtes['intent']=2
        message=render_template("question_tip")
    }
    elif(intent == 2){ #acitivite

        session.attributtes['intent']=3
        message=render_template("question_activites")
    }
    elif(intent == 3 ){ #opertunities

        session.attributtes['intent']=4
        message=render_template("question_oppertunites")
    }
    else{
        message = render_template('good_bye')
    }

    return question(message)


@ask.intent('AMAZON.CancelIntent')
@ask.intent('AMAZON.StopIntent')
@ask.session_ended
def session_ended():
    return "{}", 200


@ask.intent("YesGoalsIntent")
def yes_intent():
    print userinfo_item['userid']
    # tips_message = tips.generateTipsMessage(userinfo_item['userid'])
    tips_message = render_template('tips')
    return statement(tips_message)

if __name__ == '__main__':
    app.run(debug=True)
