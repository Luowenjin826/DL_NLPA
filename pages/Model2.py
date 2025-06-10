

# 禁用文件监视器
import streamlit as st
st.set_option('server.fileWatcherType', 'none')

# 修复 torch 路径
import torch
if hasattr(torch, '__path__') and not hasattr(torch.__path__, '_path'):
    torch.__path__._path = [path for path in torch.__path__]

import streamlit as st
import numpy as np
import pickle
import tabpfn

with open("mean_sd.pkl", "rb") as f:
        mean_std_df = pickle.load(f)
        
with open("alternative_model.pkl", "rb") as f:
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
    wc_text = "Waist Circumference (cm)"
    sbp_text = "Systolic Blood Pressure (mmHg)"
    dbp_text = "Diastolic Blood Pressure (mmHg)"
    tg_text = "Triglycerides (mmol/L)"
    ldl_text = "LDL Cholesterol (mmol/L)"
    fbg_text = "Fasting Blood Glucose (mmol/L)"
    ascvd_text = "Coronary heart diseease or stroke"
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
    wc_text = "腰围 (cm)"
    sbp_text = "收缩压 (mmHg)"
    dbp_text = "舒张压 (mmHg)"
    tg_text = "甘油三酯 (mmol/L)"
    ldl_text = "低密度脂蛋白胆固醇 (mmol/L)"
    fbg_text = "空腹血糖 (mmol/L)"
    ascvd_text = "冠心病或脑卒中"
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
    wc_text = "Circonferenza Vita (cm)"
    sbp_text = "Pressione Sanguigna Sistolica (mmHg)"
    dbp_text = "Pressione Sanguigna Diastolica (mmHg)"
    tg_text = "Trigliceridi (mmol/L)"
    ldl_text = "Colesterolo LDL (mmol/L)"
    fbg_text = "Glucosio a Digiuno (mmol/L)"
    ascvd_text = "Malattia coronarica o ictus"
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
    wc = st.number_input(wc_text, min_value=30.0, max_value=150.0, value=80.0, format="%.1f")
    sbp = st.number_input(sbp_text, min_value=40, max_value=300, value=120)
    dbp = st.number_input(dbp_text, min_value=20, max_value=200, value=80)
with col2:
    tg = st.number_input(tg_text, min_value=0.00, max_value=15.00, value=1.50, format="%.2f")
    ldl = st.number_input(ldl_text, min_value=0.00, max_value=15.00, value=2.50, format="%.2f")
    fbg = st.number_input(fbg_text, min_value=2.00, max_value=30.00, value=5.00, format="%.2f")
    ascvd = st.selectbox(ascvd_text, hypok_options)
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
        ascvd_num = 1 if ascvd == hypok_options[0] else 0
        input_values = np.array([age, bmi, wc, sbp, dbp, np.log2(tg), ldl, np.log2(fbg)])
    
        # Standardize input values using the 'Mean' and 'SD' columns from mean_std_df
        means = {
            'Age': mean_std_dict['Mean']['Age'],
            'BMI': mean_std_dict['Mean']['BMI'],
            'WC': mean_std_dict['Mean']['WC'],
            'TG': mean_std_dict['Mean']['TG'],
            'LDL': mean_std_dict['Mean']['LDL'],
            'FBG': mean_std_dict['Mean']['FBG'],
            'SBP': mean_std_dict['Mean']['SBP'],
            'DBP': mean_std_dict['Mean']['DBP']
        }
    
        stds = {
            'Age': mean_std_dict['SD']['Age'],
            'BMI': mean_std_dict['SD']['BMI'],
            'WC': mean_std_dict['SD']['WC'],
            'TG': mean_std_dict['SD']['TG'],
            'LDL': mean_std_dict['SD']['LDL'],
            'FBG': mean_std_dict['SD']['FBG'],
            'SBP': mean_std_dict['SD']['SBP'],
            'DBP': mean_std_dict['SD']['DBP']
        }
        
        z_scores = [(input_values[i] - list(means.values())[i]) / list(stds.values())[i] for i in range(len(input_values))]
        features = np.array(z_scores + [sex_num, ascvd_num]).reshape(1, -1)
    
        # Prediction
        prediction = model.predict(features)
        prediction_proba = model.predict_proba(features)[0]
        
        # Determine the predicted disease class
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
        
        # Display results and advice using st.write
        st.write(predicted_disease_text, prediction_result)
        st.write(prob_text) 
