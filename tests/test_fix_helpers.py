from pathlib import Path

from fix import changed_files, make_diff


def _dirs(tmp_path):
    before = tmp_path / "before"
    after = tmp_path / "after"
    before.mkdir()
    after.mkdir()
    return before, after


def test_detects_changed_and_new_files_only(tmp_path):
    before, after = _dirs(tmp_path)
    (before / "a.py").write_text("x = 1\n")
    (after / "a.py").write_text("x = 2\n")
    (before / "same.py").write_text("y = 1\n")
    (after / "same.py").write_text("y = 1\n")
    (after / "new.py").write_text("z = 1\n")
    files = changed_files(before, after)
    assert sorted(str(f) for f in files) == ["a.py", "new.py"]


def test_diff_shows_removed_and_added_lines(tmp_path):
    before, after = _dirs(tmp_path)
    (before / "a.py").write_text("x = 1\n")
    (after / "a.py").write_text("x = 2\n")
    diff = make_diff(before, after, [Path("a.py")])
    assert "-x = 1" in diff
    assert "+x = 2" in diff


def test_cache_folders_are_ignored(tmp_path):
    before, after = _dirs(tmp_path)
    (after / "__pycache__").mkdir()
    (after / "__pycache__" / "junk.py").write_text("junk")
    assert changed_files(before, after) == []
