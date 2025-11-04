import streamlit as st
st.title('시그너스왕국의 마왕을 물리쳐주세요!')
name=st.text_input('용사님의 이름을 알려주세요!')
menu=st.selectbox('원하시는 성유물을 선택해주세요:',['아발론','토오사카 린의 10년 치 마력이 담긴 보석'])
if st.button('인사말 생성'):
  st.info(name+'용사님! 안녕하세요!')
  st.warning(menu+', 이제 어떠한 적이라도 두렯지 않겠어요!')
  st.error('저희에겐 용사님 뿐이에요')
  st.balloons()
