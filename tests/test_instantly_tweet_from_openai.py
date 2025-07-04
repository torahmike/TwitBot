import sys
print(sys.path)
import types
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True)
def patch_sys_modules(monkeypatch):
    # Mock 'keys' and 'functions' modules before importing the script
    sys.modules['keys'] = types.ModuleType('keys')
    functions = types.ModuleType('functions')
    functions.generate_response = MagicMock(return_value="Pytest tweet!")
    mock_client = MagicMock()
    # client.create_tweet
    functions.initialize_tweepy = MagicMock(return_value=(mock_client, None))
    functions.get_formatted_date = MagicMock()
    sys.modules['functions'] = functions
    yield

def test_send_post_print_and_tweet(capsys):
    # Import the module fresh to pick up our mocks
    import importlib
    import src.instantly_tweet_from_openai as module
    importlib.reload(module)

    # Patch client.create_tweet to track calls
    client, _ = module.initialize_tweepy()
    client.create_tweet.reset_mock()

    # Call the function
    module.send_post()

    # Check tweet was posted with correct text
    client.create_tweet.assert_called_once_with(text="Pytest tweet!")

    # Check success message was printed
    captured = capsys.readouterr()
    assert "Tweet posted successfully" in captured.out
