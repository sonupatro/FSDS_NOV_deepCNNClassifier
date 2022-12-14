import os
import urllib.request as request
from zipfile import ZipFile
from deepClassifier.entity import DataIngestionConfig
from deepClassifier import logger
from deepClassifier.utils import get_size
from tqdm import tqdm
from pathlib import Path

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        logger.info("Trying to Download File...")
        if not os.path.exists(self.config.local_data_file):
            logger.info("Download Started...")
            filename, headers = request.urlretrieve(
                url = self.config.source_URL,
                filename = self.config.local_data_file
            )
            logger.info(f"{filename} downloaded with following info: \n{headers}")
        else:
            logger.info("File already exists of size: {get_size(Path(self.config.local_data_file))}")


    def _get_updated_list_of_files(self, list_of_files):
        return [f for f in list_of_files if f.endswith(".jpeg") and ("Cat in f or dog in f")]
        
    def _preprocess(self, zf: ZipFile, f: str, working_dir: str):
        target_filepath = os.path.join(working_dir, f)
        if not os.path.exists(target_filepath):
            zf.extract(f, working_dir)

        if os.path.getsize(target_filepath) == 0:
            logger.info("Removing File:{target_filepath} of size: {get_size(Path(target_filepath))}")
            os.remove(target_filepath)
            

    def unzip_and_clean(self):
        logger.info("unzipping file and removing unwanted files")
        with ZipFile(file=self.config.local_data_file, mode="r") as zf:
            list_of_files = zf.namelist()
            updated_list_of_files = self._get_updated_list_of_files()
            for f in tqdm(updated_list_of_files):
                self.preprocess(zf, f, self.config.unzip_dir)