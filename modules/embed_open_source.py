from modules.model.open_source_llm import create_embeddings
import pandas as pd

# Initialize embeddings
embeddings = create_embeddings()

def embed_articles(df):
    """
    Generate embeddings for articles using open source sentence transformers
    
    Args:
        df: DataFrame with columns 'Title', 'SubTitle', 'Sub_Subtitle', 'Text'
        
    Returns:
        DataFrame with embeddings
    """
    finma_df = pd.DataFrame(columns=["Embedding"])
    
    for index, item in enumerate(df['Text']):
        print(f"Processing article {index + 1}/{len(df)}")
        
        # Build complete article text
        complete_article = df['Title'][index]
        
        if df['SubTitle'][index] and str(df['SubTitle'][index]) != 'nan':
            complete_article = complete_article + '\n' + df['SubTitle'][index]
            
        if 'Sub_Subtitle' in df.columns and df['Sub_Subtitle'][index] and str(df['Sub_Subtitle'][index]) != 'nan': 
            complete_article = complete_article + '\n' + df['Sub_Subtitle'][index]
        
        complete_article = complete_article + '\n' + item
        
        # Generate embedding
        cur_embedding = embeddings.embed_query(complete_article)
        print(f"Generated embedding of length: {len(cur_embedding)}")
        
        # Add to DataFrame
        new_row = [{
            "Embedding": cur_embedding,
        }]
        finma_df = pd.concat([finma_df, pd.DataFrame(new_row)], ignore_index=True)
        
    return finma_df

def embed_documents(texts):
    """
    Generate embeddings for multiple documents
    
    Args:
        texts: List of text strings to embed
        
    Returns:
        List of embeddings
    """
    return embeddings.embed_documents(texts)

# Example usage for existing data
if __name__ == "__main__":
    # Load existing data
    df_2017 = pd.read_excel('Data/Finma_EN/splitted/finma2017.xlsx') 
    finma_df_2017 = embed_articles(df_2017)    
    finma_df_2017.to_excel('Data/Finma_EN/splitted/embedding_2017_open_source.xlsx', index=False)
    print("Generated embeddings for 2017 data")
    
    # Uncomment to process other years
    # df_2023 = pd.read_excel('Data/Finma_EN/splitted/finma2023.xlsx') 
    # finma_df_2023 = embed_articles(df_2023)    
    # finma_df_2023.to_excel('Data/Finma_EN/splitted/embedding_2023_open_source.xlsx', index=False)
    
    # df_2008 = pd.read_excel('Data/Finma_EN/splitted/finma2008.xlsx') 
    # finma_df_2008 = embed_articles(df_2008)    
    # finma_df_2008.to_excel('Data/Finma_EN/splitted/embedding_2008_open_source.xlsx', index=False)
