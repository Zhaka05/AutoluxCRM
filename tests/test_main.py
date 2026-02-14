import pytest
import requests

def test_page_content():
    page = requests.get("http://127.0.0.1:8000")
    assert "All tickets" in page.text
    assert "New Request" in page.text
    assert "Report" in page.text

def test_main_page_status_code():
    page = requests.get("http://127.0.0.1:8000")
    assert page.status_code == 200