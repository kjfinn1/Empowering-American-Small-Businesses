import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import time, datetime

# you can also add themes, or add secrets as well, can organize in columns too, progress bar if predicting is slow, use @st.cache() decorater before the prediction function runs (this will speed up running predictions/making graphs)

st.write("Hello world")

st.write('Hello, *World!* :sunglasses:')

st.write(1234)

# write dataframes as markdown tables
df = pd.DataFrame({
     'first column': [1, 2, 3, 4],
     'second column': [10, 20, 30, 40]
     })
st.write(df)

# write plotly objects in their full interactive form
plot = px.scatter(df, x='first column', y='second column')
st.write(plot)

# create a button
if st.button('Say hello'):
     st.write('Why hello there')
else:
     st.write('Goodbye')

# selectbox
option = st.selectbox(
     'What is your favorite color?',
     ('Blue', 'Red', 'Green'))

# sidebar
st.sidebar.header("Sidebar")
sidebar_options = st.sidebar.multiselect(
        'Here are options',
        ['1', 'two', '3.0'])

# multi-select
options = st.multiselect(
     'What are your favorite colors',
     ['Green', 'Yellow', 'Red', 'Blue'], #options
     ['Yellow', 'Red']) #starting selected

st.write('You selected:', options)
        
# checkboxes:
st.write ('What would you like to order?')
icecream = st.checkbox('Ice cream')
coffee = st.checkbox('Coffee')
cola = st.checkbox('Cola')

# slider tests: 
# Standard Slider
st.subheader('Slider')

age = st.slider('How old are you?', 0, 130, 25) # beginning, end, start
st.write("I'm ", age, 'years old')

# Range Slider

st.subheader('Range slider')

values = st.slider(
     'Select a range of values',
     0.0, 100.0, (25.0, 75.0)) #beginning, end, (start0, start1)
st.write('Values:', values)

# Range slider (time)

st.subheader('Range time slider')

appointment = st.slider(
     "Schedule your appointment:",
     value=(time(11, 30), time(12, 45)))
st.write("You're scheduled for:", appointment)

# Datetime slider

st.subheader('Datetime slider')

start_time = st.slider(
     "When do you start?",
     value=datetime(2020, 1, 1, 9, 30),
     format="MM/DD/YY - hh:mm")
st.write("Start time:", start_time)

# Forms!! Better than sidebar probably at least for initial input

with st.form('my_form'):
    st.subheader('**Order your coffee**')

    # Input widgets
    coffee_bean_val = st.selectbox('Coffee bean', ['Arabica', 'Robusta'])
    coffee_roast_val = st.selectbox('Coffee roast', ['Light', 'Medium', 'Dark'])
    brewing_val = st.selectbox('Brewing method', ['Aeropress', 'Drip', 'French press', 'Moka pot', 'Siphon'])
    serving_type_val = st.selectbox('Serving format', ['Hot', 'Iced', 'Frappe'])
    milk_val = st.select_slider('Milk intensity', ['None', 'Low', 'Medium', 'High'])
    owncup_val = st.checkbox('Bring own cup')

    # Every form must have a submit button
    submitted = st.form_submit_button('Submit')

if submitted:
    st.markdown(f'''
        ☕ You have ordered:
        - Coffee bean: `{coffee_bean_val}`
        - Coffee roast: `{coffee_roast_val}`
        - Brewing: `{brewing_val}`
        - Serving type: `{serving_type_val}`
        - Milk: `{milk_val}`
        - Bring own cup: `{owncup_val}`
        ''')
else:
    st.write('☝️ Place your order!')
