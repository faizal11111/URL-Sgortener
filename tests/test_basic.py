import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.get_json()['status'] == 'healthy'

def test_shorten_url(client):
    res = client.post('/api/shorten', json={"url": "https://example.com"})
    assert res.status_code == 201
    data = res.get_json()
    assert 'short_code' in data
    assert 'short_url' in data

def test_invalid_url(client):
    res = client.post('/api/shorten', json={"url": "invalid-url"})
    assert res.status_code == 400

def test_redirect_and_stats(client):
    shorten = client.post('/api/shorten', json={"url": "https://example.com"})
    code = shorten.get_json()['short_code']

    redirect = client.get(f'/{code}')
    assert redirect.status_code == 302

    stats = client.get(f'/api/stats/{code}')
    data = stats.get_json()
    assert data['url'] == "https://example.com"
    assert data['clicks'] == 1
    assert 'created_at' in data

def test_unknown_short_code(client):
    res = client.get('/api/stats/fake123')
    assert res.status_code == 404
