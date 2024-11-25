import streamlit as st
import pandas as pd
import plotly.express as px

# network url http://10.0.0.61:8501 
# until i deploy

l_submit = False
def launch_loans():
    st.subheader("Time to make your loan allocations")
    loan_form = st.form('u_loans')
    c1_loan = loan_form.slider(label= f"Please select your allocation for {c_names[0]}. A minimum of $25M must be allocated",
                                min_value = 25,
                                max_value = 425,
                                step = 25,
                                key = 'c1')
    c2_loan = loan_form.slider(label= f"Please select your allocation for {c_names[1]}. A minimum of $25M must be allocated",
                                min_value = 25,
                                max_value = 425,
                                step = 25,
                                key = 'c2')
    c3_loan = loan_form.slider(label= f"Please select your allocation for {c_names[2]}. A minimum of $25M must be allocated",
                                min_value = 25,
                                max_value = 425,
                                step = 25,
                                key = 'c3')
    c4_loan = loan_form.slider(label= f"Please select your allocation for {c_names[3]}. A minimum of $25M must be allocated",
                                min_value = 25,
                                max_value = 425,
                                step = 25,
                                key = 'c4')
    l_submit = loan_form.form_submit_button('Submit')

st.title('Financed Emissions Calculator')
st.text('This is a web app to learn about financed emissions')
st.markdown('### Introduction')

raw = {
    "company": ["Tesla", "Stellantis", "Subaru", "Kia", "Nissan", "Hyundai", "Honda", "BMW", "Volvo"],
    "scope1": [185000, 1641028, 232070, 365100, 697851, 723966, 1120000, 699713, 77000],
    "scope2": [403000, 2233459, 359408, 774000, 1541276, 1660238, 3380000, 138849, 45000],
    "scope3": [1954000, 523300000, 28026000, 67563304, 127735901, 101790793, 249980000, 121705368, 19561000],
    "sales_vol": [0.94, 6.5, 0.86, 2.66, 3.88, 3.89, 4.55, 2.62, 0.7],
    "debt_eq": [62131, 87910, 14805, 52863, 149862, 204446, 186383, 76533, 33094]
}

data = pd.DataFrame(raw)
# u_selections = {}
st.header('User Inputs')
# start by just receiving and printint out the inputs
comp_form = st.form("u_comp")
c_names = comp_form.multiselect(label = "Please select exactly four companies to provide loans to", 
                      options= data['company'].unique(),
                      max_selections= 4,
                      key = 'c_names'
                      )
# c1_loan = comp_form.slider(label=f"Please select your allocation for {c_names[0]}. A minimum of $25M must be allocated",
#                         min_value=25,
#                         max_value=425,
#                         step = 25) 

c_submit = comp_form.form_submit_button('Submit') 

if c_submit:
    # Check if total of 4 selected
    total = len(set(c_names))
    if total == 4:
        st.success(f"You selected: {c_names}") # next iteration, print more nicely than this
        u_selections = dict.fromkeys(c_names)
        launch_loans()


    else:
        st.error(f"Number of companies selected: {total}. Please select exactly 4")
        # c_submit = False # not sure if this makes a difference - looks like no. at least for now

if l_submit:
    st.write(c1_loan)


# company allocation selection based on prior company selection

    
    # run validations
    # if passed print confirmation message with st.success
    # if failed, print error message and set c_submit to false 

# def comp_val(companies = c_names):
#     # Check if total of 4 selected
#     total = len(set(c_names))


# would do 


# # uncontained multiselect
# u_cs_1 = st.multiselect(label = "Please select exactly four companies to provide loans to", 
#                       options= data['company'].unique(),
#                       max_selections= 4,
#                       key='u_cs_1'
#                       )

# returns a list. so let's check in the list that it's 4. 
# multiselect already enforces spelling and not duplicating entries



# use this as a reference when i get to the allocation selections
# c1_a = comp_form.slider(label="Please select your allocation for this company. A minimum of $25M must be allocated",
#                         min_value=25,
#                         max_value=425,
#                         step = 25) 

st.header('Descriptive Stats')
st.write(data.describe())

st.header('Data Header')
st.write(data.head())


st.subheader('Plotly Scatterplot')
st.markdown('**Sales Volume vs Scope 1 Emissions**')
scatter_fig = px.scatter(data_frame = data, x = 'sales_vol', y = 'scope1', color = 'company',
                         labels = {'sales_vol':'Sales Volume (Millions of Vehicles)',
                                   'scope1': 'Scope 1 Emissions (tCO2e)',
                                   'company': 'Financed Company'})
st.plotly_chart(scatter_fig)
# can also add title to the scatter_fig paramaeters but don't like how it looks, kinda squiches the plot don 
#  title = 'Sales Volume vs Scope 1 Emissions'
