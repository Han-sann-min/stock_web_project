import streamlit as st
import pandas as pd
import FinanceDataReader as fdr
import datetime
import matplotlib.pyplot as plt
import matplotlib 
from io import BytesIO
import plotly.graph_objects as go
import pandas as pd
from datetime import date
import plotly.io as pio # Plotly input output
import plotly.express as px # 빠르게 그리는 방법
import plotly.graph_objects as go # 디테일한 설정
import plotly.figure_factory as ff # 템플릿 불러오기
from plotly.subplots import make_subplots # subplot 만들기
from plotly.validators.scatter.marker import SymbolValidator # Symbol 꾸미기에 사용됨
import xlsxwriter
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

output = BytesIO()


def get_stock_info():
    base_url =  "http://kind.krx.co.kr/corpgeneral/corpList.do"    
    method = "download"
    url = "{0}?method={1}".format(base_url, method)   
    df = pd.read_html(url, header=0, encoding='cp949')[0]
    df['종목코드']= df['종목코드'].apply(lambda x: f"{x:06d}")     
    df = df[['회사명','종목코드']]
    return df

def get_ticker_symbol(company_name):     
    df = get_stock_info()
    code = df[df['회사명']==company_name]['종목코드'].values    
    ticker_symbol = code[0]
    return ticker_symbol


# Use widgets' returned values in variables
st.sidebar.markdown("<p style='font-size:24px;'><b>회사 이름과 기간을 입력하세요</b></p>", unsafe_allow_html=True)
company_name = st.sidebar.text_input("회사이름")


    # 날짜 범위 선택 (달력 형태) - Sidebar에서 입력
date_range = st.sidebar.date_input("날짜 선택", min_value=date(2009, 1, 1), max_value=date(2023, 12, 1), value=(date(2019, 1, 1),date(2019, 1, 3)))

    # 선택된 날짜 기간 출력
start_date = date_range[0] if len(date_range) > 0 else None
end_date = date_range[1] if len(date_range) > 1 else None
button_check = st.sidebar.button('주가 데이터 확인')

st.markdown("<p style='font-size:42px;'><b>무슨 주식을 사야 부자가 되려나...</b></p>", unsafe_allow_html=True)

# 코드 조각 추가
if button_check == True:
    ticker_symbol = get_ticker_symbol(company_name)     
    start_p = start_date            
    end_p = end_date
    df = fdr.DataReader(ticker_symbol, start_p, end_p, exchange="KRX")
    df.index = df.index.date
    st.subheader(f"[{company_name}] 주가 데이터")
    st.dataframe(df.head())
    df.reset_index(inplace=True)
    df.rename(columns={"index": "Date"}, inplace=True)
    fig = px.line(df, x="Date", y="Close",
             title='주식 차트',
             
             )
    fig.update_layout(title=dict(text=f"{company_name}의 주식 차트", x=0.5))
    st.plotly_chart(fig)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="CSV 파일 다운로드",
            data=df.to_csv(),
            file_name=f'{company_name}주가 정보.csv',
            mime='text/csv',
        )
    excel_data = BytesIO()   
    
    with col2 :
        st.download_button(
            label="엑셀 파일 다운로드",
            data = excel_data.read(),
            file_name=f'{company_name}주가 정보.xlsx',
            
        )
