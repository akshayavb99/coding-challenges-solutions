import pytest


def test_build_char_frequency_map_counts_binary_data(make_encoder) -> None:
    encoder = make_encoder("sample.bin", b"aabbc")

    encoder.build_char_frequency_map()

    assert encoder.frequency_mapping == {97: 2, 98: 2, 99: 1}


def test_build_char_frequency_map_handles_empty_file(make_encoder) -> None:
    encoder = make_encoder("empty.bin", b"")

    encoder.build_char_frequency_map()

    assert encoder.frequency_mapping == {}


def test_build_char_frequency_map_raises_for_missing_file(make_encoder) -> None:
    encoder = make_encoder("missing.bin")

    with pytest.raises(FileNotFoundError):
        encoder.build_char_frequency_map()
