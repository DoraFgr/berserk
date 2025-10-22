import pytest

from berserk import Client


def test_get_top_valid(monkeypatch, requests_mock):
    client = Client()

    sample = {
        "active": [],
        "upcoming": [],
        "past": {"currentPage": 1, "maxPerPage": 24, "currentPageResults": []},
    }

    requests_mock.get(
        "https://lichess.org/api/broadcast/top?page=1&html=False",
        json=sample,
    )

    res = client.broadcasts.get_top(page=1, html=False)
    assert isinstance(res, dict)
    assert res["past"]["currentPage"] == 1


def test_get_top_invalid_page_type():
    client = Client()
    with pytest.raises(ValueError):
        client.broadcasts.get_top(page="one")  # type: ignore


def test_get_top_invalid_page_value():
    client = Client()
    with pytest.raises(ValueError):
        client.broadcasts.get_top(page=0)
