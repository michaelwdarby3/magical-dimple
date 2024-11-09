
# Model Usage

This document provides guidance on loading, fine-tuning, and using models in the Retriever-Augmented Generation (RAG) pipeline.

## Overview

The RAG pipeline utilizes two primary models:
1. **Retriever Model**: Generates embeddings for retrieving relevant documents or data.
2. **Generator Model**: Produces text-based responses using the retrieved context.

These models can be pre-trained or fine-tuned based on specific project requirements.

## Model Loading

### Pre-trained Model Loading

Pre-trained models can be loaded from the `transformers` library. Use `model_utils.py` to configure and load models as needed.

Example:

```python
from transformers import AutoModel, AutoTokenizer

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
```

### Fine-tuning Models

To fine-tune a model on specific data:
1. **Prepare the Dataset**: Organize training data in a format compatible with the model (e.g., CSV, JSON).
2. **Train the Model**: Use Hugging Face’s `Trainer` API for fine-tuning. Adjust parameters such as batch size, learning rate, and number of epochs based on your data.

Example script in `model/fine_tune.py`:

```python
from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(output_dir="./models/my_model", num_train_epochs=3)
trainer = Trainer(model=model, args=training_args, train_dataset=dataset)
trainer.train()
```

## Model Storage and Versioning

Fine-tuned models should be saved in `src/models/`. Keep separate folders for each version to ensure reproducibility:

```plaintext
models/
└── my_model_v1/
    ├── config.json
    ├── pytorch_model.bin
    └── tokenizer.json
```

## Troubleshooting

- **Model Not Found**: Ensure the model name is correct and check internet connectivity if loading from Hugging Face.
- **Slow Loading**: For large models, consider loading in a GPU environment if available.
- **Compatibility**: Verify that `torch` and `transformers` versions are compatible with your model.

Refer to `rag_pipeline.md` for integrating models into the RAG pipeline.
