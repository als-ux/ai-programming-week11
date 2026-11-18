"""load_scores 테스트 (11주차)

설계표의 여덟 케이스(정상 3 · 예외 2 · 경계 3)를 명세서 6칸만 보고 먼저 만들고,
커버리지의 Missing 줄을 보고 '추가' 케이스를 덧붙였습니다.
"""
from pathlib import Path

import pytest

from load_scores import load_scores

HERE = Path(__file__).parent


def 쓰기(tmp_path, 본문, 이름="임시.csv"):
    """본문(헤더 제외)을 헤더와 함께 임시 CSV로 저장하고 경로를 돌려준다."""
    p = tmp_path / 이름
    p.write_text("name,score\n" + 본문, encoding="utf-8")
    return str(p)


# ── 정상 ──────────────────────────────────────────────
def test_정상_파일을_읽는다():
    kept, skipped = load_scores(str(HERE / "scores.csv"))
    assert len(kept) == 5


def test_빈_줄은_건너뛴다(tmp_path):
    path = 쓰기(tmp_path, "가,80\n\n나,90\n")
    kept, skipped = load_scores(path)
    assert kept == [("가", 80), ("나", 90)]
    assert skipped == []            # 빈 줄은 기록도 하지 않는다


def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    path = 쓰기(tmp_path, '"최,나비",77\n')
    kept, skipped = load_scores(path)
    assert kept == [("최,나비", 77)]
    assert skipped == []


# ── 예외 ──────────────────────────────────────────────
def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores(str(HERE / "empty.csv"))
    assert kept == []
    assert skipped == []


# ── 경계값 ────────────────────────────────────────────
@pytest.mark.parametrize("점수, 유효한가", [
    (-1,  False),   # 경계 바로 아래
    (0,   True),    # ★ 아래쪽 경계
    (1,   True),
    (99,  True),
    (100, True),    # ★ 위쪽 경계
    (101, False),   # 경계 바로 위
])
def test_점수_경계값(tmp_path, 점수, 유효한가):
    path = 쓰기(tmp_path, f"가,{점수}\n")
    kept, skipped = load_scores(path)
    assert (len(kept) == 1) == 유효한가
    assert (len(skipped) == 0) == 유효한가


# ── 추가: 커버리지 Missing 줄에서 나온 케이스 ─────────────
def test_열이_세_개면_건너뛰고_기록한다(tmp_path):
    path = 쓰기(tmp_path, "가,80,비고\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped == [(2, "가,80,비고", "열 개수가 2가 아님")]


def test_이름이_비면_건너뛴다(tmp_path):
    path = 쓰기(tmp_path, ",90\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped[0][2] == "이름이 비어 있음"


def test_점수가_비면_건너뛴다(tmp_path):
    path = 쓰기(tmp_path, "가,\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped[0][2] == "점수가 비어 있음"


@pytest.mark.parametrize("원본", ["결석", "88.5", "7 2"])
def test_점수가_정수가_아니면_건너뛴다(tmp_path, 원본):
    path = 쓰기(tmp_path, f"가,{원본}\n")
    kept, skipped = load_scores(path)
    assert kept == []
    assert skipped[0][2] == "점수가 정수가 아님"


def test_같은_이름은_지우지_않고_둘_다_남긴다(tmp_path):
    path = 쓰기(tmp_path, "김하나,88\n김하나,91\n")
    kept, skipped = load_scores(path)
    assert kept == [("김하나", 88), ("김하나", 91)]


def test_앞뒤_공백은_무시한다(tmp_path):
    path = 쓰기(tmp_path, "가,  77\n")
    kept, skipped = load_scores(path)
    assert kept == [("가", 77)]
