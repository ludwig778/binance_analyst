from pathlib import Path

from pandas import DataFrame, read_json


class DataFrameToolbox:
    @staticmethod
    def save(df: DataFrame, path: Path) -> None:
        if not path.parent.exists():
            path.parent.mkdir(parents=True)

        df.to_json(path)

    @staticmethod
    def read(path: Path) -> DataFrame:
        if not path.exists():
            return DataFrame()

        df = read_json(path)
        df.index.rename("timestamp", inplace=True)

        return df
