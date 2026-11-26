import pandas as pd


def 정제(df):
    df = df.copy()  
    print("시작        ", len(df))

    df = df.dropna(subset=["점수"]) 
    print("빈 칸 제거  ", len(df))

    df = df.drop_duplicates() 
    print("중복 제거   ", len(df))

    df["반"] = df["반"].str.strip()  
    df["과목"] = df["과목"].str.strip()
    print("공백 제거   ", len(df))

    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)]  
    print("범위 밖 제거", len(df))

    df["점수"] = df["점수"].astype(int) 
    return df


def 수학만(df):
   
    r = df[df["과목"] == "수학"]
    print("수학 행 수:", len(r))
    return r


def 일반_90이상(df):
   
    return df[(df["반"] == "1반") & (df["점수"] >= 90)]


def 그룹평균(df):

    반별 = df.groupby("반")["점수"].mean()
    과목반 = df.groupby(["과목", "반"])["점수"].mean()
    print(반별)
    print(과목반)
    return 반별, 과목반


def 반별통계(df):

    return df.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2)


def 반별평균(df):
   
    return df.groupby("반")["점수"].mean().round(2)


if __name__ == "__main__":
    본 = 정제(pd.read_csv("scores_2026.csv"))
    수학만(본)
    print(일반_90이상(본).shape[0], "행 (1반 & 90점 이상)")
    그룹평균(본)
    print(반별통계(본))
