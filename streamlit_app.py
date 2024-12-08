import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import io

# Function to generate PDF
def generate_pdf(name, email, phone, bio, skills, image_path):
    # Create a PDF in memory
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title of the Resume
    c.setFont("Helvetica-Bold", 18)
    c.drawString(30, height - 50, f"{name}'s Resume")

    # Contact Info
    c.setFont("Helvetica", 12)
    c.drawString(30, height - 80, f"Email: {email}")
    c.drawString(30, height - 100, f"Phone: {phone}")
    
    # Bio Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 140, "Biography:")
    c.setFont("Helvetica", 12)
    text = c.beginText(30, height - 160)
    text.setFont("Helvetica", 12)
    for line in bio.split('\n'):
        text.textLine(line)
    c.drawText(text)

    # Skills Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, height - 250, "Skills:")
    c.setFont("Helvetica", 12)
    skill_list = skills.split(", ")
    for i, skill in enumerate(skill_list):
        c.drawString(30, height - 270 - i * 20, f"- {skill}")

    # Profile Picture (if uploaded)
    if image_path:
        img = Image.open(image_path)
        img.save("temp_img.png")
        c.drawImage("temp_img.png", width - 150, height - 180, width=120, height=120)

    # Save the PDF
    c.showPage()
    c.save()

    # Return the PDF as bytes
    buffer.seek(0)
    return buffer

# Streamlit App
def main():
    st.title("Digital Professional Resume Builder")

    # User inputs
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    bio = st.text_area("Biography")
    skills = st.text_input("Skills (comma-separated)")

    # Profile picture upload
    image = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])

    if st.button("Generate Resume"):
        if not name or not email or not phone or not bio or not skills:
            st.error("Please fill in all fields.")
        else:
            if image:
                image_path = image
            else:
                image_path = None

            # Generate PDF
            pdf_buffer = generate_pdf(name, email, phone, bio, skills, image_path)

            # Provide download link
            st.download_button(
                label="Download Resume as PDF",
                data=pdf_buffer,
                file_name=f"{name}_resume.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
