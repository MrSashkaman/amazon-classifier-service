import sys
import logging

from fastapi import FastAPI
from omegaconf import OmegaConf

from src.containers.containers import AppContainer
from src.routes import classifier as clf_routes
from src.routes.routers import router as app_router
from src.logger import LOGGER

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(name)s.%(funcName)s --> %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)])

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    cfg = OmegaConf.load('config/config.yaml')
    cfg = OmegaConf.to_container(cfg, resolve=True)
    container = AppContainer()
    container.config.from_dict(cfg)
    container.wire([clf_routes])
    app = FastAPI()

    set_routers(app)
    return app


def set_routers(app: FastAPI):
    app.include_router(app_router, prefix='/amazon_photo', tags=['amazon_photo'])
