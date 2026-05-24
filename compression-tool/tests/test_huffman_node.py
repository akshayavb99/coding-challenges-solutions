import main


def test_huffman_node_initializes_defaults() -> None:
    node = main.HuffmanNode()

    assert node.char == ""
    assert node.freq == 0
    assert node.left is None
    assert node.right is None


def test_huffman_node_initializes_leaf_node() -> None:
    node = main.HuffmanNode(97, 3)

    assert node.char == 97
    assert node.freq == 3


def test_huffman_node_compares_by_frequency() -> None:
    low_frequency = main.HuffmanNode(65, 1)
    high_frequency = main.HuffmanNode(66, 2)

    assert low_frequency < high_frequency


def test_huffman_node_uses_char_as_tie_breaker() -> None:
    earlier_char = main.HuffmanNode(65, 2)
    later_char = main.HuffmanNode(66, 2)

    assert earlier_char < later_char
