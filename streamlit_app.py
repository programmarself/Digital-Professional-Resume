import streamlit as st

# Set the page title
st.set_page_config(page_title='Resume', page_icon=':memo:')

# Header section
st.title("John Smith")
st.subheader("Your Profession Here")

# Contact information
st.markdown("### Contact")
st.markdown("""
- **Email:** johnsmith@example.com
- **Phone:** +123 456 7890
- **LinkedIn:** [linkedin.com/in/johnsmith](https://linkedin.com/in/johnsmith)
- **GitHub:** [github.com/johnsmith](https://github.com/johnsmith)
""")

# About Me section
st.markdown("### About Me")
st.write("A brief description about yourself.")

# Experience section
st.markdown("### Experience")
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
st.markdown("### Education")
st.markdown("""
**Education Name**  
*Degree*  
*Year*

**Education Name**  
*Degree*  
*Year*
""")

# Skills section
st.markdown("### Skills")
st.markdown("""
- Web Development
- UI Design
- Graphic Design
- Animation
""")

# Languages section
st.markdown("### Languages")
st.markdown("""
- English
- Spanish
- French
""")
