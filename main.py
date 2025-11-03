import streamlit as st
st.title('시그너스왕국의 마왕을 물리쳐주세요!')
name=st.text_input('용사님의 이름을 알려주세요!')
menu=st.selectbox('원하시는 서번트를 선택해주세요:',['아처','세이버'])
if st.button('인사말 생성'):
  st.info(name+'용사님! 안녕하세요!')
  st.warning(menu+'역시 주인을 따르는 충성심! 최강의 서번트!')
  st.error('저희에겐 용사님 뿐이에요')
  st.balloons()
