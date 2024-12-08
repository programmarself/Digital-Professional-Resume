import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import io
from reportlab.lib import colors

# Function to generate a more professional and creative PDF with emojis and better design
def generate_pdf(name, email, phone, bio, skills, education, work_experience, projects, certifications, image_path):
    # Create a PDF in memory
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title of the Resume with emoji
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkblue)
    c.drawString(30, height - 50, f"{name}'s Resume 🎉")

    # Contact Info with emojis
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawString(30, height - 80, f"📧 Email: {email}")
    c.drawString(30, height - 100, f"📱 Phone: {phone}")

    # Profile Picture (if uploaded), with a circular border
    if image_path:
        img = Image.open(image_path)
        img = img.resize((120, 120))  # Ensure the image fits the size
        img.save("temp_img.png")
        c.setStrokeColor(colors.gray)
        c.setLineWidth(1)
        c.circle(width - 150, height - 180, 60)  # Draw a circle around the image
        c.drawImage("temp_img.png", width - 180, height - 200, width=120, height=120)

    # Draw a line after contact info
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(1)
    c.line(30, height - 120, width - 30, height - 120)

    # Biography Section with an emoji
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, height - 160, "👤 Biography:")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    text = c.beginText(30, height - 100)
    text.setFont("Helvetica", 12)
    for line in bio.split('\n'):
        text.textLine(line)
    c.drawText(text)

    # Skills Section with an emoji
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, height - 250, "💼 Skills:")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    skill_list = skills.split(", ")
    for i, skill in enumerate(skill_list):
        c.drawString(30, height - 270 - i * 20, f"- {skill}")

    # Education Section with an emoji
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, height - 350, "🎓 Education:")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    text = c.beginText(30, height - 370)
    text.setFont("Helvetica", 12)
    for line in education.split('\n'):
        text.textLine(line)
    c.drawText(text)

    # Work Experience Section with an emoji
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, height - 450, "💼 Work Experience:")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    text = c.beginText(30, height - 470)
    text.setFont("Helvetica", 12)
    for line in work_experience.split('\n'):
        text.textLine(line)
    c.drawText(text)

    # Projects Section with an emoji
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, height - 550, "📂 Projects:")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    text = c.beginText(30, height - 570)
    text.setFont("Helvetica", 12)
    for line in projects.split('\n'):
        text.textLine(line)
    c.drawText(text)

    # Certifications Section with an emoji
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, height - 650, "🏅 Certifications:")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    text = c.beginText(30, height - 670)
    text.setFont("Helvetica", 12)
    for line in certifications.split('\n'):
        text.textLine(line)
    c.drawText(text)

    # Draw a line before the footer
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(1)
    c.line(30, height - 690, width - 30, height - 690)

    # Footer (Social Media, LinkedIn, etc.)
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.darkblue)
    c.drawString(30, 30, f"🔗 LinkedIn: www.linkedin.com/in/{name.lower().replace(' ', '')}")
    c.drawString(width - 250, 30, f"🐱 GitHub: github.com/{name.lower().replace(' ', '')}")

    # Save the PDF
    c.showPage()
    c.save()

    # Return the PDF as bytes
    buffer.seek(0)
    return buffer

# Streamlit App
def main():
    st.title("Digital Professional Resume Builder")

    # Style for the Streamlit interface
    st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 12px;
    }
    .stTextInput>div>div>input {
        background-color: #f0f8ff;
        border: 1px solid #add8e6;
    }
    .stTextArea>div>div>textarea {
        background-color: #f0f8ff;
        border: 1px solid #add8e6;
    }
    .stFileUploader>div>div>div>input {
        background-color: #f0f8ff;
        border: 1px solid #add8e6;
    }
    </style>
    """, unsafe_allow_html=True)

    # User inputs
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    bio = st.text_area("Biography")
    skills = st.text_input("Skills (comma-separated)")
    education = st.text_area("Education (each entry on a new line)")
    work_experience = st.text_area("Work Experience (each entry on a new line)")
    projects = st.text_area("Projects (each entry on a new line)")
    certifications = st.text_area("Certifications (each entry on a new line)")

    # Profile picture upload
    image = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])

    # Styling for button
    if st.button("Generate Resume"):
        if not name or not email or not phone or not bio or not skills or not education or not work_experience or not projects or not certifications:
            st.error("Please fill in all fields.")
        else:
            if image:
                image_path = image
            else:
                image_path = None

            # Generate PDF
            pdf_buffer = generate_pdf(name, email, phone, bio, skills, education, work_experience, projects, certifications, image_path)

            # Provide download link
            st.download_button(
                label="Download Resume as PDF",
                data=pdf_buffer,
                file_name=f"{name}_resume.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
