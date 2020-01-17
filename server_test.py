from server import create_response


def test_create_response_hello():
    message_json = {"message": "/hello", "username": "sauceboss"}
    fake_client = ("fake", "client")
    response, clients = create_response(message_json, None, [fake_client])
    assert clients == [fake_client]
    assert response["username"] == "server"
    assert response["message"] == "sauceboss joined the chat"


def test_create_response_who():
    message_json = {"message": "/who", "username": "sauceboss"}
    fake_sender = ("fakesender", "fakesenderport")
    fake_clients = [("fake", "client"), ("fake2", "client2")]
    response, clients = create_response(message_json, fake_sender, fake_clients)
    assert clients == [fake_sender]
    assert response["username"] == "server"
    assert response["message"] == "people in room: fake, fake2"
    

def test_create_response_goodbye():
    message_json = {"message": "/goodbye", "username": "sauceboss"}
    fake_clients = [("fake", "client"), ("fake2", "client2")]
    response, clients = create_response(message_json, fake_clients[0], fake_clients)
    assert clients == [fake_clients[0]] # we removed the first client; the only client left is the 2nd one
    assert response["message"] == "sauceboss left the chat"
    assert response["username"] == "server"


def test_create_response_emote():
    message_json = {"message": "/me waves", "username": "sauceboss", "color": 420}
    fake_clients = [("fake", "client"), ("fake2", "client2")]
    response, clients = create_response(message_json, fake_clients[0], fake_clients)
    assert clients == fake_clients # we removed the first client; the only client left is the 2nd one
    assert response["message"] == "sauceboss waves"
    assert response["username"] == None 
    assert response["color"] == 420 


def test_message():
    message_json = {"message": "this is a test", "username": "sauceboss", "color": 420}
    fake_clients = [("fake", "client"), ("fake2", "client2")]
    response, clients = create_response(message_json, fake_clients[0], fake_clients)
    assert clients == fake_clients # we removed the first client; the only client left is the 2nd one
    assert response["message"] == "this is a test"
    assert response["username"] == "sauceboss" 
    assert response["color"] == 420 


