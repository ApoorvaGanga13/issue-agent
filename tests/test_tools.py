import pytest

from agent.tools import RepoTools, run_pytest


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "a.py").write_text("def f():\n    return 1\n")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.py").write_text("x = 1\nx = 1\n")
    return tmp_path


def test_list_files(repo):
    out = RepoTools(str(repo)).list_files()
    assert "a.py" in out
    assert "b.py" in out


def test_read_file(repo):
    assert "return 1" in RepoTools(str(repo)).read_file("a.py")


def test_parent_path_is_blocked(repo):
    with pytest.raises(ValueError):
        RepoTools(str(repo)).read_file("../outside.txt")


def test_absolute_path_outside_repo_is_blocked(repo, tmp_path_factory):
    outside = tmp_path_factory.mktemp("other") / "secret.txt"
    outside.write_text("secret")
    with pytest.raises(ValueError):
        RepoTools(str(repo)).read_file(str(outside))


def test_sibling_folder_with_same_prefix_is_blocked(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    evil = tmp_path / "repo_evil"
    evil.mkdir()
    (evil / "secret.txt").write_text("secret")
    with pytest.raises(ValueError):
        RepoTools(str(repo)).read_file("../repo_evil/secret.txt")


def test_edit_replaces_unique_text(repo):
    tools = RepoTools(str(repo))
    assert tools.edit_file("a.py", "return 1", "return 2") == "Edit applied"
    assert "return 2" in (repo / "a.py").read_text()


def test_edit_rejects_ambiguous_match(repo):
    out = RepoTools(str(repo)).edit_file("sub/b.py", "x = 1", "x = 2")
    assert out.startswith("Error")
    assert (repo / "sub" / "b.py").read_text() == "x = 1\nx = 1\n"


def test_edit_rejects_missing_text(repo):
    out = RepoTools(str(repo)).edit_file("a.py", "not in the file", "x")
    assert out.startswith("Error")


def test_search_finds_text_with_line_number(repo):
    assert "a.py:2" in RepoTools(str(repo)).search("return 1")


def test_search_reports_no_matches(repo):
    assert RepoTools(str(repo)).search("zzzz") == "No matches"


def test_run_pytest_reports_a_passing_suite(tmp_path):
    (tmp_path / "test_ok.py").write_text("def test_ok():\n    assert True\n")
    code, _ = run_pytest(tmp_path, mode="off")
    assert code == 0


def test_run_pytest_reports_a_failing_suite(tmp_path):
    (tmp_path / "test_bad.py").write_text("def test_bad():\n    assert False\n")
    code, _ = run_pytest(tmp_path, mode="off")
    assert code == 1
