import configparser
import os
import discord

class Config:
    def __init__(self, config, logger):
        self.config_path = config
        self.logger = logger
        self._load_config()
        self.logger.debug(f"Config initialized with path: {self.config_path}")

    def _load_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        for section in config.sections():
            for key, value in config[section].items():
                key_upper = key.upper()
                try:
                    if value == 'ENV':
                        env_value = os.getenv(key_upper)
                        if env_value is None:
                            self.logger.error(f"Environment variable {key_upper} not found.")
                        else:
                            self.logger.info(f"Environment variable {key_upper} found.")
                            setattr(self, key_upper, env_value)
                    else:
                        if value.startswith('0x') and len(value) == 8:
                            value = discord.Color(int(value, 16))
                        setattr(self, key_upper, value)
                except Exception as e:
                    self.logger.error(f"Error setting attribute {key_upper}: {e}")

    def save_config(self):
        try:
            config = configparser.ConfigParser()
            config['DEFAULT'] = {k.lower(): str(v) for k, v in vars(self).items() if k.isupper()}
            with open(self.config_path, 'w') as configfile:
                config.write(configfile)
            self.logger.info(f"Config saved to path: {self.config_path}")
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")

    def set_variable(self, key, value):
        try:
            if not key.isidentifier():
                raise ValueError("Invalid key format.")
            if not isinstance(value, (str, int, float, bool)):
                raise ValueError("Invalid value type.")
            setattr(self, key.upper(), value)
            self.logger.info(f"Variable {key.upper()} set with value: {value}")
            self.save_config()
        except Exception as e:
            self.logger.error(f"Error setting variable {key}: {e}")
            raise

    def get_variable(self, key, default=None):
        value = getattr(self, key.upper(), default)
        self.logger.debug(f"Retrieved variable {key.upper()}: {value}")
        return value

    def variable_exists(self, key):
        exists = hasattr(self, key.upper())
        self.logger.debug(f"Variable exists check for {key.upper()}: {exists}")
        return exists

    def get_all_variables(self):
        return {k: v for k, v in vars(self).items() if k.isupper()}

    def print_config(self):
        for key, value in self.get_all_variables().items():
            print(f"{key} = {value}")