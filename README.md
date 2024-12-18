# HR Leave Checking Application

## Overview

The HR Leave Checking Application is a Streamlit-based chatbot app designed to simplify employee interactions regarding leave balance and leave requests. It integrates with Google Vertex AI and uses LangChain to handle user queries through a function-calling mechanism. The app also includes a secure login process using Azure AD authentication.

## Features

- **Leave Balance Inquiry**: Retrieve detailed leave balance information for the authenticated user.
- **Leave Request Submission**: (Future Implementation) Submit leave requests through the app.
- **Secure Authentication**: Login process integrated with Azure Active Directory.
- **Chat Interface**: User-friendly chat interface for seamless interaction.
- **Google Vertex AI Integration**: Uses Vertex AI for language model functionality.
- **Cloud Run Deployment**: Easily deployable to Google Cloud Run.

## Technologies Used

- **Streamlit**: For the app's user interface.
- **Google Vertex AI**: To handle natural language processing and response generation.
- **LangChain**: For function calling and tool integration.
- **Azure Active Directory**: For user authentication.
- **Python**: Core programming language for the application.
- **PostgreSQL**: For database management.
- **Google Cloud Run**: For serverless deployment.

## Setup Instructions

### Prerequisites

1. Python 3.8 or higher installed.
2. Access to Google Cloud Project with Vertex AI and Cloud Run enabled.
3. Azure Active Directory app registration for authentication.
4. PostgreSQL database setup for storing user leave balance information.

### Environment Variables

Set the following environment variables in your system:

- `PROJECT_ID`: Your Google Cloud Project ID.
- `REGION`: The region for Vertex AI.
- `MODEL_NAME`: The name of your Vertex AI model.
- `POSTGRES_HOST`: Hostname or IP address of your PostgreSQL database.
- `POSTGRES_DB`: Name of the PostgreSQL database.
- `POSTGRES_USER`: Username for the PostgreSQL database.
- `POSTGRES_PASSWORD`: Password for the PostgreSQL database.
- `CLIENT_ID`: Azure AD client ID.
- `TENANT_ID`: Azure AD tenant ID.
- `CLIENT_SECRET`: Azure AD client secret (stored in Secret Manager).
- `REDIRECT_URI`: Redirect URI for Azure AD authentication.

### Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd hr-leave-langchain
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application locally:

   ```bash
   streamlit run main.py
   ```

### Deploying to Google Cloud Run
The service can be deployed on Google Cloud Run. Detailed deployment steps and configurations will be outlined in the blog (link to be provided later).

## Usage

1. Navigate to the app in your browser using the Cloud Run URL.
2. Log in using your Azure AD credentials via the sidebar.
3. Use the chat interface to:
   - Query leave balances by asking questions like "What is my leave balance?"
   - Submit leave requests (functionality under development).

## Code Structure

- **main.py**: Entry point for the Streamlit application.
- **app/auth.py**: Handles Azure AD authentication processes.
- **app/db.py**: Database connection and query utilities.

## Tools Defined

1. **get\_leave\_balance**: Fetches the user's leave balance.
2. **submit\_leave\_request**: Placeholder for leave request submission functionality.


## Acknowledgments

The Azure AD authentication was inspired by and incorporates ideas from Parham's great blog post:
- [Streamlit login with Azure AD Authentication](https://medium.com/@prhmma/streamlit-login-with-azure-ad-authentication-66ebd1691858)
- [GitHub Repository: Streamlit Authentication with Azure AD](https://github.com/Prhmma/Streamlit_Azure_AD)

