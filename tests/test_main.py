
def test_shorten_returns_a_short_code(client):
    response = client.post("/shorten", json={"url": "https://www.python.org/about/"})
    assert response.status_code == 200
    body = response.json()
    assert body["short_code"] == "1"  
    assert body["original_url"] == "https://www.python.org/about/"
    assert body["short_url"].endswith("/1")


def test_redirect_follows_to_original_url(client):
    create_response = client.post("/shorten", json={"url": "https://fastapi.tiangolo.com/"})
    short_code = create_response.json()["short_code"]
    redirect_response = client.get(f"/{short_code}", follow_redirects=False)

    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://fastapi.tiangolo.com/"


def test_multiple_links_get_distinct_increasing_codes(client):
    urls = [
        "https://www.google.com/",
        "https://www.python.org/",
        "https://docs.sqlalchemy.org/",
    ]
    short_codes = []
    for url in urls:
        response = client.post("/shorten", json={"url": url})
        short_codes.append(response.json()["short_code"])

    assert short_codes == ["1", "2", "3"]
    for short_code, expected_url in zip(short_codes, urls):
        response = client.get(f"/{short_code}", follow_redirects=False)
        assert response.headers["location"] == expected_url


def test_nonexistent_but_validly_formatted_short_code_returns_404(client):
    response = client.get("/zzzzz")
    assert response.status_code == 404


def test_short_code_with_invalid_characters_returns_404_not_500(client):
    response = client.get("/not-base62-because-of-the-dash")
    assert response.status_code == 404


def test_shorten_rejects_malformed_url(client):
    response = client.post("/shorten", json={"url": "not-a-real-url"})
    assert response.status_code == 422  