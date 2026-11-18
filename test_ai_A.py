# 프롬프트 A (load_scores.py 코드를 보고 작성)
import pytest
from load_scores import load_scores


def write_csv(tmp_path, content, name="data.csv"):
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return str(p)


def test_valid_rows(tmp_path):
    path = write_csv(tmp_path, "name,score\nAlice,90\nBob,75\n")
    kept, skipped = load_scores(path)
    assert kept == [("Alice", 90), ("Bob", 75)]
    assert skipped == []


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_scores("does_not_exist.csv")


def test_header_only(tmp_path):
    path = write_csv(tmp_path, "name,score\n")
    assert load_scores(path) == ([], [])


def test_blank_line_ignored(tmp_path):
    path = write_csv(tmp_path, "name,score\nAlice,90\n\nBob,80\n")
    kept, skipped = load_scores(path)
    assert len(kept) == 2
    assert skipped == []


def test_wrong_column_count(tmp_path):
    path = write_csv(tmp_path, "name,score\nAlice,90,extra\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped == [(2, "Alice,90,extra", "열 개수가 2가 아님")]


def test_empty_name(tmp_path):
    path = write_csv(tmp_path, "name,score\n,90\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped[0][2] == "이름이 비어 있음"


def test_empty_score(tmp_path):
    path = write_csv(tmp_path, "name,score\nAlice,\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped[0][2] == "점수가 비어 있음"


def test_non_integer_score(tmp_path):
    path = write_csv(tmp_path, "name,score\nAlice,abc\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped[0][2] == "점수가 정수가 아님"


@pytest.mark.parametrize("score,valid", [(-1, False), (0, True), (100, True), (101, False)])
def test_score_boundaries(tmp_path, score, valid):
    path = write_csv(tmp_path, f"name,score\nAlice,{score}\n")
    kept, skipped = load_scores(path)
    assert (len(kept) == 1) == valid


def test_duplicate_names_kept(tmp_path):
    path = write_csv(tmp_path, "name,score\nAlice,90\nAlice,80\n")
    kept, _ = load_scores(path)
    assert kept == [("Alice", 90), ("Alice", 80)]


def test_whitespace_stripped(tmp_path):
    path = write_csv(tmp_path, "name,score\n  Alice , 90 \n")
    kept, _ = load_scores(path)
    assert kept == [("Alice", 90)]
