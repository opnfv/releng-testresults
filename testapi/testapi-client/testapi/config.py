import ConfigParser
import io
import os


class Config:
    # Load the configuration file
    config = ''
    mode = ''

    @staticmethod
    def parse_conf(mode):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(__location__ + "/config.ini") as f:
            sample_config = f.read()
        Config.config = ConfigParser.RawConfigParser(allow_no_value=True)
        Config.config.readfp(io.BytesIO(sample_config))
        Config.mode = mode
