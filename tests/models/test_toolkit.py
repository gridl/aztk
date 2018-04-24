import pytest

from aztk.error import InvalidModelError
from aztk.models import Toolkit
from aztk.utils import constants

docker_image_version = constants.DOCKER_IMAGE_VERSION

def test_basic_toolkit():
    toolkit = Toolkit(software="spark", version="2.2")
    assert toolkit.software == "spark"
    assert toolkit.version == "2.2"

def test_numeric_value():
    toolkit = Toolkit(software="spark", version=2.2)
    assert toolkit.software == "spark"
    assert toolkit.version == "2.2"

def test_environment():
    toolkit = Toolkit(software="spark", version="2.2", environment="python")
    assert toolkit.software == "spark"
    assert toolkit.version == "2.2"
    assert toolkit.environment == "python"

# Test validation
def test_valid_software_and_version():
    Toolkit(software="spark", version="2.2").validate()

def test_valid_software_version_and_environment():
    Toolkit(software="spark", version="2.2", environment="python").validate()

def test_missing_software_raise_error():
    with pytest.raises(InvalidModelError):
        Toolkit(software=None, version="2.2").validate()

def test_invalid_software_raise_error():
    with pytest.raises(InvalidModelError):
        Toolkit(software="non-supported", version="2.2").validate()

def test_missing_version_raise_error():
    with pytest.raises(InvalidModelError):
        Toolkit(software="spark", version=None).validate()

def test_invalid_version_raise_error():
    with pytest.raises(InvalidModelError):
        Toolkit(software="spark", version="780.0").validate()

def test_invalid_environment_raise_error():
    with pytest.raises(InvalidModelError):
        Toolkit(software="spark", version="2.2", environment="dos").validate()

def test_invalid_environment_version_raise_error():
    with pytest.raises(InvalidModelError):
        Toolkit(software="spark", version="2.2", environment="python", environment_version="7.1.9").validate()


## Test get docker image
def test_get_right_docker_repo():
    repo = Toolkit(software="spark", version="2.2").get_docker_repo(False)

    assert repo == "aztk/spark:v{0}-spark2.2-base".format(docker_image_version)

def test_get_right_docker_repo_for_gpu():
    repo = Toolkit(software="spark", version="2.1").get_docker_repo(True)

    assert repo == "aztk/spark:v{0}-spark2.1-gpu".format(docker_image_version)


def test_get_right_docker_repo_with_env():
    repo = Toolkit(software="spark", version="2.2", environment="python").get_docker_repo(False)

    assert repo == "aztk/spark:v{0}-spark2.2-python-base".format(docker_image_version)

def test_get_right_docker_repo_with_env_for_gpu():
    repo = Toolkit(software="spark", version="2.2", environment="python").get_docker_repo(True)

    assert repo == "aztk/spark:v{0}-spark2.2-python-gpu".format(docker_image_version)
