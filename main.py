import streamlit as st
st.title('시그너스왕국의 마왕을 물리쳐주세요!')
name=st.text_input('용사님의 이름을 알려주세요!')
if st.button('인사말 생성'):
  st.info(name+'용사님! 안녕하세요!')
  st.warning('우리 왕국을 도와주세요!')
  st.balloons()
