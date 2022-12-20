import streamlit as st 

from app_home import run_home_app
from app_all_age import run_all_age
from app_grad import run_grad_app
def main() :
    
    menu = ['home' ,'모든 연령','대학원 졸업과 대학교 졸업' , '대학교 졸업과 고등학교 졸업']

    choice = st.sidebar.selectbox( '메뉴를 선택하시오' , menu )
    
    if choice == 'home' :
        run_home_app()
    if choice == '모든 연령' :
        run_all_age()
    if choice == '대학원 졸업과 대학교 졸업' :
        run_grad_app()
    if choice == '대학교 졸업과 고등학교 졸업' :
        pass



if __name__ == '__main__' :
    main()