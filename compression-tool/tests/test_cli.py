from pathlib import Path

import pytest

import main


def test_main_handles_missing_file_gracefully(
    isolated_data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "missing.bin")

    main.main()

    captured = capsys.readouterr()
    assert "could not be found inside the data folder" in captured.out


def test_main_runs_workflow_for_valid_file(
    isolated_data_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    (isolated_data_dir / "sample.txt").write_bytes(b"hello hello")
    monkeypatch.setattr("builtins.input", lambda _: "sample.txt")

    main.main()

    captured = capsys.readouterr()
    assert "Encoding completed!" in captured.out
    assert "Decoded file can be found" in captured.out
    assert (isolated_data_dir / "sample_decoded.txt").read_bytes() == b"hello hello"


def test_main_handles_permission_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("builtins.input", lambda _: "sample.txt")
    monkeypatch.setattr(
        main.HuffmanEncoderDecoder,
        "build_char_frequency_map",
        lambda self: (_ for _ in ()).throw(PermissionError()),
    )

    main.main()

    captured = capsys.readouterr()
    assert "Permission denied" in captured.out
