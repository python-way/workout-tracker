import uuid

name = f"{uuid.uuid4()}"
email = f"{uuid.uuid4()}@gmail.com"
password = '12345678'

def test_register(client):
    res = client.post('/register', json={"name":name, "email":email, "password":password})
    assert res.status_code == 201

def test_login(client):
    res = client.post('/login', json={"name":name, "email":email, "password":password})
    assert res.status_code == 200 and res.json.get("token") != None

