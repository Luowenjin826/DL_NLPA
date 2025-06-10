import streamlit as st
import numpy as np
import pickle
import tabpfn

with open("mean_sd.pkl", "rb") as f:
    mean_std_df = pickle.load(f)
        
with open("main_model.pkl", "rb") as f:
    model = pickle.load(f)

mean_std_dict = mean_std_df.set_index('Variable').to_dict()

# Language selection
language = st.radio("Please select language", ["中文","English", "Italiano"])

# Define text for each language
if language == "English":
    title_text = "Disease Prediction App"
    age_text = "Age (years)"
    sex_text = "Sex"
    sex_options = ["Male", "Female"]
    bmi_text = "BMI (kg/m2)"
    sbp_text = "Systolic Blood Pressure (mmHg)"
    dbp_text = "Diastolic Blood Pressure (mmHg)"
    pac_text = "Plasma aldosterone (ng/dL)"
    renin_type_text = "Select Renin Type"
    renin_concentration_text = "Renin Concentration (uIU/ml)"
    renin_activity_text = "Renin Activity (ng/mL/h)"
    hypok_text = "History of Hypokalemia"
    nodule_text = "Adrenal Nodules"
    hypok_options = ["Yes", "No", "Unknown"]
    predict_button_text = "Predict"
    predicted_disease_text = "Predicted Disease: "
elif language == "中文":
    title_text = "疾病预测应用程序"
    age_text = "年龄 (年)"
    sex_text = "性别"
    sex_options = ["男", "女"]
    bmi_text = "体重指数 (kg/m2)"
    sbp_text = "收缩压 (mmHg)"
    dbp_text = "舒张压 (mmHg)"
    pac_text = "血浆醛固酮浓度 (ng/dL)"
    renin_type_text = "选择肾素类型"
    renin_concentration_text = "血浆肾素浓度 (uIU/ml)"
    renin_activity_text = "血浆肾素活性 (ng/mL/h)"
    hypok_text = "低钾血症病史"
    nodule_text = "肾上腺结节"
    hypok_options = ["是", "否", "不知道"]
    predict_button_text = "预测"
    predicted_disease_text = "预测疾病: "
elif language == "Italiano":
    title_text = "Applicazione di Predizione delle Malattie"
    age_text = "Età (anni)"
    sex_text = "Sesso"
    sex_options = ["Maschio", "Femmina"]
    bmi_text = "BMI (kg/m2)"
    sbp_text = "Pressione Sanguigna Sistolica (mmHg)"
    dbp_text = "Pressione Sanguigna Diastolica (mmHg)"
    pac_text = "Concentrazione di aldosterone plasmatica (ng/dL)"
    renin_type_text = "Seleziona Tipo di Renina"
    renin_concentration_text = "Concentrazione di Renina (uIU/ml)"
    renin_activity_text = "Attività di Renina (ng/mL/h)"
    hypok_text = "Anamnesi Della Ipopotemia"
    nodule_text = "Nodulo Surrenalico"
    hypok_options = ["Sì", "No", "No lo so"]
    predict_button_text = "Predici"
    predicted_disease_text = "Malattia Predetta: "

st.title(title_text)

col1, col2 = st.columns([1, 1])  # Adjust column width ratios
with col1:
    age = st.number_input(age_text, min_value=0, max_value=120, value=30)
    sex = st.selectbox(sex_text, sex_options)
    bmi = st.number_input(bmi_text, min_value=10.00, max_value=80.00, value=25.00, format="%.2f")
    sbp = st.number_input(sbp_text, min_value=40, max_value=300, value=120)
    dbp = st.number_input(dbp_text, min_value=20, max_value=200, value=80)
    
with col2:
    pac = st.number_input(pac_text, min_value=0.0, max_value=1500.0, value=15.0, format="%.1f")
    renin_type = st.selectbox(renin_type_text, [renin_concentration_text, renin_activity_text])
    if renin_type == renin_concentration_text:
        renin_value = st.number_input(renin_concentration_text, min_value=0.0, max_value=1000.0, value=20.0, format="%.1f")
    else:
        renin_value = st.number_input(renin_activity_text, min_value=0.0, max_value=100.0, value=2.0, format="%.1f")
    hypok = st.selectbox(hypok_text, hypok_options)
    nodule = st.selectbox(nodule_text, hypok_options)
    
# Prediction and advice
if st.button(predict_button_text):
    if hypok == hypok_options[0] or nodule == hypok_options[0]:
        if language == "中文":
            prediction_result = "建议到肾上腺专科门诊进一步检查。"
        elif language == "English":
            prediction_result = "Please referring to adrenal specialty"
        elif language == "Italiano":
            prediction_result = "Si raccomanda un ulteriore esame a livello ambulatoriale da parte di adrenalina specializzata."
        st.write(predicted_disease_text, prediction_result)
    else:
        sex_num = 1 if sex == sex_options[0] else 0
        input_values = np.array([age, bmi, sbp, dbp, np.log2(pac)])

        # 标准化输入值
        means = {
            'Age': mean_std_dict['Mean']['Age'],
            'BMI': mean_std_dict['Mean']['BMI'],
            'SBP': mean_std_dict['Mean']['SBP'],
            'DBP': mean_std_dict['Mean']['DBP'],
            'PAC': mean_std_dict['Mean']['PAC']
        }
    
        stds = {
            'Age': mean_std_dict['SD']['Age'],
            'BMI': mean_std_dict['SD']['BMI'],
            'SBP': mean_std_dict['SD']['SBP'],
            'DBP': mean_std_dict['SD']['DBP'],
            'PAC': mean_std_dict['SD']['PAC']
        }
    
        if renin_type == renin_concentration_text:
            renin_mean = mean_std_dict['Mean']['Renin_concentration'] 
            renin_std = mean_std_dict['SD']['Renin_concentration']    
        else:
            renin_mean = mean_std_dict['Mean']['Renin_activity'] 
            renin_std = mean_std_dict['SD']['Renin_activity'] 
    
        input_values = np.append(input_values, np.log2(renin_value))
        means['Renin'] = renin_mean
        stds['Renin'] = renin_std
        z_scores = [(input_values[i] - list(means.values())[i]) / list(stds.values())[i] for i in range(len(input_values))]
        features = np.array(z_scores + [sex_num]).reshape(1, -1)
    
        # 预测
        prediction = model.predict(features)
        prediction_proba = model.predict_proba(features)[0]
        
        # 确定预测疾病类别
        if prediction == 1:
            if language == "中文":
                prediction_result = "非单侧性原发性醛固酮增多症"
            elif language == "English":
                prediction_result = "non-lateralizing primary aldosteronism"
            elif language == "Italiano":
                prediction_result = "non-lateralizzazione aldosteronismo primario"
        else:
            if language == "中文":
                prediction_result = "原发性高血压"
            elif language == "English":
                prediction_result = "Essential Hypertension"
            elif language == "Italiano":
                prediction_result = "Ipertensione Essenziale"

        predicted_prob = prediction_proba[1] if prediction[0] == 1 else prediction_proba[0]
        if language == "中文":
            prob_text = f"预测概率: {predicted_prob*100:.1f}%"
        elif language == "English":
            prob_text = f"Prediction Probability: {predicted_prob*100:.1f}%"
        elif language == "Italiano": 
                prob_text = f"Probabilità di Previsione: {predicted_prob*100:.1f}%" 
        
        # 显示结果
        st.write(predicted_disease_text, prediction_result)
        st.write(prob_text)
