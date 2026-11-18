# 프롬프트 B (명세서 6칸만 보고 작성 — 코드는 보지 않음)
import pytest
from load_scores import load_scores


def make(tmp_path, body):
    p = tmp_path / "t.csv"
    p.write_text("name,score\n" + body, encoding="utf-8")
    return str(p)


def test_정상_여러_줄(tmp_path):
    kept, skipped = load_scores(make(tmp_path, "가,80\n나,90\n"))
    assert kept == [("가", 80), ("나", 90)]
    assert skipped == []


def test_없는_파일은_오류(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(str(tmp_path / "none.csv"))


def test_헤더만_있으면_빈_결과(tmp_path):
    assert load_scores(make(tmp_path, "")) == ([], [])


def test_열이_2개가_아니면_건너뜀(tmp_path):
    kept, skipped = load_scores(make(tmp_path, "가,80,1\n나\n"))
    assert kept == []
    assert len(skipped) == 2


@pytest.mark.parametrize("raw", ["", "abc", "7.5"])
def test_점수가_비었거나_정수가_아니면_건너뜀(tmp_path, raw):
    kept, skipped = load_scores(make(tmp_path, f"가,{raw}\n"))
    assert kept == []
    assert len(skipped) == 1


@pytest.mark.parametrize("score,ok", [(-1, False), (0, True), (100, True), (101, False)])
def test_점수_범위_경계(tmp_path, score, ok):
    kept, skipped = load_scores(make(tmp_path, f"가,{score}\n"))
    assert (len(kept) == 1) == ok
    assert (len(skipped) == 1) == (not ok)


def test_이름이_비면_건너뜀(tmp_path):
    kept, skipped = load_scores(make(tmp_path, ",80\n"))
    assert kept == []
    assert len(skipped) == 1


def test_같은_이름은_둘_다_남긴다(tmp_path):
    kept, _ = load_scores(make(tmp_path, "가,80\n가,90\n"))
    assert len(kept) == 2


def test_빈_줄은_기록_없이_건너뜀(tmp_path):
    kept, skipped = load_scores(make(tmp_path, "가,80\n\n나,90\n"))
    assert len(kept) == 2
    assert skipped == []


def test_건너뛴_줄에는_줄번호가_기록된다(tmp_path):
    kept, skipped = load_scores(make(tmp_path, "가,80\n나,abc\n"))
    assert skipped[0][0] == 3
