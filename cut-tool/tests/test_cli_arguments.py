import pytest
import subprocess
import sys
import os
from pathlib import Path


@pytest.fixture
def sample_file(tmp_path):
    """Create a temporary sample file for CLI tests"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("name\tage\tcity\nAlice\t30\tNYC\nBob\t25\tLA\n")
    return str(test_file)


class TestArgumentParsing:
    """Test command-line argument parsing"""

    def test_fails_when_both_f_and_d_are_missing(self, sample_file):
        """Test that the tool errors when neither -f nor -d is provided"""
        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", sample_file],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True
        )

        assert result.returncode != 0

    def test_succeeds_with_only_d_flag(self, sample_file):
        """Test that providing only -d (without -f) is valid"""
        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", "-d", "\t", sample_file],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True
        )

        assert result.returncode == 0

    def test_fields_argument_with_file(self, sample_file):
        """Test basic usage with -f flag"""
        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", "-f", "2", sample_file],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert lines[0] == 'age'
        assert lines[1] == '30'

    def test_multiple_fields_comma_separated(self, sample_file):
        """Test specifying multiple fields with comma separation"""
        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", "-f", "1,3", sample_file],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert lines[0] == 'name\tcity'

    def test_multiple_fields_space_separated(self, sample_file):
        """Test specifying multiple fields with space separation"""
        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", "-f", "1 3", sample_file],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert 'name\tcity' in lines[0]

    def test_custom_delimiter(self, tmp_path):
        """Test custom delimiter with -d flag"""
        test_file = tmp_path / "comma.txt"
        test_file.write_text("name,age,city\nAlice,30,NYC\nBob,25,LA\n")

        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", "-f", "2", "-d", ",", str(test_file)],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert lines[0] == 'age'
        assert lines[1] == '30'

    def test_default_delimiter_is_tab(self, sample_file):
        """Test that tab is default delimiter when -d not specified"""
        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", "-f", "2", sample_file],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        # Should successfully parse tab-separated file
        assert lines[0] == 'age'

    def test_file_not_found_error(self):
        """Test error message when file doesn't exist"""
        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", "-f", "1", "nonexistent.txt"],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True
        )

        assert result.returncode != 0
        # Should contain error about file not found
        assert "nonexistent" in result.stderr.lower() or "error" in result.stderr.lower()

    def test_help_flag(self):
        """Test --help flag"""
        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", "--help"],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "usage" in result.stdout.lower() or "build your own" in result.stdout.lower()


class TestErrorHandling:
    """Test error handling in CLI"""

    def test_missing_file_argument_with_stdin(self):
        """Test that stdin is used when file argument is missing"""
        input_data = "a\tb\tc\n"
        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", "-f", "1"],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            input=input_data,
            capture_output=True,
            text=True
        )

        # Should succeed and read from stdin
        assert result.returncode == 0
        assert result.stdout.strip() == "a"

    def test_invalid_field_number(self, sample_file):
        """Test non-numeric field argument"""
        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", "-f", "abc", sample_file],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True
        )

        # Should fail due to invalid integer
        assert result.returncode != 0


class TestStdinProcessing:
    """Test stdin input processing"""

    def test_stdin_input_basic(self):
        """Test reading and processing stdin input"""
        input_data = "name\tage\tcity\nAlice\t30\tNYC\nBob\t25\tLA\n"

        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", "-f", "2"],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            input=input_data,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert lines[0] == 'age'
        assert lines[1] == '30'
        assert lines[2] == '25'

    def test_stdin_with_custom_delimiter(self):
        """Test stdin input with custom delimiter"""
        input_data = "name,age,city\nAlice,30,NYC\nBob,25,LA\n"

        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", "-f", "2", "-d", ","],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            input=input_data,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert lines[0] == 'age'
        assert lines[1] == '30'

    def test_stdin_multiple_fields(self):
        """Test stdin input with multiple fields"""
        input_data = "a\tb\tc\nd\te\tf\n"

        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", "-f", "1,3"],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            input=input_data,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        lines = result.stdout.strip().split('\n')
        assert lines[0] == 'a\tc'
        assert lines[1] == 'd\tf'

    def test_stdin_empty_input(self):
        """Test handling of empty stdin"""
        input_data = ""

        result = subprocess.run(
            [sys.executable, "-m", "cut_tool.main", "-f", "1"],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            input=input_data,
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert result.stdout == ""
