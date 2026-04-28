#!/usr/bin/env python3

"""
 wc-tool: A command-line utility to analyze file properties.

 Supports counting bytes, lines in a file, similar to the Unix `wc` command.
 """

import argparse # Needed to receive and process the input arguments

def main():
    """
     Entry point for the wc-tool CLI.

     Parses command-line arguments and dispatches to the appropriate
     counting function. Prints results to stdout.
     """
    # Define argument parser
    parser = argparse.ArgumentParser(description="Hello from wc-tool!")
    
    # Add flags
    parser.add_argument("-c", "--bytes", action="store_true", help="Count bytes")
    parser.add_argument("-l", "--lines", action="store_true", help="Count number of lines")
    
    # Add argument for taking filename as input
    parser.add_argument("file", help="File to process")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Get the required results
    result = []
    if args.bytes:
        size = count_bytes(args.file)
        result.append(str(size))
        #print(f"{size} {args.file}")
    
    if args.lines:
        line_count = count_lines(args.file)
        result.append(str(line_count))
        #print(f"{line_count} {args.file}")
    
    print(" ".join(result) + " " + args.file)
        
    

def count_bytes(filepath):
    """
     Count the number of bytes in a file.

     Args:
         filepath (str): Path to the file to measure.

     Returns:
         int: Total size of the file in bytes.
     """
    with open(filepath, "rb") as f:
        f.seek(0, 2)   # move to end
        return f.tell()  # byte position = size

def count_lines(filepath, chunk_size=8192):
    """
     Count the number of lines in a file.

     Args:
         filepath (str): Path to the file to measure.

     Returns:
         int: Total number of lines.
     """
    count = 0
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            count += chunk.count(b"\n")
    return count

# Entry point
if __name__ == "__main__":
    main()
