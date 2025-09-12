#This file checks that an error is raised when a file is called that should be ignored according to the config

import yaml
from commit_messenger.utils import utils
import os
import pytest

here = os.path.dirname(__file__)

yaml_path = os.path.join(here, "test_config_files_should_be_ignored.yaml")
with open(yaml_path, "r") as stream:
    test_yaml_file = yaml.safe_load(stream)

config = utils.Config(test_yaml_file)

def test_raise_error_file_should_be_ignored():
    with pytest.raises(ValueError, match = "File file_that_should_be_ignored.py should be ignored, commit message can't be generated"):
        config.create_error_if_file_should_be_ignored("file_that_should_be_ignored.py")