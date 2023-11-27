from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient('mongodb+srv://iabd:iabdiabd@cluster0.dfaz5er.mongodb.net')

def lambda_handler(event, context):
    
    un_doc = client.sample_training.zips.find_one()   

    return {
        'statusCode': 200,
        'body': dumps(un_doc)
    }
