import streamlit as st
from app.auth import initialize_app, authentication_process, get_user_id
from app import db
import vertexai
import os

from langchain_google_vertexai import VertexAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.schema import HumanMessage, AIMessage

# Environment variable setup for Vertex AI
PROJECT_ID = os.environ.get('PROJECT_ID')
REGION = os.environ.get('REGION')
MODEL_NAME = os.environ.get('MODEL_NAME')
vertexai.init(project=PROJECT_ID, location=REGION)  

# Initialize VertexAI model
model = VertexAI(
    model_name=MODEL_NAME,
    max_output_tokens=8192,  # Ensure appropriate output length
    temperature=1.0,         # Control response randomness
    top_p=0.95               # Adjust probability sampling
)

# Tool: Fetch Leave Balance
def fetch_leave_balance(input=None):
    """Fetches the user's leave balance from the database."""
    conn = db.connect_to_db()
    if conn:
        try:
            user_id = get_user_id()
            if user_id:
                leave_balance = db.fetch_user_leave_balance(conn, user_id)
                if leave_balance:
                    response = "Your leave balance:\n\n"
                    for leave_type, available, used in leave_balance:
                        response += f"- {leave_type}: Available: {available}, Used: {used}\n"
                    return response
                return "No leave balance found for your account."
            return "User ID not found. Please log in again."
        except Exception as e:
            return f"Error fetching leave balance: {e}"
        finally:
            conn.close()
    return "Failed to connect to the database."

# Tool: Submit Leave Request
def submit_leave_request(input=None):
    """Submits a leave request (placeholder implementation)."""
    return "Submit leave functionality is not yet implemented."

# Define tools for function calling
tools = [
    Tool(
        name="get_leave_balance",
        func=fetch_leave_balance,
        description="Fetch the user's leave balance."
    ),
    Tool(
        name="submit_leave_request",
        func=submit_leave_request,
        description="Submit a leave request for the user."
    )
]

# Define a prompt template
prompt_template = """
You are an HR assistant. Based on the user's input, identify the intent and call the appropriate tool.
Available tools:
1. get_leave_balance: Fetch user's leave balance.
2. submit_leave_request: Submit a leave request.

Respond clearly and appropriately based on the user's query.

User Input:
{query}
"""

def main():
    """
    Main function for the HR Leave Application Streamlit app.
    """
    
    # Set up the page configuration
    st.set_page_config(page_title="HR Leave App", page_icon=":date:")
    
    # Sidebar for user authentication
    st.sidebar.title("Login")

    # Ensure session state for authentication
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    # Authentication process
    if not st.session_state["authenticated"]:
        app = initialize_app()
        if app is not None:
            auth_result = authentication_process(app)
            if auth_result:
                user_data, token = auth_result
                st.session_state["authenticated"] = True
                st.session_state["display_name"] = user_data.get("displayName")
                st.session_state["user_id"] = user_data.get("id")
                st.session_state["token"] = token
                st.rerun()
        return

    # Chat Interface
    st.title("HR Leave Chatbot")
    st.sidebar.write(f"Welcome, {st.session_state['display_name']}")

    # Initialize message history
    if "messages" not in st.session_state:
        st.session_state["messages"] = [AIMessage(content="How can I help you with your leave today?")]

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message("assistant" if isinstance(message, AIMessage) else "user"):
            st.markdown(message.content)

    # User Input
    if prompt := st.chat_input("Enter your query"):
        st.session_state.messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Agent Setup: Function Calling
        agent = initialize_agent(
            tools=tools,
            llm=model,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

        # Call agent to determine the response
        try:
            tool_response = agent.run(prompt)
        except Exception as e:
            tool_response = f"An error occurred: {e}"

        # Append and display assistant response
        st.session_state.messages.append(AIMessage(content=tool_response))
        with st.chat_message("assistant"):
            st.markdown(tool_response)

# Entry point for the application            
if __name__ == "__main__":
    main()