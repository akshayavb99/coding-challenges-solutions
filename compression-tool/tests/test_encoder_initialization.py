def test_encoder_uses_only_filename_basename(make_encoder) -> None:
    encoder = make_encoder("../nested/sample.txt")

    assert encoder.path.name == "sample.txt"
    assert encoder.path.parent.name == "data"


def test_encoder_creates_expected_paths(make_encoder) -> None:
    encoder = make_encoder("sample.txt")

    assert encoder.path.name == "sample.txt"
    assert encoder.encoded_file.name == "sample_encoded.txt"
    assert encoder.decoded_file.name == "sample_decoded.txt"


def test_encoder_initializes_empty_internal_state(make_encoder) -> None:
    encoder = make_encoder("sample.txt")

    assert encoder.heap == []
    assert encoder.frequency_mapping == {}
    assert encoder.prefix_table == {}
    assert encoder.inverse_prefix_table == {}
    assert encoder.expected_total_chars == 0
