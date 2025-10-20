
from model.bedrock import bedrock_embedding
import pandas as pd

bedrock_embeddings=bedrock_embedding()

def embed_articles(df):
    finma_df = pd.DataFrame(columns=["Embedding"])
    for index,item in enumerate(df['Text']):
        print(index)
        complete_article=df['Title'][index]
        if df['SubTitle'][index] and str(df['SubTitle'][index])!='nan':
            complete_article=complete_article+'\n'+df['SubTitle'][index]
            
        if df['Sub_Subtitle'][index] and str(df['Sub_Subtitle'][index])!='nan': 
            complete_article=complete_article+'\n'+df['Sub_Subtitle'][index]
        
        # complete_article=complete_article+'\n Article: '+df_2017['Margin'][index]
        complete_article=complete_article+'\n'+item
        cur_embedding=bedrock_embeddings.embed_query(complete_article)
        print(type(cur_embedding))
        new_row = [{
                    "Embedding": cur_embedding,
                }]
        finma_df = pd.concat([finma_df, pd.DataFrame(new_row)], ignore_index=True)
    return finma_df

df_2017=pd.read_excel('Data/Finma_EN/splitted/finma2017.xlsx') 
finma_df_2017= embed_articles(df_2017)    
finma_df_2017.to_excel('Data/Finma_EN/Splitted/embedding_2017.xlsx')

# df_2023=pd.read_excel('Data/Finma_EN/splitted/finma2023.xlsx') 
# finma_df_2023= embed_articles(df_2023)    
# finma_df_2023.to_excel('Data/Finma_EN/Splitted/embedding_2023.xlsx')  

# df_2008=pd.read_excel('Data/Finma_EN/splitted/finma2008.xlsx') 
# finma_df_2008= embed_articles(df_2008)    
# finma_df_2008.to_excel('Data/Finma_EN/Splitted/embedding_2008.xlsx')  