def test_build_binary_tree_handles_empty_frequency_map(make_encoder) -> None:
    encoder = make_encoder("empty.bin")

    encoder.build_binary_tree()

    assert encoder.heap == []


def test_build_binary_tree_handles_single_byte_frequency_map(make_encoder) -> None:
    encoder = make_encoder("single.bin")
    encoder.frequency_mapping = {97: 5}

    encoder.build_binary_tree()

    assert len(encoder.heap) == 1
    assert encoder.heap[0].char == 97
    assert encoder.heap[0].freq == 5


def test_build_binary_tree_root_frequency_equals_total(make_encoder) -> None:
    encoder = make_encoder("sample.bin")
    encoder.frequency_mapping = {97: 2, 98: 3, 99: 4}

    encoder.build_binary_tree()

    assert len(encoder.heap) == 1
    assert encoder.heap[0].freq == 9
