import streamlit as st
import pandas as pd
import base64

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

def check_column_existence(df, column):
    return column in df.columns

def filter_data(min_10th, max_10th, min_12th, max_12th, min_diploma, max_diploma, min_cgpa, max_cgpa, genders, ug_specializations, departments, sections, uploaded_file, selected_columns):
    # Load user-uploaded dataset
    master = pd.read_csv(uploaded_file)

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

    if 'All' in departments:
        department_condition = master['UG-Department'].notna()
    else:
        department_condition = master['UG-Department'].isin(departments)

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
        & department_condition  # Filtering based on UG Department
        & section_condition
    ]

    # Select only the columns chosen by the user
    filtered_df = filtered_df[selected_columns]

    return filtered_df

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

        # Upload file through Streamlit
        uploaded_file = st.file_uploader("Upload the Master Data ", type=["csv"])

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
        ug_specializations = st.multiselect('UG Specialization', ['All', 'Cyber', 'AIML', 'IOT', 'Data Science'], default='All')

        # Dropdown for UG department
        departments = st.multiselect('UG Department', ['All', 'CSE', 'ECE', 'MECH'], default='All')

        # Dropdown for sections
        sections = st.selectbox('Sections', ['All', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'M', 'N'])

        # Checkbox group for selecting columns in the output CSV file
        # Default columns
        default_columns = ['S.No.', 'Registration', 'Name', 'DOB', 'UG-Section', 'UG-Department', 'UG-Specialization', 'Email', 'Gender']

        # Additional columns
        additional_columns = ['First Name', 'Last Name', 'CGPA', 'Active Backlogs', 'History Arrears', 'Academic Gap',
                           'Diploma-Percentage', 'Diploma-Specialization', '12-Percentage',
                            '10th-Percentage',
                            'Aadhar', 'PAN', 'City', 'City Pincode', 'District', 'State',
                           'Mobile-1']

        # Checkbox group for selecting columns
        selected_columns = st.multiselect('Select Columns for CSV Output', default_columns + additional_columns, default=default_columns)
        output_file = st.text_input('Output File Name', 'company_name.csv')

        # Display conclusion with bug reporting contact
        if st.button('Filter'):
            if uploaded_file is not None:
                filtered_df = filter_data(min_10th, max_10th, min_12th, max_12th, min_diploma, max_diploma, min_cgpa, max_cgpa, genders, ug_specializations, departments, sections, uploaded_file, selected_columns)

                # Display results
                st.title('KARE TPO Automation - Filter Result')
                st.write('Filtering completed. Result saved to:', output_file)

                # Display filtered data without commas and with row numbers
                filtered_df_without_commas = filtered_df.reset_index(drop=True)
                st.dataframe(filtered_df_without_commas.style.format("{:}"))

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

                # Display the general statistics table
                general_stats_table = pd.DataFrame({
                    'Statistic': ['Total Number of Students', 'Number of Girls', 'Number of Boys'],
                    'Count': [total_students, num_girls, num_boys]
                })

                # Display the general statistics table
                st.table(general_stats_table)

                # 3. Members from Each Section
                if check_column_existence(filtered_df, 'UG-Section'):
                    section_counts = filtered_df['UG-Section'].value_counts()

                    # Create a DataFrame for section-wise statistics
                    section_stats_table = pd.DataFrame({
                        'Section': section_counts.index,
                        'Number of Students': section_counts.values
                    })

                    # Add a new column for the percentage of students in each section
                    section_stats_table['Percentage'] = (section_stats_table['Number of Students'] / total_students) * 100

                    # Display the section-wise statistics table
                    st.subheader('Section-wise Statistics')
                    st.table(section_stats_table.style.format({'Number of Students': '{:}', 'Percentage': '{:.2f}%'}))
                else:
                    st.warning("Please Include 'UG-Section' in the columns to see more stats.")

                # 4. Members from Each UG Department
                if check_column_existence(filtered_df, 'UG-Department'):
                    department_counts = filtered_df['UG-Department'].value_counts()

                    # Create a DataFrame for department-wise statistics
                    department_stats_table = pd.DataFrame({
                        'Department': department_counts.index,
                        'Number of Students': department_counts.values
                    })

                    # Add a new column for the percentage of students in each department
                    department_stats_table['Percentage'] = (department_stats_table['Number of Students'] / total_students) * 100

                    # Display the department-wise statistics table
                    st.subheader('Department-wise Statistics')
                    st.table(department_stats_table.style.format({'Number of Students': '{:}', 'Percentage': '{:.2f}%'}))
                else:
                    st.warning("Please include 'UG-Specialization' in the columns to see more stats.")

                # 5. Members from Each UG Specialization
                if check_column_existence(filtered_df, 'UG-Specialization'):
                    ug_spec_counts = filtered_df['UG-Specialization'].value_counts()

                    # Create a DataFrame for UG specialization-wise statistics
                    ug_spec_stats_table = pd.DataFrame({
                        'UG Specialization': ug_spec_counts.index,
                        'Number of Students': ug_spec_counts.values
                    })

                    # Add a new column for the percentage of students in each UG specialization
                    ug_spec_stats_table['Percentage'] = (ug_spec_stats_table['Number of Students'] / total_students) * 100

                    # Display the UG specialization-wise statistics table
                    st.subheader('UG Specialization-wise Statistics')
                    st.table(ug_spec_stats_table.style.format({'Number of Students': '{:}', 'Percentage': '{:.2f}%'}))
                else:
                    st.warning("Please include 'UG-Specialization' in the columns to see more stats.")
                # 6. CGPA Distribution
                st.subheader('CGPA Distribution')
                st.write("Distribution of students based on CGPA")

                # 7. Top 3 Students from Each Section based on CGPA
                if check_column_existence(filtered_df, 'CGPA'):
                    st.subheader('Top 3 Students from Each Section based on CGPA')
                    top_students_cgpa = filtered_df.groupby('UG-Section').apply(lambda x: x.nlargest(3, 'CGPA')).reset_index(drop=True)
                    st.table(top_students_cgpa[['UG-Section', 'Name', 'CGPA']].style.format({'CGPA': '{:.2f}'}))
                else:
                    st.warning("Please include CGPA in the Column to see more Stats.")

            else:
                st.warning("Please upload a CSV file.")

            # Display conclusion with bug reporting contact
            st.subheader('Contact')
            st.write(
                """
                Thank you for using KARE TPO Automation. If you encounter any bugs or issues, please contact the admin at +91 88259 88659.
                Maintained by Totelligence Solutions.
                """
            )

if __name__ == '__main__':
    main()
