import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# network url http://10.0.0.61:8501 
# may not work well in safari, chrome recommended 
# hmm, url not secure. may not be able to be opened at work. maybe example flow in ppt?

st.title('Financed Emissions Calculator')
st.text('This is a web app to learn about financed emissions')
st.markdown('### Introduction')

# uploaded = st.file_uploader('Upload your file here')
# I think i'll just load a dictionary for simplicity

raw = {
    "company": ["Tesla", "Stellantis", "Subaru", "Kia", "Nissan", "Hyundai", "Honda", "BMW", "Volvo"],
    "scope1": [185000, 1641028, 232070, 365100, 697851, 723966, 1120000, 699713, 77000],
    "scope2": [403000, 2233459, 359408, 774000, 1541276, 1660238, 3380000, 138849, 45000],
    "scope3": [1954000, 523300000, 28026000, 67563304, 127735901, 101790793, 249980000, 121705368, 19561000],
    "sales_vol": [0.94, 6.5, 0.86, 2.66, 3.88, 3.89, 4.55, 2.62, 0.7],
    "debt_eq": [62131, 87910, 14805, 52863, 149862, 204446, 186383, 76533, 33094]
}

raw_data = pd.DataFrame(raw)
st.header('Descriptive Stats')
st.write(raw_data.describe())

st.header('Data Header')
st.write(raw_data.head())

st.header('Matplotlib Chart')
fig,ax = plt.subplots(1,1)
ax.scatter(x=raw_data['sales_vol'], y = raw_data['scope1'])
ax.set_xlabel('Sales Volume Millions')
ax.set_ylabel('Scope 1 Emissions Tonnes')
st.pyplot(fig)

# okay it's an altair issue. so can't ge those simple and pretty plots without messing with my python version unfortunately
# st.header('Streamlit Native Chart')
# st.bar_chart(data = raw_data, x = 'sales_vol', y = 'scope1', x_label='Sales Volume Millions', y_label='Scope 1 Emissions Tonnes')