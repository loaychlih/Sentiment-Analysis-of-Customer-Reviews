import streamlit as st
import pandas as pd
from langchain.llms import Ollama
from pandasai import SmartDataframe
import os
import shutil  

# Function to clear the chart directory
def clear_chart_directory(chart_path):
    if os.path.exists(chart_path):
        shutil.rmtree(chart_path)  
        os.makedirs(chart_path) 

# Function to analyze data with PandasAI
def analyze_data_with_pandasai(data):
    try:
        llm = Ollama(model="mistral")  
        st.write(data.head(3))  

        smart_df = SmartDataframe(data, config={"llm": llm})
        prompt = st.text_area("Enter your prompt for data analysis (e.g., 'How many rows?' or 'Plot distribution of column X'):")

        if st.button("Generate"):
            if prompt:
                chart_path = "exports/charts"
                clear_chart_directory(chart_path)  # Clear the old plots

                with st.spinner("Generating response..."):
                    # Generate response from PandasAI
                    result = smart_df.chat(prompt)
                    

                    # Check if a new plot has been saved in the chart directory
                    if os.path.exists(chart_path):
                        image_files = [f for f in os.listdir(chart_path) if f.endswith(".png")]

                        # Only display the image if a PNG file is found
                        if image_files:
                            image_path = os.path.join(chart_path, image_files[0])  # Get the first image
                            st.image(image_path, caption="Generated Chart")
                        else:
                            st.write(result)  # Display textual result
                    else:
                        st.info("No chart directory found, so no image is displayed.")
            else:
                st.warning("Please enter a prompt!")
    except Exception as e:
        st.error("An error occurred while processing your request. Please try again with a different prompt.")

# Main Streamlit app for CSV data analysis
def main():
    st.set_page_config(page_title="Analyze CSV with PandasAI")
    st.title("Analyze CSV Data with PandasAI 💡")

    # File uploader for CSV files
    st.header("Upload CSV File for Data Analysis")
    csv_file = st.file_uploader("Select CSV file", type="csv")

    # Analyze CSV with PandasAI
    if csv_file:
        df = pd.read_csv(csv_file)
        analyze_data_with_pandasai(df)

if __name__ == "__main__":
    main()
