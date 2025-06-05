import os
from datasets import load_dataset
from pathlib import Path
from textSummarizer.logging import logger
from textSummarizer.utils.common import get_size
from textSummarizer.entity import (DataIngestionConfig)
# from textSummarizer.utils.common import save_json   # a helper to save datasets

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def fetch_and_optionally_save(self):
        logger.info(f"Loading dataset: {self.config.dataset_name}")
        
        for split_name, hf_split in self.config.splits.items():
            logger.info(f"Loading {split_name} split...")
            dataset_split = load_dataset(self.config.dataset_name, split=hf_split)

            if self.config.save_local:
                save_path = self.config.root_dir / f"{split_name}.json"
                logger.info(f"Saving {split_name} to {save_path}")
                dataset_split.to_json(str(save_path), orient="records", lines=True)

        logger.info("Data ingestion complete.")
