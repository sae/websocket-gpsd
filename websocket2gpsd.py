#!/usr/bin/env python

#simple server websocket to gpsd
#browser must open websocket then send a "poll" command, and parse a json response
#WebsocketServer from https://github.com/Pithikos/python-websocket-server/

import socket
import time
import threading
from websocket_server import WebsocketServer

host="127.0.0.1"
port=2947
ws_port=9001

# Called for every client connecting (after handshake)
def new_client(client, server):
	print("New client connected and was given id %d" % client['id'])
	server.send_message_to_all("Hey all, a new client has joined us")


# Called for every client disconnecting
def client_left(client, server):
	print("Client(%d) disconnected" % client['id'])


# Called when a client sends a message
def message_received(client, server, message):
    if (message=="poll"):
        server.send_message(client,poll);        
	#if len(message) > 200:
		#message = message[:200]+'..'
        #server.send_message(client,"OK");
	print("Client(%s) >> %s" % (client['address'], message))



server = WebsocketServer(ws_port,"0.0.0.0")
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
# Start a thread with the server -- that thread will then start one
# more thread for each request
server_thread = threading.Thread(target=server.serve_forever)
# Exit the server thread when the main thread terminates
server_thread.daemon = True
server_thread.start()
#server.run_forever()

poll="" #buffer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.recv(1024) 
s.send("?WATCH={\"enable\":true}")
s.recv(1024)
#every second poll gpsd, save result to common buffer
while True: 
    s.send("?POLL;")
    poll=s.recv(10000) #ais may be big
    print(poll)
    time.sleep(1)



