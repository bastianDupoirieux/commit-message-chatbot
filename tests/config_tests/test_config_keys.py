#This test ensures that the function to check the existence of mandatory keys in the Config class works
import yaml
from commit_messenger.utils import utils
import os
import pytest

here = os.path.dirname(__file__)

yaml_path = os.path.join(here, "test_config_keys.yaml")
with open(yaml_path, "r") as stream:
    test_yaml_file = yaml.safe_load(stream)

config = utils.Config(test_yaml_file)

def test_raise_key_error():
    with pytest.raises(KeyError, match = "Missing key value files_to_ignore in config"):
        config.run_config_checks()

