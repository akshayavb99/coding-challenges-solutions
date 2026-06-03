import pytest
import os
import sys

fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')

@pytest.fixture
def sample_tab_file():
    return os.path.join(fixtures_dir, 'sample_tab.txt')

@pytest.fixture
def sample_comma_file():
    return os.path.join(fixtures_dir, 'sample_comma.txt')

@pytest.fixture
def sample_pipe_file():
    return os.path.join(fixtures_dir, 'sample_pipe.txt')

@pytest.fixture
def empty_file():
    return os.path.join(fixtures_dir, 'empty.txt')

@pytest.fixture
def single_line_file():
    return os.path.join(fixtures_dir, 'single_line.txt')

@pytest.fixture
def with_empty_fields_file():
    return os.path.join(fixtures_dir, 'with_empty_fields.txt')
