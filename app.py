import streamlit as st
import pandas as pd
#import numpy as np
import joblib
#import plotly.express as px

model= joblib.load('rd_clf.model')
# Load the model
# with open('rd_clf.model', 'rb') as f:
#     model = joblib.load(f)
    
data = []

headers = ['lead_time', 'previous_cancellations', 'booking_changes', 'required_car_parking_spaces', 'total_of_special_requests',
                'hotel', 'market_segment', 'deposit_type', 'agent', 'customer_type']
    
hotels = ['City Hotel', 'Resort Hotel']
market_segments = ['Offline TA/TO', 'Corporate', 'Direct', 'Online TA', 'Groups', 'Aviation', 'Complementary', 'Undefined']
deposit_types = ['Non Refund', 'No Deposit', 'Refundable']
agents = ['Yes', 'No']
customer_types = ['Transient', 'Transient-Party', 'Group', 'Contract']


# Page configurations
st.set_page_config(
    page_title="Hotel Booking Cancellation App",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Create a function for each page
def home_page():
    st.title("Home Page")
    st.write("Welcome to the Home Page")
    
    # Display the dataframe
    st.subheader("Prediction Preview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        hotel = st.radio("Hotel:", options=hotels)
        agent= st.radio("Agents:", options=agents)
        deposit_type= st.radio("Deposit Type:", options=deposit_types)
    with col2:
        
        market_segment= st.selectbox("Market Segments:", options=market_segments)
        customer_type = st.selectbox("Customer Type:", options=customer_types)
        required_car_parking_spaces = st.number_input("Required Car Parking Spaces:", min_value=0, max_value=100, value=1, step=1)
    with col3:
        previous_cancelations = st.number_input("Previous Cancelations:", min_value=0, max_value=100, value=1, step=1)
        booking_changes = st.number_input("Booking Changes:", min_value=0, max_value=100, value=1, step=1)
        
        total_of_special_requests = st.number_input("Total of Special Requests:", min_value=0, max_value=100, value=1, step=1)
    lead_time = st.slider("Lead Time:", min_value=0, max_value=100, value=35, step=1)

    # Store inputs in a dictionary and append it to the data list
    if st.button("Check Cancellation"):
        
        new_entry = {
            "hotel": hotel,
            "lead_time":lead_time, 
            "market_segment":market_segment,
            "previous_cancellations": previous_cancelations, 
            "booking_changes":booking_changes, 
            "deposit_type": deposit_type,
            "agent": agent,
            "customer_type": customer_type,
            "required_car_parking_spaces": required_car_parking_spaces,
            "total_of_special_requests": total_of_special_requests
            }
        
        data.append(new_entry)
        
        # st.success("Input recorded successfully!")

    if data:
        df_test1 = pd.DataFrame(data)

        
        df_test1['hotel'] = df_test1['hotel'].map({'Resort Hotel' : 0, 'City Hotel' : 1})
        df_test1['market_segment'] = df_test1['market_segment'].map({'Direct': 0, 'Corporate': 1, 'Online TA': 2, 'Offline TA/TO': 3,
                                                                'Complementary': 4, 'Groups': 5, 'Undefined': 6, 'Aviation': 7})
        df_test1['agent'] = df_test1['agent'].map({'Yes' : 0, 'No' : 1})
        df_test1['deposit_type'] = df_test1['deposit_type'].map({'No Deposit': 0, 'Refundable': 1, 'Non Refund': 2})
        df_test1['customer_type'] = df_test1['customer_type'].map({'Transient': 0, 'Contract': 1, 'Transient-Party': 2, 'Group': 3})


        df_test1 = df_test1[headers]
        df_pred2 = model.predict(df_test1)

        if df_pred2 == 1:
            st.success("This booking will be confirmed!", icon="✅")
        else:
            st.error("This booking will be cancelled!", icon="🚨")
    
def search_page():
    st.title("Single Search")
    st.write("This app demonstrates dynamic multi-page navigation using Streamlit.")
    
    df_test = pd.read_csv('hotel_bookings2.csv')
    df_test1 = df_test
      
    df_test1['hotel'] = df_test1['hotel'].map({'Resort Hotel' : 0, 'City Hotel' : 1})
    df_test1['market_segment'] = df_test1['market_segment'].map({'Direct': 0, 'Corporate': 1, 'Online TA': 2, 'Offline TA/TO': 3,
                                                            'Complementary': 4, 'Groups': 5, 'Undefined': 6, 'Aviation': 7})
    df_test1['agent'] = df_test1['agent'].map({'Yes' : 0, 'No' : 1})
    df_test1['deposit_type'] = df_test1['deposit_type'].map({'No Deposit': 0, 'Refundable': 1, 'Non Refund': 2})
    df_test1['customer_type'] = df_test1['customer_type'].map({'Transient': 0, 'Contract': 1, 'Transient-Party': 2, 'Group': 3})


    df_test1 = df_test1[headers]
    df_pred = model.predict(df_test1)  
    
    df_pred1 = pd.DataFrame()
    df_pred1['Predicted'] = df_pred.data.tolist()
    df_real = df_test
    df_final = pd.concat([df_pred1, df_real], axis = 1)
    df_final
    

def customer_page():
    st.title("Customer Search")
    st.title("Search Registration Number and Cancellation")

    df = pd.read_csv('hotel_bookings2.csv')

    # Display the DataFrame
    st.subheader("Data Table")
    st.write(df)

    # Input for searching the registration number
    search_reg = st.number_input("Enter index Number to Search", placeholder="e.g., 15", step=1, format="%d")

    # Perform the search
    if search_reg:
        # Check if the registration number exists in the DataFrame
        search_result = df[df["indexNo"] == search_reg]

        # If the registration number is found, display the row
        if not search_result.empty:
            st.success(f"Record found for index Number: {search_reg}")
            st.write(search_result)

            # Export the row as a new DataFrame
            df_test1 = search_result.reset_index(drop=True)  # Reset index for the new DataFrame

            df_test1['hotel'] = df_test1['hotel'].map({'Resort Hotel' : 0, 'City Hotel' : 1})
            df_test1['market_segment'] = df_test1['market_segment'].map({'Direct': 0, 'Corporate': 1, 'Online TA': 2, 'Offline TA/TO': 3,
                                                                    'Complementary': 4, 'Groups': 5, 'Undefined': 6, 'Aviation': 7})
            df_test1['agent'] = df_test1['agent'].map({'Yes' : 0, 'No' : 1})
            df_test1['deposit_type'] = df_test1['deposit_type'].map({'No Deposit': 0, 'Refundable': 1, 'Non Refund': 2})
            df_test1['customer_type'] = df_test1['customer_type'].map({'Transient': 0, 'Contract': 1, 'Transient-Party': 2, 'Group': 3})


            df_test1 = df_test1[headers]
            df_pred2 = model.predict(df_test1)

            if df_pred2 == 1:
                st.success("This booking will be confirmed!", icon="✅")
            else:
                st.error("This booking will be cancelled!", icon="🚨")

        else:
            st.error(f"Index Number {search_reg} not found in the table.")  

def dashboard_page():
    st.title("Dashboard Page")
    st.write("Here you can visualize data and see various insights.")

# Define a dictionary to map page names to functions
PAGES = {
    "Home": home_page,
    "Search": search_page,
    "Customer": customer_page,
    "Dashboard": dashboard_page,
}


# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page:", list(PAGES.keys()))

# Display the selected page
PAGES[page]()

# Footer
st.write("© 2024 Untangle BI | Gateway ICT")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 





# Footer
st.write("© 2024 Dynamic Machine Learning App")
