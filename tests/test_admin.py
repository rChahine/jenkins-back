

def test_auth(client_auth_admin):
    data = client_auth_admin.get('user/me').json()

    assert data["role"] == "A"
    assert data["username"] == "admin"


def test_add_choice(client_auth_admin):
    r = client_auth_admin.post('/choices', json={'wording': 'new_choice'}).json()

    assert r["detail"] == "Choice added"


def test_add_user(client_auth_admin):

    fail = {
        'role': 'P',
        'username': 'username',
        'password': 'password'
    }

    success = {
        'role': 'A',
        'username': 'username',
        'password': 'password'
    }

    r = client_auth_admin.post('/user', json=fail)
    assert r.status_code == 422  # role must be A or P

    r = client_auth_admin.post('/user', json=success)
    assert r.status_code == 200
    assert r.json()["detail"] == 'User added'

    r = client_auth_admin.post('/user', json=success)
    assert r.status_code == 409


def test_get_choice_no_login(get_client):
    r = get_client.get('/choices')
    assert r.status_code == 200


def test_get_choices_logged_in(client_auth_admin):
    r = client_auth_admin.get('/')