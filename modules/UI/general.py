import streamlit as st
from modules.UI.img_to_base import image_to_base64

def hide_sidebar():
    return    st.markdown(
    """
        <style>
            [data-testid="stSidebarCollapsedControl"] {
                display: none 
                                            
            }
            [data-testid="stSidebar"] {
                display: none ; 
                                              
            }
        </style>
        """,
            unsafe_allow_html=True,
        )

def show_logo():
    # Logo removed - function kept for compatibility
    pass

def rotate_circle():
    # Rotating circle removed - function kept for compatibility
    pass

def button_design():
    button_html = """
    <style>
    /* Custom button styling */
    .stButton button , .stDownloadButton button {
        padding: 2.5em 1.5em 1.3em 1.6em; /* Add padding for better aesthetics */
        border: none; /* Remove default border */
        border-radius: 15px; /* Rounded corners */
        position: relative; /* For gradient border overlay */
        z-index: 1; /* Ensure button text is above the pseudo-element */

        display: flex; /* Use flexbox for layout */
        flex-direction: column; /* Arrange children vertically */
        align-items: center; /* Center items horizontally */
        justify-content: center; /* Center items vertically */
        text-align: center; /* Center text alignment for child elements */
    }
    .stButton button span , .stDownloadButton button span{
        font-size: 3.2rem; /* Make font bigger */
        margin-bottom: 0.2em; /* For gradient border overlay */
        text-align: center;
    }
    .stButton button p , .stDownloadButton button p{
        font-size: 1.2rem; /* Make font bigger */
        margin-bottom: 0.2em;
    }
    .stButton button::before , .stDownloadButton button::before{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 15px; /* Match the border radius */
        padding: 2px; /* Width of the gradient border */
        background: linear-gradient(45deg, #FB3135, #6256EF, #48E7FE); /* Gradient colors */
        -webkit-mask: 
            linear-gradient(#fff 0 0) content-box, 
            linear-gradient(#fff 0 0);
        mask: 
            linear-gradient(#fff 0 0) content-box, 
            linear-gradient(#fff 0 0);
        -webkit-mask-composite: destination-out;
        mask-composite: exclude; /* Creates the inner transparent area */
        z-index: -1; /* Place it behind the button content */
        transition: background 1 ease; /* Smooth transition for gradient angle */
    }
    .stButton button:hover::before ,.stDownloadButton button:hover::before {
        background: linear-gradient(135deg, #FB3135, #6256EF, #48E7FE); /* Change gradient angle on hover */
    }
    .stButton button:hover ,.stDownloadButton button:hover{
        color: white; /* Change text color to white */
        background: #20203C;
        transition: all 0.5s ease; /* Smooth transition for hover effects */
    }

    /* Styling for disabled button */
    .stButton button:disabled ,.stDownloadButton button:disabled {
        cursor: not-allowed; /* Show not-allowed cursor */
        background: none; /* Remove background */
        border: 2px solid gray; /* Add a gray border */
        pointer-events: none; /* Disable hover effects */
    }
    .stButton button:disabled::before ,.stDownloadButton button:disabled::before  {
        display: none; /* Remove gradient border effect */
    }
    </style>
    """

    
    st.markdown(button_html, unsafe_allow_html=True)           

def upload_button_design():    
    upload_button_html = """
   <style>
    /* Custom button styling */
    [data-testid="stFileUploaderDropzone"] {
        padding: 1.5em 0.5em 1.5em 1.5em; /* Add padding for better aesthetics */
        border: none; /* Remove default border */
        border-radius: 15px; /* Rounded corners */
        background: #121222;
        position: relative; /* For gradient border overlay */
        z-index: 1; /* Ensure button text is above the pseudo-element */
        display: flex; /* Use flexbox for layout */       
        align-items: center; /* Center items horizontally */
        justify-content: center; /* Center items vertically */
        text-align: center; /* Center text alignment for child elements */
        

    }
    [data-testid="stFileUploaderDropzoneInstructions"] {
        margin-right: inherit;
        
    }

    /* Ensure the SVG icon is centered */
    [data-testid="stFileUploaderDropzoneInstructions"] svg {
        font-size: 3rem; /* Make the icon larger */
        color: #fff; /* Icon color */
         /* Remove any default margin */
        
    }
    [data-testid="stFileUploaderDropzone"] div{
       display: block;
       
    }

    /* Style the upload text (Span) */
    [data-testid="stFileUploaderDropzoneInstructions"] div span {
        visibility: hidden; /* Hide the default text */
       
    }

    [data-testid="stFileUploaderDropzoneInstructions"] div span:after {
        content: "Upload your Document"; /* Custom text */
        visibility: visible; /* Make the custom text visible */
        font-size: 1.2rem; /* Adjust font size */
        font-weight: 600;
        color: #fff; /* White text */
        display: block;
        text-align: center;
        margin-top: -1em;
        
    }

    /* Remove the small default text (Limit message) */
    [data-testid="stFileUploaderDropzoneInstructions"] small {
        display: none; /* Hide the limit text */
    }

    /* Add gradient border effect */
    [data-testid="stFileUploaderDropzone"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 15px; /* Match the border radius */
        padding: 2px; /* Width of the gradient border */
        background: linear-gradient(45deg, #FB3135, #6256EF, #48E7FE); /* Gradient colors */
        -webkit-mask: 
            linear-gradient(#fff 0 0) content-box, 
            linear-gradient(#fff 0 0);
        mask: 
            linear-gradient(#fff 0 0) content-box, 
            linear-gradient(#fff 0 0);
        -webkit-mask-composite: destination-out;
        mask-composite: exclude; /* Creates the inner transparent area */
        z-index: -1; /* Place it behind the button content */
        transition: background 1s ease; /* Smooth transition for gradient angle */
    }

    /* Hover effects */
    [data-testid="stFileUploaderDropzone"]:hover::before {
        background: linear-gradient(135deg, #FB3135, #6256EF, #48E7FE); /* Change gradient angle on hover */
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        background: #20203C;
    }

    /* Hide the default upload button */
    [data-testid="stFileUploaderDropzone"] button {
        display: none;
    }
   </style>
    """
        
    st.markdown(upload_button_html, unsafe_allow_html=True)  