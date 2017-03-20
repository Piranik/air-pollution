from managers.resources_manager import Resources_Manager
from config_utils.config import ConfigYaml

if __name__ == '__main__':
    app_config = ConfigYaml().get_config()
    resources_manager = Resources_Manager(app_config)
    resources_manager.remove_stations()
    resources_manager.remove_parameters()
