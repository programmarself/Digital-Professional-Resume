import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
import datetime
import streamlit_antd_components as sac
import re


def format_date(date):
    return date.strftime("%b %Y")


def generate_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )
    styles = getSampleStyleSheet()
    story = []

    # Title and Name
    title_style = ParagraphStyle(
        name="Title",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontSize=26,
        fontName="Helvetica-Bold",
        spaceAfter=6,
        textColor=colors.darkblue,
    )
    story.append(Paragraph(f"{data['name']}".upper(), title_style))
    story.append(Spacer(1, 12))

    # Contact Info
    contact_style = ParagraphStyle(
        name="Contact",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=12,
        spaceAfter=6,
        textColor=colors.black,
    )

    contact_parts = []
    if data["email"]:
        contact_parts.append(f"Email: {data['email']}")
    if data["phone"]:
        contact_parts.append(f"Phone: {data['phone']}")
    if data["linkedin"]:
        contact_parts.append(f"<link href='{data['linkedin']}'><font color='blue'><u>LinkedIn</u></font></link>")
    if data["github"]:
        contact_parts.append(f"<link href='{data['github']}'><font color='blue'><u>GitHub</u></font></link>")

    contact_info = " | ".join(contact_parts)
    story.append(Paragraph(contact_info, contact_style))

    story.append(Spacer(1, 12))

    # Add section dividers with color
    story.append(
        HRFlowable(width="100%", thickness=0.5, color=colors.grey, spaceBefore=0, spaceAfter=12)
    )

    # Sections
    section_style = ParagraphStyle(
        name="SectionHeader",
        parent=styles["Heading2"],
        fontSize=16,
        fontName="Helvetica-Bold",
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.darkblue,
    )

    normal_style = ParagraphStyle(
        name="Normal", parent=styles["Normal"], fontSize=12, spaceAfter=6
    )

    # Iterate over sections (e.g., Education, Experience, Skills)
    for section_title, section_key in [("SUMMARY", "summary"), ("EDUCATION", "education"), ("EXPERIENCE", "experience"), ("SKILLS", "skills")]:
        if section_key in data and data[section_key]:
            story.append(Paragraph(section_title, section_style))

            if isinstance(data[section_key], list):  # For Education or Experience
                for item in data[section_key]:
                    story.append(Paragraph(item, normal_style))
            else:  # For simple text fields like Summary
                story.append(Paragraph(data[section_key], normal_style))

            story.append(Spacer(1, 6))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceBefore=6, spaceAfter=6))

    doc.build(story)
    buffer.seek(0)
    return buffer


def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    pattern = r"^\+?[0-9]{10,14}$"
    return re.match(pattern, phone) is not None


def is_valid_url(url):
    pattern = r"^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)$"
    return re.match(pattern, url) is not None


def is_valid_grade(grade):
    try:
        float(grade)
        return True
    except ValueError:
        return False


st.set_page_config(page_title="Digital Resume Builder", layout="wide")

# Custom styling with CSS
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #f7f7f7;
        font-family: 'Helvetica', sans-serif;
    }
    h1, h2 {
        color: #0073e6;
    }
    .stButton button {
        background-color: #0073e6;
        color: white;
    }
    .stTextInput input, .stTextArea textarea {
        border-radius: 5px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border: 1px solid #0073e6;
    }
    .stForm { 
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Create Your Digital Resume")
st.markdown("Built by [Irfan Khanj](https://www.linkedin.com/in/iukhan/)")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = {
        "name": "",
        "email": "",
        "phone": "",
        "linkedin": "",
        "github": "",
        "summary": "",
        "education": [],
        "experience": [],
        "skills": "",
        "languages": "",
        "certifications": "",
        "hobbies": "",
    }

# Step-by-step progress bar
current_step = sac.steps(
    items=[
        sac.StepsItem(title="Basic Info"),
        sac.StepsItem(title="Education"),
        sac.StepsItem(title="Experience"),
        sac.StepsItem(title="Skills"),
        sac.StepsItem(title="Generate PDF"),
    ],
    size="xs",
    return_index=True,
)

if current_step == 0:
    with st.form("basic_info_form"):
        st.subheader("Basic Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            name = st.text_input("Full Name", st.session_state.data["name"])
        with col2:
            email = st.text_input("Email", st.session_state.data["email"])
        with col3:
            phone = st.text_input("Phone", st.session_state.data["phone"])

        col4, col5 = st.columns(2)
        with col4:
            linkedin = st.text_input("LinkedIn Link", st.session_state.data["linkedin"])
        with col5:
            github = st.text_input("GitHub Link", st.session_state.data["github"])

        summary = st.text_area("Summary", st.session_state.data["summary"])
        submit = st.form_submit_button("Save & Continue")

        if submit:
            error = False

            if not name:
                st.error("Please enter your full name.")
                error = True

            if not is_valid_email(email):
                st.error("Please enter a valid email address.")
                error = True

            if not is_valid_phone(phone):
                st.error(
                    "Please enter a valid phone number (10-14 digits, optionally starting with +)."
                )
                error = True

            if linkedin and not is_valid_url(linkedin):
                st.error("Please enter a valid LinkedIn URL.")
                error = True

            if github and not is_valid_url(github):
                st.error("Please enter a valid GitHub URL.")
                error = True

            if not error:
                st.session_state.data.update(
                    {
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "linkedin": linkedin,
                        "github": github,
                        "summary": summary,
                    }
                )
                st.success("Basic information saved successfully!")

elif current_step == 1:
    # Display existing education entries
    for i, edu in enumerate(st.session_state.data["education"]):
        st.write(f"Entry {i+1}: {edu['school']} - {edu['course']}")

    # Form for adding new education entry
    with st.form("education_form"):
        st.subheader("Education")
        col1, col2 = st.columns(2)
        with col1:
            school = st.text_input("School Name")
            start_date = st.date_input(
                "Start Date",
                min_value=datetime.date(1900, 1, 1),
                max_value=datetime.date.today(),
            )
        with col2:
            course = st.text_input("Course Name")
            end_date = st.date_input(
                "End Date",
                min_value=datetime.date(1900, 1, 1),
                max_value=datetime.date.today(),
            )

        grade = st.text_input("Grade/CGPA")
        submit = st.form_submit_button("Add Education")

        if submit:
            error = False
            if not school or not course:
                st.error("Please provide school and course names.")
                error = True
            if not is_valid_grade(grade):
                st.error("Please enter a valid grade or CGPA.")
                error = True
            if not error:
                st.session_state.data["education"].append(
                    {
                        "school": school,
                        "course": course,
                        "start_date": format_date(start_date),
                        "end_date": format_date(end_date),
                        "grade": grade,
                    }
                )
                st.success("Education entry added successfully!")
