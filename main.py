import pandas as pd
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="서울 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide",
)

# 데이터 주소
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/"
    "main/data/seoul.csv"
)

st.title("🌡️ 서울의 연평균 기온 변화")
st.write("1907년부터 기록된 서울의 연평균 기온이 어떻게 변해 왔는지 살펴봅니다.")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온을 숫자형으로 변환
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 분석에 필요한 데이터만 사용
    df = df.dropna(subset=["날짜", "평균기온"]).copy()

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    return df


df = load_data()

# 연도별 평균기온 계산
yearly_temp = (
    df.groupby("연도", as_index=False)["평균기온"]
    .mean()
    .rename(columns={"평균기온": "연평균기온"})
)

# 화면에 표시할 기간
min_year = int(yearly_temp["연도"].min())
max_year = int(yearly_temp["연도"].max())

st.subheader(f"{min_year}년 ~ {max_year}년 연평균 기온")

# Streamlit line_chart를 사용하기 위한 형태로 변환
chart_data = yearly_temp.set_index("연도")[["연평균기온"]]

st.line_chart(
    chart_data,
    y="연평균기온",
    x_label="연도",
    y_label="연평균 기온 (℃)",
    height=500,
)

# 간단한 요약 정보
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("분석 기간", f"{min_year}~{max_year}년")

with col2:
    warmest = yearly_temp.loc[
        yearly_temp["연평균기온"].idxmax()
    ]
    st.metric(
        "가장 따뜻했던 해",
        f"{int(warmest['연도'])}년",
        f"{warmest['연평균기온']:.1f}℃",
    )

with col3:
    coldest = yearly_temp.loc[
        yearly_temp["연평균기온"].idxmin()
    ]
    st.metric(
        "가장 추웠던 해",
        f"{int(coldest['연도'])}년",
        f"{coldest['연평균기온']:.1f}℃",
    )

st.caption(
    "출처: 기상 관측 데이터(seoul.csv) | "
    "연평균 기온은 해당 연도의 일평균기온을 평균하여 계산했습니다."
)
