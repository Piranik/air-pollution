from config_utils.config import ConfigYaml
from downloader.downloader import Donwloader
from data_importer import import_data

from managers.transform_data_manager import Data_Transformer
from managers.resources_manager import Resources_Manager

if __name__ == '__main__':
    app_config = ConfigYaml().get_config()
    downloader = Donwloader(app_config)
    resources_manager = Resources_Manager(app_config)
    # downloader.prepare_environment()
    # downloader.download_stations()
    # downloader.download_diseases()
    import_data(app_config)
    data_transformer = Data_Transformer(app_config)
    data_transformer.transform_data()
    resources_manager.add_county('romania')


