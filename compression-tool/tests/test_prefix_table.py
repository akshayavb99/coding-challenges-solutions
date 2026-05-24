def assert_prefix_codes_are_unique(prefix_table: dict[int, str]) -> None:
    codes = list(prefix_table.values())
    assert len(codes) == len(set(codes))


def test_generate_prefix_table_does_nothing_for_empty_heap(make_encoder) -> None:
    encoder = make_encoder("empty.bin")

    encoder.generate_prefix_table()

    assert encoder.prefix_table == {}


def test_generate_prefix_table_handles_single_byte_tree(make_encoder) -> None:
    encoder = make_encoder("single.bin")
    encoder.frequency_mapping = {97: 5}
    encoder.build_binary_tree()

    encoder.generate_prefix_table()

    assert encoder.prefix_table == {97: "0"}


def test_generate_prefix_table_contains_code_for_each_byte(make_encoder) -> None:
    encoder = make_encoder("sample.bin")
    encoder.frequency_mapping = {97: 2, 98: 3, 99: 4}
    encoder.build_binary_tree()

    encoder.generate_prefix_table()

    assert set(encoder.prefix_table) == {97, 98, 99}
    assert all(encoder.prefix_table.values())


def test_generate_prefix_table_codes_are_unique(make_encoder) -> None:
    encoder = make_encoder("sample.bin")
    encoder.frequency_mapping = {97: 2, 98: 3, 99: 4, 100: 5}
    encoder.build_binary_tree()

    encoder.generate_prefix_table()

    assert_prefix_codes_are_unique(encoder.prefix_table)
