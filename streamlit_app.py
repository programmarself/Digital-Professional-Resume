import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
import streamlit_antd_components as sac
import datetime, re
from reportlab.pdfbase.ttfonts import TTFont
from reportlab import pdfmetrics

# Function to format date in "Month Year" format
def format_date(date):
    return date.strftime("%b %Y")

# Function to generate PDF with custom styling
def generate_pdf(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    
    # Load custom fonts
    pdfmetrics.registerFont(TTFont('HelveticaNeue', 'path/to/HelveticaNeue.ttf'))
    
    # Set up styles
    styles = getSampleStyleSheet()
    custom_font_style = ParagraphStyle(
        name="CustomFont",
        parent=styles['Normal'],
        fontName='HelveticaNeue',  # Custom font
        fontSize=12,
        leading=14,
        textColor=colors.black
    )
    
    title_style = ParagraphStyle(
        name="Title",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        fontName='HelveticaNeue',
        fontSize=24,
        textColor=colors.black,
        spaceAfter=10,
    )
    
    story = []
    
    # Title (Name)
    if data["name"]:
        story.append(Paragraph(f"{data['name']}".upper(), title_style))
    
    story.append(Spacer(1, 6))
    
    # Contact Information (Email, Phone, LinkedIn, GitHub)
    contact_style = ParagraphStyle(
        name="Contact",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        spaceAfter=10,
        textColor=colors.grey
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
    
    if contact_parts:
        contact_info = " | ".join(contact_parts)
        story.append(Paragraph(contact_info, contact_style))

    # Add a separator line
    story.append(Spacer(1, 12))
    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.grey,
            spaceBefore=0,
            spaceAfter=10
        )
    )
    
    # General styling for other sections
    normal_style = ParagraphStyle(
        name="Normal", parent=styles["Normal"], fontSize=11, spaceAfter=6
    )
    
    bold_style = ParagraphStyle(
        name="Bold", parent=styles["Normal"], fontSize=12, spaceAfter=6, alignment=TA_LEFT, fontName='HelveticaNeue-Bold'
    )

    # Create sections (Education, Experience, etc.)
    sections = [
        ("SUMMARY", "summary"),
        ("EDUCATION", "education"),
        ("EXPERIENCE", "experience"),
        ("ADDITIONAL INFORMATION", "additional_information"),
    ]
    
    for section_title, section_key in sections:
        if section_key == "education":
            story.append(Paragraph(section_title, bold_style))
            for edu in data["education"]:
                if edu["school"] and edu["timeline"]:
                    timeline_str = f"{format_date(edu['timeline'][0])} - {format_date(edu['timeline'][1])}"
                    story.append(Paragraph(f"<b>{edu['school'].title()}</b> | <b>{timeline_str}</b>", bold_style))
                if edu["course"]:
                    story.append(Paragraph(f"{edu['course'].title()}", normal_style))
                if edu["grade"]:
                    story.append(Paragraph(f"\u2022 Grade: {edu['grade']}", normal_style))
                story.append(Spacer(1, 6))

        elif section_key == "experience":
            story.append(Paragraph(section_title, bold_style))
            for exp in data["experience"]:
                if exp["company"] and exp["timeline"] and exp["role"]:
                    timeline_str = f"{format_date(exp['timeline'][0])} - {format_date(exp['timeline'][1])}"
                    story.append(Paragraph(f"<b>{exp['company'].title()} - {exp['role'].title()}</b> | <b>{timeline_str}</b>", bold_style))
                if exp["experience_summary"]:
                    bullet_points = re.split(r"\s*-\s+", exp["experience_summary"].strip())
                    for point in bullet_points:
                        if point:
                            story.append(Paragraph(f"\u2022 {point}", normal_style))
                story.append(Spacer(1, 6))

        elif section_key == "additional_information":
            story.append(Paragraph(section_title, bold_style))
            if data["skills"]:
                story.append(Paragraph(f"<b>Skills:</b> {data['skills']}", normal_style))
            if data["languages"]:
                story.append(Paragraph(f"<b>Languages:</b> {data['languages']}", normal_style))
            if data["certifications"]:
                story.append(Paragraph(f"<b>Certifications:</b> {data['certifications']}", normal_style))
            if data["hobbies"]:
                story.append(Paragraph(f"<b>Hobbies:</b> {data['hobbies']}", normal_style))

        elif section_key in data and data[section_key].strip():
            story.append(Paragraph(section_title, bold_style))
            story.append(Paragraph(data[section_key], normal_style))

        # Add a horizontal line separator
        story.append(Spacer(1, 12))
        story.append(
            HRFlowable(
                width="100%",
                thickness=1,
                color=colors.grey,
                spaceBefore=0,
                spaceAfter=10
            )
        )

    # Build PDF document
    doc.build(story)
    buffer.seek(0)
    return buffer

# Utility functions for validation (unchanged)
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

# Streamlit UI components
st.title("Digital Professional Resume")
st.markdown("Built by [Irfan Khanj](https://www.linkedin.com/in/iukhan/)")

# Add the remaining steps and logic (unchanged, use the same form flow)
# Step 1: Basic Info
# Step 2: Education
# Step 3: Experience
# Step 4: Additional Information
# Step 5: Generate PDF

