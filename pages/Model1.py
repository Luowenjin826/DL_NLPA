import streamlit as st
import numpy as np
import pickle
import tabpfn
from fpdf import FPDF
import time

with open("mean_sd.pkl", "rb") as f:
    mean_std_df = pickle.load(f)
    
with open("model1.pkl", "rb") as f:
    model = pickle.load(f)

mean_std_dict = mean_std_df.set_index('Variable').to_dict()
        
# Generate PDF report function
def create_pdf(input_data, prediction_result, prediction_proba, advice, renin_type, language):
    pdf = FPDF()
    pdf.add_page()

    # Add and set Unicode fonts
    pdf.add_font('SIMYOU', '', 'SIMYOU.TTF', uni=True)  # For Chinese
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)  # For English and Italian

    # Set the font based on the selected language
    if language == "English":
        pdf.set_font('DejaVu', '', 16)
    elif language == "中文":
        pdf.set_font('SIMYOU', '', 16)
    elif language == "Italiano":
        pdf.set_font('DejaVu', '', 16)

    pdf.cell(200, 10, txt="Prediction Report", ln=True, align='C')

    pdf.set_font('DejaVu' if language in ["English", "Italiano"] else 'SIMYOU', '', 12)
    pdf.cell(200, 10, txt="Input Values:", ln=True)

    for key, value in input_data.items():
        if key == "Renin Value":
            continue
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    renin_unit = "uIU/ml" if renin_type == "Renin Concentration (uIU/ml)" else "ng/mL/h"
    pdf.cell(200, 10, txt=f"Renin Value: {input_data['Renin Value']} {renin_unit}", ln=True)

    pdf.cell(200, 10, txt=f"Predicted Disease: {prediction_result}", ln=True)

    pdf.cell(200, 10, txt="Advice:", ln=True)
    for line in advice.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)

    pdf_file = "prediction_report.pdf"
    pdf.output(pdf_file)
    return pdf_file

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
    predict_button_text = "预测"
    predicted_disease_text = "预测疾病: "
elif language == "Italiano":
    title_text = "Applicazione di Predizione delle Malattie"
    age_text = "Età (anni)"
    sex_text = "Sesso"
    sex_options = ["Maschio", "Femmina"]
    bmi_text = "BMI (kg/m2)"
    sbp_text = "Pressione Arteriosa Sistolica (mmHg)"
    dbp_text = "Pressione Arteriosa Diastolica (mmHg)"
    pac_text = "Concentrazione di aldosterone plasmatica (ng/dL)"
    renin_type_text = "Seleziona Tipo di Renina"
    renin_concentration_text = "Concentrazione di Renina (uIU/ml)"
    renin_activity_text = "Attività di Renina (ng/mL/h)"
    predict_button_text = "Predici"
    predicted_disease_text = "Malattia Predetta: "

st.title(title_text)

col1, col2 = st.columns([1, 1])  # Adjust column width ratios
with col1:
    age = st.number_input(age_text, min_value=0, max_value=120, value=30)
    sex = st.selectbox(sex_text, sex_options)
    bmi = st.number_input(bmi_text, min_value=10.00, max_value=80.00, value=25.00, format="%.2f")
    sbp = st.number_input(sbp_text, min_value=40, max_value=300, value=120)
    
with col2:
    dbp = st.number_input(dbp_text, min_value=20, max_value=200, value=80)
    pac = st.number_input(pac_text, min_value=0.0, max_value=1500.0, value=15.0, format="%.1f")
    renin_type = st.selectbox(renin_type_text, [renin_concentration_text, renin_activity_text])
    if renin_type == renin_concentration_text:
        renin_value = st.number_input(renin_concentration_text, min_value=0.0, max_value=1000.0, value=20.0, format="%.1f")
    else:
        renin_value = st.number_input(renin_activity_text, min_value=0.0, max_value=100.0, value=2.0, format="%.1f")
    
# Prediction and advice
if st.button(predict_button_text):
    sex_num = 1 if sex == sex_options[0] else 0

    # Input values array (without renin for now)
    input_values = np.array([age, bmi, sbp, dbp,np.log2(pac)])

    # Standardize input values using the 'Mean' and 'SD' columns from mean_std_df
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

    # Handle Renin based on renin_type
    if renin_type == "Renin Concentration (uIU/ml)":
        renin_mean = mean_std_dict['Mean']['Renin_concentration'] 
        renin_std = mean_std_dict['SD']['Renin_concentration']    
    else:
        renin_mean = mean_std_dict['Mean']['Renin_activity'] 
        renin_std = mean_std_dict['SD']['Renin_activity'] 

    # Add renin to the input values, means, and stds
    input_values = np.append(input_values, np.log2(renin_value))
    means['Renin'] = renin_mean
    stds['Renin'] = renin_std

    # Standardize input values
    z_scores = [(input_values[i] - list(means.values())[i]) / list(stds.values())[i] for i in range(len(input_values))]
    features = np.array(z_scores + [sex_num]).reshape(1, -1)

    # Prediction
    with st.spinner('模型预测中...' if language == "中文" else 'Predicting...' if language == "English" else 'Predicendo...'):
            progress_bar = st.progress(0)
            progress_bar.progress(20)
            time.sleep(0.5)
            
            progress_bar.progress(40)
            time.sleep(0.5)
            
            prediction = model.predict(features)
            prediction_proba = model.predict_proba(features)[0]
            progress_bar.progress(60)
            time.sleep(0.5)
            
            progress_bar.progress(100)
            time.sleep(0.5)
            progress_bar.empty()
    
    # Determine the predicted disease class
    if prediction == 1:
        if language == "中文":
            prediction_result = "非单侧性原发性醛固酮增多症"
            advice = """
            - **医学评估**: 请咨询内分泌科医生进行详细评估。
            - **生活方式改变**: 遵循低钠饮食，并进行定期的体育活动。
            - **监测钾水平**: 定期监测钾水平。
            - **随访护理**: 定期与您的医生进行随访。
            """
        elif language == "English":
            prediction_result = "non-lateralizing primary aldosteronism"
            advice = """
            - **Medical evaluation**: Consult an endocrinologist for a detailed evaluation.
            - **Lifestyle changes**: Follow a low-sodium diet and engage in regular physical activity.
            - **Monitor potassium levels**: Regularly monitor potassium levels.
            - **Follow-up care**: Regular check-ups with your healthcare provider.
            """
        elif language == "Italiano":
            prediction_result = "non-lateralizzazione aldosteronismo primario"
            advice = """
        - **Valutazione Medica**: Consulta un endocrinologo per una valutazione dettagliata.
        - **Cambiamenti dello stile di vita**: Segui una dieta a basso contenuto di sodio e fai attività fisica regolare.
        - **Monitoraggio dei livelli di potassio**: Monitora regolarmente i livelli di potassio.
        - **Cure di follow-up**: Effettua controlli regolari con il tuo medico.
        """
    else:
        if language == "中文":
            prediction_result = "原发性高血压"
            advice = """
            - **生活方式改变**: 减少盐的摄入，保持健康饮食，并定期锻炼。
            - **定期监测**: 定期监测血压，并咨询医生。
            """
        elif language == "English":
            prediction_result = "Essential Hypertension"
            advice = """
            - **Lifestyle changes**: Reduce salt intake, maintain a healthy diet, and exercise regularly.
            - **Regular monitoring**: Keep track of blood pressure and consult your doctor.
            """
        elif language == "Italiano":
            prediction_result = "Ipertensione Essenziale"
            advice = """
        - **Cambiamenti dello stile di vita**: Riduci l'assunzione di sale, mantieni una dieta 
            sana e fai esercizio fisico regolare.
        - **Monitoraggio regolare**: Tieni traccia della pressione sanguigna e consulta il medico.
        """
    
    # Display results and advice using st.write
    st.write(predicted_disease_text, prediction_result)
    predicted_prob = prediction_proba[1] if prediction[0] == 1 else prediction_proba[0]
    if language == "中文":
        prob_text = f"预测概率: {predicted_prob*100:.1f}%"
    elif language == "English":
        prob_text = f"Prediction Probability: {predicted_prob*100:.1f}%"
    elif language == "Italiano": 
            prob_text = f"Probabilità di Previsione: {predicted_prob*100:.1f}%" 
    st.write(prob_text) 
    
    # Show the advice section in Streamlit
    st.subheader("Advice:")
    st.write(advice)

    # Collect input data for the report
    input_data = {
        'Age': age,
        'Sex': sex,
        'BMI': bmi,
        'SBP': sbp,
        'DBP': dbp,
        'PAC': pac,
        'Renin Value': renin_value
    }

    # Generate PDF report
    pdf_file = create_pdf(input_data, prediction_result, prediction_proba, advice, renin_type, language)
    
    # Download PDF button
    with open(pdf_file, "rb") as f:
        pdf_data = f.read()
        
    if language == "中文":
        st.download_button(label="下载报告", data=pdf_data, file_name="报告.pdf", mime="application/pdf")
    elif language == "Italiano":
        st.download_button(label="Scarica il rapporto", data=pdf_data, file_name="rapporto.pdf", mime="application/pdf")
    else:
        st.download_button(label="Download Report as PDF", data=pdf_data, file_name="prediction_report.pdf", mime="application/pdf")
