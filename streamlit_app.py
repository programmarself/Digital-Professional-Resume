import streamlit as st

# Set the page title
st.set_page_config(page_title='Resume', page_icon=':memo:')

# Custom CSS for styling
st.markdown("""
    <style>
        .header {
            background-color: #007ACC;
            color: white;
            padding: 10px;
            text-align: center;
        }
        .section-title {
            color: #007ACC;
            font-size: 24px;
            margin-top: 20px;
        }
        .contact {
            background-color: #f0f8ff;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .experience, .education, .skills, .languages {
            background-color: #e0f7fa;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Header section
st.markdown('<div class="header"><h1>John Smith</h1><h3>Your Profession Here</h3></div>', unsafe_allow_html=True)

# Contact information
st.markdown('<div class="contact"><h4>Contact</h4></div>', unsafe_allow_html=True)
st.markdown("""
- **Email:** johnsmith@example.com
- **Phone:** +123 456 7890
- **LinkedIn:** [linkedin.com/in/johnsmith](https://linkedin.com/in/johnsmith)
- **GitHub:** [github.com/johnsmith](https://github.com/johnsmith)
""")

# About Me section
st.markdown('<div class="section-title">About Me</div>', unsafe_allow_html=True)
st.write("A brief description about yourself.")

# Experience section
st.markdown('<div class="experience"><h4>Experience</h4></div>', unsafe_allow_html=True)
st.markdown("""
**Company Name**  
*Your Position*  
*Jan 2019 - Present*  
- Responsibility 1
- Responsibility 2
- Responsibility 3

**Company Name**  
*Your Position*  
*Jan 2018 - Dec 2018*  
- Responsibility 1
- Responsibility 2
- Responsibility 3
""")

# Education section
st.markdown('<div class="education"><h4>Education</h4></div>', unsafe_allow_html=True)
st.markdown("""
**Education Name**  
*Degree*  
*Year*

**Education Name**  
*Degree*  
*Year*
""")

# Skills section
st.markdown('<div class="skills"><h4>Skills</h4></div>', unsafe_allow_html=True)
st.markdown("""
- Web Development
- UI Design
- Graphic Design
- Animation
""")

# Languages section
st.markdown('<div class="languages"><h4>Languages</h4></div>', unsafe_allow_html=True)
st.markdown("""
- English
- Spanish
- French
""")
