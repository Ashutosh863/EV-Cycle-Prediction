import streamlit as st
import joblib
import pandas as pd
from pathlib import Path
import matplotlib.pylab as plt
import seaborn as sns

st.set_page_config(page_title="EV Battery Life Predictor",layout='wide')
st.title("EV Battery Remaining Life Predictor")

# load save model
model_path = Path("ev_battery_project/best_model.joblib")
model_data = joblib.load(model_path)

model = model_data['Pipeline']
metadata = model_data['metadata']


num_cols = metadata['num_cols']
cat_cols = metadata['cat_cols']

# sidebar for inputs
st.sidebar.header("Enter Battery Features")

inputs = {}
for c in num_cols:
    inputs[c] = st.sidebar.number_input(c,value=0.0)

for c in cat_cols:
    inputs[c] = st.sidebar.text_input(c,value="")

# predictions
if st.sidebar.button("Predict RUL"):
    new_data = pd.DataFrame([inputs])
    prediction = model.predict(new_data)[0]
    st.success(f"Predicted Remaining Useful Life: {prediction:.2f} cycles")

# visulization
st.subheader("Model Evaluation Visuals")

# load dataset for plotting only
data_path = Path("Battery_RUL.csv")
if data_path.exists():
    df = pd.read_csv(data_path)
    target_col = metadata["target_col"]
    
    # distribution of target
    st.write("Distribution of remaining useful life RUL")
    fig , ax = plt.subplot(figsize=(6,4))
    sns.histplot(df[target_col],bins=30,kde=True,c='green',ax=ax)
    st.pyplot(fig)

# feature importance if random forest
if "RandomForest" in metadata['results']:
    try:
        rf_model = model.names_steps['model']
        if hasattr (rf_model,"feature_importance"):
            importance = rf_model.feature_importance
            feature_names = num_cols
            fi = pd.Series(importance,index=feature_names).sort_values(ascending=False)

            st.write("**Feature Importance (RandomForest):**")
            fig, ax = plt.subplots(figsize=(6,4))
            sns.barplot(x=fi.values, y=fi.index, palette="viridis", ax=ax)
            st.pyplot(fig)
    except Exception as e:
        st.warning(f"Feature importance not available: {e}")