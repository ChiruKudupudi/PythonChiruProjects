import streamlit as st
import pandas as pd
import plotly.express as px

CORRECT_USER_ID = "Admin"
CORRECT_PASSWORD = "123"

# Page configuration should be set before any Streamlit elements are created
st.set_page_config(
    page_title="Operations",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

@st.cache_data
def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"The file '{file_path}' was not found.")
        return pd.DataFrame()

@st.cache_data
def merge_dataframes(df1, df2):
    if not df2.empty:
        return pd.merge(df1, df2, left_on='UserId', right_on='Userid', how='left')
    return df1

@st.cache_data
def process_data(df):
    df['Date'] = pd.to_datetime(df['CreationDate']).dt.date
    summary_df = df.groupby(['Fullname', 'UserId', 'Date', 'Operation']).size().reset_index(name='Count of Operations')
    final_summary_df = summary_df.groupby('Fullname').agg({
        'UserId': 'first',
        'Date': 'first',
        'Operation': 'first',
        'Count of Operations': 'sum'
    }).reset_index()
    return final_summary_df

def display_report1():
    # Load the primary CSV file
    try:
        df = pd.read_csv("inputfile.csv")
    except FileNotFoundError:
        st.error("The file 'inputfile.csv' was not found.")
        return

    # Load the secondary CSV file
    try:
        df1 = pd.read_csv("inputfile1.csv")
    except FileNotFoundError:
        st.warning("The file 'inputfile1.csv' was not found. Proceeding with only 'inputfile.csv'.")
        df1 = pd.DataFrame()  # Empty DataFrame if the file is not found

    # Check if the necessary columns exist
    if 'UserId' not in df.columns:
        st.error("The column 'UserId' is missing from 'inputfile.csv'.")
        return
    if not df1.empty and 'Userid' not in df1.columns:
        st.error("The column 'Userid' is missing from 'inputfile1.csv'.")
        return

    # Perform a left join if the secondary DataFrame is not empty
    if not df1.empty:
        df_merged = pd.merge(df, df1, left_on='UserId', right_on='Userid', how='left')
    else:
        df_merged = df

    df_merged['Date'] = pd.to_datetime(df_merged['CreationDate']).dt.date

    # Sidebar filters for Operation and CreationDate
    st.sidebar.header("Filters")
    selected_operation = st.sidebar.multiselect("Select Operation(s)", df_merged["Operation"].unique())
    selected_dates = st.sidebar.multiselect("Select Date(s)", df_merged["CreationDate"].unique())

    # Apply filters to create filtered DataFrame
    if selected_operation:
        df_merged = df_merged[df_merged['Operation'].isin(selected_operation)]
    if selected_dates:
        df_merged = df_merged[df_merged['CreationDate'].isin(selected_dates)]

    st.write(df_merged)

    # Group by UserId, Date, and Operation to count occurrences
    summary_df = df_merged.groupby(['Fullname', 'UserId', 'Date', 'Operation']).size().reset_index(name='Count of Operations')

    final_summary_df = summary_df.groupby('Fullname').agg({
        'UserId': 'first',
        'Date': 'first',
        'Operation': 'first',
        'Count of Operations': 'sum'
    }).reset_index()

    st.subheader("Operation Count by UserId, Date, and Operation")
    st.table(final_summary_df[['Fullname', 'UserId', 'Date', 'Operation', 'Count of Operations']])

    # Group by Date to count occurrences of Operation
    count_by_date = df_merged.groupby('Date').size().reset_index(name='Count of Operations')

    # Plotting bar chart for Count of Operations by CreationDate
    st.subheader("Count of Operations by Creation Date")
    fig_bar = px.bar(count_by_date, x='Date', y='Count of Operations', text='Count of Operations', template='seaborn', title='Count of Operations by Creation Date')
    fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_bar.update_layout(xaxis_title='Creation Date', yaxis_title='Count of Operations')
    st.plotly_chart(fig_bar, use_container_width=True)

    # Group by Operation to sum RecordType
    record_type_summary = df_merged.groupby('Operation')['RecordType'].sum().reset_index()

    # Plotting pie chart for Sum of RecordType by Operation
    st.subheader("Sum of RecordType by Operation")
    fig_pie = px.pie(record_type_summary, values='RecordType', names='Operation', title='Sum of RecordType by Operation', hole=0.5)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)



def display_report2():
    st.title("Report2")
    
    df = load_csv("inputfile.csv")
    df1 = load_csv("inputfile1.csv")

    if 'UserId' not in df.columns:
        st.error("The column 'UserId' is missing from 'inputfile.csv'.")
        return
    if not df1.empty and 'Userid' not in df1.columns:
        st.error("The column 'Userid' is missing from 'inputfile1.csv'.")
        return

    df_merged = merge_dataframes(df, df1)

    if 'Fullname' not in df_merged.columns:
        st.error("The column 'Fullname' is missing from the merged DataFrame.")
        return

    selected_full_names = st.sidebar.multiselect("Select Full Name(s)", df_merged["Fullname"].unique())

    if selected_full_names:
        df_filtered = df_merged[df_merged['Fullname'].isin(selected_full_names)]
    else:
        df_filtered = df_merged

    if not df_filtered.empty:
        count_by_full_name = df_filtered.groupby('Fullname').size().reset_index(name='Count of Operations')

        fig_bar_full_name = px.bar(count_by_full_name, x='Fullname', y='Count of Operations', text='Count of Operations', template='seaborn', title='Count of Operations by Full Name')
        fig_bar_full_name.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig_bar_full_name.update_layout(xaxis_title='Fullname', yaxis_title='Count of Operations')
        st.plotly_chart(fig_bar_full_name, use_container_width=True)

def display_report3():
    st.title("Report3")

    df1 = load_csv("inputfile1.csv")

    if 'Dept' not in df1.columns:
        st.error("The column 'Dept' is missing from 'inputfile1.csv'.")
        return

    count_by_dept = df1['Dept'].value_counts().reset_index()
    count_by_dept.columns = ['Dept', 'Count']

    fig_line = px.line(count_by_dept, x='Dept', y='Count', title='Count of Dept', markers=True)
    fig_line.update_layout(xaxis_title='Dept', yaxis_title='Count')
    st.plotly_chart(fig_line, use_container_width=True)

# Initialize page state
if "loggedin" not in st.session_state:
    st.session_state.loggedin = False

# Check if logged_in query parameter is set to True
query_params = st.experimental_get_query_params()
if query_params.get('logged_in') == ['true']:
    st.session_state.loggedin = True

# Check if logged in and display content accordingly
if st.session_state.loggedin:
    st.sidebar.header("Navigation")

    is_page_report1 = query_params.get('page', ['report1'])[0] == 'report1'
    is_page_report2 = query_params.get('page', ['report1'])[0] == 'report2'
    is_page_report3 = query_params.get('page', ['report1'])[0] == 'report3'

    report1_button_css = '<style>div.stButton > button:first-child {background-color: #007bff;color:white;}</style>'
    report2_button_css = '<style>div.stButton > button:first-child {background-color: #007bff;color:white;}</style>'
    report3_button_css = '<style>div.stButton > button:first-child {background-color: #007bff;color:white;}</style>'

    if is_page_report1:
        st.markdown(report1_button_css, unsafe_allow_html=True)
    elif is_page_report2:
        st.markdown(report2_button_css, unsafe_allow_html=True)
    elif is_page_report3:
        st.markdown(report3_button_css, unsafe_allow_html=True)

    report1_button = st.sidebar.button("Report1", key='report1_button', help="Go to Report1", on_click=lambda: st.experimental_set_query_params(logged_in=True, page="report1"))
    report2_button = st.sidebar.button("Report2", key='report2_button', help="Go to Report2", on_click=lambda: st.experimental_set_query_params(logged_in=True, page="report2"))
    report3_button = st.sidebar.button("Report3", key='report3_button', help="Go to Report3", on_click=lambda: st.experimental_set_query_params(logged_in=True, page="report3"))

    if is_page_report1:
        display_report1()
    elif is_page_report2:
        display_report2()
    elif is_page_report3:
        display_report3()

else:
    st.sidebar.header("Login")

    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    login_button = st.button("Login")

    if login_button:
        if user_id == CORRECT_USER_ID and password == CORRECT_PASSWORD:
            st.success("Logged in successfully!")
            st.session_state.loggedin = True
            st.experimental_set_query_params(logged_in=True)
            st.experimental_rerun()
        else:
            st.error("Incorrect User ID or Password. Please try again.")
