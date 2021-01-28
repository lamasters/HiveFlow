from flask import Flask
import sys, threading, time
from api_handler import APIHandler

ClientServer = Flask(__name__)
ApiServer = APIHandler()

api_index = {}

t_api = threading.Thread(target=ApiServer.handle_apis)
t_api.daemon = True

print("Getting API list")
for i in range(len(ApiServer.api_list)):
    api_name = ApiServer.api_list[i].name
    api_index[api_name] = i
print("List filled")

@ClientServer.route('/')
def default():
    return "Connected!"

@ClientServer.route('/news')
def news():
    data = ApiServer.api_data[api_index['google']]
    return data

t_api.start()
ClientServer.run()