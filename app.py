import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random

# Create GSheets connection
conn = st.connection("gsheets", type=GSheetsConnection)




@st.cache_data
def get_toss():
    return random.randint(0, 1)

toss = get_toss()

st.title("Social Media Usage Survey")

group = "Control" if toss == 0 else "Treatment"
# st.write(f"You are in the {group} group.")


if group == "Treatment":
    st.markdown("""
    ## 🤔  Think Before You Scroll: Social Media's Impact

    Before you answer, quickly consider how excessive social media, especially doomscrolling and short-form content, might affect you.

    ---

    ### 📱 What is Doomscrolling?

    **Doomscrolling** is the act of compulsively scrolling through negative news or social media content, even when it's upsetting.

    ### 📉 Potential Effects:

    *   **Mental Health:**
        *   Increased anxiety, stress, and mood swings.
        *   Sleep disruption.


    *   **Cognitive Effects:**
        *   Reduced attention span.
        *   Information overload and distraction.


    *   **Social Impacts:**
        *   Feelings of comparison, envy, and social isolation.
        *   Exposure to echo chambers and increased polarization.


    ---

    **Now, please proceed with the survey.**

    """)

with st.form(key="survey"):

    age = st.number_input(
        "What is your age?",
        min_value=0,
        max_value=100,
        step=1
    )
    
    gender = st.radio(
        "What is your gender?",
        options=["Male", "Female", "Other", "Prefer not to say"],
        index=None
    )
    
    grade_level = st.selectbox(
        "What is your grade level?",
        options=["9th Grade", "10th Grade", "11th Grade", "12th Grade", "College", "Graduated"],
        index=None
    )
    
    ethnicity = st.selectbox(
        "What ethnicity are you?",
        options=["Asian", "Black", "Hispanic/Latino", "White", "Other", "Prefer not to say"],
        index=None
    )
    
    st.write("Please answer the following questions:")
    social_media_allowed = st.radio(
        "Do you think that high school students should be allowed to spend more than an hour a day on social media/short-form content?",
        options=["Yes", "No"],
        index = None
    )

    hours_spent = st.slider(
        "How many hours a day do you spend using social media or watching short-form content?",
        min_value=0,
        max_value=24,
        # value=1,
        step=1,
        
    )
    high_school = st.radio(
        "Are you currently in high school?",
        options=["Yes", "No"], 
        index=None
    )

    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        new_row = {
            "Timestamp": pd.Timestamp.now(),
            "Group": group,
            "Age": age,
            "Gender": gender,
            "Grade Level": grade_level,
            "Ethnicity": ethnicity,
            "Social Media Allowed": social_media_allowed,
            "Hours Spent": hours_spent,
            "High School": high_school
        }
        df = conn.read(ttl=0)
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        st.success("Response recorded successfully!")
        st.dataframe(df)
        st.cache_data.clear()
        conn.update(data=df)