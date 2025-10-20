
# old_version="""You are an expert in text analysis. Your task is to evaluate a provided text against the requirements outlined in an article. Follow these instructions:
#     1. Read the article to identify all its requirements.
#     2. Compare the text against these requirements.
#     3. Output one of the following:
#         - If all requirements are covered, respond with: "All requirements are covered."
#         - If any requirements are missing, respond with: "Missing requirements:" followed by a numbered list of the missing requirements.
    
# Article:
# <article>
# {}
# </article>

# Text:
# <text>
# {}
# </text>"""
#If the article does not contain any requirements, respond with: "There are no requirements in this article.". Otherwise, Output one of the following:
finma2017_terms="""I. Subject matter
This circular sets out the requirements to be met by the corporate governance, risk management, internal control system and internal audit at banks, securities firms, financial groups (Art. 3c para. 1 BA) and financial conglomerates dominated by banking or securities trading (Art. 3c para. 2 BA). These are referred to below as "institutions".

II. Terms
Corporate governance is understood to mean the principles and structures on the basis of which an institution is directed and controlled by its governing bodies.
Risk management comprises the methods, processes and organisational structures used to define risk strategies and risk management measures in addition to the identification, analysis, assessment, management, monitoring and reporting of risks.
Risk tolerance comprises quantitative and qualitative considerations regarding the key risks which an institution is prepared to take to achieve its strategic business objectives in the context of its capital and liquidity planning. Where relevant, risk tolerance is defined per risk category as well as per institution.
The risk profile provides an overall picture of the risk positions entered into by an institution at institution level and per risk category at a particular point in time.
The internal control system (ICS) comprises the totality of the control structures and processes which at all levels of an institution form the basis for achieving its business objectives and ensuring orderly business operations. The ICS comprises retrospective controls and planning and management elements. An effective ICS consists of control activities which are integrated into work processes, appropriate risk management and compliance processes, and monitoring bodies – particularly an independent risk control and compliance function – which adequately reflect the size, complexity and risk profile of an institution.
Compliance is understood to mean abiding by the relevant statutory, regulatory and internal rules and observing generally accepted market standards and codes of conduct.

III. Scope of application (the principle of proportionality)
This circular applies to all institutions as defined in margin no. 1. The requirements are to be implemented on a case-by-case basis, giving due consideration to the size, complexity, structure and risk profile of each institution. FINMA can relax or tighten the rules in individual cases."""
#1. Use the provided general terms related to the article to guide your analysis and make the evaluation easier. 
def build_gap_prompt(retrieved_doc,article):
    text=''
    for item in retrieved_doc:
        text=text+'\n'+item.page_content
    text= text.replace("Title: ",'Section: ').replace(' SubTitle:','SubSection')    
    prompt="""You are an expert in concept analysis. Your task is to evaluate a provided concept against the requirements outlined in an article. Follow these instructions:
    1. Read the article to identify all its requirements.
    2. Compare the concept against these requirements.
    3. Output one of the following:
        - Covered Requirements: List all the requirements from the article that are fully addressed in the concept. For each covered requirement, specify the full section name and subsection (if applicable) of the concept that covers it (e.g. Section "4.Risk Management -> Identification").
        - Missing Requirements: List all the requirements from the article that are not addressed or only partially addressed in the concept.

Article:
<article>
{}
</article>

Concept:
<Concept>
{}
</Concept>""".format(article,text) #finma2017_terms

    return prompt.encode('unicode_escape').decode('utf-8')


def build_table_prompt(response):
  
    prompt="""Convert the given list of covered and missing requirements into a table. The table should have four columns:
1. Requirements: The short summary of the requirement.
2. Covered: Indicate whether the requirement is "Yes" (covered) or "No" (missing) or "Partially".
3. Reference in Document: If covered, mention the title of the specific section or reference in the concept that addresses the requirement. If not covered, leave this column blank.
4. Comment: The full sentence related to the requirment without changing it.

If there are no missing requirements, do not include rows for missing requirements in the table.

Input Example:

Covered Requirements:

1. The concept covers the requirement "The board of directors sets out the business strategy and defines guiding principles for the institution's corporate culture" in the section "3.	Organization and Responsibilities -> Board of Directors", which states that the Board of Directors establishes the overarching principles for risk management, including risk appetite and additional risk-related policies.

Missing Requirements:

The article mentions the compliance function as a separate independent control body, but the concept does not provide details about a dedicated compliance function or its responsibilities.

Output Example:
<table>
| Requirements| Covered | Reference in Document| Comment|  
|-------------|---------|----------------------|--------|  
| The board of directors sets out the business strategy and corporate culture. | Yes | 3.Organization and Responsibilities -> Board of Directors | The concept covers the requirement "The board of directors sets out the business strategy and defines guiding principles for the institution's corporate culture" in the section "3.	Organization and Responsibilities -> Board of Directors", which states that the Board of Directors establishes the overarching principles for risk management, including risk appetite and additional risk-related policies. |  
| The compliance function as a separate independent control body | No |  | The article mentions the compliance function as a separate independent control body, but the concept does not provide details about a dedicated compliance function or its responsibilities. |  
</table>

Using the structure and examples above, generate the table for the following requirements list:
<list>
{}
</list>""".format(response)

    return prompt.encode('unicode_escape').decode('utf-8')