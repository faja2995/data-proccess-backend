# CSV/Excel Data Type Inference and Manual Type Change Django Project

## Overview
This Django project allows users to upload CSV or Excel files, where the application then infers the data types of the columns automatically. Users have the option to manually change the inferred data types if needed. 

## Features
- **File Upload**: Users can upload CSV or Excel files through a user-friendly interface.
- **Automatic Data Type Inference**: Upon file upload, the application automatically infers the data types of the columns.
- **Manual Type Change**: Users have the ability to manually change the data types if they disagree with the inferred types.
- **Export**: The application enables users to export the modified data with specified data types.

## Installation

1. Clone this repository to your local machine:

    ```bash
    git clone <repository_url>
    ```

2. Navigate to the project directory:

    ```bash
    cd <project_directory>
    ```

2. Create a virtual envirenment:

    ```bash
    python -m venv <your_env_name>
    #linux
    source <your_env_name>/bin/activate
    #windows
    <your_env_name>\Scripts\activate.bat
    ```

4. Install the required dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the Django development server:

    ```bash
    python manage.py runserver
    ```

2. Access the application through your web browser at `http://127.0.0.1:8000`.

3. Upload your CSV or Excel file using the provided interface.

4. Review the inferred data types and make manual changes if necessary.

5. Export the modified data with specified data types.

