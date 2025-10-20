from langchain_community.document_loaders import PDFMinerPDFasHTMLLoader
from bs4 import BeautifulSoup
import re
import pandas as pd

def chunk_html_content(content):
    cur_fs = None
    cur_text = ''
    cur_ft=''
    snippets = []   # first collect all snippets that have the same font size
    for c in content:
        sp = c.find('span')
        if sp:
            text = ''.join(sp.stripped_strings).replace('-\n', '').replace('\n', ' ').replace("*",'').replace("\xa0", ' ')
            sp.string = text
         
        if not sp or sp.string.isdigit():
            continue
        st = sp.get('style')
        if not st:
            continue
   
        fs = re.findall('font-size:(\d+)px',st)
        if 'Bold' in st:
            ft='B'
        else:
            ft='N'
        if not fs:
            continue
        fs = int(fs[0])
        if not cur_fs:
            cur_fs = fs
        if not cur_ft:
            cur_ft=ft
        if fs == cur_fs and ft==cur_ft:
            cur_text += "\\line "+c.text
            if "•" in cur_text or 'b)' in cur_text:
               cur_text=cur_text.replace("\\line ",' ').replace("•","\\line •").replace('participant.','participant.\\line')
        else:
            snippets.append((cur_text,cur_fs,cur_ft))
            cur_fs = fs
            cur_text = c.text
            cur_ft=ft
    snippets.append((cur_text,cur_fs,cur_ft))

    return snippets

def create_df(snippets):
    finma_df = pd.DataFrame(columns=["Title","SubTitle","Margin", "Text"])
    title=''
    sub_title=''
    context=[]
    par_num=1
    for item in snippets:
        if  item[0]=='Annex 1':
            break
        if item[1]==12 or item[1]==16:
            if title and context:
                for par in context:
                    for subpar in par:
                        new_row = [{
                                    "Title": title,
                                    "SubTitle": sub_title,
                                    "Margin":par_num,
                                    "Text": subpar,
                                }]
                        finma_df = pd.concat([finma_df, pd.DataFrame(new_row)], ignore_index=True)
                        par_num+=1
            context=[]
            if item[2]=='B':
                title=item[0].replace('\xa0','').replace('\\line',' ').strip()
                sub_title=''
            elif item[2]=='N':
                sub_title=item[0].replace('\xa0','').replace('\\line',' ').strip()
        elif item[1]==9:
            context.append(item[0].replace('\xa0','').replace('•\n•','•').replace('•\n','• ').replace('\n',' ').replace('- ','').replace('  ',' ').strip().split("\\line"))
    new_row = [{
                "Title": title,
                "SubTitle": sub_title,
                "Margin":par_num,
                "Text": context,
            }]
    finma_df = pd.concat([finma_df, pd.DataFrame(new_row)], ignore_index=True)

    return finma_df

# =========================
# Rregulloret ekzistuese
# =========================

loader_2017 = PDFMinerPDFasHTMLLoader("Data/Finma_EN/finma rs 2017 01 20200101.pdf")
data_2017 = loader_2017.load()
soup_2017 = BeautifulSoup(data_2017[0].page_content,'html.parser')
content_2017 = soup_2017.find_all("div")
snippets_2017=chunk_html_content(content_2017)
df_2017=create_df(snippets_2017[141:])

loader_2023 = PDFMinerPDFasHTMLLoader("Data/Finma_EN/finma rs 2023 01 20221207.pdf")
data_2023 = loader_2023.load()
soup_2023= BeautifulSoup(data_2023[0].page_content,'html.parser')
content_2023= soup_2023.find_all("div")
snippets_2023=chunk_html_content(content_2023)
df_2023=create_df(snippets_2023[141:])

loader_2008= PDFMinerPDFasHTMLLoader("Data/Finma_EN/ch-finma-circular-2008-21-en.pdf")
data_2008 = loader_2008.load()
soup_2008= BeautifulSoup(data_2008[0].page_content,'html.parser')
content_2008= soup_2008.find_all("div")
snippets_2008=chunk_html_content(content_2008)
df_2008=create_df(snippets_2008)

# =========================
# Rregullorja e re: Operational Risk 2024
# =========================

loader_optional = PDFMinerPDFasHTMLLoader("Data/Finma_EN/op-risk.pdf")
data_optional = loader_optional.load()
soup_optional = BeautifulSoup(data_optional[0].page_content,'html.parser')
content_optional = soup_optional.find_all("div")
snippets_optional = chunk_html_content(content_optional)
df_optional = create_df(snippets_optional)  # mund të përdorësh [141:] nëse të jep shumë tekste hyrëse

# Ruaj në Excel
df_optional.to_excel("Data/Finma_EN/splitted/finma_optional.xlsx", index=False)

