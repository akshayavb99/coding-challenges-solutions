import pytest


def test_write_table_to_output_writes_metadata(make_encoder) -> None:
    encoder = make_encoder("sample.bin")
    encoder.frequency_mapping = {97: 2, 98: 1}
    encoder.prefix_table = {97: "1", 98: "0"}

    encoder.write_table_to_output()

    metadata = encoder.encoded_file.read_bytes()
    assert b"PREFIX-TABLE-START\n" in metadata
    assert b"TOTAL-COUNT 3\n" in metadata
    assert b"97 1\n" in metadata
    assert b"98 0\n" in metadata
    assert b"PREFIX-TABLE-END\n" in metadata


def test_read_table_from_input_reads_metadata(make_encoder) -> None:
    encoder = make_encoder("sample.bin")
    encoder.encoded_file.write_bytes(
        b"PREFIX-TABLE-START\n"
        b"TOTAL-COUNT 3\n"
        b"97 1\n"
        b"98 0\n"
        b"PREFIX-TABLE-END\n"
    )

    with encoder.encoded_file.open("rb") as encoded_file:
        encoder.read_table_from_input(encoded_file)

    assert encoder.expected_total_chars == 3
    assert encoder.inverse_prefix_table == {"1": 97, "0": 98}


def test_read_table_from_input_raises_for_invalid_header(make_encoder) -> None:
    encoder = make_encoder("sample.bin")
    encoder.encoded_file.write_bytes(b"INVALID\n")

    with encoder.encoded_file.open("rb") as encoded_file:
        with pytest.raises(ValueError, match="Invalid encoded file format"):
            encoder.read_table_from_input(encoded_file)
