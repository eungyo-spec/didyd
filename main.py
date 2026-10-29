import streamlit as st
st. title('먼작귀')
a=st.text_input('이름을 입력해주세요.')
b=st.selectbox('당신이 좋아하는 캐릭터는?',['우사기','하치와레','치이카와','모몽가'])
if st.button('야호'):
  st.write('반갑습니다!')
  st.info(a+'님! 안녕하세요!')
  st.warning('감히'b+'를 좋아하시네요!')
  st.error('ㅎㅎ 화이팅 하세요;~')
  st.balloons()
