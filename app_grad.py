from matplotlib import pyplot as plt
import streamlit as st 
import pandas as pd
import plotly.express as px 
import seaborn as sb
import plotly.graph_objects as go
import numpy as np
import platform

def run_grad_app() :
    df = pd.read_csv('csv/grad-students.csv',index_col=0)
    
    st.subheader('학과를 선택하면 졸업,취업,실업자수를 보여드립니다.')
    choice = st.selectbox('학과의 카테고리를 선택해주세요' , df['Major_category'].unique())
    
    
    select = st.selectbox('학과를 선택해주세요' ,df.loc[df['Major_category'] == choice, :]['Major'] )
    st.info('{}과를 선택하셨습니다.'.format(select))
    
    df = df.drop(['Grad_sample_size','Grad_median','Grad_P25','Grad_P75','Nongrad_unemployment_rate','Nongrad_median','Nongrad_P25','Nongrad_P75','Nongrad_full_time_year_round','Grad_unemployment_rate','Grad_full_time_year_round','Major_code'],axis= 1)
    
    
    if True :
        st.dataframe(df.loc[df['Major'] == select , : ])
        st.text('결과를 보여드리겠습니다.')
    
    
    
    
    st.subheader('학과별로 비교해드립니다.')
    

   
    
    column = st.radio('원하시는 컬럼을 선택하세요' , df.columns[2 : ])
    
 
    st.text('Grad_total = 총 대학원 졸업생 수\nGrad_employed = 대학원 졸업 취업자 수 \nGrad_unemployed = 대학원 졸업 실업자 수 \nNongrad_total = 총 대학교 졸업자 수 \nNongrad_employed = 대학교 졸업 취업자 수 \nNongrad_unemployed = 대학교 졸업 실업자 수 \nGrad_share = 대학원 졸업자 비율 \nGrad_premium = 둘의 급여 차이')
 
    
    fig = px.bar(df, y=column, x='Major', text=column)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig)

    st.subheader('대학원졸과 대졸이 가장 많이 취업되는 학과 입니다.')


    st.text(' y축에는 대졸 취업율을 , x축에는 대학원 취업율을 적용했습니다.')
    
    st.text('BUSINESS MANAGEMENT AND ADMINISTRATION가 가장 높습니다.')
    
    fig1 = px.scatter(df, x="Grad_employed", y="Nongrad_employed",
    size="Grad_employed", color="Major_category",
    hover_name="Major", log_x=True, size_max=60)
    st.plotly_chart(fig1)
   
    if True :
        st.subheader('대학원졸의 취업수,졸업비율,급여차이비율의 관계')
        st.text('위에서 말한 비율은 대학교와의 비율이다. \n취업수의 비율을 맞추기 위해 나누기 100000을 했다. ')
        st.text('꼭짓점에서 멀어질수록 수치는 낮아진다.')
        st.text('모든 학과를 볼 수 있으며 카테고리별로 색을 정했다.')
        
        df['Grad_employed'] = df['Grad_employed'] / 100000
        fig2 = px.scatter_ternary(df, a="Grad_employed", b="Grad_share", c="Grad_premium", hover_name="Major",
        color="Major_category", size="Grad_share", size_max=15,
        color_discrete_map = {"Grad_employed": "blue", "Grad_share": "green", "Grad_premium":"red"} )
        st.plotly_chart(fig2)

        df2 = df.corr()
        st.subheader('상관계수 분석')
        
        st.text('일반적으로 \nr이 -1.0과 -0.7 사이이면, 강한 음적 선형관계,\nr이 -0.7과 -0.3 사이이면, 뚜렷한 음적 선형관계,\nr이 -0.3과 -0.1 사이이면, 약한 음적 선형관계,\nr이 -0.1과 +0.1 사이이면, 거의 무시될 수 있는 선형관계,\nr이 +0.1과 +0.3 사이이면, 약한 양적 선형관계,\nr이 +0.3과 +0.7 사이이면, 뚜렷한 양적 선형관계,\nr이 +0.7과 +1.0 사이이면, 강한 양적 선형관계'
        )
        fig3 = plt.figure()
        
        heatmap = sb.heatmap(data= df2 ,cmap= 'RdPu' , annot = True , fmt='.2f' , linewidth=0.8)
        
        st.pyplot(fig3)
        
        st.subheader('대졸 취업자, 급여비율차이,졸업비율 관계')
        st.text('대학원 졸업비율이 낮을수록 대졸은 취업이 잘 되고\n급여차이가 날 수록 취업이 안된다.')
        df_grad = df
        
        df_grad['Nongrad_employed'] = df_grad['Nongrad_employed']/100000
        df_grad['Grad_share'] = round(df_grad['Grad_share'],1)
        df_grad['Grad_premium'] = round(df_grad['Grad_premium'],1)
        df_grad['Nongrad_employed'] = round(df_grad['Nongrad_employed'],1)
        
        fig = px.scatter_3d(df_grad, x='Nongrad_employed', y='Grad_share', z='Grad_premium',
              color='Grad_premium', size='Grad_premium', size_max=18,
              symbol='Major', opacity=0.7)

        # tight layout
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        st.plotly_chart(fig)