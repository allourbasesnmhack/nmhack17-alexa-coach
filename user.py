import boto3
from flask import render_template
from boto3.dynamodb.conditions import Key, Attr

def getUser(userid):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    userinfo_table = dynamodb.Table('userinfo')
    response = userinfo_table.get_item(
        Key={
            'userid': userid,
        }
    )
    userinfo_item = response['Item']
    return userinfo_item
