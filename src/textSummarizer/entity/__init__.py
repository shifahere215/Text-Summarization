from dataclasses import dataclass
from pathlib import Path
from typing import Dict

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    dataset_name: str
    splits: Dict[str, str]
    save_local: bool = False  # Optional: for saving locally
