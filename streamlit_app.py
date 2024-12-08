import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import io
from reportlab.lib import colors

# Function to generate a more professional and creative PDF with emojis and better design
def generate_pdf(name, job_title, phone, email, linked_in, github, portfolio, achievements, education, skills, project_title, project_details, work_experience, volunteer, hackathons, articles, references, image_path):
    # Create a PDF in memory
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title of the Resume with emoji
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkblue)
    c.drawString(30, height - 50, f"{name}'s Resume 🎉")
    y_position = height - 100  # Initial position

    # Profile Picture on the top-right
    img_height = 120  # Set height for profile picture
    img_width = 120   # Set width for profile picture

    if image_path:
        img = Image.open(image_path)
        img = img.resize((img_width, img_height))  # Ensure the image fits the size
        img.save("temp_img.png")
        # Position the image on the top-right corner
        c.setStrokeColor(colors.gray)
        c.setLineWidth(1)
        c.circle(width - 120, height - 120, 60)  # Draw a circle around the image
        c.drawImage("temp_img.png", width - 140, height - 160, width=img_width, height=img_height)
        y_position -= 140  # Move down after profile picture to avoid overlap
    else:
        y_position -= 40  # If no image, move down without affecting text flow

    # Contact Info
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawString(30, y_position, f"📧 Email: {email}")
    y_position -= 20
    c.drawString(30, y_position, f"📱 Phone: {phone}")
    y_position -= 20
    c.drawString(30, y_position, f"🔗 LinkedIn: {linked_in}")
    y_position -= 20
    c.drawString(30, y_position, f"🐱 GitHub: {github}")
    y_position -= 20
    c.drawString(30, y_position, f"🌐 Portfolio: {portfolio}")
    y_position -= 40  # Add space after contact info

    # Achievements Section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "🏆 Achievements:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    for line in achievements.split('\n'):
        c.drawString(30, y_position, f"- {line}")
        y_position -= 20
    y_position -= 20  # Add space after achievements section

    # Education Section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "🎓 Education:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    for line in education.split('\n'):
        c.drawString(30, y_position, f"- {line}")
        y_position -= 20
    y_position -= 20  # Add space after education section

    # Skills Section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "💼 Skills:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    for line in skills.split(','):
        c.drawString(30, y_position, f"- {line.strip()}")
        y_position -= 20
    y_position -= 20  # Add space after skills section

    # Final Year Project Section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "🖥 Final Year Project:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    c.drawString(30, y_position, f"Title: {project_title}")
    y_position -= 20
    c.drawString(30, y_position, f"Details: {project_details}")
    y_position -= 40  # Add space after project section

    # Work Experience Section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "💼 Work Experience:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    for line in work_experience.split('\n'):
        c.drawString(30, y_position, f"- {line}")
        y_position -= 20
    y_position -= 20  # Add space after work experience section

    # Volunteer Section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "🤝 Volunteer Activities:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    for line in volunteer.split('\n'):
        c.drawString(30, y_position, f"- {line}")
        y_position -= 20
    y_position -= 20  # Add space after volunteer section

    # Hackathons Section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "🏆 International Hackathons:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    for line in hackathons.split('\n'):
        c.drawString(30, y_position, f"- {line}")
        y_position -= 20
    y_position -= 20  # Add space after hackathons section

    # Articles Section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "📝 Articles Written:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    for line in articles.split('\n'):
        c.drawString(30, y_position, f"- {line}")
        y_position -= 20
    y_position -= 20  # Add space after articles section

    # References Section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.darkblue)
    c.drawString(30, y_position, "📑 References:")
    y_position -= 20
    c.setFont("Helvetica", 12)
    for line in references.split('\n'):
        c.drawString(30, y_position, f"- {line}")
        y_position -= 20

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
    job_title = st.text_input("Job Title (e.g. Software Engineer, Data Scientist)")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    linked_in = st.text_input("LinkedIn URL")
    github = st.text_input("GitHub URL")
    portfolio = st.text_input("Portfolio URL")
    
    achievements = st.text_area("Achievements (each entry on a new line)")
    education = st.text_area("Education (each entry on a new line)")
    skills = st.text_input("Skills (comma-separated)")
    project_title = st.text_input("Project Title")
    project_details = st.text_area("Project Details")
    work_experience = st.text_area("Work Experience (each entry on a new line)")
    volunteer = st.text_area("Volunteer Activities (each entry on a new line)")
    hackathons = st.text_area("Hackathons (each entry on a new line)")
    articles = st.text_area("Articles Written (each entry on a new line)")
    references = st.text_area("References (each entry on a new line)")
    
    image = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])

    # Generate Resume button
    if st.button("Generate Resume"):
        if not name or not email or not phone or not achievements or not education or not skills:
            st.error("Please fill in all fields.")
        else:
            image_path = image if image else None

            # Generate PDF
            pdf_buffer = generate_pdf(name, job_title, phone, email, linked_in, github, portfolio, achievements, education, skills, project_title, project_details, work_experience, volunteer, hackathons, articles, references, image_path)

            # Provide download link
            st.download_button(
                label="Download Resume as PDF",
                data=pdf_buffer,
                file_name=f"{name}_resume.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
