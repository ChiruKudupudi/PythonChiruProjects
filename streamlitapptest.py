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
def display_main_content(df_merged):
    st.subheader("Operation Count by UserId, Date, and Operation")

    # Sidebar filters for Operation and CreationDate
    st.sidebar.header("Filters")
    selected_operation = st.sidebar.multiselect("Select Operation(s)", df_merged["Operation"].unique())
    selected_dates = st.sidebar.multiselect("Select Date(s)", df_merged["CreationDate"].unique())

    # Apply filters to create filtered DataFrame
    if selected_operation:
        df_filtered = df_merged[df_merged['Operation'].isin(selected_operation)]
    else:
        df_filtered = df_merged.copy()
    if selected_dates:
        df_filtered = df_filtered[df_filtered['CreationDate'].isin(selected_dates)]

    # Group by UserId, Date, and Operation to count occurrences
    summary_df = df_filtered.groupby(['Fullname', 'UserId', 'CreationDate', 'Operation']).size().reset_index(name='Count of Operations')

    final_summary_df = summary_df.groupby('Fullname').agg({
        'UserId': 'first',
        'CreationDate': 'first',
        'Operation': 'first',
        'Count of Operations': 'sum'
    }).reset_index()

    st.table(final_summary_df[['Fullname', 'UserId', 'CreationDate', 'Operation', 'Count of Operations']])

    # Group by Date to count occurrences of Operation
    count_by_date = df_filtered.groupby('CreationDate').size().reset_index(name='Count of Operations')

    # Plotting bar chart for Count of Operations by CreationDate
    st.subheader("Count of Operations by Creation Date")
    fig_bar = px.bar(count_by_date, x='CreationDate', y='Count of Operations', text='Count of Operations',
                     template='seaborn', title='Count of Operations by Creation Date')
    fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig_bar.update_layout(xaxis_title='Creation Date', yaxis_title='Count of Operations')
    st.plotly_chart(fig_bar, use_container_width=True)

    # Group by Operation to sum RecordType
    record_type_summary = df_filtered.groupby('Operation')['RecordType'].sum().reset_index()

    # Plotting pie chart for Sum of RecordType by Operation
    st.subheader("Sum of RecordType by Operation")
    fig_pie = px.pie(record_type_summary, values='RecordType', names='Operation',
                     title='Sum of RecordType by Operation', hole=0.5)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

# Function to display another page content
def display_another_page(df_merged):
    st.title("Page 2")

    # Sidebar filter for Full Name
    st.sidebar.header("Filters")
    selected_full_names = st.sidebar.multiselect("Select Full Name(s)", df_merged["Fullname"].unique())

    # Apply Full Name filter to the DataFrame
    if selected_full_names:
        df_filtered = df_merged[df_merged['Fullname'].isin(selected_full_names)]
    else:
        df_filtered = df_merged.copy()

    # Group by Full Name to count occurrences of Operation
    count_by_full_name = df_filtered.groupby('Fullname').size().reset_index(name='Count of Operations')

    # Plotting bar chart for Count of Operations by Full Name
    st.subheader("Count of Operations by Full Name")
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

# CSS style for sidebar buttons
st.markdown(
    """
    <style>
    .sidebar-content .block-container.stButton-pressed > button {
        background-color: blue !important;
        color: white !important;
    }
    .sidebar-content .block-container a:hover,
    .sidebar-content .block-container button:hover {
        background-color: darkblue !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Run the app
if st.session_state.loggedin:
    # Navigation links in the sidebar
    st.sidebar.header("Navigation")

    # Handle navigation buttons
    if st.sidebar.button("Page 1"):
        st.experimental_set_query_params(logged_in=True, page="main")
        st.experimental_rerun()
    if st.sidebar.button("Page 2"):
        st.experimental_set_query_params(logged_in=True, page="another")
        st.experimental_rerun()

    # Load the primary CSV file
    try:
        df = pd.read_csv("inputfile.csv")
    except FileNotFoundError:
        st.error("The file 'inputfile.csv' was not found.")
        st.stop()

    # Load the secondary CSV file
    try:
        df1 = pd.read_csv("inputfile1.csv")
    except FileNotFoundError:
        st.warning("The file 'inputfile1.csv' was not found. Proceeding with only 'inputfile.csv'.")
        df1 = pd.DataFrame()  # Empty DataFrame if the file is not found

    # Check if the necessary columns exist
    if 'UserId' not in df.columns:
        st.error("The column 'UserId' is missing from 'inputfile.csv'.")
        st.stop()
    if not df1.empty and 'Userid' not in df1.columns:
        st.error("The column 'Userid' is missing from 'inputfile1.csv'.")
        st.stop()

    # Perform a left join if the secondary DataFrame is not empty
    if not df1.empty:
        df_merged = pd.merge(df, df1, left_on='UserId', right_on='Userid', how='left')
    else:
        df_merged = df

    if 'Fullname' not in df_merged.columns:
        st.error("The column 'Fullname' is missing from the merged DataFrame.")
        st.stop()

    if query_params.get('page', ['main'])[0] == 'main':
        display_main_content(df_merged)
    elif query_params.get('page', ['main'])[0] == 'another':
        display_another_page(df_merged)
else:
    st.sidebar.header("Login")

    # Create input fields for User ID and Password
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")

    # Add a login button
    login_button = st.button("Login")

    # Check credentials upon login button press
    if login_button:
        if user_id == CORRECT_USER_ID and password == CORRECT_PASSWORD:
            st.success("Logged in successfully!")
            st.session_state.loggedin = True
            # Redirect to another page after successful login
            st.experimental_set_query_params(logged_in=True)  # Set query params to indicate logged in
            st.experimental_rerun()  # Rerun the script to reflect the new state
        else:
            st.error("Incorrect User ID or Password. Please try again.")
