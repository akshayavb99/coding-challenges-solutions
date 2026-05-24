import pytest

import main


def run_full_pipeline(encoder: main.HuffmanEncoderDecoder) -> None:
    encoder.build_char_frequency_map()
    encoder.build_binary_tree()
    encoder.generate_prefix_table()
    encoder.encode()
    encoder.decode()


def test_encode_creates_output_file_with_metadata(make_encoder) -> None:
    encoder = make_encoder("sample.bin", b"hello")
    encoder.build_char_frequency_map()
    encoder.build_binary_tree()
    encoder.generate_prefix_table()

    encoder.encode()

    assert encoder.encoded_file.exists()
    assert encoder.encoded_file.read_bytes().startswith(b"PREFIX-TABLE-START\n")


def test_encode_handles_empty_file(make_encoder) -> None:
    encoder = make_encoder("empty.bin", b"")
    encoder.build_char_frequency_map()
    encoder.build_binary_tree()
    encoder.generate_prefix_table()

    encoder.encode()

    assert encoder.encoded_file.exists()
    assert b"TOTAL-COUNT 0\n" in encoder.encoded_file.read_bytes()


def test_encode_raises_key_error_when_prefix_table_is_missing_byte(make_encoder) -> None:
    encoder = make_encoder("sample.bin", b"ab")
    encoder.frequency_mapping = {97: 1, 98: 1}
    encoder.prefix_table = {97: "0"}

    with pytest.raises(KeyError):
        encoder.encode()


@pytest.mark.parametrize(
    ("filename", "content"),
    [
        ("text.txt", b"hello hello hello"),
        ("single.bin", b"aaaaaa"),
        ("all-bytes.bin", bytes(range(256))),
        ("binary.bin", bytes([0, 255, 10, 0, 128, 255, 1])),
    ],
)
def test_encode_decode_round_trip(make_encoder, filename: str, content: bytes) -> None:
    encoder = make_encoder(filename, content)

    run_full_pipeline(encoder)

    assert encoder.decoded_file.read_bytes() == content


def test_decode_writes_exactly_expected_byte_count_despite_padding(make_encoder) -> None:
    encoder = make_encoder("single.bin", b"aaaaaa")
    run_full_pipeline(encoder)

    assert encoder.decoded_file.read_bytes() == b"aaaaaa"
    assert encoder.decoded_file.stat().st_size == 6


def test_decode_raises_for_invalid_encoded_metadata(make_encoder) -> None:
    encoder = make_encoder("sample.bin")
    encoder.encoded_file.write_bytes(b"INVALID\n")

    with pytest.raises(ValueError, match="Invalid encoded file format"):
        encoder.decode()


def test_save_decoded_text_writes_exact_bytes(make_encoder) -> None:
    encoder = make_encoder("sample.bin")

    encoder._save_decoded_text(bytearray([0, 1, 255]))

    assert encoder.decoded_file.read_bytes() == bytes([0, 1, 255])
