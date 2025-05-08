# File     : st_sale_dashboard.py
# Title    : Streamlit銷售案例應用
# Date     : 2025.04.05
# Author   : Ming-Chang Lee
# YouTube  : https://www.youtube.com/@alan9956
# RWEPA    : http://rwepa.blogspot.tw/
# GitHub   : https://github.com/rwepa
# Email    : alan9956@gmail.com

# 載入模組
import pandas as pd
import plotly.express as px  
import streamlit as st  

# 設定頁面標題
st.set_page_config(page_title="RWEPA - 銷售儀表板", page_icon=":bar_chart:", layout="wide")

# 快取資料裝飾子
@st.cache_data  # @: 指保留資料

# 匯入Excel檔案
# Excel下載: https://github.com/rwepa/DataDemo/blob/master/superstore_tw.xlsx
def get_data_from_excel():
    df = pd.read_excel(
        io="data/superstore_tw.xlsx",
        engine="openpyxl",
        sheet_name="訂單",
    )
    return df

df = get_data_from_excel()

# 新增評估欄位 InvoiceYearMonth 發票年月
df['訂單年月'] = df['訂單日期'].map(lambda date: 100*date.year + date.month)  # EX: 2018*100+08=201800+08=201808

# 左側面板佈置

st.sidebar.image("data/rwepa_logo.png")   # 加上企業logo圖

st.sidebar.header("資料篩選")

# 滑桿-年
on = st.sidebar.toggle('選取年')   # toggle:表示滑桿中所要用來選取的欄位、on:表示有滑桿的意思

if on:   # 有就要跑出底下這些資訊
    year = st.sidebar.slider(
        '選取年:',
        min_value = df['訂單日期'].dt.year.min(),
        max_value = df['訂單日期'].dt.year.max(),
        format='%0.0f'
    )
    df = df[df['訂單日期'].dt.year == year]

# 多重選單-區域
area = st.sidebar.multiselect(
    "選取區域:",
    options=df["區域"].unique(),
    default=df["區域"].unique()
)

# 多重選單-細分
customer_type = st.sidebar.multiselect(
    "選取客戶型態:",
    options=df["細分"].unique(),
    default=df["細分"].unique(),
)

# 多重選單-郵寄方式
mailing = st.sidebar.multiselect(
    "選取郵寄方式:",
    options=df["郵寄方式"].unique(),
    default=df["郵寄方式"].unique()
)

# 篩選資料
df_selection = df.query(
    "區域 == @area & 細分 == @customer_type & 郵寄方式 == @mailing"
)

# 檢查資料集篩選結果是否為空白
if df_selection.empty:
    st.warning("目前沒有選取任何資料!")
    st.stop() # 沒有任何資料,先停止App執行.

# 右側佈置
st.title(":bar_chart: 銷售儀表板-2025")

# 關鍵績效指標
total_sales = int(df_selection["銷售額"].sum())

average_sales = round(df_selection["銷售額"].mean(), 1)

average_profits = round(df_selection["利潤"].mean(), 1)

net_profit_margin = round((df_selection["利潤"].sum()/df_selection["銷售額"].sum())*100, 2)

# 右側佈置-4欄設定
column1, column2, column3, column4 = st.columns(4)

with column1:
    st.write('總銷售額:')
    st.markdown('## {:0,.0f}'.format(total_sales))
    
with column2:
    st.write('每筆訂單平均銷售額:')
    st.markdown('## {:0,.0f}'.format(average_sales))
    
with column3:
    st.write('每筆訂單平均獲利:')
    st.markdown('## {:0,.0f}'.format(average_profits))
    
with column4:
    st.write('淨利率(%):')
    st.markdown('## {:0,.2f}'.format(net_profit_margin))

# 右側佈置-3個繪圖區
chart1, chart2, chart3 = st.columns(3)

with chart1:
    
    # 季銷售額線圖

    st.write('季銷售額線圖')

    # 建立季為群組,收入小計資料
    df_sale_quarter = df.groupby(df['訂單日期'].dt.to_period('Q'))['銷售額'].sum().reset_index()

    df_sale_quarter['日期'] = pd.PeriodIndex(df_sale_quarter['訂單日期'], freq='Q').strftime('%Y-%m')
    
    df_sale_quarter = df_sale_quarter.sort_values(by='日期', ascending=True)

    fig_linechart = px.line(df_sale_quarter, x="日期", y="銷售額", markers=True)

    st.plotly_chart(fig_linechart, use_container_width=True)
  
with chart2:

    # 區域vs.銷售額-水平長條圖

    st.write('區域vs.銷售額-水平長條圖')
    sales_by_area = df_selection.groupby(by=['區域'])[['銷售額']].sum().reset_index()
    sales_by_area = sales_by_area.sort_values(by='銷售額').reset_index(drop=True)

    st.bar_chart(sales_by_area, x='區域', y='銷售額', use_container_width=True)

with chart3:

    # 子類別 vs. 銷售額-圓形圖

    st.write('子類別vs.銷售額-圓形圖')    
    sales_by_product_type = df_selection.groupby(by=["子類別"])[["銷售額"]].sum().sort_values(by="銷售額").reset_index()

    sales_by_product_type['銷售額'] = sales_by_product_type['銷售額'].round(2)

    fig_product_pie = px.pie(data_frame = sales_by_product_type,
                             labels = '子類別',
                             values = '銷售額',
                             hover_data= ['子類別'],
                             hole=0.6)

    st.plotly_chart(fig_product_pie, use_container_width=True)

st.write('Powered By: RWEPA, YouTube: https://www.youtube.com/@alan9956')
st.write('Python + Streamlit: https://github.com/rwepa/streamlit_sales_dashboard')
# end
