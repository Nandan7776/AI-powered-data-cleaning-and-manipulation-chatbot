import logging
import re
import pandas as pd
from io import StringIO, BytesIO
import chardet
import os
import google.generativeai as genai
import time
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def get_data_info(file_content, file_ext):
    logging.debug(f"Received file with extension {file_ext}")

    # Ensure file_content is a string
    if isinstance(file_content, bytes):
        file_content = file_content.decode('utf-8')  # Convert bytes to string

    # Read the file content into DataFrame
    if file_ext == '.csv':
        df = pd.read_csv(StringIO(file_content))
        logging.info("CSV file successfully read into DataFrame")
    else:
        logging.error("Unsupported file type. Only CSV files are supported.")
        raise ValueError("Unsupported file type. Only CSV files are supported.")

    # Get DataFrame info
    buf = StringIO()
    df.info(buf=buf)
    df_info = buf.getvalue()
    logging.debug("Generated DataFrame info")

    # Get a sample of the data (5 random rows)
    sample_data = df.head(5).to_string(index=False)
    logging.debug("Generated sample data")

    # Combine DataFrame info and sample data
    combined_info = f"DataFrame Info:\n{df_info}\n\nSample Data (5 random rows):\n{sample_data}"
    
    return combined_info


    
def generate_pandas_code(prompt, data_info,  retries=3):
    logging.debug("Initializing Google Generative AI client")


    system_instruction = f"""Based on the dataset information provided, you are a highly knowledgeable data scientist tasked with generating the exact Python pandas code needed to fulfill the user's request.
    
If the user's request is related to cleaning, processing, or transforming data (like handling missing values, duplicates, or formatting issues), generate the exact pandas code needed.

However, if the request is not related to data cleaning, reply with: "Please provide a query related to data cleaning."

Dataset summary (including sample data):
{data_info}


User query: "{prompt}"

Return either only the functional pandas code for cleaning the data or a message asking for a cleaning-related query."""

    for attempt in range(retries):
        try:
            # Initialize the Google Generative AI client
            genai.configure(api_key= os.getenv('API_KEY'))
            model = genai.GenerativeModel(model_name='gemini-1.5-pro')

            logging.debug("Sending prompt to Google Generative AI")

            # Generate content by passing the system_instruction as 'contents'
            response = model.generate_content(contents=[system_instruction])
            logging.debug("Received response from Google Generative AI")

            # Extract generated content
            if response.candidates:
                full_response = response.candidates[0].content.parts[0].text
                logging.debug("Full response: " + full_response)

                if "Please provide a query related to data cleaning" in full_response:
                    logging.info("The query was not related to data cleaning.")
                    return "No code found."

                # Extract code using regular expressions
                code_blocks = re.findall(r"```(?:python)?\n(.*?)```", full_response, re.DOTALL)
                logging.debug(f"Extracted code blocks: {code_blocks}")

            if code_blocks:
                pandas_code = code_blocks[0].strip()
                logging.info("Pandas code extracted successfully")
                return pandas_code
            else:
                logging.warning("No code found in the response.")
                return "No code found."
        
        except Exception as e:
            logging.error(f"Error during code generation attempt {attempt+1}: {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return f"Error in generating code: " + str(e)



def execute_generated_code(code, df):
    logging.debug("Cleaning and preparing code for execution")
    
    # Ensure the code only operates on the provided DataFrame
    if 'pd.DataFrame' in code or 'read_csv' in code or 'read_excel' in code:
        code = re.sub(r'pd\.DataFrame\(.*?\)', 'df', code)
        code = re.sub(r'pd\.read_csv\(.*?\)', 'df', code)
        code = re.sub(r'pd\.read_excel\(.*?\)', 'df', code)
        logging.debug(f"Modified code: {code}")

    # Define a restricted local environment for the exec function
    local_scope = {'df': df, 'pd': pd}

    try:
        # Execute the cleaned code
        logging.debug("Executing generated code")
        exec(code, {}, local_scope)
        
        # Check if `df` was modified and return the cleaned DataFrame
        if 'df' in local_scope:
            logging.info("Code executed successfully, returning modified DataFrame")
            return local_scope['df']
        else:
            logging.warning("DataFrame not found after code execution.")
            return None
    except Exception as e:
        logging.error(f"An error occurred while executing the code: {e}")
        return None
