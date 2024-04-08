import streamlit as st
import pandas as pd
import os
import re
import preprocessor as p
import joblib
import base64



project_description = """
# Hotel Data Analysis Project

## Overview

I have completed a hotel data analysis project using an instant web scraper. 
This project involved scraping hotel data and hotel reviews separately, cleaning the data, 
concatenating it, and performing sentiment analysis on the DataFrame. 
Additionally, I clustered the hotel reviews, applied sentiment analysis, and passed 
those clusters to an LLM (Language Model) to extract strengths and weaknesses of hotels.

## Steps

### 1. Scraping Hotel Data

- Utilized an instant web scraper to collect hotel data.
- Scraped hotel data separately from hotel reviews.

### 2. Data Collection

- Collected hotel data and hotel reviews data separately for each hotel.

### 3. Data Cleaning

- Cleaned the collected data to remove any inconsistencies or errors.
- Applied preprocessing techniques to prepare the data for analysis.

### 4. Data Concatenation

- Concatenated the cleaned hotel data and hotel reviews data to create a unified dataset for analysis.

### 5. Sentiment Analysis

- Performed sentiment analysis on the concatenated DataFrame.
- Utilized the results to understand the overall sentiment of hotel reviews.

### 6. Clustering Hotel Reviews

- Clustered the hotel reviews based on their content to identify patterns and similarities.

### 7. Extracting Strengths and Weaknesses

- Passed the clustered reviews to an LLM (Language Model) to extract strengths and weaknesses of hotels.
- Used the extracted information to gain insights into customer perceptions.

## Conclusion

This project demonstrates the use of web scraping, data cleaning, sentiment analysis, and clustering techniques to analyze hotel data. 
The extracted strengths and weaknesses provide valuable insights for hotel management to improve customer satisfaction and service quality.
"""
def create_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download CSV file</a>'
    return href

# Path to the directory containing CSV files
directory_path = r'hotel reviews'

# Get a list of CSV files in the directory
csv_files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]

# Function to concatenate selected columns
def concatenate_columns(df, selected_columns):
    concatenated_data = df[selected_columns[0]].tolist() + df[selected_columns[1]].tolist()
    return pd.DataFrame({'ConcatenatedData': concatenated_data})

# Function to display selected dataset
def display_selected_dataset(selected_dataset):
    dataset_path = os.path.join(directory_path, selected_dataset)
    selected_df = pd.read_csv(dataset_path)
    st.subheader(f'Dataset: {selected_dataset}')
    st.write(selected_df)
def clean_tweets(series):
    REPLACE_NO_SPACE = re.compile("[.;:!\'?,\"()\[\]]")
    REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    tempArr = []
    for line in series:
        # Check if the value is NaN
        if pd.isnull(line):
            tempArr.append("")
            continue
        # Send to tweet_processor
        tmpL = p.clean(line)
        # Remove punctuation
        tmpL = REPLACE_NO_SPACE.sub("", tmpL.lower())
        # Replace specific characters with spaces
        tmpL = REPLACE_WITH_SPACE.sub(" ", tmpL)
        # Remove extra spaces
        tmpL = " ".join(tmpL.split())
        tempArr.append(tmpL)
    return tempArr

# Streamlit app
def main():
    

    # Create a menu bar
    menu = st.sidebar.selectbox(
        'Navigation',
        ['Home', 'collected hotel data', 'Display Hotel Data', 'Display hotel reviews Datasets', 'CSV Column Concatenation and Sentiment Analysis']
    )

    if menu == 'Home':
        st.markdown(project_description)

    elif menu == 'collected hotel data':
        # Display DataFrame
        df = pd.read_csv('chennai hotes.csv')
        df1 = pd.read_csv('stream.csv')
        st.subheader('Collected chennai hotes Data')
        st.write(df)
        st.subheader('preprocess applyed data')
        st.write(df1)

    elif menu == 'Display Hotel Data':
        # Display hotel data
        df = pd.read_csv('stream.csv')
        css = """
            <style>
                .hotel-container {
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 10px;
                    margin-bottom: 20px;
                }
                .hotel-image {
                    max-width: 100%;
                    border-radius: 5px;
                    margin-bottom: 10px;
                }
                .hotel-details {
                    font-size: 16px;
                }
            </style>
        """
        st.markdown(css, unsafe_allow_html=True)
        for index, row in df.iterrows():
            st.markdown(f"""
        <div class="hotel-container">
            <img class="hotel-image" src="{row['hotel image']}">
            <div class="hotel-details">
                <h2>{row['Hotel Name']}</h2>
                <p><strong>Rating:</strong> {row['rating']}</p>
                <p><strong>Location:</strong> {row['location']} ({row['nearest places']})</p>
                <p><strong>Website:</strong> <a href="{row['hotel website']}">Website link</a></p>
                <p><strong>Number of Reviews:</strong> {row['number of reviewss 2']}</p>
                <p><strong>Room Type:</strong> {row['room type']}</p>
                <p><strong>Price:</strong> {row['price']}</p>
                <p><strong>Strengths:</strong> {row['Strengths']}</p>
                <p><strong>Weaknesses:</strong> {row['Weaknesses']}</p>
            </div>
        </div>
       """, unsafe_allow_html=True)


    elif menu == 'Display hotel reviews Datasets':
        selected_dataset = st.selectbox('Select Dataset', csv_files)
        if selected_dataset:
            display_selected_dataset(selected_dataset)

    elif menu == 'CSV Column Concatenation and Sentiment Analysis':
        st.title('CSV Column Concatenation and Sentiment Analysis')

        new_names = {
            'a3332d346a': 'Reviewer Name',
            'afac1f68d9': 'Reviewer Country',
            'abf093bdfe': 'Room Type',
            'abf093bdfe 2': 'Length of Stay',
            'abf093bdfe 3': 'Review Date',
            'abf093bdfe 4': 'Traveler Type',
            'abf093bdfe 5': 'Second Review Date',
            'f6431b446c': 'Overall Rating',
            'a53cbfa6de': 'Positive Comments',
            'a53cbfa6de 2': 'Negative Comments',
            'a3332d346a 2': 'Hotel Response',
            'a53cbfa6de 3': 'Hotel Response1'
        }

        # File upload
        uploaded_file = st.file_uploader('Upload CSV file', type=['csv'])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            df.rename(columns=new_names, inplace=True)

            # Show original DataFrame
            st.subheader('Original DataFrame:')
            st.write(df)

            # Select columns
            selected_columns = st.multiselect('Select columns to concatenate', df.columns)

            if st.button('Concatenate columns'):
                if len(selected_columns) == 2:
                    # Concatenate columns
                    new_df = concatenate_columns(df, selected_columns)

                    # Remove null values
                    new_df = new_df.dropna()

                    # Drop duplicates
                    new_df = new_df.drop_duplicates()

                    # Reset the index
                    new_df = new_df.reset_index(drop=True)

                    # Clean tweets
                    new_df['CleanedData'] = clean_tweets(new_df['ConcatenatedData'])

                    # Load the saved model
                    loaded_model = joblib.load('sentiment_analysis_model.pkl')

                    # Apply sentiment analysis
                    new_df['Sentiment'] = loaded_model.predict(new_df['CleanedData'])

                    # Display concatenated, cleaned, and sentiment analyzed DataFrame
                    st.subheader('Concatenated, Cleaned, and Sentiment Analyzed DataFrame:')
                    st.write(new_df)

                    # Create download link
                    st.markdown(create_download_link(new_df, 'concatenated_sentiment_analyzed_data'), unsafe_allow_html=True)
                else:
                    st.warning('Please select exactly two columns to concatenate.')

# Run the app
if __name__ == '__main__':
    main()
