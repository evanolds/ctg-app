# Author:
#   Evan Olds
#
# Created:
#   April 7, 2026

import streamlit as st
from CTGProblem import CTGProblem

# Samples at:
# https://docs.streamlit.io/

# I'd remove the following title from a real app, but I 
# wanted to make sure that I "branded" this app
st.title("Evan Olds's C.T.G. App")

st.header("Solve the limit:")

# Check if a problem already exists in the session state
if "problem" not in st.session_state:
    # Create a CTGProblem instance
    problem = CTGProblem.make_random()
    st.session_state["problem"] = problem
else:
    problem = st.session_state["problem"]

# Make the denominator string
denom_str = f"x^2+{problem.get_c()}x+{problem.get_b()}"

# Display the forumla of interest
latex_str = r'''\lim\limits_{x\to -1}'''
latex_str += "\n"
latex_str += r'''\sqrt{\frac{x+1}{'''
latex_str += denom_str + "}}"
st.latex(latex_str)

user_input = st.text_input(
    "Your answer:",
    placeholder="Please enter your answer as a fraction, decimal, or simplified numeric expression",
    key="new_item_text",
)
if user_input:
    explanation_parts = problem.get_explanation(user_input)
    
    for part in explanation_parts:
        if part["type"] == "badge":
            if part["value"] == "Incorrect":
                st.badge("Incorrect", icon=":material/x_circle:", color="red")
            else:
                st.badge("Correct", icon=":material/check:", color="green")
        elif part["type"] == "text":
            st.text(part["value"])
        elif part["type"] == "latex":
            st.latex(part["value"])