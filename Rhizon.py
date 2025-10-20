import streamlit as st
import toml
from modules.UI.img_to_base import image_to_base64
from modules.UI.general import hide_sidebar,show_logo, rotate_circle, button_design

primaryColor = toml.load(".streamlit/config.toml")['theme']['primaryColor']

def main():
    # Set the page configuration
    st.set_page_config(page_title="Gap Analysis", page_icon="design/logo/logo2.png")  

    hide_sidebar()

    st.write("#")
    
    st.markdown(
    "<h2 style='text-align: center;'>AI-based Gap Analysis</h2>", 
    unsafe_allow_html=True)
    
    st.markdown(
    "<h4 style='text-align: center; color: #8888a1;'>Upload, manage and analyze your documents using advanced artificial intelligence</h4>", 
    unsafe_allow_html=True)

    show_logo()
    rotate_circle()
    button_design()    
 
    left, right = st.columns(2)
    # Display the input text
    if left.button("**Regulatory Repository**", icon=":material/storage:", key="repos", use_container_width=True):
        # response=ask_claude(user_input,1)
        st.switch_page('pages/regulatory_repo.py')
    
    if right.button("**GAP-Analyzer**",help='Perform your gap analysis based on AI', icon=":material/search:", key="analyzer", use_container_width=True):
        
        st.switch_page('pages/gap_analyzer.py')

   
if __name__ == "__main__":
    main()