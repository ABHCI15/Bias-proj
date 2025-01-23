import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import random
from streamlit_cookies_controller import CookieController
import time



st.set_page_config(
    page_title="Survey Social Media",
    page_icon="📱",
    # layout="wide"
)
controller = CookieController()

if controller.get("submitted") == "True":
    st.success("You have already submitted your response. Thank you for participating!")

if controller.get("submitted") is None:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # @st.cache_data
    def get_toss():
        return random.randint(0, 1)

    if controller.get("toss") is None:
        toss = get_toss()
        controller.set("toss", toss)
    else:
        toss = controller.get("toss")

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
            options=["Asian","Asian Indian", "Black", "Hispanic/Latino", "White", "Other", "Prefer not to say"],
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
            if age == 0 or not gender or not grade_level or not ethnicity or not social_media_allowed or hours_spent is None or not high_school:
                st.warning("⚠️ Please fill out all fields before submitting.")
            else:
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
                
                # Add toast sequence
                msg = st.toast('Recording your response...')
                time.sleep(1)
                msg.toast('Analyzing social media habits...')
                time.sleep(1)
                msg.toast('Maybe time to touch some grass? 🌱', icon='📱')
                
                st.success("Response recorded successfully!")
                st.cache_data.clear()
                conn.update(data=df)
                controller.set("submitted", "True")