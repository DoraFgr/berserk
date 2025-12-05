import time
import pytest
import vcr


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["authorization"],
        "match_on": ["method", "scheme", "host", "port", "path", "query", "body"],
        "decode_compressed_response": True,
    }


def pytest_addoption(parser):
    parser.addoption(
        "--live-api",
        action="store_true",
        default=False,
        help="Run all tests live against the API, ignoring VCR cassettes",
    )
    parser.addoption(
        "--live-api-throttle",
        type=float,
        default=1.0,
        help="Number of seconds to wait between live API tests (default 1s)",
    )


@pytest.fixture(autouse=True)
def configure_live_api_mode(request, monkeypatch):
    if request.config.getoption("--live-api"):
        # 1. Bypass VCR decorators
        def pass_through_decorator(*args, **kwargs):
            def decorator(func):
                return func

            return decorator

        monkeypatch.setattr(vcr.VCR, "use_cassette", pass_through_decorator)

        # 2. Polite throttle between tests
        throttle = request.config.getoption("--live-api-throttle")
        time.sleep(throttle)
