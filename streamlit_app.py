import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_pdf(name, profession, contact_info, skills, experience):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 20)
    p.drawString(50, height - 50, name)
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 70, profession)

    # Contact Info
    p.drawString(50, height - 100, contact_info)

    # Skills
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 130, "Skills and Competencies")
    p.setFont("Helvetica", 12)
    y = height - 150
    for skill in skills:
        p.drawString(50, y, f"- {skill.strip()}")
        y -= 15

    # Experience
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "Work Experience")
    p.setFont("Helvetica", 12)
    y -= 20
    for exp in experience:
        p.drawString(50, y, exp.strip())
        y -= 15

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# Streamlit app
st.title("Digital Professional Resume")

# User Input
with st.form("resume_form"):
    name = st.text_input("Full Name")
    profession = st.text_input("Profession")
    contact_info = st.text_area("Contact Information")
    skills = st.text_area("Skills (comma-separated)").split(',')
    experience = st.text_area("Work Experience (one per line)").splitlines()
    
    # Submit button
    submitted = st.form_submit_button("Generate PDF")

    if submitted:
        if name and profession:  # Ensure required fields are filled
            pdf_buffer = generate_pdf(name, profession, contact_info, skills, experience)
            
            # Use a separate button for downloading the PDF
            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name="resume.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Please fill in all required fields.")
