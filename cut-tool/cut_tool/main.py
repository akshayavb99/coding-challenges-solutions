"""
Cut Tool - A Python implementation of the Unix cut command.

This module provides functionality to extract columns or fields from text input,
similar to the Unix cut command. It supports field-based extraction with custom
delimiters and can read from files or standard input.

Example:
    Extract fields 1 and 3 from a CSV file:
    $ cccut -f 1,3 -d ',' data.csv

    Extract fields from stdin:
    $ cat data.csv | cccut -f 2 -d ','
"""

import argparse
import sys
from typing import List, Optional, TextIO


class CutTool:
    """
    A tool for extracting specific fields or columns from text input.
    
    This class mimics the functionality of the Unix cut command, allowing users
    to select specific fields from structured text data. Fields are identified
    by position (1-indexed) and separated by a configurable delimiter.
    
    Attributes:
        fields (List[int] or None): Zero-indexed positions of fields to extract.
            None means select all fields.
        delimiter (str): The character or string used to separate fields.
        input_content (TextIO or List[str]): The input source to process.
    
    Example:
        >>> lines = ["apple,banana,cherry\\n", "1,2,3\\n"]
        >>> tool = CutTool("1,3", ",", lines)
        >>> result = tool.get_result()
        >>> result
        ['apple,cherry', '1,3']
    """
    
    def __init__(self, fields: Optional[str], delimiter: str, input_content: TextIO):
        """
        Initialize the CutTool with field specifications and input data.
        
        Args:
            fields (str or None): Comma or space-separated field numbers (1-indexed).
                Examples: "1,3,5", "1 3 5", or None to select all fields.
            delimiter (str): The character or string that separates fields.
                Examples: ",", "\t", "|", etc.
            input_content (TextIO): A file-like object or iterable of strings
                containing the lines to process. Typically sys.stdin or an open file.
        
        Raises:
            ValueError: If fields string is malformed or contains non-integer values.
        """
        self.fields = self.get_fields(fields)
        self.delimiter = delimiter
        self.input_content = input_content
    
    def get_fields(self, fields: Optional[str]) -> Optional[List[int]]:
        """
        Parse and convert field specifications to zero-indexed positions.
        
        Converts user-friendly 1-indexed field numbers to 0-indexed Python list
        indices. Supports multiple input formats and deduplicates field indices.
        
        Args:
            fields (str or None): Field specification string. Supports:
                - Comma-separated: "1,2,3"
                - Space-separated: "1 2 3"
                - Mixed: "1, 2, 3"
                - None: Select all fields
        
        Returns:
            List[int]: Zero-indexed positions of specified fields, or None if
                all fields should be selected. Duplicate fields are removed.
        
        Raises:
            ValueError: If field specification contains non-integer values
                or if conversion fails.
        
        Example:
            >>> tool = CutTool("1,3,5", ",", [])
            >>> tool.fields
            [0, 2, 4]
            
            >>> tool2 = CutTool(None, ",", [])
            >>> tool2.fields is None
            True
        """
        if fields is None:
            return None  # meaning "select all"

        result = []

        # Support both "1,2,3" and "1 2 3" formats
        parts = fields.replace(",", " ").split()

        for part in parts:
            try:
                f = int(part) - 1  # Convert to 0-based index
                if f not in result:  # Avoid duplicate field indices
                    result.append(f)
            except ValueError:
                raise ValueError(f"Invalid field specification: '{part}' is not an integer")
        
        return result

    def get_result(self) -> List[str]:
        """
        Extract specified fields from input lines.
        
        Processes each line of input, splits by the configured delimiter,
        extracts the specified fields, and returns the results with the
        same delimiter.
        
        Returns:
            List[str]: Processed output lines with selected fields joined by
                the original delimiter. Each line has trailing newlines removed.
        
        Raises:
            FileNotFoundError: If the input file cannot be found.
            IOError: If there are issues reading from the input source.
            Exception: For any other errors during processing.
        
        Example:
            >>> lines = ["apple,banana,cherry\\n", "1,2,3\\n"]
            >>> tool = CutTool("1,3", ",", lines)
            >>> tool.get_result()
            ['apple,cherry', '1,3']
        
        Note:
            If a line has fewer fields than requested, only available fields
            are included in the output.
        """
        try:
            result = []
            for line in self.input_content:
                # Split line by delimiter and remove trailing newline
                fields = line.rstrip("\n").split(self.delimiter)
                
                if self.fields is None:
                    # Select all fields
                    selected = fields
                else:
                    # Select only specified fields that exist in the line
                    selected = [fields[i] for i in self.fields if i < len(fields)]
                
                # Rejoin selected fields with the original delimiter
                result.append(self.delimiter.join(selected))

            return result

        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {e}")
        except IOError as e:
            raise IOError(f"Cannot read content: {e}")


def main() -> None:
    """
    Entry point for the cut tool command-line interface.
    
    Parses command-line arguments, opens the input file (or uses stdin),
    creates a CutTool instance, and prints the results to stdout.
    
    Command-line Arguments:
        -f, --fields (str, optional): Comma or space-separated field numbers
            (1-indexed). Examples: "1,3,5" or "1 3 5"
        -d, --delimiter (str, optional): Field delimiter character. 
            Defaults to tab (\t) if not specified.
        file (str, optional): Input file path. If omitted or "-", reads from stdin.
    
    Behavior:
        - Requires either -f or -d to be specified (or both)
        - Reads from the specified file, or stdin if no file given
        - Prints extracted fields to stdout, one line per input line
        - Default delimiter is tab, matching Unix cut behavior
    
    Raises:
        SystemExit: If invalid arguments are provided or if required arguments
            are missing.
    
    Example:
        Extract fields 1 and 2 from a CSV:
        $ cccut -f 1,2 -d ',' data.csv
        
        Extract field 2 from piped input:
        $ cat data.csv | cccut -f 2 -d ','
    """
    parser = argparse.ArgumentParser(
        prog='cccut',
        description='Python implementation of the Unix cut command. Extract columns from text input.',
        add_help=True
    )
    
    parser.add_argument(
        "-f", 
        "--fields", 
        type=str, 
        required=False,
        help="Field numbers to extract (1-indexed). Format: '1,3,5' or '1 3 5'"
    )
    parser.add_argument(
        '-d', 
        '--delimiter', 
        type=str, 
        required=False,
        help="Field delimiter character (default: tab)"
    )
    parser.add_argument(
        'file', 
        nargs="?", 
        type=str, 
        default=None,
        help="Input file path. Omit or use '-' to read from stdin"
    )
    
    args = parser.parse_args()
    
    # Validate that at least one of -f or -d is specified
    if args.fields is None and args.delimiter is None:
        parser.error("Please specify a delimiter (-d) or list of fields (-f)")
    
    # Set default delimiter to tab if not specified (Unix cut default)
    if not args.delimiter:
        args.delimiter = "\t"
    
    # Open input file or use stdin
    args.file = open(args.file, 'r') if args.file and args.file != "-" else sys.stdin
    
    try:
        # Create tool instance and process input
        cut_obj = CutTool(args.fields, args.delimiter, args.file)
        for line in cut_obj.get_result():
            print(line)
    finally:
        # Close file if it was opened (not stdin)
        if args.file != sys.stdin:
            args.file.close()


if __name__ == "__main__":
    main()