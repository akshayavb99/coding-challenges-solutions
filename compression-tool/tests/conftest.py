import sys
from pathlib import Path
from typing import Callable

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def isolated_data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create an isolated project-like data directory for file-based tests."""
    import main

    base_dir = tmp_path / "project"
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True)

    monkeypatch.setattr(main, "__file__", str(base_dir / "main.py"))
    return data_dir


@pytest.fixture
def make_encoder(
    isolated_data_dir: Path,
) -> Callable[[str, bytes | None], "main.HuffmanEncoderDecoder"]:
    """Create test input files and return encoders pointed at temp data."""
    import main

    def _make_encoder(
        filename: str,
        content: bytes | None = None,
    ) -> main.HuffmanEncoderDecoder:
        if content is not None:
            (isolated_data_dir / Path(filename).name).write_bytes(content)
        return main.HuffmanEncoderDecoder(filename)

    return _make_encoder
