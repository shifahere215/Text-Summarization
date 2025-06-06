from textSummarizer.constants import *
from textSummarizer.utils.common import read_yaml, create_directories
from textSummarizer.entity import (DataIngestionConfig, DataValidationConfig)
from pathlib import Path

class ConfigurationManager:
    def __init__(
        self,
        config_filepath: Path = CONFIG_FILE_PATH,
        params_filepath: Path = PARAMS_FILE_PATH
    ):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])  # Note: dictionary access now

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config["root_dir"]])

        data_ingestion_config = DataIngestionConfig(
            # root_dir=config.root_dir,
            # dataset_name=config.dataset_name,
            # splits=config.splits,
            # save_local=config.get("save_local", False)
            
            root_dir=Path(config["root_dir"]),  # ✅ this line is crucial
            dataset_name=config["dataset_name"],
            splits=config["splits"],
            save_local=config.get("save_local", False)
        )
        
    


        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            ALL_REQUIRED_FILES=config.ALL_REQUIRED_FILES,
        )

        return data_validation_config