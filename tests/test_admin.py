

def test_auth(client_auth_admin):
    data = client_auth_admin.get('user/me').json()

    assert data["role"] == "A"
    assert data["username"] == "admin"


def test_add_choice(client_auth_admin):
    r = client_auth_admin.post('/choices', json={'wording': 'new_choice'}).json()

    assert r["detail"] == "Choice added"
