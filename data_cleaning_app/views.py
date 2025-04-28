from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
import pandas as pd
import chardet
import io
import os
from io import StringIO, BytesIO
from .forms import UploadFileForm
from .data_cleaning import get_data_info, generate_pandas_code, execute_generated_code


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_name = file.name
            file_ext = os.path.splitext(file_name)[1].lower()

            # Set a maximum file size limit (10 MB)
            max_file_size = 10 * 1024 * 1024  # 10 MB in bytes

            # Check file size before reading its content
            if file.size > max_file_size:
                return render(request, 'upload.html', {
                    'form': form,
                    'error': 'File size exceeds the 10 MB limit. Please upload a smaller file.'
                })

            # Reset query history and cleaned data when uploading a new file
            request.session['query_history'] = []
            request.session['cleaned_data'] = None

            try:
                # Handle CSV files
                if file_ext == '.csv':
                    # Read only after size check
                    file_content = file.read()

                    # Detect encoding with chardet
                    detector = chardet.universaldetector.UniversalDetector()
                    detector.feed(file_content)
                    detector.close()
                    encoding = detector.result['encoding']

                    # Read CSV file with detected encoding
                    df = pd.read_csv(io.StringIO(file_content.decode(encoding)))

                    # Store file content in session
                    request.session['uploaded_file_content'] = file_content.decode(encoding)

                # Handle Excel files
                elif file_ext in ['.xls', '.xlsx']:
                    # Read only after size check
                    file_content = file.read()

                    # Read Excel file
                    df = pd.read_excel(io.BytesIO(file_content))
                    csv_buffer = StringIO()
                    df.to_csv(csv_buffer, index=False)
                    csv_content = csv_buffer.getvalue()

                    # Store CSV content in session
                    request.session['uploaded_file_content'] = csv_content

                else:
                    return render(request, 'upload.html', {'form': form, 'error': 'Unsupported file type.'})

                # Store metadata about the uploaded file
                request.session['uploaded_file_name'] = file_name
                request.session['uploaded_file_ext'] = '.csv'  # Treat as CSV after conversion

                # Get DataFrame information (rows, columns)
                shape = df.shape
                shape_text = f"Rows: {shape[0]}, Columns: {shape[1]}"

                # Data info: column names, null values, and data types
                info = pd.DataFrame({
                    'Column Name': df.columns,
                    'Null Values': df.isnull().sum(),
                    'Data Type': df.dtypes
                }).to_html(classes='table table-striped', index=False)

                # Convert DataFrame to HTML for preview
                html_table = df.to_html(classes='table table-striped', index=False)

                return render(request, 'upload.html', {
                    'form': form,
                    'table': html_table,
                    'shape': shape_text,
                    'info': info,
                    'cleaning_link': True  # Indicates the link to proceed to cleaning
                })
            except Exception as e:
                return render(request, 'upload.html', {'form': form, 'error': f'Error reading file: {e}'})
        else:
            return render(request, 'upload.html', {'form': form, 'error': 'Form is not valid.'})
    else:
        form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})


def clean_data(request):
    if request.method == 'POST':
        user_query = request.POST.get('user_query')
        file_ext = request.session.get('uploaded_file_ext', None)
        cleaned_data = request.session.get('cleaned_data', None)
        file_content = request.session.get('uploaded_file_content', None)

        if not user_query:
            return render(request, 'clean_data.html', {'error': 'Please provide a query.'})

        try:
            # Determine whether to use cleaned data or original data
            if cleaned_data:
                # Load the DataFrame from cleaned data in session
                if file_ext == '.csv':
                    df = pd.read_csv(io.StringIO(cleaned_data))
                elif file_ext in ['.xls', '.xlsx']:
                    df = pd.read_excel(io.BytesIO(cleaned_data.encode('utf-8')))
                else:
                    return render(request, 'clean_data.html', {'error': 'Unsupported file type.'})
            else:
                # Load the DataFrame from original uploaded content
                if file_ext == '.csv':
                    df = pd.read_csv(io.StringIO(file_content))
                elif file_ext in ['.xls', '.xlsx']:
                    df = pd.read_excel(io.BytesIO(file_content.encode('utf-8')))
                else:
                    return render(request, 'clean_data.html', {'error': 'Unsupported file type.'})

            # Get DataFrame info
            data_info = get_data_info(df.to_csv(index=False).encode('utf-8'), file_ext)

            # Generate Pandas code based on user query
            generated_code = generate_pandas_code(user_query, data_info)

            if "Error" not in generated_code and "No code found" not in generated_code:
                # Execute the generated code
                cleaned_df = execute_generated_code(generated_code, df)

                if cleaned_df is not None:
                    # Convert cleaned DataFrame to HTML for preview
                    cleaned_html_table = cleaned_df.to_html(classes='table table-striped', index=False)

                    # Store the cleaned data in session as a string (to continue working with it later)
                    if file_ext == '.csv':
                        cleaned_data_str = cleaned_df.to_csv(index=False)
                    elif file_ext in ['.xls', '.xlsx']:
                        cleaned_data_str = cleaned_df.to_excel(index=False)

                    # Update session with cleaned data
                    request.session['cleaned_data'] = cleaned_data_str

                    # Store the query and generated code in session
                    query_history = request.session.get('query_history', [])
                    query_history.append({'user_query': user_query, 'generated_code': 'Data Cleaning is Successful!'})
                    request.session['query_history'] = query_history

                    return render(request, 'clean_data.html', {
                        'query_history': query_history,
                        'cleaned_data': cleaned_html_table,
                        'download_link': True  # Indicate a link to download the cleaned data
                    })
                else:
                    return render(request, 'clean_data.html', {'error': 'Error executing the generated code.'})
            else:
                return render(request, 'clean_data.html', {'error': 'Please provide a query related to data cleaning.'})
        except Exception as e:
            return render(request, 'clean_data.html', {'error': f'Error during data cleaning: {e}'})
    else:
        # Handling GET request
        query_history = request.session.get('query_history', [])
        file_ext = request.session.get('uploaded_file_ext', None)

        if file_ext and request.session.get('uploaded_file_content'):
            try:
                # Load the DataFrame from session content
                if file_ext == '.csv':
                    df = pd.read_csv(io.StringIO(request.session['uploaded_file_content']))
                elif file_ext in ['.xls', '.xlsx']:
                    df = pd.read_excel(io.BytesIO(request.session['uploaded_file_content'].encode('utf-8')))
                else:
                    return render(request, 'clean_data.html', {'error': 'Unsupported file type.'})

                # Render uploaded data for preview
                uploaded_data = df.to_html(classes='table table-striped', index=False)
                return render(request, 'clean_data.html', {
                    'query_history': query_history,
                    'uploaded_data': uploaded_data
                })
            except Exception as e:
                return render(request, 'clean_data.html', {'error': f'Error reading uploaded file: {e}'})

        return render(request, 'clean_data.html', {'query_history': query_history})

def download_cleaned_data(request):
    file_ext = request.session.get('uploaded_file_ext', None)
    cleaned_data = request.session.get('cleaned_data', None)

    if not cleaned_data:
        return HttpResponse("No cleaned data available for download.")

    try:
        if file_ext == '.csv':
            response = HttpResponse(cleaned_data, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=cleaned_data.csv'
        elif file_ext in ['.xls', '.xlsx']:
            # Use BytesIO to create an in-memory file-like object
            output = io.BytesIO()
            if file_ext == '.xls':
                with pd.ExcelWriter(output, engine='xlwt') as writer:
                    pd.read_excel(io.BytesIO(cleaned_data.encode('utf-8'))).to_excel(writer, index=False)
            elif file_ext == '.xlsx':
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    pd.read_excel(io.BytesIO(cleaned_data.encode('utf-8'))).to_excel(writer, index=False)
            output.seek(0)  # Ensure the BytesIO object is at the start
            response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=cleaned_data.xlsx'
        else:
            return HttpResponse("Unsupported file type for download.")

        return response
    except Exception as e:
        return HttpResponse(f"Error downloading file: {e}")
    
  

def instructions(request):
    return render(request, 'instructions.html')
