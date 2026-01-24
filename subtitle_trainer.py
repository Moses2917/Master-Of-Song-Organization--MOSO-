from transformers import WhisperForConditionalGeneration, WhisperProcessor

# 1. Load model
model = WhisperForConditionalGeneration.from_pretrained(
    "openai/whisper-base"
)
model.config.use_cache = False
model.gradient_checkpointing_enable()


for layer in model.model.encoder.parameters():
    layer.requires_grad = False # Freezing the layers

# Init new weights
model.model.decoder.apply(model._init_weights)
model.proj_out.apply(model._init_weights)

# this prevents default Whisper values from repopulating the fields from model.config
model.config.suppress_tokens = []
model.config.begin_suppress_tokens = []
model.config.forced_decoder_ids = None

# Make a new generation_config to match vocab
from transformers import GenerationConfig

model.generation_config = GenerationConfig(

    # Clean slate - no suppress tokens, no multilingual stuff
    forced_decoder_ids=None,
    suppress_tokens=[-1],
    begin_suppress_tokens=[-1],
)

# 4. Load processor WITH language and task specified
processor = WhisperProcessor.from_pretrained(
    "openai/whisper-base",
    language="armenian",
    task="transcribe"
)
# Need this so that the correct tokens are added when training.
processor.tokenizer.set_prefix_tokens(language="armenian", task="transcribe")

# ✅ FIXED preprocessing function
def preprocess_batched(batch):
    audio = batch["audio"]

    # Process audio features
    batch["input_features"] = processor.feature_extractor(
        [a["array"] for a in audio],
        sampling_rate=16000
    ).input_features

    batch["labels"] = processor.tokenizer(batch["sentence"]).input_ids

    return batch

from datasets import load_dataset, Audio


import evaluate

metric = evaluate.load("wer")

def compute_metrics(pred):
    pred_ids = pred.predictions
    label_ids = pred.label_ids

    # Replace -100 with pad token
    label_ids[label_ids == -100] = processor.tokenizer.pad_token_id

    # Decode predictions and labels
    pred_str = processor.tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    label_str = processor.tokenizer.batch_decode(label_ids, skip_special_tokens=True)

    wer = 100 * metric.compute(predictions=pred_str, references=label_str)

    return {"wer": wer}

# Data Collator (your version was fine, but adding decoder_start_token_id check)
from dataclasses import dataclass
from typing import Any, Dict, List, Union
import torch

@dataclass
class DataCollatorSpeechSeq2SeqWithPadding:
    processor: Any
    decoder_start_token_id: int = None

    def __post_init__(self):
        if self.decoder_start_token_id is None:
            self.decoder_start_token_id = self.processor.tokenizer.bos_token_id

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        input_features = [{"input_features": feature["input_features"]} for feature in features]
        batch = self.processor.feature_extractor.pad(input_features, return_tensors="pt")

        label_features = [{"input_ids": feature["labels"]} for feature in features]
        labels_batch = self.processor.tokenizer.pad(label_features, return_tensors="pt")

        labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)

        # Cut BOS token if present (it's added during generation)
        if (labels[:, 0] == self.decoder_start_token_id).all().cpu().item():
            labels = labels[:, 1:]

        batch["labels"] = labels
        return batch

if __name__ == '__main__':


    data_collator = DataCollatorSpeechSeq2SeqWithPadding(
        processor=processor,
        decoder_start_token_id=model.config.decoder_start_token_id
    )



    dataset = load_dataset("Chillarmo/common_voice_20_armenian", split="train")
    dataset = dataset.cast_column("audio", Audio(sampling_rate=16000))

    # Remove unnecessary columns
    features_to_remove = [col for col in dataset.column_names if col not in ['sentence', 'audio']]
    dataset = dataset.remove_columns(features_to_remove)

    train_dataset = dataset.map(
        preprocess_batched,
        batched=True,
        batch_size=16,
        num_proc=8,
        remove_columns=dataset.column_names
    )

    # Load and preprocess test set
    test_dataset = load_dataset("Chillarmo/common_voice_20_armenian", split="test")
    test_dataset = test_dataset.cast_column("audio", Audio(sampling_rate=16000))
    features_to_remove = [col for col in test_dataset.column_names if col not in ['sentence', 'audio']]
    test_dataset = test_dataset.remove_columns(features_to_remove)

    test_dataset = test_dataset.map(
        preprocess_batched,
        batched=True,
        batch_size=16,
        num_proc=8,
        remove_columns=test_dataset.column_names
    )

    from transformers import Seq2SeqTrainingArguments

    training_args = Seq2SeqTrainingArguments(
        output_dir="./whisper-armenian-lora",
        per_device_train_batch_size=8,
        gradient_accumulation_steps=2,
        learning_rate=2e-4,
        warmup_steps=500,
        num_train_epochs=15,
        fp16=True,
        eval_strategy="no",
        generation_max_length=225,
        greater_is_better=False,
        push_to_hub=False,
        predict_with_generate=True,
        dataloader_num_workers=8,
        dataloader_pin_memory=True,
        remove_unused_columns=False,
    )




    from transformers import Seq2SeqTrainer

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
        processing_class=processor.feature_extractor,
    )

    trainer.train()

    # Evaluate
    eval_results = trainer.evaluate(eval_dataset=test_dataset)
    print(f"\nWER: {eval_results['eval_wer']:.2f}%")
    print(f"Loss: {eval_results['eval_loss']:.4f}")