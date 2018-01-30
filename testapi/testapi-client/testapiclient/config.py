import ConfigParser
import io


class Config:
    # Load the configuration file
    config = ''

    @staticmethod
    def parse_conf():
        with open("/etc/testapiclient/config.ini") as f:
            sample_config = f.read()
        Config.config = ConfigParser.RawConfigParser(allow_no_value=True)
        Config.config.readfp(io.BytesIO(sample_config))
