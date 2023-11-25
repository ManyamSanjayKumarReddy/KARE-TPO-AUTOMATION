import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns

# Hardcoded login credentials
USERNAME = "Admintpo"
PASSWORD = "kare2023"

# Function to check login credentials
def authenticate(username, password):
    return username == USERNAME and password == PASSWORD

# Define a simple SessionState class
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Function to get or create the session state
def get_session():
    if "session" not in st.session_state:
        st.session_state.session = SessionState(login_status=False)
    return st.session_state.session

def filter_data(min_10th, max_10th, min_12th, max_12th, min_diploma, max_diploma, min_cgpa, max_cgpa, genders, ug_specializations, sections):
    # Load your dataset
    master = pd.read_csv('master.csv')

    # Convert sections to a list
    sections = [sections] if isinstance(sections, str) else sections

    if 'All' in sections:
        section_condition = master['UG-Section'].notna()
    else:
        section_condition = master['UG-Section'].isin(sections)

    if 'All' in ug_specializations:
        ug_spec_condition = master['UG-Specialization'].notna()
    else:
        ug_spec_condition = master['UG-Specialization'].isin(ug_specializations)

    if 'Both' in genders:
        gender_condition = master['Gender'].isin(['Male', 'Female'])
    else:
        gender_condition = master['Gender'].isin(genders)

    filtered_df = master[
        (master['10th-Percentage'] >= min_10th)
        & (master['10th-Percentage'] <= max_10th)
        & (master['12-Percentage'].fillna(min_12th) >= min_12th)
        & (master['12-Percentage'].fillna(max_12th) <= max_12th)
        & (master['Diploma-Percentage'].fillna(min_diploma) >= min_diploma)
        & (master['Diploma-Percentage'].fillna(max_diploma) <= max_diploma)
        & (master['CGPA'] >= min_cgpa)
        & (master['CGPA'] <= max_cgpa)
        & gender_condition
        & ug_spec_condition  # Filtering based on UG Specialization
        & section_condition
    ]

    return filtered_df[['S.No.', 'Registration', 'Name', 'DOB', 'UG-Section', 'UG-Department', 'UG-Specialization', 'Email', 'Gender']]

def download_link(df, filename, linktext):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # encode as bytes, then decode to get a string
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{linktext}</a>'
    return href

def main():
    st.title('Office of Corporate Relations KARE ')

    # Initialize SessionState
    session_state = get_session()

    if not session_state.login_status:
        # Additional content when not logged in
        st.write(
            """
            Welcome to the KARE Placement Office!

            Here, you can explore student data and filter based on various criteria.

            Login to access advanced features and download filtered data.

            If you don't have credentials, please contact the Placement Office.
            """
        )
        
        with st.expander("Contact Details"):
            st.write(
                """
                **Dr. A Alavudeen**
                *Director-corporate Relations*
                Kalasalingam Academy of Research and Education
                Anand Nagar, Krishnankovil-626126
                Email: [placements@klu.ac.in](mailto:placements@klu.ac.in)
                Mobile: +91-9443389276

                **Dr. S P Velmurugan**
                *University Placement Coordinator*
                Kalasalingam Academy of Research and Education
                Anand Nagar, Krishnankovil-626126
                Email: [placements@klu.ac.in](mailto:placements@klu.ac.in)
                Mobile: +91-9488335060
                """
            )

        # Image and additional text
        st.image('img1.jpg', caption='KARE Placement Office', use_column_width=True)
        st.write(
            """
            Our mission is to connect talented students with opportunities that align with their skills and ambitions.

            Explore the data to discover the potential of our students.
            """
        )

        

        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            if authenticate(username, password):
                session_state.login_status = True
                st.success("Login successful! Redirecting to the main page...")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
            
            

    if session_state.login_status:
        st.sidebar.text(f"Logged in as {USERNAME}")
        if st.sidebar.button("Logout"):
            session_state.login_status = False
            st.experimental_rerun()
            

        # Load your dataset
        master = pd.read_csv('master.csv')

        # Input fields
        min_10th = st.slider('Minimum 10th Percentage', 0.0, 100.0, 0.0)
        max_10th = st.slider('Maximum 10th Percentage', 0.0, 100.0, 100.0)
        min_12th = st.slider('Minimum 12th Percentage', 0.0, 100.0, 0.0)
        max_12th = st.slider('Maximum 12th Percentage', 0.0, 100.0, 100.0)
        min_diploma = st.slider('Minimum Diploma Percentage', 0.0, 100.0, 0.0)
        max_diploma = st.slider('Maximum Diploma Percentage', 0.0, 100.0, 100.0)
        min_cgpa = st.slider('Minimum CGPA', 0.0, 10.0, 0.0)
        max_cgpa = st.slider('Maximum CGPA', 0.0, 10.0, 10.0)

        # Checkbox group for gender
        genders = st.multiselect('Genders', ['Male', 'Female', 'Both'], default='Both')

        # Checkbox group for UG specialization
        ug_specializations = st.multiselect('UG Specialization', ['All', 'CSE (Cyber Security)', 'CSE (Artificial Intelligence & Machine Learning)', 'CSE (Internet of Things & Cybersecurity including Blockchain Technology)', 'CSE (Data Science)'], default='All')

        # Dropdown for sections
        sections = st.selectbox('Sections', ['All','A', 'B', 'C', 'D', 'E', 'F','G','H','I','J','M','N'])

        output_file = st.text_input('Output File Name', 'company_name.csv')

    # Display conclusion with bug reporting contact
        
        if st.button('Filter'):
            filtered_df = filter_data(min_10th, max_10th, min_12th, max_12th, min_diploma, max_diploma, min_cgpa, max_cgpa, genders, ug_specializations, sections)

            # Display results
            st.title('KARE TPO Automation - Filter Result')
            st.write('Filtering completed. Result saved to:', output_file)
            

            # Display filtered data with specific columns
            st.dataframe(filtered_df)

            # Allow users to download the filtered data
            st.markdown(download_link(filtered_df, output_file, 'Download Filtered Data'), unsafe_allow_html=True)

            # Calculate and display statistics
            st.title('Statistics')

            # 1. Total No of Students
            total_students = len(filtered_df)

            # 2. No of Girls and Boys
            gender_counts = filtered_df['Gender'].value_counts()
            num_girls = gender_counts.get('Female', 0)
            num_boys = gender_counts.get('Male', 0)

            # 3. Members from Each Section
            section_counts = filtered_df['UG-Section'].value_counts()

          
            stats_table = pd.DataFrame({
                'Statistic': ['Total Number of Students', 'Number of Girls', 'Number of Boys'] + [f'Number of Students in Section {section}' for section in section_counts.index],
                'Count': [total_students, num_girls, num_boys] + [section_counts.get(section, 0) for section in section_counts.index]
            })

            
            # Display the table
            st.table(stats_table)

            # Display conclusion with bug reporting contact
            st.subheader('Contact')
            st.write(
                """
                Thank you for using KARE TPO Automation. If you encounter any bugs or issues, please contact the admin at +88259 88659.
                Maintained by Totelligence Solutions.
                """
            )

if __name__ == '__main__':
    main()
