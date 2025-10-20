import streamlit as st
import pandas as pd
from modules.UI.general import hide_sidebar
from modules.UI.regulation_list import choose_reg
from modules.UI.dropdown_styling import apply_dropdown_styling

st.set_page_config(page_title="Regulatory Repository", page_icon="design/logo/logo2.png", layout="wide")
is_reg_rep = True

# Apply professional styling
apply_dropdown_styling()

choose_reg(True)

if st.session_state['regulation_rep'] != "Select a Regulation":
    # Mapping sipas përzgjedhjes
    if st.session_state['regulation_rep'] == "Circular 2023/1 Operational risks and resilience – banks":
        df = pd.read_excel('Data/Finma_EN/splitted/finma_optional.xlsx')
    elif st.session_state['regulation_rep'] == "Circular 2017/1 Corporate governance - banks":
        df = pd.read_excel('Data/Finma_EN/splitted/finma2017_open_source_embeddings.xlsx')
    else:
        df = None

    if df is not None:
        # Heq kolonën e fundit vetëm nëse ekziston (disa xlsx kanë kolonë bosh në fund)
        if df.shape[1] > 0:
            df = df.iloc[:, :-1] if df.columns[-1] == '' or df.columns[-1] is None else df

        st.subheader(st.session_state['regulation_rep'])
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.warning("Nuk u gjet asnjë dataset për rregulloren e zgjedhur.")

hide_sidebar()


# with col4:
#     if selected_subcategory2:
#         subcategories3 = data.get(selected_subcategory2, [])
#         selected_subcategory3 = st.selectbox("L4", options=subcategories3)
#     st.write("#")



## option2
# L3=None
# L4=None
# coll1, coll2, coll3, coll4= st.columns(4,border=True)    
# repo = coll1.radio(
#     "L1",
#     ["Repository"],
#     captions=[
#         "(Regulatory and Legal)",
#     ],
#     index=None,
# )

# if repo=="Repository":
#     L2 = coll2.radio(
#     "L2",
#     ["FINMA"],
 
#     index=None,
#     )
#     if L2=="FINMA":
#         L3 = coll3.radio(
#         "L3",
#         ["Operational Risk", "Liquidity Risk","Market Risk","Credit Risk","Legal and Compliance Risk" ,"Strategic Risk" ,"Reputational Risk","Other Risk"],
    
#         index=None,
#         )
#     if L3=="Operational Risk":
#         L4=coll4.radio(
#         "L4",
#         ["RS 2023/1","RS 2008/21","Vorgaben zum Business Continuity Mangement"],
#         captions=[
#         "Umgang mit operationellen Risiken",
#         "Mindeststandards für das Management operationeller Risiken",
#         ""],
    
#         index=None,
#         )     

# if L4=="RS 2023/1":
#     df = pd.DataFrame(
#     {
#         "Rz": ["1", "2", "3"],
#         "Title": ["Terms", "Terms", "Terms"],
#         "Text": ["text1nnnnnnnnnnnnnn","text2nnnnnnnnnnnn","text3nnnnnnnnnnnnnnnn"],

#     }
#     )
#     st.dataframe(
#         df,
#         use_container_width=True,
#         hide_index=True,
#     )

## option3
# options = ["Repository (Regulatory and Legal)"]
# selection1 = st.segmented_control(
#     "L1", options, selection_mode="single"
# )

# selection3=None
# selection4=None
# if selection1=="Repository (Regulatory and Legal)":
#     cl1, cl2= st.columns([0.05, 0.95]) 
#     selection2 = cl2.segmented_control(
#     "L2", ['FINMA'], selection_mode="single"
#     )

#     if selection2=='FINMA':
#         scl1, scl2= cl2.columns([0.05, 0.95]) 
#         selection3 = scl2.segmented_control(
#         "L3", ["Operational Risk", "Liquidity Risk","Market Risk","Credit Risk","Legal and Compliance Risk" ,"Strategic Risk" ,"Reputational Risk","Other Risk"], selection_mode="single"
#         )
#     if selection3=="Operational Risk":
#         sscl1, sscl2= cl2.columns([0.1, 0.9]) 
#         selection3 = sscl2.segmented_control(
#         "L4", ["RS 2023/1","RS 2008/21","Vorgaben zum Business Continuity Mangement"], selection_mode="single"
#         )    