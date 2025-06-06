import os
from pathlib import Path
from textSummarizer.logging import logger
from textSummarizer.entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_files_exist(self) -> bool:
        logger.info("Starting file validation...")
        missing_files = []

        for file_name in self.config.ALL_REQUIRED_FILES:
            file_path = Path("artifacts/data_ingestion") / file_name  # Adjust if path differs
            if not file_path.exists():
                missing_files.append(file_name)

        status = len(missing_files) == 0

        with open(self.config.STATUS_FILE, "w") as f:
            if status:
                f.write("Validation passed ✅\n")
                logger.info("All files found. Validation passed.")
            else:
                f.write(f"Validation failed ❌\nMissing: {missing_files}")
                logger.error(f"Missing files: {missing_files}")

        return status
