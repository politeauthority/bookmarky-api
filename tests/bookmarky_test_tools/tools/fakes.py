"""
    Cver Test
    Cver Test Tools - Fake
    A collection of tools to help create random test data.

"""
import random

from faker import Faker


def random_image_name() -> str:
    """Create a fake image name prefixed with "cver-test"
    """
    fake = Faker()
    fake_name = fake.name()
    fake_name = fake_name.replace(" ", "-")
    fake_name = fake_name.lower()
    return f"cver-tests/{fake_name}"


def random_int(start: int = None, end: int = None) -> int:
    if not start:
        start = 100
    if not end:
        end = 10000
    return random.randint(start, end)

# End File: cver/tests/cver_test_tools/tools/fakes.py
