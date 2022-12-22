from matplotlib import pyplot as plt
import streamlit as st 
import pandas as pd
import plotly.express as px 
import seaborn as sb
import plotly.graph_objects as go
import numpy as np
import platform

from sklearn.svm import SVR


def run_high_app() :
    
	

    
   
    df = pd.read_csv('csv/recent-grads.csv')
    
    df = df.drop(['index','Median','P25th','P75th','ShareWomen','Sample_size','Major_code','Full_time_year_round'],axis= 1)
    
    df['Woman_ratio'] = df['Women'] / df['Total'] * 100 
    df['man_ratio'] = df['Men'] / df['Total'] * 100 
    
    df['Full_time_ratio'] = (df['Full_time'] /df['Total'] * 100) 
    df['Part_time_ratio'] = (df['Part_time'] /df['Total'] * 100) 
    
    
    df['College_jobs_ratio']=df['College_jobs'] / df['Employed'] * 100 
    df['Non_college_jobs_ratio']=df['Non_college_jobs'] / df['Employed'] * 100 
    df['Low_wage_jobs_ratio']=df['Low_wage_jobs'] / df['Employed'] * 100 


    df['College_jobs_ratio'] = df['College_jobs_ratio'] / 10
    df['Non_college_jobs_ratio'] = df['Non_college_jobs_ratio'] / 10
    df['Low_wage_jobs_ratio'] = df['Low_wage_jobs_ratio'] / 10
    
    df['Low_wage_jobs_ratio'] = round(df['Low_wage_jobs_ratio'],1)
    df['Non_college_jobs_ratio'] = round(df['Non_college_jobs_ratio'],1)
    df['College_jobs_ratio'] = round(df['College_jobs_ratio'],1)
  
    
    df = df.dropna()
    
    df2 = df.loc[df['man_ratio'] + df['Woman_ratio'] == 100, ['Major','man_ratio','Woman_ratio','Major_category']]
    
    st.subheader('학과 인기 순위, 남여 비율, 취업 비율을 보여드리겠습니다.')

    st.success('Done!')
    
    choice = st.selectbox('학과의 카테고리를 선택해주세요' , df['Major_category'].unique())
    
    
    select = st.selectbox('학과를 선택해주세요' ,df.loc[df['Major_category'] == choice, :]['Major'] )
    st.info('{}과를 선택하셨습니다.'.format(select))
    st.dataframe(df.loc[df['Major'] == select , :])
    
    st.text('full_time = 정규직 \npart_time = 알바 \nunemployed = 실업자 \ncollege_jobs = 전공 직장\nlow_jobs = 저임금 직장\n뒤에 rate,ratio가 붙으면 비율을 뜻한다. ')
    
    st.subheader('인기 순위')
    
    number = st.number_input('순위를 입력하면 해당하는 데이터가 나옵니다. ' , 1 , 200 )
    
    st.text('총 173개의 데이터가 존재합니다.')
    if number > 173 : 
        st.error('존재하지 않습니다.')
    else :
        st.dataframe(df.loc[df['Rank'] == number , :])
        
    fig = px.bar(df, y='Rank', x='Major', text='Total')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')   
    st.plotly_chart(fig)
    st.text('인기 순서대로 학과를 나열했다.')
    
    st.subheader('성비율')
    
    st.text('남여 비율의 합계가 100인것을 기준으로 비율의 순위를 보여드리겠습니다.')
    
    select2 = st.radio('정렬하고 싶은 성별을 선택하세요',['남자','여자'] )
    
    if select2 == '여자' :
        st.dataframe(df.loc[df['man_ratio'] + df['Woman_ratio'] == 100, ['Major' ,'Major_category','Woman_ratio']].sort_values('Woman_ratio'))
        fig1 = px.scatter(df , x=df2["Woman_ratio"], y=df2["Woman_ratio"],
	    size=df2["Woman_ratio"], color=df2["Major_category"],
        hover_name=df2["Major"], log_x=True, size_max=60)
        
        st.plotly_chart(fig1)
    else :
        st.dataframe(df.loc[df['man_ratio'] + df['Woman_ratio'] == 100,['Major' ,'Major_category','man_ratio']].sort_values('man_ratio'))
        fig2 = px.scatter(df , x=df2["man_ratio"], y=df2["man_ratio"],
	    size=df2["man_ratio"], color=df2["Major_category"],
        hover_name=df2["Major"], log_x=True, size_max=60)
        st.plotly_chart(fig2)
    st.text('x축과y축에는 성별 비율을 넣어 정비례하게 만들었다. \n가장 작은것부터 큰 순으로 확인 가능하다.')
    
    
    st.subheader('정규직과 알바 취업율')
    
    select3 = st.selectbox('보고싶은 취업율을 고르세요',['정규직','알바'])
    select4 = st.selectbox('오름차순,내림차순을 선택하시오' , ['오름차순' , '내림차순'])
    if select3 == '정규직' :
        if select4 == '오름차순' :
            st.dataframe(df.loc[ : , ['Major','Major_category','Full_time_ratio' ]].sort_values('Full_time_ratio'))
            
        else :
            st.dataframe(df.loc[ : , ['Major','Major_category','Full_time_ratio' ]].sort_values('Full_time_ratio',ascending=False))
            
        fig3 = px.pie(df, values='Full_time_ratio', names='Major_category', title='Full time ratio of Major category')
        st.plotly_chart(fig3)

    if select3 == '알바' :
        if select4 == '오름차순' : 
            st.dataframe(df.loc[ : , ['Major','Major_category','Part_time_ratio' ]].sort_values('Part_time_ratio'))        
        
        else :
            st.dataframe(df.loc[ : , ['Major','Major_category','Part_time_ratio' ]].sort_values('Part_time_ratio',ascending=False))  
    
        fig4 = px.pie(df, values='Part_time_ratio', names='Major_category', title='Part time ratio of Major category')
        st.plotly_chart(fig4)    
    st.text('학과 카테고리별 비율이 가장 높은 순으로 크기가 크다')        
    
    
    st.subheader('비대학 일자리,저임금 일자리, 대학 일자리')
    
    select5 = st.radio('원하시는 컬럼을 선택해 주세요' , ['비대학' ,'대학' ,'저임금'])
    if select5 == '비대학' :
        st.dataframe(df.loc[ : ,[ 'Major','Major_category','Non_college_jobs_ratio']].sort_values('Non_college_jobs_ratio'))
    elif select5 == '대학' : 
        st.dataframe(df.loc[ : , ['Major','Major_category','College_jobs_ratio']].sort_values('College_jobs_ratio'))
    else : 
        st.dataframe(df.loc[ : , ['Major','Major_category','Low_wage_jobs_ratio']].sort_values('Low_wage_jobs_ratio'))
    
    fig5 = px.scatter_ternary(df, a="College_jobs_ratio", b="Non_college_jobs_ratio", c="Low_wage_jobs_ratio", hover_name="Major",
    color="Major_category", size="Non_college_jobs_ratio", size_max=15,
    color_discrete_map = {"College_jobs_ratio": "blue", "Non_college_jobs_ratio": "green", "Low_wage_jobs_ratio":"red"} )
    st.plotly_chart(fig5)
    
    st.text('대부분의 학과가 저임금 일자리보다 비대학 혹은 대학 일자리를 간다.')
    



    mesh_size = .02
    margin = 0

    

    X = df[['College_jobs_ratio', 'Non_college_jobs_ratio']]
    y = df['Low_wage_jobs_ratio']

    # Condition the model on sepal width and length, predict the petal width
    model = SVR(C=1.)
    model.fit(X, y)

    # Create a mesh grid on which we will run our model
    x_min, x_max = X.College_jobs_ratio.min() - margin, X.College_jobs_ratio.max() + margin
    y_min, y_max = X.Non_college_jobs_ratio.min() - margin, X.Non_college_jobs_ratio.max() + margin
    xrange = np.arange(x_min, x_max, mesh_size)
    yrange = np.arange(y_min, y_max, mesh_size)
    xx, yy = np.meshgrid(xrange, yrange)

    # Run model
    pred = model.predict(np.c_[xx.ravel(), yy.ravel()])
    pred = pred.reshape(xx.shape)

    # Generate the plot
    fig6 = px.scatter_3d(df, x='College_jobs_ratio', y='Non_college_jobs_ratio', z='Low_wage_jobs_ratio')
    fig6.update_traces(marker=dict(size=5))
    fig6.add_traces(go.Surface(x=xrange, y=yrange, z=pred, name='professional_employment'))
    st.plotly_chart(fig6)
    
    st.text('3차원을 통해서 조금 더 명확하게 알 수 있다.')