import streamlit as st
st. title('먼작귀')
a=st.text_input('이름을 입력해주세요.')
b=st.selectbox('당신이 좋아하는 캐릭터는?',['우사기','하치와레','치이카와','모몽가'])
if st.button('야호'):
  st.write('반갑습니다!')
  st.info(a+'님! 안녕하세요!')
  st.warning(b+'를 좋아하신다고요?')
  st.error(b+'를 감히???')
  st.balloons()
