from http import HTTPStatus

from fastapi.testclient import TestClient


def test_classes_list(client: TestClient):
    response = client.get('/amazon_photo/classes')
    assert response.status_code == HTTPStatus.OK

    classes = response.json()['classes']
    assert isinstance(classes, list)


def test_predict(client: TestClient, sample_image_bytes: bytes):
    files = {
        'image': sample_image_bytes,
    }
    response = client.post('/amazon_photo/predict', files=files)

    assert response.status_code == HTTPStatus.OK

    predicted_classes = response.json()['classes']

    assert isinstance(predicted_classes, list)


def test_predict_proba(client: TestClient, sample_image_bytes: bytes):
    files = {
        'image': sample_image_bytes,
    }
    response = client.post('/amazon_photo/predict_proba', files=files)

    assert response.status_code == HTTPStatus.OK

    genre2prob = response.json()

    for genre_prob in genre2prob.values():
        assert genre_prob <= 1
        assert genre_prob >= 0
