import configparser

config = configparser.ConfigParser()
config.read('local.settings.json')
STORAGE_CONNECTION_STRING = config.get('Values', "STORAGE_CONNECTION_STRING")
print(STORAGE_CONNECTION_STRING)