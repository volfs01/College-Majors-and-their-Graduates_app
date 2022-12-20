import streamlit as st 
import pandas as pd

def run_grad_app() :
    df = pd.read_csv('csv/grad-students.csv',index_col=0)
    
    st.subheader('학과를 선택하면 졸업,취업,실업자수를 보여드립니다.')
    choice = st.selectbox('학과의 카테고리를 선택해주세요' , df['Major_category'].unique())
    
    
    select = st.selectbox('학과를 선택해주세요' ,df.loc[df['Major_category'] == choice, :]['Major'] )
    st.info('{}과를 선택하셨습니다.'.format(select))
    
    