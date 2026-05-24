import os
import heapq
from pathlib import Path
from typing import BinaryIO, Optional, Union, cast


class HuffmanNode:
    """A node in a Huffman coding tree.

    Leaf nodes store an original byte value in ``char``. Internal nodes use an
    empty string and store the combined frequency of their child nodes.
    """

    def __init__(self, char: Union[int, str] = '', freq: int = 0) -> None:
        """Initialize a Huffman tree node.

        Args:
            char: Byte value for a leaf node, or an empty string for an
                internal node.
            freq: Frequency count represented by this node.

        Returns:
            None.

        Raises:
            No exceptions are raised directly by this method.
        """
        self.char = char  # This will hold an integer (0-255) in binary mode
        self.freq = freq
        self.left: Optional["HuffmanNode"] = None
        self.right: Optional["HuffmanNode"] = None
    
    def __lt__(self, other: "HuffmanNode") -> bool:
        """Compare two nodes for heap ordering.

        Args:
            other: The node to compare against this node.

        Returns:
            True if this node should be ordered before ``other`` in the heap;
            otherwise False. Frequency is compared first, then ``char`` is used
            as a tie breaker.

        Raises:
            AttributeError: If ``other`` does not provide ``freq`` and ``char``
                attributes.
        """
        # Tie breaker: if frequencies match, compare byte values to keep heap stable
        if self.freq == other.freq:
            return str(self.char) < str(other.char)
        return self.freq < other.freq


class HuffmanEncoderDecoder:
    """Encode and decode files using Huffman coding.

    The class expects input files to live in a ``data`` directory next to this
    script. Encoded and decoded files are also written to that directory.
    """

    def __init__(self, filename: Union[str, Path]) -> None:
        """Create a Huffman encoder/decoder for a file in the data directory.

        Args:
            filename: Name or path of the input file. Only the final file name
                component is used, which keeps all reads and writes inside the
                local ``data`` directory.

        Returns:
            None.

        Raises:
            No exceptions are raised directly by this method.
        """
        base_dir = Path(__file__).resolve().parent
        clean_filename = Path(filename).name
        
        # Absolute structural paths
        self.path: Path = base_dir / "data" / clean_filename
        
        name = Path(clean_filename).stem
        extension = Path(clean_filename).suffix
        
        self.encoded_file: Path = base_dir / "data" / f"{name}_encoded{extension}"
        self.decoded_file: Path = base_dir / "data" / f"{name}_decoded{extension}"
        
        self.heap: list[HuffmanNode] = []
        self.frequency_mapping: dict[int, int] = {}
        self.prefix_table: dict[int, str] = {}
        self.inverse_prefix_table: dict[str, int] = {}
        self.expected_total_chars: int = 0
    
    def build_char_frequency_map(self) -> None:
        """Build a frequency table for each byte value in the source file.

        Args:
            None.

        Returns:
            None. The result is stored in ``self.frequency_mapping``.

        Raises:
            FileNotFoundError: If the source file does not exist.
            PermissionError: If the source file cannot be read.
            IsADirectoryError: If the source path points to a directory.
            OSError: If another operating-system file error occurs.
        """
        # Read the input file byte by byte
        with open(self.path, "rb") as file:
            byte = file.read(1)
            while byte:
                byte_val = byte[0]  # Get integer value (0-255)
                self.frequency_mapping[byte_val] = self.frequency_mapping.get(byte_val, 0) + 1
                byte = file.read(1)

    def build_binary_tree(self) -> None:
        """Build the Huffman tree from the byte frequency mapping.

        Args:
            None.

        Returns:
            None. The tree root is stored at ``self.heap[0]`` when at least one
            byte frequency exists.

        Raises:
            No exceptions are raised directly by this method when
            ``self.frequency_mapping`` contains integer frequencies.
        """
        # Bug fixed: Correctly maps char first, then freq to match class init
        self.heap = [HuffmanNode(char, freq) for char, freq in self.frequency_mapping.items()]
        heapq.heapify(self.heap)
        
        while len(self.heap) > 1:
            left = heapq.heappop(self.heap)
            right = heapq.heappop(self.heap)
            newNode = HuffmanNode('', left.freq + right.freq)
            newNode.left = left
            newNode.right = right
            heapq.heappush(self.heap, newNode)
    
    def generate_prefix_table(self) -> None:
        """Generate the byte-to-prefix lookup table from the Huffman tree.

        Args:
            None.

        Returns:
            None. Generated prefix codes are stored in ``self.prefix_table``.

        Raises:
            No exceptions are raised directly by this method.
        """
        if not self.heap:
            return
        root = self.heap[0]
        
        def helperFunc(node: HuffmanNode, code: str) -> None:
            """Recursively traverse the Huffman tree and assign prefix codes.

            Args:
                node: Current Huffman tree node being visited.
                code: Prefix code accumulated from the root to ``node``.

            Returns:
                None. Leaf byte codes are added to ``self.prefix_table``.

            Raises:
                RecursionError: If the Huffman tree is unexpectedly deep enough
                    to exceed Python's recursion limit.
            """
            if node.left is None and node.right is None:
                self.prefix_table[cast(int, node.char)] = code
                return
            
            if node.left:
                helperFunc(node.left, code + '0')
            if node.right:
                helperFunc(node.right, code + '1')
        
        # Guard case for single-character files
        if root.left is None and root.right is None:
            self.prefix_table[cast(int, root.char)] = '0'
        else:
            helperFunc(root, '')
    
    def write_table_to_output(self) -> None:
        """Write prefix-table metadata to the encoded output file.

        Args:
            None.

        Returns:
            None. Metadata is written to ``self.encoded_file``.

        Raises:
            PermissionError: If the encoded output file cannot be written.
            IsADirectoryError: If the encoded output path points to a directory.
            OSError: If another operating-system file error occurs.
        """
        # Calculate total characters by summing up all frequencies
        total_chars = sum(self.frequency_mapping.values())
        
        with open(self.encoded_file, 'wb') as f:
            f.write("PREFIX-TABLE-START\n".encode('utf-8'))
            # Write total count on its own metadata line
            f.write(f"TOTAL-COUNT {total_chars}\n".encode('utf-8'))
            
            for byte_val, code in self.prefix_table.items():
                f.write(f"{byte_val} {code}\n".encode('utf-8'))
            f.write("PREFIX-TABLE-END\n".encode('utf-8'))
    
    def encode(self) -> None:
        """Encode the source file and write the compressed output file.

        Args:
            None.

        Returns:
            None. Encoded output is written to ``self.encoded_file``.

        Raises:
            KeyError: If ``self.prefix_table`` does not contain a code for a
                byte read from the source file.
            FileNotFoundError: If the source file does not exist.
            PermissionError: If the source or encoded output file cannot be
                accessed.
            IsADirectoryError: If a file path points to a directory.
            OSError: If another operating-system file error occurs.
        """
        # 1. Write metadata table
        self.write_table_to_output()
        
        # 2. Append packed compressed binary bits to our file
        with open(self.encoded_file, 'ab') as f_out:
            with open(self.path, 'rb') as f_in:
                bit_buffer = ""
                byte = f_in.read(1)
                
                while byte:
                    byte_val = byte[0]
                    # Append bit string ('0101...') to our buffer string
                    bit_buffer += self.prefix_table[byte_val]
                    
                    # Once we gather 8 or more bits, process them into true bytes
                    while len(bit_buffer) >= 8:
                        byte_to_write = 0
                        for i in range(8):
                            # Bit shifting: Shift left and insert bit value
                            byte_to_write = (byte_to_write << 1) | int(bit_buffer[i])
                        
                        # Write the single integer byte directly
                        f_out.write(bytes([byte_to_write]))
                        bit_buffer = bit_buffer[8:]  # Keep remaining bits
                        
                    byte = f_in.read(1)
                
                # 3. Deal with leftover padding bits at the very end of the file
                if len(bit_buffer) > 0:
                    padding_needed = 8 - len(bit_buffer)
                    # Add trailing zeros to complete the final byte
                    bit_buffer += "0" * padding_needed
                    
                    byte_to_write = 0
                    for i in range(8):
                        byte_to_write = (byte_to_write << 1) | int(bit_buffer[i])
                    f_out.write(bytes([byte_to_write]))
    
    def read_table_from_input(self, f: BinaryIO) -> None:
        """Read prefix-table metadata from an encoded file.

        Args:
            f: Binary file object positioned at the start of an encoded file.

        Returns:
            None. Parsed metadata is stored in ``self.inverse_prefix_table`` and
            ``self.expected_total_chars``.

        Raises:
            ValueError: If the encoded file does not start with the expected
                prefix-table header.
            UnicodeDecodeError: If header bytes cannot be decoded as UTF-8.
            OSError: If reading from the file object fails.
        """
        self.inverse_prefix_table = {}
        self.expected_total_chars = 0  # Track this globally in the class
        
        line = f.readline().decode('utf-8', errors='replace').strip()
        if line != "PREFIX-TABLE-START":
            raise ValueError("Invalid encoded file format")
            
        while True:
            line = f.readline().decode('utf-8', errors='replace').strip()
            if line == "PREFIX-TABLE-END" or not line:
                break
                
            # Intercept our total count variable
            if line.startswith("TOTAL-COUNT"):
                self.expected_total_chars = int(line.split(" ")[1])
                continue
                
            parts = line.split(" ")
            if len(parts) == 2:
                self.inverse_prefix_table[parts[1]] = int(parts[0])

    def decode(self) -> None:
        """Decode the encoded file and write the restored byte output.

        Args:
            None.

        Returns:
            None. Decoded bytes are written to ``self.decoded_file``.

        Raises:
            ValueError: If the encoded file metadata is invalid.
            FileNotFoundError: If the encoded file does not exist.
            PermissionError: If the encoded or decoded file cannot be accessed.
            IsADirectoryError: If a file path points to a directory.
            OSError: If another operating-system file error occurs.
        """
        print(f"Reading encoded file from {self.encoded_file}...")
        decoded_bytes = bytearray()
        
        with open(self.encoded_file, 'rb') as f_in:
            # Re-read the header and fetch expected_total_chars
            self.read_table_from_input(f_in)
            
            # Diagnostic check to make sure the header was actually parsed:
            print(f"Targeting exactly {self.expected_total_chars} characters for restoration...")
            
            current_code = ""
            chars_recovered = 0
            
            chunk = f_in.read(1024)
            while chunk:
                for byte_val in chunk:
                    # Unpack integer byte into an 8-bit sequence
                    for shift in range(7, -1, -1):
                        bit = (byte_val >> shift) & 1
                        current_code += str(bit)
                        
                        # Check the table immediately as bits drop in
                        if current_code in self.inverse_prefix_table:
                            original_byte = self.inverse_prefix_table[current_code]
                            decoded_bytes.append(original_byte)
                            chars_recovered += 1
                            current_code = ""  # Reset prefix token
                            
                            # THE HARD STOP: Exit the entire method instantly 
                            # the exact microsecond we hit our target size.
                            if chars_recovered == self.expected_total_chars:
                                print(f"Successfully recovered all {chars_recovered} bytes. Stopping.")
                                # Break out of everything by converting to text and saving
                                self._save_decoded_text(decoded_bytes)
                                return
                                
                chunk = f_in.read(1024)
                
        # Fallback if file ends early for some reason
        self._save_decoded_text(decoded_bytes)

    def _save_decoded_text(self, decoded_bytes: Union[bytes, bytearray]) -> None:
        """Save extracted data as raw bytes to preserve exact output size.

        Args:
            decoded_bytes: Bytes recovered from the encoded input.

        Returns:
            None. The data is written to ``self.decoded_file``.

        Raises:
            PermissionError: If the decoded output file cannot be written.
            IsADirectoryError: If the decoded output path points to a directory.
            OSError: If another operating-system file error occurs.
        """
        print(f"Writing decoded output to {self.decoded_file}...")
        
        # Open in 'wb' mode instead of text mode
        with open(self.decoded_file, 'wb') as f_out:
            f_out.write(decoded_bytes)
        
        
def main() -> None:
    """Run the command-line Huffman compression and decompression workflow.

    Args:
        None.

    Returns:
        None.

    Raises:
        No exceptions are intentionally propagated. Common file and operating
        system exceptions are caught and reported to the user.
    """
    print("Hello from compression-tool!")
    try:
        input_filename = input("Please give the name of the file to be encoded: ")
        huffman_obj = HuffmanEncoderDecoder(input_filename)
        
        print(f"Building character map for file at {huffman_obj.path}...")
        huffman_obj.build_char_frequency_map()
        print("Character map is complete!\n")
        
        print("Creating Huffman Tree...")
        huffman_obj.build_binary_tree()
        print("Huffman Tree created!\n")
        
        print("Generating Prefix Table...")
        huffman_obj.generate_prefix_table()
        print("Prefix Table generated!\n")
        
        print("Encoding input file...")
        huffman_obj.encode()
        print(f"Encoding completed! Encoded file can be found at {huffman_obj.encoded_file}\n")
        
        print("Decoding the encoded file...")
        huffman_obj.decode()
        print(f"Decoded file can be found at {huffman_obj.decoded_file}\n")
        
        print("Comparing file sizes...")
        original_size = os.path.getsize(huffman_obj.path)
        encoded_size = os.path.getsize(huffman_obj.encoded_file)
        decoded_size = os.path.getsize(huffman_obj.decoded_file)
        
        print(f"Original file size: {original_size} bytes")
        print(f"Encoded file size:  {encoded_size} bytes")
        print(f"Decoded file size:  {decoded_size} bytes")
        
        # Calculate reduction based on the encoded file size
        if original_size > 0:
            reduction = ((original_size - encoded_size) / original_size) * 100
            print(f"Reduction percentage: {reduction:.2f}%")
        else:
            print("Reduction percentage: 0.00% (Original file is empty)")
        
        
        
    except FileNotFoundError:
        print("Error: The requested input file could not be found inside the data folder.")
    except PermissionError:
        print("Permission denied")
    except IsADirectoryError:
        print("Expected a file, got a directory")
    except OSError as e:
        print("An OSError occurred: " + str(e))
    except Exception as e:
        print("An error occurred: " + str(e))


if __name__ == "__main__":
    main()
