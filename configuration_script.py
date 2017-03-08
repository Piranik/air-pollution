from config_utils.config import ConfigYaml
from downloader.downloader import Donwloader
from data_importer import import_data

if __name__ == '__main__':
    app_config = ConfigYaml().get_config()
    downloader = Donwloader(app_config)
    # downloader.prepare_environment()
    # downloader.download_stations()
    # downloader.download_diseases()
    import_data(app_config)



