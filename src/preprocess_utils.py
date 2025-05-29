import cv2
import numpy as np
from numpy import typing as npt

from src.app_types import ImageNp
from src.logger import LOGGER

MAX_UINT8 = 255

BROADCAST_SHAPE = (3, 1, 1)
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406]).reshape(BROADCAST_SHAPE)
IMAGENET_STD = np.array([0.229, 0.224, 0.225]).reshape(BROADCAST_SHAPE)


def preprocess(
    image: ImageNp,
    target_size: tuple[int, int],
) -> npt.NDArray[np.float32]:
    image = image.astype(np.float32)
    LOGGER.debug("Input Image shape: {}".format(image.shape))
    image = cv2.resize(image, target_size)
    LOGGER.debug("Image shape after resize: {}".format(image.shape))
    image = np.transpose(image, (2, 0, 1)) / MAX_UINT8
    LOGGER.debug("Image shape after transpose: {}".format(image.shape))
    return ((image - IMAGENET_MEAN) / IMAGENET_STD).astype(np.float32)[None]
