import streamlit as st
import streamlit.components.v1 as components

def scroll_to(element_id):
    components.html(f'''
        <script>
            var element = window.parent.document.getElementById("{element_id}");
            element.scrollIntoView({{behavior: 'smooth'}});
        </script>
    '''.encode(),height=0)

def radio_options(page, subcol32, data, selected_subcategory2):
    with subcol32.expander(st.session_state[page]):
        subcategories3 = data.get(selected_subcategory2, [])

        captions_map = {
            "Circular 2023/1 Operational risks and resilience – banks": "Operational risks and resilience framework for banks",
            "Circular 2017/1 Corporate governance - banks": "Corporate governance requirements for banks",
            "Circular 2013/8 Market conduct rules": "Market conduct requirements for securities trading",
        }

        selected_subcategory3 = st.radio(
            "Select Regulation",
            subcategories3,
            horizontal=False,
            captions=[captions_map.get(option) for option in subcategories3] if any(captions_map.get(option) for option in subcategories3) else None,
            index=None,
            label_visibility='collapsed',
        )
        if selected_subcategory3 and st.session_state[page] != selected_subcategory3:
            st.session_state[page] = selected_subcategory3
            st.rerun()
        return selected_subcategory3

def choose_reg(is_reg_rep):
    if "regulation_rep" not in st.session_state:
        st.session_state['regulation_rep']= "Select a Regulation"
    if "regulation_anlyz" not in st.session_state:
        st.session_state['regulation_anlyz']= "Select a Regulation"

    data = {
        "Main": ["(Regulatory and Legal)"],
        "(Regulatory and Legal)": ["FINMA"],
        "FINMA": ["Operational Risk", "Liquidity Risk","Market Risk","Credit Risk","Legal and Compliance Risk" ,"Strategic Risk" ,"Reputational Risk","Other Risk"],
        "Operational Risk": [
            "Circular 2023/1 Operational risks and resilience – banks",
            "Circular 2017/1 Corporate governance - banks",
        ],
        "Liquidity Risk": ["LR 2023/1", "LR 2020/1"],
        "Market Risk": ["Circular 2013/8 Market conduct rules"],
        "Credit Risk": ["CR 2023/1", "CR 2020/1"],
        "Legal and Compliance Risk": ["LCR 2023/1", "LCR 2020/1"],
        "Strategic Risk": ["SR 2023/1", "SR 2020/1"],
        "Reputational Risk": ["RR 2023/1", "RR 2020/1"],
        "Other Risk": ["OR 2023/1", "OR 2020/1"],
    }

    st.subheader("Repository", divider='rainbow' )
    scroll_to("repository")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        selected_category = st.selectbox("Repository", index=None, options=data["Main"], label_visibility="collapsed")
        if selected_category:
            subcol11, subcol12 = col2.columns([0.1,0.9])
            subcol11.markdown("<h3 style='text-align: center; margin-top:-8px;'> → </h3>",  unsafe_allow_html=True)
            subcategories1 = data.get(selected_category, [])
            selected_subcategory1 = subcol12.selectbox("Regulatory and Legal", index=None, options=subcategories1, label_visibility="collapsed")
            if selected_subcategory1:
                subcol21, subcol22 = col3.columns([0.1,0.9])
                subcol21.markdown("<h3 style='text-align: center; margin-top:-8px;'> → </h3>",  unsafe_allow_html=True)
                subcategories2 = data.get(selected_subcategory1, [])
                selected_subcategory2 = subcol22.selectbox("FINMA", index=None, options=subcategories2, label_visibility="collapsed")
                if selected_subcategory2 and selected_subcategory2 in data:
                    subcol31, subcol32 = col4.columns([0.1,0.9])
                    subcol31.markdown("<h3 style='text-align: center; margin-top:-8px;'> → </h3>",  unsafe_allow_html=True)
                    if is_reg_rep:
                        selected_subcategory3 = radio_options('regulation_rep', subcol32, data, selected_subcategory2)
                    else:
                        selected_subcategory3 = radio_options('regulation_anlyz', subcol32, data, selected_subcategory2)
                    return selected_subcategory3
