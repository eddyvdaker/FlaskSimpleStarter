"""Tests for the main blueprint."""

def test_main(client):
    # GIVEN a test client
    # WHEN the main page is visited
    # THEN the main page is shown
    req = client.get('/')
    expected_status = 200
    expected = 'Welcome'
    assert req.status_code == expected_status
    assert expected in req.data.decode()
