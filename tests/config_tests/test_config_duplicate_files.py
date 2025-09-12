import yaml
from commit_messenger.utils import utils
import os
import pytest

here = os.path.dirname(__file__)

yaml_file = os.path.join(here, 'test_config_duplicate_files.yaml')

with open(yaml_file, 'r') as stream:
    config_for_test = yaml.safe_load(stream)

config = utils.Config(config_for_test)

def test_error_when_duplicate_files():
    with pytest.raises(ValueError):
        config.run_config_checks()