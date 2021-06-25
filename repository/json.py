import json
from datetime import datetime
from pathlib import Path

import pandas as pd

from app.settings import CACHE_DIR


def default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()


class JsonManager:
    def __init__(self):
        self.dir = Path(CACHE_DIR)
        self.dir.mkdir(parents=True, exist_ok=True)

    def get(self, filename, is_df=False):
        file = self.dir / filename

        if file.is_file():
            with open(file) as fd:
                if is_df:
                    data = pd.read_json(fd)
                else:
                    data = json.load(fd)

            return data

    def save(self, filename, data, is_df=False):
        file = self.dir / filename

        with open(file, "w") as fd:
            if is_df:
                fd.write(data.to_json(indent=4, index=True))
            else:
                json.dump(data, fd, default=default)


json_manager = JsonManager()
