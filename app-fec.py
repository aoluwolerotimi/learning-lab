### Package Imports ###
import streamlit as st
import pandas as pd
import numpy as np
import random 
import plotly.express as px

# network url http://10.0.0.61:8501 
# until i deploy

###  Data, Variable, and User Defined Function Setup ### 
## Data and Variables
raw = {
    "company": ["Tesla", "Stellantis", "Subaru", "Kia", "Nissan", "Hyundai", "Honda", "BMW", "Volvo"],
    "scope1": [185000, 1641028, 232070, 365100, 697851, 723966, 1120000, 699713, 77000],
    "scope2": [403000, 2233459, 359408, 774000, 1541276, 1660238, 3380000, 138849, 45000],
    "scope3": [1954000, 523300000, 28026000, 67563304, 127735901, 101790793, 249980000, 121705368, 19561000],
    "sales_vol": [0.94, 6.5, 0.86, 2.66, 3.88, 3.89, 4.55, 2.62, 0.7],
    "debt_eq": [62131, 87910, 14805, 52863, 149862, 204446, 186383, 76533, 33094]
}

data = pd.DataFrame(raw)
funds = 500
correct = False

##  Functions 
# Function to perform calculations based on allocation selection
def calculations(data, selection, funds):
  # Subsetting to the selected companies
  df = data[data['company'].isin(selection.keys())].reset_index(drop=True)

  # Create column for authorized amount
  df['authorized'] = df['company'].map(selection)

  # Create column for amount outstanding (random value upwards of 30%)

  df['outstanding'] = df['authorized'].apply(lambda x: x * random.choice([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])).astype(int)

  # Calculate per client total emissions in megatonnes
  df['total_em'] = round((df['scope1'] + df['scope2'] + df['scope3']) / 1_000_000, 4)

  # Calculate per client emissions intensity proxy
  df['prod_intensity'] = round(df['total_em'] / df['sales_vol'], 2)

  # Calculate attribution ratio
  df['attr_ratio'] = df['outstanding'] / df['debt_eq']

  # Calculate portfolio percentage
  df['perc'] = df['authorized'] / funds

  # Calculate absolute financed emissions in megatonnes and tonnes for printing
  df['abs_em'] = df['attr_ratio'] * df['total_em']
  df['abs_em_tonnes'] = (df['attr_ratio'] * df['total_em'] * 1_000_000).astype(int)

  return df

# Analyzing the portfolio
def analyze_portfolio(results_df):
  
  # Print absolute financed emissions values
  col1, col2 = st.columns(2)

  with col1:
     st.markdown(f"The ${results_df.at[0,'authorized']} million loaned to {results_df.at[0,'company']} generated") # results_df.at[0,'company']
     st.metric(label = "Financed Emissions", value=f"{results_df.at[0,'abs_em_tonnes']:,d} tCO2e")

     st.markdown(f"The ${results_df.at[2,'authorized']} million loaned to {results_df.at[2,'company']} generated") # results_df.at[0,'company']
     st.metric(label = "Financed Emissions", value=f"{results_df.at[2,'abs_em_tonnes']:,d} tCO2e")

  with col2:
     st.markdown(f"The ${results_df.at[1,'authorized']} million loaned to {results_df.at[1,'company']} generated") # results_df.at[0,'company']
     st.metric(label = "Financed Emissions", value=f"{results_df.at[1,'abs_em_tonnes']:,d} tCO2e")

     st.markdown(f"The ${results_df.at[3,'authorized']} million loaned to {results_df.at[3,'company']} generated") # results_df.at[0,'company']
     st.metric(label = "Financed Emissions", value=f"{results_df.at[3,'abs_em_tonnes']:,d} tCO2e")

  # Calculate and print overall physical emissions intensity
  portfolio_intensity = np.average(results_df['prod_intensity'], weights=results_df['perc'])
  st.markdown(f"\nThe physical emissions intensity of this loan portfolio is")
  st.metric(label = 'Emmissions Intensity', value= f"{portfolio_intensity:.2f}")

  # Create and display a donut chart for loan portfolio allocations
  fig_donut = px.pie(
      results_df,
      names='company',
      values='authorized',
      title='Loan Portfolio Allocations Across Companies',
      hole=0.4,
      color = 'company',
      color_discrete_map= {results_df.at[0,'company']:'lightgreen',
                           results_df.at[1,'company']: 'mediumseagreen',
                           results_df.at[2,'company']: 'forestgreen',
                           results_df.at[3,'company']: 'darkgreen'}
  )
  st.plotly_chart(fig_donut)

  # Create and display a horizontal bar chart for absolute financed emissions

  fig_em = px.bar(
      results_df,
      x='abs_em_tonnes',
      y='company',
      title='Absolute Financed Emissions by Company',
      labels={'abs_em_tonnes': 'Absolute Financed Emissions (tCO2e)', 'company': 'Company'},
      orientation='h',
      color = 'company',
      color_discrete_sequence= ['lightgreen','mediumseagreen','forestgreen', 'darkgreen']
  )
  fig_em.update_layout(showlegend = False)
  st.plotly_chart(fig_em)

  # Create and display a horizontal bar chart for physical emissions intensity
  fig_pet = px.bar(
      results_df,
      x='prod_intensity',
      y='company',
      title='Physical Emissions Intensity by Company',
      labels={'prod_intensity': 'Physical Emissions Intensity (Emissions relative to vehicles sold)', 'company': 'Company'},
      orientation='h',
      color = 'company',
      color_discrete_sequence= ['lightgreen','mediumseagreen','forestgreen', 'darkgreen']
  )
  fig_pet.update_layout(showlegend = False)
  st.plotly_chart(fig_pet)




# Explain results

def explain_abs_em(results_df):
   outstanding = results_df.loc[0, 'outstanding']
   debt_eq = (results_df.loc[0, 'debt_eq'])/1_000
   total_em = results_df.loc[0, 'total_em']
   attr_ratio = round(results_df.loc[0, 'attr_ratio'] * 100, 5)
   st.markdown(f"""
    You loaned \${results_df.loc[0, 'authorized']} million to {results_df.loc[0, 'company']}. This is referred to as the authorized amount.
    Of that \${results_df.loc[0, 'authorized']} million, {results_df.loc[0, 'company']} used ${results_df.loc[0, 'outstanding']} million. This is referred to as the outstanding amount.
    This outstanding amount is used to calculate your attribution ratio,  representing your contribution to {results_df.loc[0, 'company']}'s activities for the year.

    This ratio is calculated as the value outstanding divided by the company's debt and equity that year. In {results_df.loc[0, 'company']}'s case, it would be calculated as follows
               """)

   st.latex(rf'''
    \text{{Attribution Ratio}} = \frac{{\text{{Outstanding Loan}}}}{{\text{{Debt + Equity}}}} = 
    \frac{{{outstanding} \, \text{{million}}}}{{{debt_eq:,} \, \text{{billion}}}} \approx {attr_ratio}\%
    ''')

   st.markdown(f"This attribution ratio is then multiplied by {results_df.loc[0, 'company']}'s total emissions (across scopes 1, 2, and 3)")
   
   st.latex(rf'''
    \text{{Financed Emissions}} = \text{{Attr. Ratio}} \times \text{{Total Emissions}} = 
    \left({attr_ratio} \%\right) \times {total_em} \, \text{{MtCO2e}}
    ''')
   
   st.markdown(f"Expressed in tCO2e (converted from MtCO2e), this gives you your financed emissions value of {results_df.loc[0, 'abs_em_tonnes']:,d} tCO2e")
   
 
# test explain_pet with latex and no need to explain a simple fraction, can point them to the donut chart above
def explain_pet(results_df, funds):
   portfolio_intensity = np.average(results_df['prod_intensity'], weights=results_df['perc'])
   company_name = results_df.loc[0, 'company']
   total_em = results_df.loc[0, 'total_em']
   sales_vol = results_df.loc[0, 'sales_vol']
   prod_intensity = results_df.loc[0, 'prod_intensity']

   st.markdown(f""" 
    Recall that for a single company, their emissions intensity is a normalized view of their emissions relative to their
    economic productivitsy. 
    In the absence of consistent information about production and average lifetime vehicle kilometers across produced vehicle
    classes, number of vehicles sold was used as a proxy.
    
    Thus, for each company you loaned to, their emissions intensity was calculates as their total emissions over their 
    vehicles sold for the year 
    
    Let's use {results_df.loc[0, 'company']} as an example again. 

               """)
   
   st.latex(rf'''
    \text{{Emissions Intensity}} = 
    \frac{{\text{{Total Emissions}}}}{{\text{{Vehicles Sold}}}} = 
    \frac{{{total_em} \, \text{{MtCO2e}}}}{{{sales_vol} \, \text{{million vehicles}}}} 
    \approx {prod_intensity}
    ''')

   st.markdown(f""" 
    We also computed the proportion of your total funds loaned out to each company, representing it's portion of your auto sector financing
    (recall the donut chart above).
    Taking a weighted average of the proportion per company and the emissions intensity per company we arrive at a physical emissions 
    intensity of {portfolio_intensity:.2f} for your auto sector portfolio. 
               """)


def user_output():
   st.markdown('### Your Results')
   analyze_portfolio(results_df)

   st.markdown('### Understanding Your Results')
   st.markdown('#### Calculating Absolute Emissions')
   st.markdown('Let\'s walk through an example to understand how the absolute financed emissions were calculated.')
   explain_abs_em(results_df)

   st.markdown('#### Calculating Physical Emissions Intensity')
   st.markdown(f"""
    Now let's walk through how your portfolio intensity value was derived.

    Recall that for a single company, their emissions intensity is a normalized view of their emissions relative to their economic productivity. In the asbcence of consistent information about production and average lifetime vehicle kilometres across produced vehicle classes, we used number of vehicles sold as a rough proxy.

    Thus, for each company you loaned to, we calculated their emissions intensity as their total emissions divided by vehicles sold for the year.
               """)
   explain_pet(results_df, funds)
   st.divider()
   st.markdown('**Congrats! :tada: Through this simplified example, you\'ve learned a little bit about how institutions measure their financed emissions.**')



##########
### Streamlit App ###

st.title('Financed Emissions Calculator')
st.markdown('### The Scenario')
st.markdown(f"""  
It is 2020 and you are tasked with allocating loan funding to select automakers on behalf of your institution. You have $500 million which must be allocated to four different firms.
After 1 year, you will evaluate your resulting climate metrics. Namely, your **absolute financed emissions** as well as the **phyisical emissions intensity** for your auto sector loan portfolio.

**Understanding Absolute Emissions:**
This measures the share of the companies' emissions financed by your loans.

**Understanding Physical Emissions Intensity:**
For a given company, physical emissions intensity provides a view of its emissions relative to its economic activity. The resulting metrics allows better comparability across companies or portfolios.
            """)

st.markdown('#### Creating Your Loan Portofolio')

with st.form("user_allocations"):
    st.markdown(f"""Select the 4 companies you'd like to authorize loans to as well as how much you'd like to loan them.
                For the loan amounts, you must issue the full \$500 M and each company must receive at least $25M
                """)
    c1 = st.selectbox(label = 'Please select your first company',
                      options = data['company'].unique(),
                      index= None,
                      placeholder= 'Click to select',
                      key = 'c1')
    c1_loan = st.slider(label = 'Please select your allocation to the first company',
                        min_value= 25,
                        max_value= 425,
                        step= 25,
                        key='c1_loan')
    
    c2 = st.selectbox(label = 'Please select your second company',
                      options = data['company'].unique(),
                      index= None,
                      placeholder= 'Click to select',
                      key = 'c2')
    c2_loan = st.slider(label = 'Please select your allocation to the second company',
                        min_value= 25,
                        max_value= 425,
                        step= 25,
                        key='c2_loan')
    
    c3 = st.selectbox(label = 'Please select your third company',
                      options = data['company'].unique(),
                      index= None,
                      placeholder= 'Click to select',
                      key = 'c3')
    c3_loan = st.slider(label = 'Please select your allocation to the third company',
                        min_value= 25,
                        max_value= 425,
                        step= 25,
                        key='c3_loan')

    c4 = st.selectbox(label = 'Please select your fourth company',
                      options = data['company'].unique(),
                      index= None,
                      placeholder= 'Click to select',
                      key = 'c4')
    c4_loan = st.slider(label = 'Please select your allocation to the fourth company',
                        min_value= 25,
                        max_value= 425,
                        step= 25,
                        key='c4_loan')
    
    submitted = st.form_submit_button("Submit your loan authorizations")

    if submitted:
        total_c = len(set([c1, c2, c3, c4]))
        total_l = sum([c1_loan, c2_loan, c3_loan, c4_loan])
        # validate 4 unique companies and store results of validation
        # validate total amount is 500 and store results of validation
        if (total_c == 4) & (total_l == funds):
            st.success("Thank you for your submission! Check out your results below.")
            correct = True
            # create the dictionary 
            selection = {c1:c1_loan,c2:c2_loan, c3:c3_loan, c4:c4_loan}            
        elif total_c == 1:
            st.error(f"""You selected {total_c} unique company and allocated \${total_l} million in loans.
                     You need to select 4 unique companies and allocate \$500 million in loans.""")
        else: 
            st.error(f"""You selected {total_c} unique companies and allocated \${total_l} million in loans.
                     You need to select 4 unique companies and allocate \$500 million in loans.""")


if correct:
   results_df = calculations(data = data, selection = selection, funds = funds)
   user_output()
else:
   pass


with st.expander("Expand to review project context"):
   st.markdown(f""" **Objective**

Explore methodologies of financed emissions, using the automotive sector as an example.

Referenced methodology documents include [PCAF's 2022 Financed Emissions Standard](https://carbonaccountingfinancials.com/files/downloads/PCAF-Global-GHG-Standard.pdf), [Scotiabank's Automotive Sector Emissions Targeting](https://www.scotiabank.com/content/dam/scotiabank/corporate/Documents/EN-Emissions_Reduction_Target_Automotive_Sector_1-11-23.pdf), and [Scotiabank's 2023 Climate Report](https://www.scotiabank.com/content/dam/scotiabank/corporate/Documents/Scotiabank_2023_Climate_Report_Final.pdf).

**Data Overview**

To facilitate this exercise, a micro dataset was created using OEM’s publicly reported emissions and financial data from 2021.
Applied transformations include aligning reporting units for emissions, sales volumes, and debt + equity base.

*Note: The fiscal year end for which companies reported financials and emissions differed - thus the data collection periods across companies are not the same. While the values are still representative enough for this exercise, it points to one of many intricacies of accurately deriving financed emissions.* 

---

**Data Dictionary**

| Column Name | Description |
|---|---|
| company | Company name |
| scope1 | Scope 1 emissions (tCO2e) |
| scope2 | Scope 2 emissions (tCO2e) |
| scope3 | Scope 3 emissions (tCO2e) |
| sales_vol | Vehicles sold (millions of units) |
| debt_eq | Debt + Equity base (millions USD) |

*Note: Data for Volvo is for the Volvo Cars business unit only*          
            """)