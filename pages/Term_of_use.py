import streamlit as st

# Language selection
language = st.radio("Please select language", ["中文","English", "Italiano"])

# Define content for each language
if language == "English":
    st.markdown("## Terms of Use")  # Larger header
    st.markdown("""
        ### By using this app, you agree to the following terms:
        
        #### 1. The app is for informational purposes only and should not replace medical advice from a qualified healthcare provider.
        #### 2. The app developers are not responsible for any decisions made based on the information provided by the app.
        #### 3. Always consult a healthcare professional for any medical advice or diagnosis.
    """)
elif language == "中文":
    st.markdown("## 使用条款")
    st.markdown("""
        ### 使用此应用程序即表示您同意以下条款：

        #### 1. 本应用程序仅用于信息提供，不应取代合格的医疗服务提供者的医学建议。
        #### 2. 应用程序开发人员对根据本应用程序提供的信息所做的任何决定不承担责任。
        #### 3. 始终咨询医疗保健专业人士以获得任何医疗建议或诊断。
    """)
elif language == "Italiano":
    st.markdown("## Termini di utilizzo")
    st.markdown("""
        ### Utilizzando questa app, accetti i seguenti termini:
        
        #### 1. L'app è solo a scopo informativo e non deve sostituire il consiglio medico di un operatore sanitario qualificato.
        #### 2. Gli sviluppatori dell'app non sono responsabili per eventuali decisioni prese sulla base delle informazioni fornite dall'app.
        #### 3. Consulta sempre un professionista sanitario per qualsiasi consiglio o diagnosi medica.
    """)

