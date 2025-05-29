from dependency_injector import containers, providers

from src.config import ImageClassifierConfig
from src.image_classifier import ImageClassifier


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    image_classifier = providers.Singleton(
        ImageClassifier,
        config=config.image_classifier.as_(lambda cfg: ImageClassifierConfig(**cfg)),
    )
