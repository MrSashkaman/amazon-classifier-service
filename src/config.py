from pydantic import BaseSettings


class ImageClassifierConfig(BaseSettings):
    model_path: str
    providers: list[str]
    threshold: float
    size: tuple[int, int]
    classes: dict[str, int]
