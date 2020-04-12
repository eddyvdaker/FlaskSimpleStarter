"""Tests for the errors module."""

def test_error_response(client):
    # GIVEN a testing client
    # WHEN a non-existing page is requested
    # THEN a 404 error page is returned
    req = client.get('/no-such-route')
    expected_status = 404
    expected = 'Not Found'
    assert req.status_code == expected_status
    assert expected in req.data.decode()
