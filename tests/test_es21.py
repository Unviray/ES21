from datetime import date


def test_first(client):
    rv = client.get('/')

    assert b'Ho fanombohana dia mampidira mpitory iray' in rv.data


def test_new_first(client):
    rv = client.post('/mpitory-vaovao', data={
        'first_name': 'jo',
        'phone1': '033 33 333 33',
        'birth': date(2000, 2, 20),
        'promo': '',
        'gender': 'Lahy',
    }, follow_redirects=True)

    print(rv.data.decode())
    assert rv.status_code == 200
    assert b'invalid' not in rv.data
    assert b'Mpitory vaovao' not in rv.data
    assert b'jo' in rv.data
    assert b'033 33 333 33' in rv.data
    assert b'20 febroary 2000' in rv.data
