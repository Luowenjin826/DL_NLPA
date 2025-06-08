import streamlit as st

language = st.radio("Please select language", ["中文", "English", "Italiano"])

# 根据语言显示不同标题和图片
if language == "中文":
    st.write("## 非单侧性原发性醛固酮增多症预测模型")
    st.image("cover_page1.jpg")
    st.markdown(
        """
        ### 用户可根据本地可用数据选择相应模型：
        - **模型1**: 可获得血浆醛固酮浓度和肾素水平
        - **模型2**: 血浆醛固酮浓度和肾素水平均不可获得
        """,
        unsafe_allow_html=True
    )
elif language == "English":
    st.write("## Predicting Model for Non-lateralizing PA")
    st.image("cover_page2.jpg")
    st.markdown(
        """
        ### Users can select the appropriate model based on locally available data:
        - **Model 1**: Plasma aldosterone concentration and renin level are available
        - **Model 2**: Neither plasma aldosterone concentration nor renin level is available
        """,
        unsafe_allow_html=True
    )
elif language == "Italiano":
    st.write("## Modello Predittivo per PA Non Lateralizzante")
    st.image("cover_page3.jpg")
    st.markdown(
        """
        ### Gli utenti possono selezionare il modello appropriato in base ai dati disponibili localmente:
        - **Modello 1**: Sono disponibili concentrazione di aldosterone plasmatico e livello di renina
        - **Modello 2**: Né la concentrazione di aldosterone plasmatico né il livello di renina sono disponibili
        """,
        unsafe_allow_html=True
    )
