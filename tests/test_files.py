from entsoe.files import EntsoeFileClient
import os
import pytest


try:
    # Optional helper for local development; tests should still run without it.
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
except ModuleNotFoundError:
    pass

@pytest.fixture
def client():
    if os.getenv("ENTSOE_USERNAME") is None or os.getenv("ENTSOE_PWD") is None:
        pytest.skip("ENTSOE_USERNAME/ENTSOE_PWD not set; skipping ENTSO-E file API integration tests.")
    yield EntsoeFileClient()


def test_single_file(client):
    files = client.list_folder('EnergyPrices_12.1.D_r3')
    assert len(files) > 0
    df = client.download_single_file('EnergyPrices_12.1.D_r3', max(files))
    assert len(df) > 0

def test_list_file(client):
    files = client.list_folder('EnergyPrices_12.1.D_r3')
    assert len(files) > 0
    df = client.download_multiple_files([
        files[max(files)]
    ])
    assert len(df) > 0