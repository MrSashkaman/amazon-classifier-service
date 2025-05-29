import os.path  # noqa: WPS301

import cv2
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from omegaconf import OmegaConf

from app import set_routers
from src.containers.containers import AppContainer
from src.routes import classifier as clf_routes

TESTS_DIR = os.path.dirname(__file__)


@pytest.fixture(scope='session')
def sample_image_bytes():
    with open(os.path.join(TESTS_DIR, 'images', 'amazon_test.png'), 'rb') as f:
        return f.read()


@pytest.fixture
def sample_image_np():
    img = cv2.imread(os.path.join(TESTS_DIR, 'images', 'amazon_test.png'))
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


@pytest.fixture(scope='session')
def app_config():
    cfg = OmegaConf.load(os.path.join(TESTS_DIR, 'test_config.yml'))
    return OmegaConf.to_container(cfg, resolve=True)


@pytest.fixture(scope='session')
def app_container(app_config):
    container = AppContainer()
    container.config.from_dict(app_config)
    return container


@pytest.fixture(scope='session')
def wired_app_container(app_config):
    container = AppContainer()
    container.config.from_dict(app_config)
    container.wire([clf_routes])
    yield
    container.unwire()


@pytest.fixture(scope='session')
def test_app(wired_app_container):
    app = FastAPI()
    set_routers(app)
    return app


@pytest.fixture(scope='session')
def client(test_app):
    return TestClient(test_app)
