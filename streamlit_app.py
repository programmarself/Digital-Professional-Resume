import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

def generate_pdf(name, profession, contact_info, skills, experience):
    # Create a buffer to hold the generated PDF
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
    
    # Rewind buffer to the beginning so that it can be read from the start
    buffer.seek(0)
    return buffer

# Streamlit app
st.title("Digital Professional Resume")

# User Input with st.form("resume_form"):
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
            # Generate the PDF buffer
            pdf_buffer = generate_pdf(name, profession, contact_info, skills, experience)
            
            # Provide the download button
            st.download_button(
                label="Download PDF",
                data=pdf_buffer.getvalue(),  # Extract binary data from the buffer
                file_name="resume.pdf",  # Define the file name
                mime="application/pdf"  # Set MIME type for the download
            )
        else:
            st.error("Please fill in all required fields.")
