from __future__ import annotations

import os
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://0.0.0.0:11434/v1")
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "llama3.2:latest")
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
WORK_DIR = Path(__file__).resolve().parent
CACHE_JSON_PATH = WORK_DIR / "cache.json"


@dataclass
class CliArgs:
    location: str

    @classmethod
    def from_cli(cls) -> CliArgs:
        parser = ArgumentParser()
        parser.add_argument(
            "-l", "--location", type=str, help="The location to get the weather"
        )
        args = parser.parse_args()
        return cls(location=args.location)
