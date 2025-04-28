# AI-powered-data-cleaning-and-manipulation-chatbot
# AI Driven Data Quality Enhancement / Data Cleaning

## Project description:
This project involves creating an AI-powered data cleansing web application using the Gemini model and Django framework, allowing users to clean and preprocess data through simple, natural language commands. Users can upload CSV or Excel files up to 10 MB in size, preview their datasets, and input cleaning instructions like "remove duplicates" or "fill missing values with zeros." The Gemini model interprets these instructions and automatically generates the necessary Python code, which Django then uses to perform the requested data cleaning tasks. This setup is designed to help users without programming skills efficiently prepare and improve the quality of their datasets.

The application provides an intuitive user interface for seamless data uploading, previewing, and downloading of cleaned data. Built with Django and powered by the Gemini model for natural language processing, the platform emphasizes accessibility and ease of use, ensuring a smooth experience even for users new to data manipulation. By addressing data inaccuracies and inconsistencies, the application saves time and empowers users to achieve higher data quality through AI-driven solutions.

## Repositories structure:

```bash

AI02_data_cleansing/
├── manage.py                    # Django project management script
├── requirements.txt             # Python dependencies (Django, Gemini model, Pandas, etc.)
├── .env                         # Environment variables (e.g., secret keys, API keys)
├── README.md                    # Project documentation
├── data_cleaning_project/       # Main project configuration folder
│   ├── __init__.py
│   ├── settings.py              # Core settings (database, installed apps, etc.)
│   ├── urls.py                  # Project-level URL routing
│   ├── wsgi.py                  # WSGI entry point for deployment
│   └── __pycache__/             # Compiled Python files for performance
│                                # (Auto-generated __pycache__ files)
│
├── data_cleaning_app/           # Main application for data cleansing
│   ├── __init__.py
│   ├── admin.py                 # Django admin interface (if needed)
│   ├── apps.py                  # Application configuration
│   ├── models.py                # Database models (e.g., for file uploads)
│   ├── views.py                 # Handles file upload, preview, and data cleaning
│   ├── urls.py                  # Application-specific URL routing
│   ├── forms.py                 # Django forms for file upload and data preview
│   ├── data_cleaning.py         # Contains functions to interpret commands & clean data
│   ├── tests/                   # Folder containing unit test cases for this app
│   │   ├── data_clean_tests.py  # Unit tests for data cleaning functionality
│   │   └── views_tests.py       # Unit tests for views handling file uploads and data previews
│   └── __pycache__/             # Compiled Python files for performance
│                                # (Auto-generated __pycache__ files)
│
├── templates/                   # Global templates folder for HTML templates
│   ├── clean_data.html          # Data cleansing page
│   ├── upload.html              # File upload page
│   └── instructions.html        # Instructions page
│       
├── static/                      # Static files directory for images and other assets
│   └── images/                  # Folder for storing images
│                                # (Add image files here)
│
└── Unittest.py                  # Main file to run unit tests                             

```

## Configuring and running the project locally:
1.**Prerequisites**    
    Install Python 3.11.9 version    
    Install Git    
  
2.**Clone the Repository**  
    Clone the repository to your local machine:  
    ``bash   
    git clone gitclonehttps://shriram_b@bitbucket.org/intelligentpathways/ai02_data_cleansing.git   
    cd AI02_data_cleansing  
  
3.**Create a Virtual Environment**  
    Create a virtual environment for managing dependencies:  
    ``bash   
    python -m venv venv   
    source venv/bin/activate    # On Windows usevenv\Scripts\activate`  
  
4.**Install Dependencies**  
    Install the required Python packages using pip:  
    ``bash pip install -r requirements.txt       
    Use python version 3.11.9.  
  
5.**Setting Up the `.env` File**  
    Create a new file named `.env` in the root directory of the project.  
    Retrieve your Google Gemini API key from Google Studio, then add it to your .env file as follows:    
    API_KEY="your_api_key_here"  
    Save the .env file once done.    
  
6.**Run the Application**  
    Start the Django application:  
    ``bash python manage.py runserver  
  
7.**Access the Application**  
    Open your web browser and go to http://127.0.0.1:8000 to access the application. You can enter data through the input form or upload a CSV file to get predictions.  

  
## Unit Testing:

| Test ID | Function              | Test Case                                         | Steps Involved                                                                                                                                               | Expected Result                                                        | Pass/Fail |
|---------|------------------------|---------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------|-----------|
| TC_001  | `get_data_info`        | Verify DataFrame info for CSV input               | 1. Create a CSV string input for `get_data_info`. <br> 2. Call `get_data_info` with CSV content and `.csv` extension. <br> 3. Assert that "DataFrame Info:" is in the result.                        | The result should contain "DataFrame Info:" indicating that the CSV data was successfully processed into a DataFrame.                                  | Pass      |
| TC_002  | `get_data_info`        | Handle unsupported file extension                 | 1. Call `get_data_info` with CSV-like content but `.txt` as the extension. <br> 2. Assert that it raises a `ValueError` with the message "Unsupported file type. Only CSV files are supported."     | A `ValueError` should be raised, indicating the file type is unsupported.                                                                               | Pass      |
| TC_003  | `get_data_info`        | Verify DataFrame info for bytes input             | 1. Create a byte format CSV string input for `get_data_info`. <br> 2. Call `get_data_info` with the byte content and `.csv` extension. <br> 3. Assert that "DataFrame Info:" is in the result.     | The result should contain "DataFrame Info:" indicating that the byte-encoded CSV data was successfully processed.                                      | Pass      |
| TC_004  | `generate_pandas_code` | Generate code for filtering rows                  | 1. Provide CSV content and a prompt to `generate_pandas_code`. <br> 2. Verify that the output contains a filter code for rows where age > 30.                | The generated code should contain `df[df['age'] > 30]`.                                                                                            | Pass      |
| TC_005  | `generate_pandas_code` | Handle no code generation                         | 1. Provide CSV content and a prompt that doesn't require code (e.g., "Describe the data"). <br> 2. Assert that the result is "No code found."                | The result should be "No code found," indicating no code generation was necessary.                                                                   | Pass      |
| TC_006  | `generate_pandas_code` | Exception handling in code generation             | 1. Provide CSV content and a prompt. <br> 2. Call `generate_pandas_code` and verify that a result is returned without raising errors.                       | A valid result should be returned without any exceptions.                                                                                             | Pass      |
| TC_007  | `execute_generated_code` | Execute generated code to add a new column      | 1. Create a DataFrame from CSV content. <br> 2. Use `execute_generated_code` to run code adding an "age_plus_5" column. <br> 3. Assert the presence of "age_plus_5" with values correctly incremented by 5. | The DataFrame should have a new "age_plus_5" column with correct values (e.g., `35` for the first row).                                               | Pass      |
| TC_008  | `execute_generated_code` | Execute generated code to filter rows           | 1. Create a DataFrame from CSV content. <br> 2. Use `execute_generated_code` to run code that filters rows where age > 30. <br> 3. Assert that only one row remains with `name` = "Charlie".       | Only one row should remain with `name` equal to "Charlie".                                                                                           | Pass      |
| TC_009  | `execute_generated_code` | Execute code with LLM correction for syntax error | 1. Create a DataFrame. <br> 2. Introduce an intentional syntax error in code (e.g., `df['C'] = df['A'] + df['B"`). <br> 3. Call `execute_generated_code` and verify that LLM corrects and adds "C" as sum of A and B in the DataFrame. | LLM should correct the syntax and successfully add a column "C" with values as the sum of "A" and "B" (`5, 7, 9`).                                   | Pass      |
| TC_010  | `handle_error_with_llm` | Correct faulty code with LLM assistance          | 1. Provide a DataFrame and a faulty code string with a syntax error. <br> 2. Define the correct code. <br> 3. Call `handle_error_with_llm` with an error message and faulty code, then assert correction matches the expected result. | LLM should generate the corrected code `df['C'] = df['A'] + df['B']`, fixing the syntax error, and return the modified code.                         | Pass      |
| TC_011  | `upload_file_valid_csv`        | Test upload with a valid CSV file                 | 1. Create a sample CSV file. <br> 2. Post file to `upload_url`. <br> 3. Check response status and context keys for `table`, `shape`, and `info`.             | Status code 200 with context keys `table`, `shape`, and `info` indicating successful file upload and parsing. | Pass      |
| TC_012  | `upload_file_valid_excel`      | Test upload with a valid Excel file               | 1. Create a DataFrame and save it as Excel. <br> 2. Post file to `upload_url`. <br> 3. Check response status and context keys for `table`, `shape`, and `info`. | Status code 200 with context keys `table`, `shape`, and `info` confirming successful Excel file upload.        | Pass      |
| TC_013  | `upload_file_invalid_file_type` | Test upload with an invalid file type             | 1. Create a sample `.txt` file. <br> 2. Post file to `upload_url`. <br> 3. Check response status and for error message "Unsupported file type."             | Status code 200 with `error` context, error message "Unsupported file type."                                  | Pass      |
| TC_014  | `upload_file_exceeds_size_limit` | Test upload with file exceeding size limit       | 1. Create a CSV file exceeding 10 MB. <br> 2. Post file to `upload_url`. <br> 3. Check for error message about file size.                                   | Status code 200 with `error` context, error message "File size exceeds the 10 MB limit."                       | Pass      |
| TC_015  | `clean_data_with_query`         | Test cleaning data with a valid query             | 1. Upload a CSV file. <br> 2. Post a data-cleaning query to `clean_url`. <br> 3. Check for `cleaned_data` and `query_history` in response context.           | Status code 200 with `cleaned_data` and `query_history` in context, indicating successful cleaning.           | Pass      |
| TC_016  | `clean_data_without_query`      | Test cleaning data without a query               | 1. Upload a CSV file. <br> 2. Post an empty query to `clean_url`. <br> 3. Check for error message "Please provide a query."                                | Status code 200 with `error` context, error message "Please provide a query."                                 | Pass      |
| TC_017  | `clean_data_with_invalid_query` | Test cleaning with an invalid query              | 1. Upload a CSV file. <br> 2. Post an invalid query to `clean_url`. <br> 3. Check for error context with relevant message about cleaning query.            | Status code 200 with `error` context, error message for invalid query related to data cleaning.               | Pass      |
| TC_018  | `download_cleaned_data_csv`     | Test downloading cleaned data as CSV             | 1. Upload and clean a CSV file. <br> 2. Send GET request to `download_url`. <br> 3. Check response for CSV content type and filename.                      | Status code 200, Content-Type `text/csv`, and Content-Disposition header with filename `cleaned_data.csv`.    | Pass      |
| TC_019  | `download_cleaned_data_no_data` | Test download request without data               | 1. Send GET request to `download_url` without uploading or cleaning data. <br> 2. Check response content for no data message.                               | Status code 200, response message "No cleaned data available for download."                                  | Pass      |
| TC_020  | `instructions_page`             | Test accessing the instructions page             | 1. Send GET request to `instructions_url`. <br> 2. Check response status and if template `instructions.html` is used.                                       | Status code 200 and usage of `instructions.html` template.                                                   | Pass      |


## Application Screenshots    

### Upload Page      

This is the **Upload Page** where users can upload CSV or Excel files to start the data cleaning process. The interface allows users to drag and drop their files or use a file picker.    

![Upload Page](application_images/web1.PNG)    

After the file is uploaded, the **Data Preview** section provides users with a preview of the uploaded data. Users can check if the data looks correct before proceeding with the cleaning process.    

![Upload Page](application_images/web2.PNG)    

### Data Cleaning Page    
  
The **Data Cleaning Page** shows the main interface for cleansing data. Users can see a preview of the data, apply cleaning operations, and view the results. The data is displayed in a table format for easy review.  
  
![Data Cleaning Page](application_images/web3.PNG)      
  
In this step, users can apply various data cleaning actions, such as:  
- Removing duplicates  
- Filling missing values  
- Normalizing text  
- Filtering specific rows or columns  
  
Once the data has been cleaned, users can preview the results in the table.      

![Data Cleaning Page](application_images/web4.PNG)    
 
After the data has been cleaned, users can download the cleaned data in **CSV** format by clicking the **Download** button. This allows users to save their cleaned data locally and use it in further analysis or reporting.  
  
![Data Cleaning Page](application_images/web5.PNG)  
  
### Instructions Page      
  
![Data Preview](application_images/web6.PNG)  

The **Instructions Page** guides user to write the user query for data cleaning.
