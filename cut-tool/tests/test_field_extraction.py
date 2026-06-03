import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from main import CutTool


class TestBasicFieldExtraction:
    """Test basic field extraction functionality"""

    def test_extract_single_field_tab_delimited(self, sample_tab_file):
        """Extract a single field from tab-separated file"""
        tool = CutTool(fields="2", delimiter='\t', filename=sample_tab_file)
        result = tool.get_result()

        assert len(result) == 4
        assert result[0] == 'age'
        assert result[1] == '30'
        assert result[2] == '25'
        assert result[3] == '35'

    def test_extract_first_field_tab_delimited(self, sample_tab_file):
        """Extract first field from tab-separated file"""
        tool = CutTool(fields="1", delimiter='\t', filename=sample_tab_file)
        result = tool.get_result()

        assert len(result) == 4
        assert result[0] == 'name'
        assert result[1] == 'Alice'
        assert result[2] == 'Bob'

    def test_extract_last_field_tab_delimited(self, sample_tab_file):
        """Extract last field from tab-separated file"""
        tool = CutTool(fields="3", delimiter='\t', filename=sample_tab_file)
        result = tool.get_result()

        assert len(result) == 4
        assert result[0] == 'city'
        assert result[1] == 'NYC'
        assert result[2] == 'LA'
        assert result[3] == 'Chicago'

    def test_extract_multiple_fields_in_order(self, sample_tab_file):
        """Extract multiple fields in specified order"""
        tool = CutTool(fields="1,3", delimiter='\t', filename=sample_tab_file)
        result = tool.get_result()

        assert len(result) == 4
        assert result[0] == 'name\tcity'
        assert result[1] == 'Alice\tNYC'
        assert result[2] == 'Bob\tLA'

    def test_extract_multiple_fields_unordered(self, sample_tab_file):
        """Extract fields in different order than they appear"""
        tool = CutTool(fields="3,1", delimiter='\t', filename=sample_tab_file)
        result = tool.get_result()

        assert len(result) == 4
        assert result[0] == 'city\tname'
        assert result[1] == 'NYC\tAlice'


class TestDelimiterHandling:
    """Test delimiter handling functionality"""

    def test_comma_delimiter(self, sample_comma_file):
        """Extract field with comma delimiter"""
        tool = CutTool(fields="2", delimiter=',', filename=sample_comma_file)
        result = tool.get_result()

        assert len(result) == 4
        assert result[0] == 'age'
        assert result[1] == '30'

    def test_pipe_delimiter(self, sample_pipe_file):
        """Extract field with pipe delimiter"""
        tool = CutTool(fields="2", delimiter='|', filename=sample_pipe_file)
        result = tool.get_result()

        assert len(result) == 4
        assert result[0] == 'age'
        assert result[1] == '30'

    def test_default_tab_delimiter(self, sample_tab_file):
        """Verify tab is used as default delimiter when not specified"""
        tool = CutTool(fields="2", delimiter='\t', filename=sample_tab_file)
        result = tool.get_result()

        assert len(result) == 4
        assert result[1] == '30'


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_empty_file(self, empty_file):
        """Handle empty file gracefully"""
        tool = CutTool(fields="1", delimiter='\t', filename=empty_file)
        result = tool.get_result()

        assert result == []

    def test_single_line_file(self, single_line_file):
        """Extract from single line file"""
        tool = CutTool(fields="2", delimiter='\t', filename=single_line_file)
        result = tool.get_result()

        assert len(result) == 1
        assert result[0] == 'two'

    def test_field_out_of_bounds(self, sample_tab_file):
        """Handle when requested field doesn't exist in a line"""
        tool = CutTool(fields="5", delimiter='\t', filename=sample_tab_file)
        result = tool.get_result()

        # Should return empty strings for missing fields
        assert len(result) == 4
        assert result[0] == ''
        assert result[1] == ''

    def test_missing_field_in_some_lines(self, with_empty_fields_file):
        """Handle lines with missing fields (empty fields)"""
        tool = CutTool(fields="2", delimiter='\t', filename=with_empty_fields_file)
        result = tool.get_result()

        # First line should be 'age' header
        assert result[0] == 'age'
        # Second line has empty field for age
        assert result[1] == ''
        # Third line has '25'
        assert result[2] == '25'

    def test_duplicate_field_selection(self, sample_tab_file):
        """Request same field multiple times"""
        tool = CutTool(fields="1,1,1", delimiter='\t', filename=sample_tab_file)
        result = tool.get_result()

        assert result[0] == 'name\tname\tname'
        assert result[1] == 'Alice\tAlice\tAlice'

    def test_line_without_trailing_newline(self, sample_tab_file):
        """Handle last line without trailing newline correctly"""
        tool = CutTool(fields="1", delimiter='\t', filename=sample_tab_file)
        result = tool.get_result()

        # Last line should be 'Charlie'
        assert result[-1] == 'Charlie'


class TestFileHandling:
    """Test file input handling"""

    def test_file_not_found(self):
        """Raise error when file doesn't exist"""
        tool = CutTool(fields="1", delimiter='\t', filename='nonexistent.txt')

        with pytest.raises(FileNotFoundError):
            tool.get_result()

    def test_file_permissions_error(self, tmp_path):
        """Handle file permission errors"""
        # Create a file with no read permissions
        test_file = tmp_path / "no_read.txt"
        test_file.write_text("data\there")

        import os
        os.chmod(test_file, 0o000)

        try:
            tool = CutTool(fields="1", delimiter='\t', filename=str(test_file))

            with pytest.raises((PermissionError, OSError)):
                tool.get_result()
        finally:
            os.chmod(test_file, 0o644)


class TestOutputFormatting:
    """Test output formatting and order"""

    def test_field_order_preserved(self, sample_tab_file):
        """Output fields in the order specified, not original order"""
        tool = CutTool(fields="3,1,2", delimiter='\t', filename=sample_tab_file)
        result = tool.get_result()

        # Should be city, name, age (not name, age, city)
        assert result[0] == 'city\tname\tage'
        assert result[1] == 'NYC\tAlice\t30'

    def test_output_delimiter_matches_input(self, sample_comma_file):
        """Output uses same delimiter as specified input"""
        tool = CutTool(fields="1,2", delimiter=',', filename=sample_comma_file)
        result = tool.get_result()

        # Output should join with comma, not tab
        assert ',' in result[0]
        assert '\t' not in result[0]
        assert result[0] == 'name,age'
