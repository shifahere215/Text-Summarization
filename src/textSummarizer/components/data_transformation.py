import os
import json
from datasets import Dataset
from transformers import AutoTokenizer
from textSummarizer.logging import logger
from textSummarizer.entity import DataTransformationConfig



class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_name)

    # def convert_examples_to_features(self, example_batch):
    #     input_encodings = self.tokenizer(
    #         example_batch['dialogue'],
    #         max_length=1024,
    #         truncation=True
    #     )

    #     target_encodings = self.tokenizer(
    #         example_batch['summary'],
    #         max_length=128,
    #         truncation=True,
    #         text_target=example_batch['summary']
    #     )

    #     return {
    #         'input_ids': input_encodings['input_ids'],
    #         'attention_mask': input_encodings['attention_mask'],
    #         'labels': target_encodings['input_ids']
    #     }

    # def convert(self):
    #     for split in ['train', 'test', 'validation']:
    #         path = os.path.join("artifacts", "data_ingestion", f"{split}.json")
    #         logger.info(f"Loading {split} data from {path}")

    #         with open(path, "r") as f:
    #             raw_data = [json.loads(line) for line in f.readlines()]

    #         dataset = Dataset.from_list(raw_data)
    #         transformed_dataset = dataset.map(self.convert_examples_to_features, batched=True)

    #         save_path = os.path.join(self.config.root_dir, f"{split}_transformed")
    #         transformed_dataset.save_to_disk(save_path)




    def convert_examples_to_features(self, example_batch):
        dialogues = example_batch.get("dialogue", [])
        summaries = example_batch.get("summary", [])

        for d, s in zip(dialogues, summaries):
            if not isinstance(d, str) or not isinstance(s, str):
                print("Invalid input:", d, "|", s)

        # Filter out non-string values
        def clean(texts):
            return [
                str(t) if isinstance(t, (str, int, float)) else ""
                for t in texts
            ]

        dialogues = clean(dialogues)
        summaries = clean(summaries)

        inputs = self.tokenizer(
            dialogues,
            max_length=1024,
            truncation=True,
            padding="max_length"
        )

        targets = self.tokenizer(
            summaries,
            max_length=128,
            truncation=True,
            padding="max_length"
        )

        return {
            "input_ids": inputs["input_ids"],
            "attention_mask": inputs["attention_mask"],
            "labels": targets["input_ids"]
        }

    



    def convert(self):
        for split in ['train', 'test', 'validation']:
            path = os.path.join("artifacts", "data_ingestion", f"{split}.json")
            logger.info(f"Loading {split} data from {path}")

            with open(path, "r") as f:
                raw_data = [json.loads(line) for line in f.readlines()]

            dataset = Dataset.from_list(raw_data)
            transformed_dataset = dataset.map(self.convert_examples_to_features, batched=True)

            save_path = os.path.join(self.config.root_dir, f"{split}_transformed")
            transformed_dataset.save_to_disk(save_path)
    