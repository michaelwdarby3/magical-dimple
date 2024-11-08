import numpy as np
from src.vectorization.vectorize_data import generate_embeddings


def test_generate_embeddings(mocker):
    mock_model = mocker.patch("src.vectorization.vectorize_data.model")
    mock_model.encode.return_value = np.array([[0.1, 0.2, 0.3]])

    texts = ["sample text"]
    embeddings = generate_embeddings(texts)
    assert embeddings.shape == (1, 3)
