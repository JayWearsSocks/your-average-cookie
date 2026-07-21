import datetime
from pathlib import Path
import string

class DataOrganization:
    DATADIR = Path("webdata")

    @staticmethod
    def now() -> string:
        return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    @classmethod
    def create_data_directory(cls, spider_name: string) -> Path:
        datadir = cls.DATADIR.joinpath(Path(f'{spider_name}_{cls.now()}'))
        datadir.mkdir(parents=True)
        return datadir

    