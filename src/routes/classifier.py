import cv2
import numpy as np

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, File

from src.containers.containers import AppContainer
from src.routes.routers import router
from src.image_classifier import ImageClassifier


@router.get('/classes')
@inject
async def classes_list(service: ImageClassifier = Depends(Provide[AppContainer.image_classifier])):
    return {'classes': service.classes}


@router.post('/predict')
@inject
async def predict(
    image: bytes = File(),
    service: ImageClassifier = Depends(Provide[AppContainer.image_classifier]),
):
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return {'classes': service.predict(img)}


@router.post('/predict_proba')
@inject
async def predict_proba(
    image: bytes = File(),
    service: ImageClassifier = Depends(Provide[AppContainer.image_classifier]),
):

    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return service.predict_proba(img)


@router.get('/health_check')
async def health_check():
    return 'OK'
