import socket, json

rgstr = {"command":"register", "username":"user01"} #message board registration
drgstr = {"command":"deregister", "username":"user01"} #message board deregistration
post_msg = {"command":"msg", "username":"user02", "message":"This is my message."} #post message on server

host = input("Enter server address: ")
port = input("Enter server port number: ")
port = int (port)

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #creating socket

username = input("Enter your username: ") 
rgstr["username"] = username
drgstr["username"] = username
post_msg["username"] = username
register = json.dumps(rgstr)
try:
    print("Registering %s..." %username)
    client.sendto(bytes(register,"utf-8"), (host, port))
finally:
    #Registration
    receive, server = client.recvfrom(1024)
    response = json.loads(receive)
    if (response["code_no"] == 401):
        print("Your username is successfully registered.")
        registered = True
    elif (response["code_no"] == 502):
        print("Registration failed. Username already exists.")
        registered = False
    else: 
        print("Registration failed.")
        registered = False

while (registered == True): 
    try:
        user_msg = input('%s (bye=exit chatroom): ' %username)
        post_msg["message"] = user_msg
        message = json.dumps(post_msg)
        client.sendto(bytes(message,"utf-8"), (host, port))
    finally:
        if user_msg == "bye":
                deregister = json.dumps(drgstr)
                client.sendto(bytes(deregister,"utf-8"), (host, port))
                print("User left...")
                client.close()
                break
        elif ((response["code_no"] == 401)):
                print("Message sent.")
        elif((response["code_no"] == 501)): 
            print("User does not exist.")
