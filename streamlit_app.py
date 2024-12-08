import streamlit as st
import pandas as pd
from fpdf import FPDF
import os

# App Title
st.title("Digital Professional Resume")

# Personal Information
with st.form("personal_info"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "png", "jpeg"])
    personal_info_submit = st.form_submit_button("Submit")

# Work Experience
with st.form("work_experience"):
    st.header("Work Experience")
    company = st.text_input("Company Name")
    position = st.text_input("Position")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    description = st.text_area("Description")
    work_exp_submit = st.form_submit_button("Add Experience")

# Education
with st.form("education"):
    st.header("Education")
    degree = st.text_input("Degree")
    institution = st.text_input("Institution")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    field_of_study = st.text_input("Field of Study")
    education_submit = st.form_submit_button("Add Education")

# Skills
with st.form("skills"):
    st.header("Skills")
    skills = st.text_input("Skills (comma-separated)")
    skills_submit = st.form_submit_button("Add Skills")

# Generate and Download PDF
def generate_pdf(personal_info, work_experience, education, skills):
    pdf = FPDF()
    pdf.add_page()

    # Add personal information
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Personal Information", ln=True)
    for key, value in personal_info.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    # Add work experience
    pdf.cell(200, 10, txt="Work Experience", ln=True)
    for key, value in work_experience.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    # Add education
    pdf.cell(200, 10, txt="Education", ln=True)
    for key, value in education.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    # Add skills
    pdf.cell(200, 10, txt="Skills", ln=True)
    pdf.cell(200, 10, txt=skills, ln=True)

    pdf.output("resume.pdf")
    return "resume.pdf"

if personal_info_submit:
    personal_info = {
        "Name": name,
        "Email": email,
        "Phone Number": phone
    }
    if profile_pic:
        profile_pic_path = os.path.join("uploads", profile_pic.name)
        with open(profile_pic_path, "wb") as f:
            f.write(profile_pic.getbuffer())
        personal_info["Profile Picture"] = profile_pic_path
    
    resume_path = generate_pdf(personal_info, {}, {}, "")
    with open(resume_path, "rb") as f:
        st.download_button("Download Resume", data=f, file_name="resume.pdf")

if work_exp_submit:
    # Process work experience
    st.session_state.work_experience = {
        "Company Name": company,
        "Position": position,
        "Start Date": start_date,
        "End Date": end_date,
        "Description": description
    }

if education_submit:
    # Process education
    st.session_state.education = {
        "Degree": degree,
        "Institution": institution,
        "Start Date": start_date,
        "End Date": end_date,
        "Field of Study": field_of_study
    }

if skills_submit:
    # Process skills
    st.session_state.skills = skills
