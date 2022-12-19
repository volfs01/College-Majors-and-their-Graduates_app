import streamlit as st 

def main() :
    
    menu = ['home' ,'모든 연령','대학원 졸업과 대학교 졸업' , '대학교 졸업과 고등학교 졸업']

    choice = st.sidebar.selectbox( '메뉴를 선택하시오' , menu )
    
    if menu == 'home' :
        pass
    if menu == '모든 연령' :
        pass
    if menu == '대학원 졸업과 대학교 졸업' :
        pass
    if menu == '대학교 졸업과 고등학교 졸업' :
        pass



if __name__ == '__main__' :
    main()