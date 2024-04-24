from unittest import TestCase, mock
from unittest.mock import patch

import requests
from giza.schemas.endpoints import Endpoint, EndpointsList
from giza.schemas.workspaces import Workspace

from giza_actions.utils import get_endpoint_uri, get_workspace_uri, read_json


@patch("giza.client.EndpointsClient.list")
def test_get_endpoint_uri_successful(mock_get):
    """
    Tests successful retrieval of the deployment URI for a model and version.
    """
    endpoint_data = Endpoint(
        id=999,
        size="S",
        is_active=True,
        model_id=999,
        version_id=999,
        uri="testing.uri",
    )
    endpoint_list = EndpointsList(root=[endpoint_data])
    mock_get.return_value = endpoint_list
    uri = get_endpoint_uri(model_id=788, version_id=23)
    assert uri == "testing.uri"
    mock_get.assert_called_once()


@patch("giza.client.EndpointsClient.list")
def test_get_endpoint_uri_not_found(mock_list):
    """
    Tests the case where no active deployment is found for the model and version.
    """
    endpoint_list = EndpointsList(root=[])
    mock_list.return_value = endpoint_list
    uri = get_endpoint_uri(model_id=516, version_id=19)
    assert uri is None
    mock_list.assert_called_once()


@mock.patch("giza.client.WorkspaceClient.get")
def test_get_workspace_uri_successful(mock_get):
    """
    Tests successful retrieval the URI of the current workspace.
    """
    mock_workspace = Workspace(status="test", url="test_url")
    mock_get.return_value = mock_workspace
    workspace_uri = get_workspace_uri()
    assert workspace_uri == "test_url"
    mock_get.assert_called_once()


@mock.patch("giza.client.WorkspaceClient.get")
def test_get_workspace_uri_request_exception(mock_get):
    """
    Tests RequestException in get_workspace_uri method().
    """
    mock_get.side_effect = requests.exceptions.RequestException

    TestCase.assertRaises(
        TestCase, requests.exceptions.RequestException, get_workspace_uri
    )


@mock.patch("builtins.open")
@mock.patch("json.load", mock.MagicMock(side_effect=[{"test": "test"}]))
def test_read_json_successful(*args):
    """
    Tests when file is found
    """
    response = read_json("path/to/open")
    assert response == {"test": "test"}
    assert response != None


@mock.patch("builtins.open", side_effect=FileNotFoundError)
def test_read_json_file_not_found(mock_open):
    """
    Tests when the JSON file is not found.
    """
    with TestCase.assertRaises(TestCase, FileNotFoundError):
        read_json("/notFound/")
