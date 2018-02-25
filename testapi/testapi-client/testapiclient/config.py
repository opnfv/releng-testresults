import ConfigParser
import io


class Config:
    # Load the configuration file
    config = {}
    __instance = None

    @staticmethod
    def get_Instance():
        """ Static access method. """
        if Config.__instance is None:
            Config()
        return Config.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if Config.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Config.__instance = self

    def parse_conf(self):
        path = "/etc/testapiclient/config.ini"
        with open(path) as f:
            sample_config = f.read()
        Config.config = ConfigParser.RawConfigParser(allow_no_value=True)
        Config.config.readfp(io.BytesIO(sample_config))

    def get_conf(self):
        if type(Config.config) != "instance":
            self.parse_conf()
        return Config.config
