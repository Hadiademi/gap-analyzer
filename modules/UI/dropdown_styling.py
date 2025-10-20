"""
Simple dropdown styling - back to working version
"""
import streamlit as st

def apply_dropdown_styling():
    """Apply minimal styling to dropdowns"""
    
    # Back to the simple version that worked
    simple_style = """
    <style>
    /* Repository header */
    h3[data-testid="stSubheader"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #48E7FE !important;
        text-shadow: 0 0 10px rgba(72, 231, 254, 0.5);
    }
    
    /* Divider styling */
    hr[data-testid="stHorizontalBlock"] {
        background: linear-gradient(90deg, #FB3135, #6256EF, #48E7FE);
        height: 3px;
        border: none;
        margin: 1.5rem 0;
    }
    
    /* Arrow styling */
    h3 {
        color: #48E7FE !important;
        text-shadow: 0 0 10px rgba(72, 231, 254, 0.5);
    }
    </style>
    """
    
    st.markdown(simple_style, unsafe_allow_html=True)

