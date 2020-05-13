import pytest
import requests

from dotestow import Checksum


def test_checksum_initialization():
    checksum = Checksum
    assert checksum