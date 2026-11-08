def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_link(client):
    response = client.post(
        "/links", 
        json={"url": "https://google.com"}
        )
    data = response.json()
    assert response.status_code == 200
    assert len(data["code"]) == 6
    assert data["short_url"] == f"http://localhost:8000/{data['code']}"
    assert data["original_url"] == "https://google.com/"

def test_redirect(client):
    response = client.post(
            "/links", 
            json={"url": "https://google.com"}
            )
    data = response.json()
    code = data["code"]
    redirect_response = client.get(f"/{code}", follow_redirects=False)
    assert redirect_response.status_code == 302
    assert redirect_response.headers["location"] == "https://google.com/"

def test_invalid_code(client):
    response = client.get("/nothing")
    assert response.status_code == 404
    assert response.json() == {"detail": "Link not found"}

def test_redirect_stats(client):
    response = client.post(
            "/links", 
            json={"url": "https://google.com"}
            )
    data = response.json()
    code = data["code"]
    for _ in range(3):
        client.get(f"/{code}", follow_redirects=False)
    stats = client.get(f"/links/{code}/stats")
    response_stats = stats.json()
    assert stats.status_code == 200
    assert response_stats["clicks"] == 3

def test_invalid_url(client):
    response = client.post(
        "/links",
        json={"url": "not-a-url"}
        )
    assert response.status_code == 422
