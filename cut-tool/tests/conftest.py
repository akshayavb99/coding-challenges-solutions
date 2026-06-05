import pytest
import os
import sys

fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures')

@pytest.fixture
def sample_tab_file():
    path = os.path.join(fixtures_dir, 'sample_tab.txt')
    f = open(path, 'r')
    yield f
    f.close()

@pytest.fixture
def sample_comma_file():
    path = os.path.join(fixtures_dir, 'sample_comma.txt')
    f = open(path, 'r')
    yield f
    f.close()

@pytest.fixture
def sample_pipe_file():
    path = os.path.join(fixtures_dir, 'sample_pipe.txt')
    f = open(path, 'r')
    yield f
    f.close()

@pytest.fixture
def empty_file():
    path = os.path.join(fixtures_dir, 'empty.txt')
    f = open(path, 'r')
    yield f
    f.close()

@pytest.fixture
def single_line_file():
    path = os.path.join(fixtures_dir, 'single_line.txt')
    f = open(path, 'r')
    yield f
    f.close()

@pytest.fixture
def with_empty_fields_file():
    path = os.path.join(fixtures_dir, 'with_empty_fields.txt')
    f = open(path, 'r')
    yield f
    f.close()
