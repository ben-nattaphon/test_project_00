# Payment Page
def show_payment_page():
    st.markdown("<h1 style='text-align: center;'>Complete Your Purchase</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Get current design
        design = st.session_state.user_designs[-1] if st.session_state.user_designs else None
        
        if not design:
            st.error("No design found. Please generate a design first.")
            if st.button("Back to Design"):
                navigate_to('design_preferences')
            return
        
        st.markdown("<h2>Order Summary</h2>", unsafe_allow_html=True)
        
        # Display order summary
        st.markdown(f"""
        <div style='border: 1px solid #ced4da; border-radius: 4px; padding: 1rem; margin-bottom: 1rem;'>
            <p><strong>Design:</strong> {design['prompt']}</p>
            <p><strong>Furniture Items:</strong> {len(design['furniture_list'])}</p>
            <p><strong>Total Cost:</strong> ${design['total_price']:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h2>Payment Information</h2>", unsafe_allow_html=True)
        
        # Payment form fields
        card_number = st.text_input("Credit Card Number", placeholder="1234 5678 9012 3456")
        
        col1, col2 = st.columns(2)
        with col1:
            expiry = st.text_input("Expiry Date (MM/YY)", placeholder="MM/YY")
        with col2:
            cvv = st.text_input("CVV", type="password", placeholder="123")
        
        name = st.text_input("Cardholder Name", placeholder="John Smith")
        
        # Billing address
        st.markdown("<h3>Billing Address</h3>", unsafe_allow_html=True)
        address = st.text_area("Address", placeholder="Enter your billing address")
        
        col1, col2 = st.columns(2)
        with col1:
            city = st.text_input("City", placeholder="City")
        with col2:
            zip_code = st.text_input("ZIP Code", placeholder="12345")
        
        # Terms and conditions
        agree = st.checkbox("I agree to the Terms of Service and Privacy Policy")
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back to Design"):
                navigate_to('design_view')
        
        with col2:
            complete_purchase = st.button("Complete Purchase →")
        
        if complete_purchase:
            if agree:
                if card_number and expiry and cvv and name and address:
                    # In a real app, this would process the payment
                    st.success("Payment successful! Your design and furniture list have been purchased.")
                    st.markdown("""
                    <div style='background-color: #d1e7dd; color: #0f5132; padding: 1rem; border-radius: 4px; margin: 1rem 0;'>
                        <h3>What's Next?</h3>
                        <p>Our team will contact you shortly to arrange delivery and installation of your furniture.</p>
                        <p>You can track your order status in the 'My Orders' section.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Back to Home"):
                        navigate_to('my_designs')
                else:
                    st.error("Please fill in all required payment fields.")
            else:
                st.error("Please agree to the Terms of Service and Privacy Policy to proceed.")import streamlit as st
import pandas as pd
import json
import uuid
import datetime

# Set page config to match RoomLab theme
st.set_page_config(
    page_title="RoomLab",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to match RoomLab theme
st.markdown("""
<style>
    .main {
        background-color: #ffffff;
    }
    .stButton>button {
        background-color: #f8f9fa;
        color: #212529;
        border-radius: 4px;
        border: 1px solid #ced4da;
        padding: 0.375rem 0.75rem;
        font-size: 1rem;
    }
    .stButton>button:hover {
        border-color: #86b7fe;
        outline: 0;
        box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
    }
    .primary-btn>button {
        background-color: #0d6efd;
        color: white;
        border-color: #0d6efd;
    }
    .primary-btn>button:hover {
        background-color: #0b5ed7;
        border-color: #0a58ca;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 4px;
        border: 1px solid #ced4da;
        padding: 0.375rem 0.75rem;
    }
    h1, h2, h3 {
        font-weight: 500;
        color: #212529;
    }
    .success-alert {
        background-color: #d1e7dd;
        color: #0f5132;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    .info-alert {
        background-color: #cff4fc;
        color: #055160;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables if they don't exist
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'
if 'customer_info' not in st.session_state:
    st.session_state.customer_info = {}
if 'property_info' not in st.session_state:
    st.session_state.property_info = {}
if 'design_preferences' not in st.session_state:
    st.session_state.design_preferences = {}
if 'generated_designs' not in st.session_state:
    st.session_state.generated_designs = []
if 'token_count' not in st.session_state:
    st.session_state.token_count = 3  # Default token count for new users
if 'user_designs' not in st.session_state:
    st.session_state.user_designs = []

# Function to navigate between pages
def navigate_to(page):
    # Store previous page for back button functionality
    st.session_state.previous_page = st.session_state.current_page
    st.session_state.current_page = page
    
    # Clear any temporary data if returning to login
    if page == 'login':
        st.session_state.customer_info = {}
        st.session_state.property_info = {}
        st.session_state.design_preferences = {}

# Mock database functions
def mock_user_login(email_or_phone):
    # In a real app, this would check a database
    # For now, we'll just accept any input and create a mock user
    return {
        "customer_id": str(uuid.uuid4()),
        "name": "Demo User",
        "email": email_or_phone if '@' in email_or_phone else "",
        "phone": email_or_phone if '@' not in email_or_phone else "",
        "token_count": 3
    }

def mock_generate_design(property_info, preferences):
    # This would call an AI service in a real app
    design_id = str(uuid.uuid4())
    return {
        "design_id": design_id,
        "property_info": property_info,
        "preferences": preferences,
        "prompt": f"Generate a {preferences['style']} design for a {property_info['room_type']} in a {property_info['property_type']} for a {preferences['household']} with a budget of ${preferences['budget']}",
        "image_url": "/api/placeholder/600/400",  # Placeholder image
        "furniture_list": [
            {"name": "Modern Sofa", "price": 1200, "vendor": "ModernHome", "type": "Seating"},
            {"name": "Coffee Table", "price": 450, "vendor": "WoodCrafters", "type": "Table"},
            {"name": "Floor Lamp", "price": 250, "vendor": "LightingCo", "type": "Lighting"},
            {"name": "Area Rug", "price": 350, "vendor": "FloorDecor", "type": "Flooring"}
        ],
        "total_price": 2250,
        "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Login Page
def show_login_page():
    # Center the content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>RoomLab</h1>", unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            email_or_phone = st.text_input("Email address or phone number")
            
            col1, col2 = st.columns(2)
            with col1:
                submit_button = st.form_submit_button("Continue")
            with col2:
                signup_button = st.form_submit_button("Sign Up")
        
        if submit_button or signup_button:
            if email_or_phone:
                # In a real app, this would validate credentials
                # For now, we'll just proceed to the next page
                user_data = mock_user_login(email_or_phone)
                st.session_state.customer_info = user_data
                st.session_state.token_count = user_data["token_count"]
                navigate_to('property_setup')
            else:
                st.error("Please enter your email or phone number")
        
        st.markdown("<p style='text-align: center; margin: 1rem 0;'>OR</p>", unsafe_allow_html=True)
        
        # Social login buttons
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.button("Continue with Google", key="google_login")
            st.button("Continue with Facebook", key="fb_login")
            st.button("Continue with LINE", key="line_login")
        
        # Footer
        st.markdown("<div style='text-align: center; margin-top: 2rem; color: #6c757d; font-size: 0.8rem;'>RoomLab | Terms of Service | Privacy Policy</div>", unsafe_allow_html=True)

# Property Setup Page
def show_property_setup():
    st.markdown("<h1 style='text-align: center;'>Set Up Your Property</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Property Type Selection
        property_type = st.selectbox(
            "Property Type",
            ["Apartment", "House", "Condo", "Studio", "Office"]
        )
        
        # Floor number with increment/decrement buttons
        st.markdown("### Floor Number")
        floor_col1, floor_col2, floor_col3 = st.columns([1, 3, 1])
        with floor_col1:
            decrement_floor = st.button("-", key="dec_floor")
        with floor_col2:
            # Initialize floor number in session state if not exists
            if 'floor_number' not in st.session_state:
                st.session_state.floor_number = 1
            
            # Update floor number based on button clicks
            if decrement_floor and st.session_state.floor_number > 1:
                st.session_state.floor_number -= 1
            
            floor_number = st.number_input(
                "",
                min_value=1,
                max_value=100,
                value=st.session_state.floor_number,
                label_visibility="collapsed"
            )
            # Update session state when input changes directly
            st.session_state.floor_number = floor_number
        
        with floor_col3:
            increment_floor = st.button("+", key="inc_floor")
            if increment_floor and st.session_state.floor_number < 100:
                st.session_state.floor_number += 1
                st.experimental_rerun()
        
        # Room Type
        room_type = st.selectbox(
            "Room Type",
            ["Living Room", "Bedroom", "Kitchen", "Bathroom", "Dining Room", "Home Office"]
        )
        
        # Room Dimensions with increment/decrement buttons
        st.markdown("### Room Dimensions")
        
        # Initialize dimensions in session state if not exists
        if 'length' not in st.session_state:
            st.session_state.length = 4.0
        if 'width' not in st.session_state:
            st.session_state.width = 3.0
        if 'height' not in st.session_state:
            st.session_state.height = 2.4
        
        # Length control
        st.markdown("#### Length (m)")
        len_col1, len_col2, len_col3 = st.columns([1, 3, 1])
        with len_col1:
            dec_length = st.button("-", key="dec_length")
            if dec_length and st.session_state.length > 1.0:
                st.session_state.length = round(st.session_state.length - 0.1, 1)
                st.experimental_rerun()
        
        with len_col2:
            length = st.number_input(
                "",
                min_value=1.0,
                max_value=20.0,
                value=st.session_state.length,
                step=0.1,
                format="%.1f",
                label_visibility="collapsed"
            )
            st.session_state.length = length
        
        with len_col3:
            inc_length = st.button("+", key="inc_length")
            if inc_length and st.session_state.length < 20.0:
                st.session_state.length = round(st.session_state.length + 0.1, 1)
                st.experimental_rerun()
        
        # Width control
        st.markdown("#### Width (m)")
        width_col1, width_col2, width_col3 = st.columns([1, 3, 1])
        with width_col1:
            dec_width = st.button("-", key="dec_width")
            if dec_width and st.session_state.width > 1.0:
                st.session_state.width = round(st.session_state.width - 0.1, 1)
                st.experimental_rerun()
        
        with width_col2:
            width = st.number_input(
                "",
                min_value=1.0,
                max_value=20.0,
                value=st.session_state.width,
                step=0.1,
                format="%.1f",
                label_visibility="collapsed"
            )
            st.session_state.width = width
        
        with width_col3:
            inc_width = st.button("+", key="inc_width")
            if inc_width and st.session_state.width < 20.0:
                st.session_state.width = round(st.session_state.width + 0.1, 1)
                st.experimental_rerun()
        
        # Height control
        st.markdown("#### Height (m)")
        height_col1, height_col2, height_col3 = st.columns([1, 3, 1])
        with height_col1:
            dec_height = st.button("-", key="dec_height")
            if dec_height and st.session_state.height > 1.0:
                st.session_state.height = round(st.session_state.height - 0.1, 1)
                st.experimental_rerun()
        
        with height_col2:
            height = st.number_input(
                "",
                min_value=1.0,
                max_value=5.0,
                value=st.session_state.height,
                step=0.1,
                format="%.1f",
                label_visibility="collapsed"
            )
            st.session_state.height = height
        
        with height_col3:
            inc_height = st.button("+", key="inc_height")
            if inc_height and st.session_state.height < 5.0:
                st.session_state.height = round(st.session_state.height + 0.1, 1)
                st.experimental_rerun()
        
        # Calculate area
        area = st.session_state.length * st.session_state.width
        
        # Display total area
        st.markdown("#### Total Area (m²)")
        st.number_input(
            "",
            min_value=1.0,
            value=round(area, 1),
            disabled=True,
            format="%.1f",
            label_visibility="collapsed"
        )
        
        # Submit button
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("← Back", key="back_to_login"):
                navigate_to('login')
        with col2:
            if st.button("Continue to Preferences →", key="continue_to_preferences"):
                # Save property info to session state
                st.session_state.property_info = {
                    "property_type": property_type,
                    "floor_number": st.session_state.floor_number,
                    "room_type": room_type,
                    "length": st.session_state.length,
                    "width": st.session_state.width,
                    "height": st.session_state.height,
                    "area": area
                }
                # Navigate to preferences page
                navigate_to('design_preferences')


# Design Preferences Page
def show_design_preferences():
    st.markdown("<h1 style='text-align: center;'>Your Design Preferences</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Design Style
        style = st.selectbox(
            "Design Style",
            ["Modern", "Minimalist", "Scandinavian", "Industrial", "Traditional", "Contemporary", "Bohemian"]
        )
        
        # Household Type
        household = st.selectbox(
            "Household Type",
            ["Single", "Couple", "Family with Children", "Roommates", "Senior"]
        )
        
        # Budget slider
        st.markdown("### Budget ($)")
        
        # Initialize budget in session state if not exists
        if 'budget' not in st.session_state:
            st.session_state.budget = 50000
        
        # Budget slider with labeled min and max values
        budget = st.slider(
            "", 
            min_value=5000, 
            max_value=100000, 
            value=st.session_state.budget, 
            step=1000,
            format="$%d",
            label_visibility="collapsed"
        )
        
        # Update budget in session state
        st.session_state.budget = budget
        
        # Display min and max values
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<div style='text-align: left; color: #6c757d;'>$5,000</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div style='text-align: center;'>${st.session_state.budget:,}</div>", unsafe_allow_html=True)
        with col3:
            st.markdown("<div style='text-align: right; color: #6c757d;'>$100,000</div>", unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="back_to_property"):
                navigate_to('property_setup')
        
        with col2:
            generate_button = st.button("Generate Design", key="generate_design")
        
        st.markdown(f"<div style='text-align: center;'>Tokens remaining: {st.session_state.token_count}</div>", unsafe_allow_html=True)
    
    if generate_button:
        if st.session_state.token_count > 0:
            # Save preferences to session state
            st.session_state.design_preferences = {
                "style": style,
                "household": household,
                "budget": st.session_state.budget
            }
            
            # Generate design (in a real app, this would call an AI service)
            design = mock_generate_design(
                st.session_state.property_info,
                st.session_state.design_preferences
            )
            
            # Add the design to the user's designs
            st.session_state.user_designs.append(design)
            
            # Decrement token count
            st.session_state.token_count -= 1
            
            # Navigate to design view page
            navigate_to('design_view')
        else:
            # Show token purchase prompt
            st.error("You've used all your design tokens. Please purchase more to continue.")
            if st.button("Purchase Tokens"):
                navigate_to('token_purchase')

# Design View Page
def show_design_view():
    # Get the most recent design
    design = st.session_state.user_designs[-1] if st.session_state.user_designs else None
    
    if not design:
        st.error("No design found. Please generate a design first.")
        if st.button("Back to Preferences"):
            navigate_to('design_preferences')
        return
    
    st.markdown("<h1 style='text-align: center;'>Your Design</h1>", unsafe_allow_html=True)
    
    # Display the design prompt
    st.markdown("<div class='info-alert'>Design Prompt:</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='padding: 1rem; background-color: #f8f9fa; border-radius: 4px; margin-bottom: 1rem;'>{design['prompt']}</div>", unsafe_allow_html=True)
    
    # Show success message
    st.markdown("<div class='success-alert'>Design generated successfully!</div>", unsafe_allow_html=True)
    
    st.markdown("<h2>Modify Your Design</h2>", unsafe_allow_html=True)
    
    # Modification options
    col1, col2 = st.columns(2)
    with col1:
        st.button("Update Wallpaper")
        st.button("Update Colors")
    with col2:
        st.button("Update Flooring")
        st.button("Update Furniture")
    
    st.markdown("<h2>Purchase Options</h2>", unsafe_allow_html=True)
    
    # Purchase design button
    if st.button("Purchase Design"):
        navigate_to('payment_page')
    
    # Display furniture list
    st.markdown("<h2>Furniture List</h2>", unsafe_allow_html=True)
    
    # Create a DataFrame for the furniture
    furniture_df = pd.DataFrame(design['furniture_list'])
    
    # Add a "View BOQ" button
    if st.button("View Detailed BOQ"):
        navigate_to('boq_summary')
    
    # Display the furniture dataframe
    st.dataframe(furniture_df, use_container_width=True)
    
    # Display total price
    st.markdown(f"<h3>Total Estimated Cost: ${design['total_price']:,.2f}</h3>", unsafe_allow_html=True)
    
    # Navigation options
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Back to Preferences"):
            navigate_to('design_preferences')
    with col2:
        if st.button("Generate New Design") and st.session_state.token_count > 0:
            # Decrement token count and navigate to preferences
            navigate_to('design_preferences')
        elif st.session_state.token_count <= 0:
            st.error("No tokens left. Please purchase more.")
    with col3:
        if st.button("View My Designs"):
            navigate_to('my_designs')

# Token Purchase Page
def show_token_purchase():
    st.markdown("<h1 style='text-align: center;'>Purchase Tokens</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h2>Select a Token Package</h2>", unsafe_allow_html=True)
        
        # Token package options
        package1, package2, package3 = st.columns(3)
        
        with package1:
            st.markdown("""
            <div style='border: 1px solid #ced4da; border-radius: 4px; padding: 1rem; text-align: center;'>
                <h3>Basic</h3>
                <h2>5 Tokens</h2>
                <h3>$9.99</h3>
                <p>$1.99 per design</p>
            </div>
            """, unsafe_allow_html=True)
            basic_selected = st.button("Select Basic")
        
        with package2:
            st.markdown("""
            <div style='border: 1px solid #ced4da; border-radius: 4px; padding: 1rem; text-align: center; background-color: #f8f9fa;'>
                <h3>Standard</h3>
                <h2>10 Tokens</h2>
                <h3>$18.99</h3>
                <p>$1.89 per design</p>
                <p>Best Value</p>
            </div>
            """, unsafe_allow_html=True)
            standard_selected = st.button("Select Standard")
        
        with package3:
            st.markdown("""
            <div style='border: 1px solid #ced4da; border-radius: 4px; padding: 1rem; text-align: center;'>
                <h3>Premium</h3>
                <h2>20 Tokens</h2>
                <h3>$34.99</h3>
                <p>$1.75 per design</p>
            </div>
            """, unsafe_allow_html=True)
            premium_selected = st.button("Select Premium")
        
        # If any package is selected, show payment form
        if basic_selected or standard_selected or premium_selected:
            st.markdown("<h2>Payment Information</h2>", unsafe_allow_html=True)
            
            with st.form("payment_form"):
                card_number = st.text_input("Credit Card Number")
                
                col1, col2 = st.columns(2)
                with col1:
                    expiry = st.text_input("Expiry Date (MM/YY)")
                with col2:
                    cvv = st.text_input("CVV", type="password")
                
                name = st.text_input("Cardholder Name")
                
                submit_payment = st.form_submit_button("Complete Purchase")
            
            if submit_payment:
                # In a real app, this would process the payment
                # For now, just add tokens and return to design page
                if basic_selected:
                    st.session_state.token_count += 5
                elif standard_selected:
                    st.session_state.token_count += 10
                elif premium_selected:
                    st.session_state.token_count += 20
                
                st.success(f"Purchase successful! You now have {st.session_state.token_count} tokens.")
                st.button("Continue to Design", on_click=lambda: navigate_to('design_preferences'))

# My Designs Page
def show_my_designs():
    st.markdown("<h1 style='text-align: center;'>My Designs</h1>", unsafe_allow_html=True)
    
    if not st.session_state.user_designs:
        st.info("You haven't created any designs yet.")
        if st.button("Create Your First Design"):
            navigate_to('property_setup')
        return
    
    # Display all user designs
    for i, design in enumerate(reversed(st.session_state.user_designs)):
        with st.container():
            st.markdown(f"### Design {len(st.session_state.user_designs) - i}")
            st.markdown(f"**Created:** {design['created_at']}")
            st.markdown(f"**Prompt:** {design['prompt']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Room Type:** {design['property_info']['room_type']}")
                st.markdown(f"**Style:** {design['preferences']['style']}")
            with col2:
                st.markdown(f"**Area:** {design['property_info']['area']} m²")
                st.markdown(f"**Budget:** ${design['preferences']['budget']}")
            
            # View button for each design
            if st.button("View Details", key=f"view_{i}"):
                # Set the current design index and navigate to design view
                st.session_state.current_design_index = len(st.session_state.user_designs) - 1 - i
                navigate_to('design_view')
            
            st.markdown("---")
    
    # Button to create a new design
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Create New Design"):
            navigate_to('property_setup')

# Payment Page
def show_payment_page():
    st.markdown("<h1 style='text-align: center;'>Complete Your Purchase</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Get current design
        design = st.session_state.user_designs[-1] if st.session_state.user_designs else None
        
        if not design:
            st.error("No design found. Please generate a design first.")
            if st.button("Back to Design"):
                navigate_to('design_preferences')
            return
        
        st.markdown("<h2>Order Summary</h2>", unsafe_allow_html=True)
        
        # Display order summary
        st.markdown(f"""
        <div style='border: 1px solid #ced4da; border-radius: 4px; padding: 1rem; margin-bottom: 1rem;'>
            <p><strong>Design:</strong> {design['prompt']}</p>
            <p><strong>Furniture Items:</strong> {len(design['furniture_list'])}</p>
            <p><strong>Total Cost:</strong> ${design['total_price']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h2>Payment Information</h2>", unsafe_allow_html=True)
        
        with st.form("design_payment_form"):
            card_number = st.text_input("Credit Card Number")
            
            col1, col2 = st.columns(2)
            with col1:
                expiry = st.text_input("Expiry Date (MM/YY)")
            with col2:
                cvv = st.text_input("CVV", type="password")
            
            name = st.text_input("Cardholder Name")
            
            # Billing address
            st.markdown("<h3>Billing Address</h3>", unsafe_allow_html=True)
            address = st.text_area("Address")
            
            col1, col2 = st.columns(2)
            with col1:
                city = st.text_input("City")
            with col2:
                zip_code = st.text_input("ZIP Code")
            
            # Terms and conditions
            agree = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            submit_payment = st.form_submit_button("Complete Purchase")
        
        if submit_payment:
            if agree:
                # In a real app, this would process the payment
                st.success("Payment successful! Your design and furniture list have been purchased.")
                st.markdown("""
                <div style='background-color: #d1e7dd; color: #0f5132; padding: 1rem; border-radius: 4px; margin: 1rem 0;'>
                    <h3>What's Next?</h3>
                    <p>Our team will contact you shortly to arrange delivery and installation of your furniture.</p>
                    <p>You can track your order status in the 'My Orders' section.</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Back to Home"):
                    navigate_to('my_designs')
            else:
                st.error("Please agree to the Terms of Service and Privacy Policy to proceed.")

# Main app logic - determine which page to show
# BOQ Summary Page
def show_boq_summary():
    st.markdown("<h1 style='text-align: center;'>BOQ Summary</h1>", unsafe_allow_html=True)
    
    # Get the current design
    design = st.session_state.user_designs[-1] if st.session_state.user_designs else None
    
    if not design:
        st.error("No design found. Please generate a design first.")
        if st.button("Back to Design"):
            navigate_to('design_preferences')
        return
    
    # Display the BOQ summary
    st.markdown("<h2>Bill of Quantities</h2>", unsafe_allow_html=True)
    
    # Create a DataFrame for the furniture
    if design['furniture_list']:
        furniture_df = pd.DataFrame(design['furniture_list'])
        
        # Calculate total for each item
        if 'quantity' in furniture_df.columns and 'price' in furniture_df.columns:
            furniture_df['total'] = furniture_df['price'] * furniture_df['quantity']
        
        # Custom display of furniture table
        st.markdown("<div style='overflow-x: auto;'>", unsafe_allow_html=True)
        st.markdown("<table style='width: 100%; border-collapse: collapse;'>", unsafe_allow_html=True)
        
        # Table header
        st.markdown("<thead><tr style='background-color: #f8f9fa;'><th style='padding: 10px; text-align: left; border: 1px solid #dee2e6;'>Item</th><th style='padding: 10px; text-align: left; border: 1px solid #dee2e6;'>Vendor</th><th style='padding: 10px; text-align: right; border: 1px solid #dee2e6;'>Price</th><th style='padding: 10px; text-align: center; border: 1px solid #dee2e6;'>Quantity</th><th style='padding: 10px; text-align: right; border: 1px solid #dee2e6;'>Total</th></tr></thead>", unsafe_allow_html=True)
        
        # Table body
        st.markdown("<tbody>", unsafe_allow_html=True)
        for i, row in furniture_df.iterrows():
            st.markdown(f"<tr><td style='padding: 10px; border: 1px solid #dee2e6;'>{row['name']}</td><td style='padding: 10px; border: 1px solid #dee2e6;'>{row['vendor']}</td><td style='padding: 10px; text-align: right; border: 1px solid #dee2e6;'>${row['price']:,.2f}</td><td style='padding: 10px; text-align: center; border: 1px solid #dee2e6;'>{row['quantity']}</td><td style='padding: 10px; text-align: right; border: 1px solid #dee2e6;'>${row['total']:,.2f}</td></tr>", unsafe_allow_html=True)
        
        # Table footer with total
        st.markdown(f"<tr style='background-color: #f8f9fa; font-weight: bold;'><td colspan='4' style='padding: 10px; border: 1px solid #dee2e6;'>Total</td><td style='padding: 10px; text-align: right; border: 1px solid #dee2e6;'>${design['total_price']:,.2f}</td></tr>", unsafe_allow_html=True)
        
        st.markdown("</tbody></table></div>", unsafe_allow_html=True)
    else:
        st.info("No furniture items in this design.")
    
    # Display total price
    st.markdown(f"<h3>Total Cost: ${design['total_price']:,.2f}</h3>", unsafe_allow_html=True)
    
    # Buttons for actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Design"):
            navigate_to('design_view')
    with col2:
        if st.button("Purchase Items →"):
            navigate_to('payment_page')

def main():
    # Sidebar with navigation
    with st.sidebar:
        st.title("Navigation")
        
        # Show different options based on login status
        if st.session_state.customer_info:
            st.write(f"Welcome, {st.session_state.customer_info.get('name', 'User')}")
            st.write(f"Tokens: {st.session_state.token_count}")
            
            if st.button("Home"):
                navigate_to('my_designs')
            
            if st.button("New Design"):
                navigate_to('property_setup')
            
            if st.button("My Designs"):
                navigate_to('my_designs')
            
            if st.button("Buy Tokens"):
                navigate_to('token_purchase')
            
            if st.button("Logout"):
                navigate_to('login')
        else:
            if st.button("Login"):
                navigate_to('login')
            
            if st.button("Sign Up"):
                navigate_to('login')
    
    # Display the appropriate page based on current_page value
    if st.session_state.current_page == 'login':
        show_login_page()
    elif st.session_state.current_page == 'property_setup':
        show_property_setup()
    elif st.session_state.current_page == 'design_preferences':
        show_design_preferences()
    elif st.session_state.current_page == 'design_view':
        show_design_view()
    elif st.session_state.current_page == 'token_purchase':
        show_token_purchase()
    elif st.session_state.current_page == 'my_designs':
        show_my_designs()
    elif st.session_state.current_page == 'payment_page':
        show_payment_page()
    elif st.session_state.current_page == 'boq_summary':
        show_boq_summary()

if __name__ == "__main__":
    main()
