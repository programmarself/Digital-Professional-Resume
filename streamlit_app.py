import streamlit as st
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from PIL import Image
from io import BytesIO
import datetime, re
import streamlit_antd_components as sac


# Function to format date
def format_date(date):
    return date.strftime("%b %Y")


# Function to generate a more professional and creative PDF with emojis and better design
def generate_pdf(data, image_path=None):
    buffer = BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=0.5 * inch,
        rightMargin=0.5 * inch,
        topMargin=0.3 * inch,
        bottomMargin=0.3 * inch,
    )

    styles = getSampleStyleSheet()
    story = []

    # Title
    if data["name"]:
        title_style = ParagraphStyle(
            name="Title",
            parent=styles["Heading1"],
            alignment=TA_CENTER,
            fontSize=24,
            spaceAfter=6,
        )
        story.append(Paragraph(f"{data['name']}".upper(), title_style))
    
    story.append(Spacer(1, 6))

    # Contact Info
    contact_style = ParagraphStyle(
        name="Contact",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        spaceAfter=6,
    )

    contact_parts = []
    if data["email"]:
        contact_parts.append(data["email"])
    if data["phone"]:
        contact_parts.append(data["phone"])
    if data["linkedin"]:
        contact_parts.append(
            f"<link href='{data['linkedin']}'><font color='blue'><u>{data['linkedin']}</u></font></link>"
        )
    if data["github"]:
        contact_parts.append(
            f"<link href='{data['github']}'><font color='blue'><u>{data['github']}</u></font></link>"
        )

    if contact_parts:
        contact_info = " | ".join(contact_parts)
        story.append(Paragraph(contact_info, contact_style))

    story.append(Spacer(1, 12))
    story.append(
        HRFlowable(
            width="100%", thickness=0.5, color=colors.grey, spaceBefore=0, spaceAfter=6
        )
    )

    normal_style = ParagraphStyle(
        name="Normal", parent=styles["Normal"], fontSize=11, spaceAfter=4
    )
    bold_style = ParagraphStyle(
        name="Normal", parent=styles["Normal"], fontSize=12, spaceAfter=4
    )

    # Add sections like Summary, Education, Experience, etc.
    sections = [
        ("SUMMARY", "summary"),
        ("EDUCATION", "education"),
        ("EXPERIENCE", "experience"),
        ("ADDITIONAL INFORMATION", "additional_information"),
    ]
    
    # Add each section to the PDF document
    for section_title, section_key in sections:
        if section_key == "education":
            story.append(Paragraph(section_title, styles["Heading2"]))
            for edu in data["education"]:
                if edu["school"] and edu["timeline"]:
                    timeline_str = f"{format_date(edu['timeline'][0])} - {format_date(edu['timeline'][1])}"
                    story.append(
                        Paragraph(
                            f"<b>{edu['school'].title()}</b> | <b>{timeline_str}</b>",
                            bold_style,
                        )
                    )
                if edu["course"]:
                    story.append(Paragraph(f"{edu['course'].title()}", normal_style))
                if edu["grade"]:
                    story.append(
                        Paragraph(f"\u2022 Grade: {edu['grade']}", normal_style)
                    )
                story.append(Spacer(1, 8))

        elif section_key == "experience":
            story.append(Paragraph(section_title, styles["Heading2"]))
            for exp in data["experience"]:
                if exp["company"] and exp["timeline"] and exp["role"]:
                    timeline_str = f"{format_date(exp['timeline'][0])} - {format_date(exp['timeline'][1])}"
                    story.append(
                        Paragraph(
                            f"<b>{exp['company'].title()}, {exp['role'].title()}</b> | <b>{timeline_str}</b>",
                            bold_style,
                        )
                    )
                if exp["experience_summary"]:
                    bullet_points = re.split(
                        r"\s*-\s+", exp["experience_summary"].strip()
                    )
                    for point in bullet_points:
                        if point:
                            story.append(Paragraph(f"\u2022 {point}", normal_style))
                story.append(Spacer(1, 8))

        elif section_key == "additional_information":
            story.append(Paragraph(section_title, styles["Heading2"]))
            if data["skills"]:
                story.append(
                    Paragraph(f"<b>Skills:</b> {data['skills']}", normal_style)
                )
            if data["languages"]:
                story.append(
                    Paragraph(f"<b>Languages:</b> {data['languages']}", normal_style)
                )
            if data["certifications"]:
                story.append(
                    Paragraph(
                        f"<b>Certifications:</b> {data['certifications']}", normal_style
                    )
                )
            if data["hobbies"]:
                story.append(
                    Paragraph(f"<b>Hobbies:</b> {data['hobbies']}", normal_style)
                )

        elif section_key in data and data[section_key].strip():
            story.append(Paragraph(section_title, styles["Heading2"]))
            story.append(Paragraph(data[section_key], normal_style))

        story.append(Spacer(1, 6))
        story.append(
            HRFlowable(
                width="100%",
                thickness=0.5,
                color=colors.grey,
                spaceBefore=0,
                spaceAfter=6,
            )
        )

    # If there's a profile image, add it to the document
    if image_path:
        img = Image.open(image_path)
        img = img.resize((120, 120))  # Resize image to fit the document
        img.save("temp_img.png")
        story.append(Spacer(1, 6))
        story.append(
            HRFlowable(
                width="100%", thickness=0.5, color=colors.grey, spaceBefore=0, spaceAfter=6
            )
        )
        story.append("<img src='temp_img.png' width='120' height='120' />")
    
    # Generate the document
    doc.build(story)
    buffer.seek(0)
    return buffer


# Streamlit UI
def main():
    st.title("Digital Professional Resume Builder")
    
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

    # Handle each step
    if current_step == 0:
        with st.form("basic_info_form"):
            st.subheader("Basic Information")
            name = st.text_input("Full Name", st.session_state.data["name"])
            email = st.text_input("Email", st.session_state.data["email"])
            phone = st.text_input("Phone", st.session_state.data["phone"])
            linkedin = st.text_input("LinkedIn", st.session_state.data["linkedin"])
            github = st.text_input("GitHub", st.session_state.data["github"])
            summary = st.text_area("Summary", st.session_state.data["summary"])
            submit = st.form_submit_button("Save & Continue")
            
            if submit:
                st.session_state.data.update({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "linkedin": linkedin,
                    "github": github,
                    "summary": summary,
                })
                st.success("Basic information saved!")

    elif current_step == 1:
        # Education form
        pass  # Implement the Education section similar to the previous example

    elif current_step == 2:
        # Experience form
        pass  # Implement the Experience section similar to the previous example

    elif current_step == 3:
        # Skills form
        pass  # Implement the Skills section similar to the previous example

    elif current_step == 4:
        # Generate PDF
        st.subheader("Generate PDF")
        if st.button("Generate Resume PDF"):
            pdf = generate_pdf(st.session_state.data)
            st.download_button(
                label="Download Resume PDF",
                data=pdf,
                file_name=f"{st.session_state.data['name']}_resume.pdf",
                mime="application/pdf",
            )

if __name__ == "__main__":
    main()
