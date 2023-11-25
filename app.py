import streamlit as st
import pandas as pd
import base64

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

    return filtered_df[['S.No.', 'Registration', 'Name', 'DOB', 'UG-Section', 'UG-Department', 'UG-Specialization', 'Email']]

def download_link(df, filename, linktext):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # encode as bytes, then decode to get a string
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{linktext}</a>'
    return href

def main():
    st.title('KARE TPO Automation')

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

    output_file = st.text_input('Output File Name', 'comapany_name.csv')

    if st.button('Filter'):
        filtered_df = filter_data(min_10th, max_10th, min_12th, max_12th, min_diploma, max_diploma, min_cgpa, max_cgpa, genders, ug_specializations, sections)

        # Display results
        st.title('KARE TPO Automation - Filter Result')
        st.write('Filtering completed. Result saved to:', output_file)

        # Display filtered data with specific columns
        st.dataframe(filtered_df)

        # Allow users to download the filtered data
        st.markdown(download_link(filtered_df, output_file, 'Download Filtered Data'), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
