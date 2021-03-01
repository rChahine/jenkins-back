def test_auth(client_auth_user):
    data = client_auth_user.get('user/me').json()

    assert data["role"] == "U"
    assert data["username"] == "user"


def test_add_choice(client_auth_user):
    r = client_auth_user.post('/choices', json={'wording': 'new_choice'})

    assert r.status_code == 401


def test_add_user(client_auth_user):

    success = {
        'role': 'A',
        'username': 'username',
        'password': 'password'
    }

    r = client_auth_user.post('/user', json=success)
    assert r.status_code == 401


def test_get_choices_logged_in(client_auth_user):
    r = client_auth_user.get('/choices_connected')
    assert r.status_code == 200


def test_add_vote(client_auth_user, client_auth_admin):
    r = client_auth_user.put('/vote/1')
    assert r.status_code == 401


def test_delete_vote(client_auth_user):
    r = client_auth_user.delete('/vote/1')
    assert r.status_code == 404


def test_delete_choice(client_auth_user):
    r = client_auth_user.delete('/choices/1')
    assert r.status_code == 401
