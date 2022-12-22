from matplotlib import pyplot as plt
import streamlit as st 
import pandas as pd
import plotly.express as px 
import seaborn as sb
import plotly.graph_objects as go
import numpy as np

# 이코드는 ec2한글 폰트가 설치되어있어야하고
# 파이썬에서 한글이 가능하도록 먼저 셋팅해야한다
# https://luvris2.tistory.com/119#1.4.%20matplotlib%EC%97%90%20%ED%95%9C%EA%B8%80%20%ED%8F%B0%ED%8A%B8%20%ED%99%95%EC%9D%B8
import platform
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Linux':
    rc('font', family='NanumGothic')
    
from sklearn.decomposition import PCA
from sklearn.datasets import load_boston
import webbrowser

def run_all_age() :
    df = pd.read_csv('csv/all-ages.csv',index_col=0)
    
    st.subheader('학과를 선택하면 졸업,취업,실업자수를 보여드립니다.')
    choice = st.selectbox('학과의 카테고리를 선택해주세요' , df['Major_category'].unique())
    
    
    select = st.selectbox('학과를 선택해주세요' ,df.loc[df['Major_category'] == choice, :]['Major'] )
    st.info('{}과를 선택하셨습니다.'.format(select))
    df = df.drop(['Major_code','Median','P25th','P75th','Employed_full_time_year_round'] , axis= 1)


   
     
    df = df.rename( columns = { 'Major_category' : '학과 카테고리','Total' : '총 졸업자', 'Employed':'취업자 수','Unemployed':'실업자','Unemployment_rate' : '실업자비율'})
    df2 = df.loc[df['Major']==select , :]
    st.dataframe(df2)
        
 
    

    
    fig2=plt.figure()
    plt.bar(np.arange(3),df2.iloc[0,-4:-1])
    plt.xticks(np.arange(3),['Total','Employed','Unemployed'])

    st.pyplot(fig2)
    

    
    
    
    

    
    
    st.text('Major는 학과 입니다.')
    
    st.success('카테고리별 취업율 1위부터 10위까지 보여드리겠습니다.')
    st.info('{}카테고리를 선택하셨습니다.'.format(choice))
    
    df['취업율'] = (df['취업자 수']/df['총 졸업자'] * 100) 
    
    df_category = df.loc[df['학과 카테고리']==choice , : ]
    
    st.dataframe(df_category.sort_values('취업율', ascending=False).head(10))
    
    df_max = df.loc[(df['학과 카테고리']==choice )   ,  ]
    max = df_max.loc[df_max['취업율'] == df_max['취업율'].max(), 'Major'].values
    st.text('가장 높은 학과는 {}입니다.'.format(max))
    
    
    st.success('전체 중 취업율 1위부터 10위까지 보여드리겠습니다.')
    st.dataframe(df.sort_values('취업율', ascending=False).head(10))
    
    
    
    st.text('가장 높은 학과는 COMPUTER AND INFORMATION SYSTEMS입니다.')
    


    X = df[['취업자 수','실업자']]

    pca = PCA(n_components=2)
    components = pca.fit_transform(X)

    fig3 = px.scatter(components, x=0, y=1, color=df['학과 카테고리'])
    st.plotly_chart(fig3)
    
    st.text('pca기법으로 실업자수와 취업자수를 분석해서 나타냈습니다.')
    st.text('설명이 필요하다면 아래 페이지를 들어가 주세요')
    if st.button('pca설명') :
        webbrowser.open('http://matrix.skku.ac.kr/math4ai-intro/W12/')
    