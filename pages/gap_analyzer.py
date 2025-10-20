import streamlit as st
import pandas as pd
from modules.model.open_source_llm import create_embeddings, get_llm
from modules.UI.general import hide_sidebar,show_logo, rotate_circle, button_design,upload_button_design
from modules.UI.regulation_list import choose_reg
from modules.UI.dropdown_styling import apply_dropdown_styling
from modules.design_excel import write_to_excel
from modules.gap_analyzer_claude import perform_gap_analysis
import os

st.set_page_config(page_title="Gap Analysis", page_icon="design/logo/logo2.png",layout="wide")

# Apply professional styling
apply_dropdown_styling()  

col1,col2,col3= st.columns([0.25,0.5,0.25])
hide_sidebar()

col2.markdown(
    "<h2 style='text-align: center;'>AI-based Gap Analysis</h2>", 
    unsafe_allow_html=True)
    
col2.markdown(
"<h4 style='text-align: center; color: #8888a1;'>Upload, manage and analyze your documents using advanced artificial intelligence</h4>", 
unsafe_allow_html=True)



# Initialize session state variables
for key, default in [("regbox", False), ("reg_is_seleceted", False), ("doc_is_uploaded", False), ("disabled", True), ("uploaded_file", None), ("regulation_file", None)]:
    if key not in st.session_state:
        st.session_state[key] = default


# Function to dynamically update the disabled state
def update_disabled_state():
    st.session_state["disabled"] = not (
        st.session_state["reg_is_seleceted"] and st.session_state["doc_is_uploaded"]
    )

def show_repo():
    # Regulation selection logic
    if st.session_state['regbox']:
        # Simulate regulation selection process
        selecteditem = choose_reg(False)
        if selecteditem:
            st.session_state["reg_is_seleceted"]=True
        else:
            st.session_state['reg_is_seleceted'] = False
            st.session_state['regulation_anlyz']= "Select a Regulation"
    
        update_disabled_state()  

# Columns layout
left, middle, right = col2.columns([0.4, 0.1, 0.4])


# File uploader for documents
try:
    file = left.file_uploader("", type=['.docx'], help="Policies, Contracts, any", key="file_uploader")
    if file is not None:
        # Validate file size (200MB limit)
        if file.size > 200 * 1024 * 1024:  # 200MB in bytes
            left.error("File size too large! Maximum 200MB allowed.")
        else:
            st.session_state['doc_is_uploaded'] = True
            st.session_state['uploaded_file'] = file
            left.success(f"File uploaded! Size: {file.size / 1024:.1f} KB", icon="✅")
            update_disabled_state()
            right.write("#")
            middle.write("#")
    else:
        st.session_state['doc_is_uploaded'] = False
        st.session_state['uploaded_file'] = None
        update_disabled_state()
except Exception as e:
    left.error(f"Upload error: {str(e)}")
    st.session_state['doc_is_uploaded'] = False
    st.session_state['uploaded_file'] = None
    update_disabled_state()

# Choose regulation button
if left.button("**Choose Regulation**", help='Select', icon=":material/gavel:", use_container_width=True):
    st.session_state['regbox'] = True

show_repo()

if st.session_state["reg_is_seleceted"]:
    selecteditem=st.session_state['regulation_anlyz']
    left.success(f'{selecteditem} selected!', icon="✅")


# Display the arrow image based on the `disabled` state
middle.title("")
arrow_image = "design/arrow/disable.png" if st.session_state["disabled"] else "design/arrow/able.png"
middle.image(arrow_image)

# GAP Analyzer button
right.write("#")

# Perform Gap Analysis when button is clicked
if right.button("**GAP-Analyzer**", help='Perform your gap analysis based on AI', icon=":material/search:", key="gap_analyzer", use_container_width=True, disabled=st.session_state['disabled']):
    # Get regulation file path
    regulation_name = st.session_state.get('regulation_anlyz', '')
    
    # Map regulation name to file path
    regulation_files = {
        'Circular 2023/1 Operational risks and resilience – banks': 'Data/Finma_EN/splitted/finma_optional.xlsx',
        'Circular 2017/1 Corporate governance - banks': 'Data/Finma_EN/splitted/finma2017_open_source_embeddings.xlsx',
    }
    
    regulation_file = regulation_files.get(regulation_name)
    
    if regulation_file and os.path.exists(regulation_file):
        try:
            # Perform gap analysis
            with st.spinner('Analyzing your document with Claude AI...'):
                df_results = perform_gap_analysis(
                    uploaded_file=st.session_state['uploaded_file'],
                    regulation_file=regulation_file,
                    regulation_name=regulation_name
                )
            
            # Generate Excel file
            excel_file = write_to_excel(df_results)
            
            # Success message
            st.success('Gap analysis completed! Download your report below.')
            
            # Download button
            st.download_button(
                label="Download Excel Report",
                data=excel_file,
                file_name=f"gap_analysis_{regulation_name.replace('/', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            
        except Exception as e:
            st.error(f"Error performing gap analysis: {str(e)}")
    else:
        st.error(f"Regulation file not found: {regulation_name}")

# Update the disabled state dynamically
update_disabled_state()
         

show_logo()
rotate_circle()
button_design()    
upload_button_design()

