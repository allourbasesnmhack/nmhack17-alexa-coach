import logging
import boto3
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
response = activities_table.scan(FilterExpression=boto3.dynamodb.conditions.Attr('userid').eq(1))
activities_items = response['Items']
print activities_items
count= 0
for activity_item in activities_items:
    count = count + activity_item['count']
    print count


@ask.launch
def start_skill():
    #welcome_message = render_template('welcome', first_name=item['first_name'], last_name=item['last_name'], openact=item['openact'], factfind=item['factfind'], suspects=item['suspects'], meals=item['meals'])
    welcome_message = render_template('welcome', first_name=userinfo_item['first_name'], last_name=userinfo_item['last_name'], openact=count)
    return question(welcome_message)

@ask.intent("YesGoalsIntent")
def yes_intent():
    if item['openact'] > 10:
        goals_message = render_template('goals_good', first_name=item['first_name'], openact=item['openact'])
    else:
        goals_message = render_template('goals_bad', first_name=item['first_name'], openact=item['openact'])
    # goals_message = render_template('tester')
    return question(goals_message)

@ask.intent("NoGoalsIntent")
def no_intent():
    no_message = render_template('good_bye')
    return statement(no_message)

if __name__ == '__main__':
    app.run(debug=True)
