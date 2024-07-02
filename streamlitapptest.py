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

# Function to display the main content after login
def display_main_content():
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

    st.write(df_merged)

    df_merged['Date'] = pd.to_datetime(df_merged['CreationDate']).dt.date
    df1_copy = df_merged.copy()

    # Group by UserId, Date, and Operation to count occurrences
    summary_df = df1_copy.groupby(['Fullname','UserId', 'Date', 'Operation']).size().reset_index(name='Count of Operations')

    final_summary_df = summary_df.groupby('Fullname').agg({
        'UserId':'first',
        'Date': 'first',
        'Operation': 'first',
        'Count of Operations': 'sum'
    }).reset_index()

    st.subheader("Operation Count by UserId, Date, and Operation")
    st.table(final_summary_df[['Fullname','UserId', 'Date', 'Operation', 'Count of Operations']])

    # Sidebar filters for Operation and CreationDate
    st.sidebar.header("Filters")
    selected_operation = st.sidebar.multiselect("Select Operation(s)", df_merged["Operation"].unique())
    selected_dates = st.sidebar.multiselect("Select Date(s)", df_merged["CreationDate"].unique())

    # Apply filters to create filtered DataFrame
    if selected_operation:
        df_merged = df_merged[df_merged['Operation'].isin(selected_operation)]
    if selected_dates:
        df_merged = df_merged[df_merged['CreationDate'].isin(selected_dates)]

    # Group by Date to count occurrences of Operation
    count_by_date = df_merged.groupby('Date').size().reset_index(name='Count of Operations')

    # Plotting bar chart for Count of Operations by CreationDate
    st.subheader("Count of Operations by Creation Date")
    fig_bar = px.bar(count_by_date, x='Date', y='Count of Operations', text='Count of Operations',
                     template='seaborn', title='Count of Operations by Creation Date')
    fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_bar.update_layout(xaxis_title='Creation Date', yaxis_title='Count of Operations')
    st.plotly_chart(fig_bar, use_container_width=True)

    # Group by Operation to sum RecordType
    record_type_summary = df_merged.groupby('Operation')['RecordType'].sum().reset_index()

    # Plotting pie chart for Sum of RecordType by Operation
    st.subheader("Sum of RecordType by Operation")
    fig_pie = px.pie(record_type_summary, values='RecordType', names='Operation', 
                     title='Sum of RecordType by Operation', hole=0.5)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

# Function to display another page content
def display_another_page():
    st.title("Page 2")
    
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

    # Check if the 'Full Name' column exists
    if 'Fullname' not in df_merged.columns:
        st.error("The column 'Full Name' is missing from the merged DataFrame.")
        return

    # Sidebar filter for Full Name
    selected_full_names = st.sidebar.multiselect("Select Full Name(s)", df_merged["Fullname"].unique())

    # Apply Full Name filter to the DataFrame
    if selected_full_names:
        df_filtered = df_merged[df_merged['Fullname'].isin(selected_full_names)]
    else:
        df_filtered = df_merged

    # Group by Full Name to count occurrences of Operation
    count_by_full_name = df_filtered.groupby('Fullname').size().reset_index(name='Count of Operations')

    # Plotting bar chart for Count of Operations by Full Name
    fig_bar_full_name = px.bar(count_by_full_name, x='Fullname', y='Count of Operations', text='Count of Operations',
                               template='seaborn', title='Count of Operations by Full Name')
    fig_bar_full_name.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_bar_full_name.update_layout(xaxis_title='Fullname', yaxis_title='Count of Operations')
    st.plotly_chart(fig_bar_full_name, use_container_width=True)

# Initialize page state
if "loggedin" not in st.session_state:
    st.session_state.loggedin = False

# Check if logged_in query parameter is set to True
query_params = st.experimental_get_query_params()
if query_params.get('logged_in') == ['true']:
    st.session_state.loggedin = True

# Check if logged in and display content accordingly
if st.session_state.loggedin:
    # Navigation links in the sidebar
    st.sidebar.header("Navigation")

    # Determine which page is active based on query parameters
    is_page_main = query_params.get('page', ['main'])[0] == 'main'
    is_page_another = query_params.get('page', ['main'])[0] == 'another'

    # Highlight the active button based on the current page
    page1_button_css = '<style>div.stButton > button:first-child {background-color: #007bff;color:white;}</style>'
    page2_button_css = '<style>div.stButton > button:first-child {background-color: #007bff;color:white;}</style>'

    if is_page_main:
        st.markdown(page1_button_css, unsafe_allow_html=True)
        page1_button = st.sidebar.button("Page 1", key='page1_button', help="Go to Page 1", on_click=lambda: st.experimental_set_query_params(logged_in=True, page="main"))
        page2_button = st.sidebar.button("Page 2", key='page2_button', help="Go to Page 2", on_click=lambda: st.experimental_set_query_params(logged_in=True, page="another"))
    elif is_page_another:
        st.markdown(page2_button_css, unsafe_allow_html=True)
        page1_button = st.sidebar.button("Page 1", key='page1_button', help="Go to Page 1", on_click=lambda: st.experimental_set_query_params(logged_in=True, page="main"))
        page2_button = st.sidebar.button("Page 2", key='page2_button', help="Go to Page 2", on_click=lambda: st.experimental_set_query_params(logged_in=True, page="another"))

    if is_page_main:
        display
