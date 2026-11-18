# 성적 관리 프로그램

## 무엇을 하나요 (What)
성적 CSV 파일을 읽어 유효한 (이름, 점수)만 골라 내고, 건너뛴 줄은 이유와 함께 기록합니다.

## 왜 만들었나요 (Why)
실제 성적 파일에는 빈 칸 · 범위 밖 점수 · 정수가 아닌 값 · 중복 이름이 섞여 있어 그냥 읽으면 프로그램이 죽거나 잘못된 평균이 나오기 때문입니다.
(※ 이 칸은 본인의 경험과 말로 다시 다듬어 주세요.)

## 어떻게 쓰나요 (How)
```
python load_scores.py scores.csv
```
- 점수는 0~100 사이 정수만 인정합니다.
- 같은 이름이 두 번 나오면 지우지 않고 둘 다 남깁니다(동명이인 가능성).
- 파일이 없으면 `FileNotFoundError`를 그대로 올립니다.

## 어떻게 테스트하나요
```
pip install pytest pytest-cov
pytest
pytest --cov=load_scores --cov-report=term-missing
```
통과 화면 캡처: (여기에 이미지 삽입)

## 파일 구성
| 파일 | 역할 |
|---|---|
| `load_scores.py` | 성적 CSV를 읽는 함수 |
| `test_load_scores.py` | 직접 만든 테스트 (정상·예외·경계값) |
| `test_ai_A.py` · `test_ai_B.py` | AI에게 코드/명세를 줘서 받은 테스트 |
| `scores.csv` · `empty.csv` · `weird.csv` | 시험용 데이터 |
| `bug3_logic.py` | 함정 실험용 고장난 코드 |
| `prompts.txt` | A/B 프롬프트 원문 |

## 만든 사람
손민준 (2026100284) · 미래융합학부
AI 사용: 테스트 코드와 README 초안 작성에 Claude를 활용했고, 케이스 설계와 검증은 직접 했습니다.
