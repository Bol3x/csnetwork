import socket, json

#setting variables 
incomplete = {"command":"ret_code", "code_no":201} #command parameters incomplete
unknown = {"command":"ret_code", "code_no":301} #command unknown
accepted = {"command":"ret_code", "code_no":401} #command accepted
not_registered = {"command":"ret_code", "code_no":501} #user not registered
user_exist = {"command":"ret_code", "code_no":502} #user account exists

host = socket.gethostbyname("")
#host = socket.gethostbyname(socket.gethostname())
#host = input("Enter the listening address: ")
port = input("Enter the listening port number: ")
port = int(port)
registered_user = []

server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #creating socket
print ("Starting up on %s port %d" %(host, port)) 
server.bind((host, port)) #binding socket
print ('\nServer waiting for request...')

while True:
    data, address= server.recvfrom(1024)
    client_request = json.loads(data)

    #Client registration
    if client_request["command"] == "register":
        if client_request["username"] in registered_user:
            server_response = user_exist
            print('User account exists.')
        elif len(client_request) == 0:
            print('Incomplete parameters.')
            server_response = incomplete
        else:
            registered_user.append(client_request["username"])
            server_response = accepted
            print('User successfully registered.')
            print("Online user/s: %s" %(registered_user))

    #Client's message
    elif client_request["command"] == "msg":
        if client_request["username"] in registered_user:
            print("%s: %s" %(client_request["username"], client_request["message"])) 
            server_response = accepted
        elif len(client_request) == 0:
            print('Incomplete parameters.')
            server_response = incomplete
        else:
            print('User not registered.')
            server_response = not_registered

    #Deregistration
    elif client_request["command"] == "deregister":
        if len(client_request) == 0:
            print('Incomplete parameters.')
            server_response = incomplete
        else:
            registered_user.remove(client_request["username"])
            print("%s left the chat room." %(client_request["username"]))
            print("Online user/s: %s" %(registered_user))
            server_response = accepted
    else:
        print('Command Unknown.')
        server_response = unknown

    response = json.dumps(server_response)
    server.sendto(bytes(response ,"utf-8"), address)  
