# Some interface code 
import streamlit as st
import pandas as pd
import numpy as np
import time

# TODO Create a nav bar on the left side of the screen 
home_Button = st.sidebar.button("Home")
CP_Button = st.sidebar.button("C&P Button")
UBar_Button = st.sidebar.button("UBar Button")
Custom_Button = st.sidebar.button("Custom Button")
#2 gates between cutsom z

if Custom_Button:
	left_input, right_input = st.columns(2)
	with left_input:
		custom1 = st.text_input("Custom1", key="gate1", placeholder="Enter a number")
	with right_input:
		custom2 = st.text_input("Custom2", key="gate2", placeholder="Enter a number")
		
    #custom_df = 


# TODO Create a place to display the data frame s

dataframe = pd.DataFrame({
	'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

st.dataframe(dataframe, hide_index=True)


# TODO Create a section on the right to display some analytics boxes 


