from matplotlib import pyplot as plt
import streamlit as st 
import pandas as pd
import plotly.express as px 
import seaborn as sb
import plotly.graph_objects as go

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
        
    x = df.loc[df['Major']==select , '총 졸업자'].values
    y = df.loc[df['Major']==select , '취업자 수'].values
    z = df.loc[df['Major']==select , '실업자'].values
    
    
    df_fig = pd.DataFrame({ 'columns' :['총 졸업자', '취업자 수', '실업자'] ,'sum':[x, y, z],
                             }, index = ['총 졸업자', '취업자 수', '실업자'])
    
    st.dataframe(df_fig)
    
    fig = plt.figure()
    plt.scatter(data= df_fig ,x='columns' , y='sum')
    plt.title('sepal Length Vs Width')
    plt.xlabel('sepal_length')
    plt.ylabel('sepal_width')
    st.pyplot(fig)
    
    fig3 = plt.figure()
    plt.hist(data=df_fig , x= 'columns' ,bins=10 ,rwidth=0.3 )
    st.pyplot(fig3)
    
    fig3 = plt.figure()
    fig = px.bar(df_fig, x="columns", y="sum", title="gg")
    st.plotly_chart(fig)
    st.pyplot(fig3)
    
    df_sorted = df_fig.sort_values('Sum' , ascending= False)
    fig7 = px.bar(df_sorted , x= 'columns' ,y='Sum')
    st.plotly_chart(fig7)
    
    
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
    
    st.dataframe(df)
    
    st.text('가장 높은 학과는 COMPUTER AND INFORMATION SYSTEMS입니다.')
    
    