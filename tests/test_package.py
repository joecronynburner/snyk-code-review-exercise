from django.test import Client

# review: you cover the recursive dependency case but lost coverage on a flat dependency hierarchy

# review: you should add more tests to cover edge cases, such as invalid versions, missing dependencies, etc.

# review: this test only works with internet access so I'd consider it an integration test, consider adding pure unit tests that utilize mocking to test the logic in isolation

def test_get_package():
    client = Client()
    response = client.get("/package/minimatch/3.1.2")
    assert response.status_code == 200
    assert response.json() == {
        "dependencies": [
            {
                "dependencies": [
                    {"dependencies": [], "name": "balanced-match", "version": "1.0.2"},
                    {"dependencies": [], "name": "concat-map", "version": "0.0.1"},
                ],
                "name": "brace-expansion",
                "version": "1.1.11",
            }
        ],
        "name": "minimatch",
        "version": "3.1.2",
    }
