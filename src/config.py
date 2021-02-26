import json, os

with open(os.environ["CONFIG_FILE"]) as config_file:
    configs = json.load(config_file)