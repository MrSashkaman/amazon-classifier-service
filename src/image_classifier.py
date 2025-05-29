import numpy as np
import onnxruntime
from numpy import typing as npt

from src.app_types import ImageNp
from src.config import ImageClassifierConfig
from src.preprocess_utils import preprocess
from src.logger import LOGGER


def sigmoid(arr: np.ndarray) -> np.ndarray:
    return np.exp(-np.logaddexp(0, -arr))


class ImageClassifier:

    def __init__(self, config: ImageClassifierConfig):
        LOGGER.info('Initializing ImageClassifier...')
        self._config = config
        self._ort_session = onnxruntime.InferenceSession(
            config.model_path,
            providers=config.providers,
        )

    @property
    def classes(self) -> list[str]:
        return list(self._config.classes)

    def predict(self, image: ImageNp) -> list[str]:
        probs = sigmoid(self._predict(image))
        LOGGER.debug(f'Probabilities in ImageClassifier: {probs}')
        return self._postprocess_predict(probs)

    def predict_proba(self, image: ImageNp) -> dict[str, float]:
        LOGGER.info('Predicting ImageClassifier probabilities...')
        probs = sigmoid(self._predict(image))
        return self._postprocess_predict_proba(probs)

    def _predict(self, image: ImageNp) -> npt.NDArray[np.float32]:
        ort_inputs = {
            self._ort_session.get_inputs()[0].name: preprocess(image, self._config.size),
        }
        return self._ort_session.run(None, ort_inputs)[0][0]

    def _postprocess_predict(self, predict: npt.NDArray[np.float32]) -> list[str]:
        LOGGER.debug("Postprocessing predict {}...".format(predict))
        return [
            class_name
            for idx, class_name in enumerate(self._config.classes)
            if predict[idx] > self._config.threshold
        ]

    def _postprocess_predict_proba(self, probs: np.ndarray) -> dict[str, float]:
        LOGGER.debug("Postprocessing predict {}...".format(probs))
        classes = list(self._config.classes)
        sorted_idxs = list(reversed(probs.argsort()))
        return {
            classes[idx]: float(probs[idx])
            for idx in sorted_idxs
        }
