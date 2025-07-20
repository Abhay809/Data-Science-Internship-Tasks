import streamlit as st
import pandas as pd
import joblib

model = joblib.load('./models/randomforestregression.pkl')

st.set_page_config(page_title="Laptop Price Predictor", layout="centered")
st.title("💻 Laptop Price Prediction")

company_map = {'Apple': 0, 'Dell': 1, 'HP': 2, 'Acer': 3, 'Lenovo': 4, 'Asus': 5, 'MSI': 6}
typename_map = {'Ultrabook': 0, 'Notebook': 1, 'Gaming': 2, '2 in 1': 3, 'Workstation': 4, 'Netbook': 5}
cpu_map = {'Intel Core i3': 0, 'Intel Core i5': 1, 'Intel Core i7': 2, 'AMD Ryzen': 3, 'Other': 4}
gpu_map = {'Intel': 0, 'Nvidia': 1, 'AMD': 2}
os_map = {'Windows': 0, 'Mac': 1, 'Linux': 2, 'Other': 3}

company_label = st.selectbox("Company", list(company_map.keys()))
typename_label = st.selectbox("Type", list(typename_map.keys()))
ram = st.slider("RAM (GB)", 2, 64, 8)
weight = st.number_input("Weight (kg)", 0.5, 5.0, 1.5)
touchscreen = st.selectbox("Touchscreen", ['No', 'Yes'])
ips = st.selectbox("IPS Display", ['No', 'Yes'])
ppi = st.number_input("PPI", 80.0, 400.0, 150.0)
cpu_label = st.selectbox("CPU Brand", list(cpu_map.keys()))
ssd = st.slider("SSD (GB)", 0, 2000, 256)
hdd = st.slider("HDD (GB)", 0, 2000, 0)
gpu_label = st.selectbox("GPU Brand", list(gpu_map.keys()))
os_label = st.selectbox("Operating System", list(os_map.keys()))

input_df = pd.DataFrame([{
    'Company': company_map[company_label],
    'TypeName': typename_map[typename_label],
    'Ram': ram,
    'Weight': weight,
    'TouchScreen': 1 if touchscreen == 'Yes' else 0,
    'IPS': 1 if ips == 'Yes' else 0,
    'ppi': ppi,
    'Cpu Brand': cpu_map[cpu_label],
    'SSD': ssd,
    'HDD': hdd,
    'Gpu Brand': gpu_map[gpu_label],
    'OS': os_map[os_label]
}])

if st.button("Predict Price"):
    try:
        price = model.predict(input_df)[0]
        st.success(f"💰 Estimated Price: ₹ {round(price, 2)}")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
