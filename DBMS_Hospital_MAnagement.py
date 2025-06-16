import streamlit as st
import mysql.connector
from streamlit_option_menu import option_menu
import pandas as pd
import time
import numpy as np
from streamlit_extras.stylable_container import stylable_container
conn = mysql.connector.connect(
        host='localhost',        
        user='root',            
       password='@Pradeep007', 
       auth_plugin='mysql_native_password', 
        database='clinic'         
    )
db=conn.cursor()




# Set the sidebar to be collapsed initially

def main_page():
    st.title("Welcome to DOOM's Clinic")
    background_image = """
    <style>
.stApp {
    background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZI5wBS34W777lOIuCpil5af14EIJoGlghQQ&s");
    background-size: cover;  /* Cover the entire app */
    background-position: center;  /* Center the image */
    /* Do not repeat the image */
}
</style>

    """

# Display the background image
    st.markdown(background_image, unsafe_allow_html=True)
    
    st.image("doom.jpg",caption="Doctor Doom",width=450)
    
    st.markdown("<h3 style='text-align: center;'><b>Doctor Doom</b></h3>", unsafe_allow_html=True)

# Function to display the doctor page
def doctor():
    st.title("Welcome Doctor")
    user_in = st.text_input("Enter your ID:",key="name_input1")
    with stylable_container(
        key = "doctor",
        css_styles="""
    button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: white;
        background-color: #4681f4 ; 
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: transform 0.2s; 
        width : 150px; 
    }
    button:hover{
        transform: scale(1.1); 
    }
    """,
      ):
        if st.button("Submit"):
            query=f"SELECT *FROM  doctors1"
            db.execute(query)
            try:
                df = pd.read_sql(query, conn)
                st.table(df)
            except Exception as e:
                st.error("Id not found")
            finally:
                conn.close()
                
def insertdata(user_in, user_age,user_gender,user_BP,user_reason,user_phone_number):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mytable (name, age) VALUES (%s, %s,%s,%s,%s,%s)", (user_in, user_age,user_gender,user_BP,user_reason,user_phone_number))
    db.commit()
    cursor.close()
    conn.close()
#def displaydoctor():
    # Initialize connection.
    #query="SELECT *FROM doctors1"


# Perform query.
    #conn=create_connection()

    #df=pd.read_sql(query,conn)

# Print results.
    #for row in df.itertuples():
        #st.write(f"{row.name} has a :{row.age}:")


def display():
    st.write("Displaying Doctor Details")
    query="SELECT *FROM doctors1"
    df=pd.read_sql(query,conn)
    conn.close()
    st.dataframe(df)
def Old_patient(name,age):
    query = f"""
    SELECT * 
    FROM patient
    WHERE name = '{name}' AND age = {age};
    """
    df=pd.read_sql(query,conn)

# Print results.
    st.table(df)
    conn.close()

def patient():
    with stylable_container(
        key = "Patient",
        css_styles="""
    button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: white;
        background-color: #4681f4 ; 
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: transform 0.2s; 
        width : 150px; 
    }
    button:hover{
        transform: scale(1.1); 
    }
    """,
      ):
        st.text("Click 'New' for new patient registration:")
        if st.button("New"):
            st.session_state.current_page = "New_patient"  

        st.text("Click here for seeing existing patients:")
        if st.button("Old"):
            st.session_state.current_page = "Old_patient" 

# Function for new patient registration page
def New_patient():
    with stylable_container(
        key = "patient_New",
        css_styles="""
    button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: white;
        background-color: #4681f4 ; 
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: transform 0.2s; 
        width : 150px; 
    }
    button:hover{
        transform: scale(1.1); 
    }
    """,
      ):
        user_in1 = st.text_input("Name:",key="name_input2")
        user_age1 = st.text_input("Age:",key="age_input1")
        user_gender = st.text_input("Gender:",key="gender_input1")
        user_BP = st.text_input("Blood Pressure:",key="BP_input1")
        user_reason = st.text_input("Reason:",key="reason_input1")
        user_phone_number = st.text_input("Phone Number:",key="ph_no_input1")
        submit_button = st.button(label='Submit',key="submit_button")
        token = 1
        if submit_button:
        
            #b = duplicate(user_in1,user_age1)
            b=True
            if b == True:
                insertdata(user_in1, user_age1,user_gender,user_BP,user_reason,user_phone_number)
                st.success(f"Your token number is {token} Please wait in the waiting room")
                token=token+1
            else:
                st.write("Patient already registered...")
                st.success(f"your token number is {token} Please wait in waiting room")
                token=token+1
                Old_patient(user_in1,user_age1)


def addinven():
    with stylable_container(
        key = "ADDinventory",
        css_styles="""
    button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: white;
        background-color: #4681f4 ; 
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: transform 0.2s; 
        width : 150px; 
    }
    button:hover{
        transform: scale(1.1); 
    }
    """,
      ):
        item_name = st.text_input("Item Name:")
        item_id = st.text_input("Item id:")
        quantity = st.number_input("Quantity on Hand:", min_value=0)
        min_stock = st.number_input("Minimum Stock Level:", min_value=0)

        if st.button("Submit"):
            insert_item(item_id,item_name,  quantity, min_stock)
            st.success("Item added successfully!")
def display_inven():
    query = "SELECT * FROM inventory"
    
    try:
        df = pd.read_sql(query, conn)
        st.dataframe(df)
        query = "SELECT item_name, quantity, min_stock FROM inventory"
        conn.execute(query)

        items = conn.fetchall()

        alert_messages = []
    
        for item in items:
            item_name, net_quantity, min_quantity = item
        
        if net_quantity <= min_quantity:
            alert_messages.append(f"Alert: {item_name} has a net quantity of {net_quantity}, which is below the minimum quantity of {min_quantity}.")

        conn.close()

        if alert_messages:
            for message in alert_messages:
                st.warning(message,icon="⚠️")
        else:
            st.success("All items are above their minimum quantities.")
    except Exception as e:
        st.error(f"Error fetching inventory data: {e}")
    finally:
        conn.close()
    

def update_inventory():
    item_name = st.text("Enter the Name of the item:")
    new_quantity = st.number_input("Enter new quantity:")
    with stylable_container(
        key = "inventory",
        css_styles="""
    button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: white;
        background-color: #4681f4 ; 
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: transform 0.3s; 
        width : 150px; 
    }
    button:hover{
        transform: scale(1.1); 
    }
    """,
      ):
        if(st.button("Submit")):
            query = f"UPDATE inventory SET quantity = {new_quantity} WHERE item_name = '{item_name}'"
            db.execute(query)
            db.commit()

            st.success('Item Quantity Updated')

def inventory():
    st.title("Clinic Inventory Management")
    with stylable_container(
        key = "inventory",
        css_styles="""
    button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: white;
        background-color: #4681f4 ; 
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: transform 0.3s;
        width : 150px; 
    }
    button:hover{
        transform: scale(1.1); 
    }
    """,
      ):
        st.text("Click 'Add' for add new items :")
        if st.button("New"):
            st.session_state.current_page = "Add_inventory"  
        st.text("Click here for Updating existing items:")
        if st.button("Update"):
            st.session_state.current_page = "Update_inventory"

        st.text("Click here for seeing existing items:")
        if st.button("show"):
            st.session_state.current_page = "Display_inventory"
    
            

    

def insert_item(item_id, name, quantity, min_stock):
    
    db.execute("""
        INSERT INTO inventory (inventory_id,item_name, quantity, min_stock)
        VALUES (%s, %s, %s, %s)
    """, (item_id, name, quantity, min_stock))
    db.commit()
    db.close()
    conn.close()

with st.sidebar:
    selected = option_menu(
        menu_title="Main menu",
        options=["Home", "Doctor", "Patient","Inventory"],
        icons=["house", "book", "envelope","book"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#C0C0C0"},  # Light red background
            "icon": {"font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px", "color": "#f4f7f9"},  # Red text
            "nav-link-selected": {"background-color": "#FF7F50"},  # Selected item background color
        }
    )

    # Update session state based on selection
    if selected:
        st.session_state.current_page = selected
    


    
sidebar_image = """
<div style="text-align: center;">
    <img src="data:image/png;base64,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" width="150"/>
</div>
"""

st.sidebar.markdown(sidebar_image, unsafe_allow_html=True)


pages = {
    "Home": main_page,
    "New_patient": New_patient,
    "Old_patient": Old_patient,
    "Inventory": inventory,
    "Doctor": doctor,
    "Patient": patient,
    "Add_inventory":addinven,
    "Display_inventory":display_inven,
    "Update_inventory":update_inventory
}
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if st.session_state.current_page in pages:
    pages[st.session_state.current_page]()







    