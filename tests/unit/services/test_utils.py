from omegaconf import OmegaConf
import numpy as np
from src.preprocess_utils import preprocess


def test_image_has_right_size_after_preprocessing(app_config: OmegaConf, sample_image_np: np.ndarray):
    processed_image = preprocess(sample_image_np, target_size=app_config['image_classifier']['size'])
    assert list(processed_image.shape[2::]) == app_config['image_classifier']['size']
