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

    # Define initial Y position for text to start (based on the title size)
    y_position = height - 50

    # Title of the Resume with emoji
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, f"{name}'s Resume 🎉")
    y_position -= 40  # Move down after title

    # Profile Picture and Contact Info at the top
    img_height = 120  # Set height for profile picture
    img_width = 120   # Set width for profile picture

    if image_path:
        img = Image.open(image_path)
        img = img.resize((img_width, img_height))  # Ensure the image fits the size
        img.save("temp_img.png")
        # Position the image and create a circular frame
        c.setStrokeColor(colors.gray)
        c.setLineWidth(1)
        c.circle(80, y_position - 60, 60)  # Draw a circle around the image
        c.drawImage("temp_img.png", 20, y_position - 80, width=img_width, height=img_height)
        y_position -= 140  # Move down after profile picture to avoid overlap
    else:
        y_position -= 40  # If no image, move down without affecting text flow

    # Contact Info (name, email, phone) next to the image
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawString(160, y_position, f"📧 Email: {email}")
    y_position -= 20
    c.drawString(160, y_position, f"📱 Phone: {phone}")
    y_position -= 40  # Add space after contact info

    # Draw a line after contact info
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(1)
    c.line(30, y_position, width - 30, y_position)
    y_position -= 20  # Move down after line

    # Biography Section with an emoji
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "👤 Biography:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    text = c.beginText(30, y_position)
    text.setFont("Helvetica", 12)
    for line in bio.split('\n'):
        text.textLine(line)
        y_position -= 14  # Adjust line height dynamically
    c.drawText(text)
    y_position -= 20  # Add space after biography section

    # Skills Section with an emoji
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "💼 Skills:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    skill_list = skills.split(", ")
    for i, skill in enumerate(skill_list):
        c.drawString(30, y_position, f"- {skill}")
        y_position -= 20  # Move down after each skill
    y_position -= 20  # Add space after skills section

    # Education Section with an emoji
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "🎓 Education:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    text = c.beginText(30, y_position)
    text.setFont("Helvetica", 12)
    for line in education.split('\n'):
        text.textLine(line)
        y_position -= 14  # Adjust line height dynamically
    c.drawText(text)
    y_position -= 20  # Add space after education section

    # Work Experience Section with an emoji
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "💼 Work Experience:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    text = c.beginText(30, y_position)
    text.setFont("Helvetica", 12)
    for line in work_experience.split('\n'):
        text.textLine(line)
        y_position -= 14  # Adjust line height dynamically
    c.drawText(text)
    y_position -= 20  # Add space after work experience section

    # Projects Section with an emoji
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "📂 Projects:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    text = c.beginText(30, y_position)
    text.setFont("Helvetica", 12)
    for line in projects.split('\n'):
        text.textLine(line)
        y_position -= 14  # Adjust line height dynamically
    c.drawText(text)
    y_position -= 20  # Add space after projects section

    # Certifications Section with an emoji
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "🏅 Certifications:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    text = c.beginText(30, y_position)
    text.setFont("Helvetica", 12)
    for line in certifications.split('\n'):
        text.textLine(line)
        y_position -= 14  # Adjust line height dynamically
    c.drawText(text)
    y_position -= 20  # Add space after certifications section

    # Draw a line before the footer
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(1)
    c.line(30, y_position, width - 30, y_position)
    y_position -= 20  # Move down after line

    # Footer (Social Media, LinkedIn, etc.)
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, f"🔗 LinkedIn: www.linkedin.com/in/{name.lower().replace(' ', '')}")
    c.drawString(width - 250, y_position, f"🐱 GitHub: github.com/{name.lower().replace(' ', '')}")

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
