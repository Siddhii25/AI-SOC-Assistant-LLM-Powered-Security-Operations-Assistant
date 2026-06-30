import streamlit as st
from agent.planner import Agent
from chat.conversation import ConversationManager

# Configure the Streamlit application
st.set_page_config(
    page_title="AI SOC Assistant",
    page_icon="🤖"
)
st.title("🤖 AI SOC Assistant")

# Create session objects only once
if "conversation" not in st.session_state:
    st.session_state.conversation = ConversationManager()

if "agent" not in st.session_state:
    st.session_state.agent = Agent()


conversation = st.session_state.conversation
agent = st.session_state.agent


# Display the previous conversation
for message in conversation.get_messages():

    with st.chat_message(message["role"]):
        st.write(message["content"])


# Accept user input from the chat box
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Save user's message
    conversation.add_message(
        "user",
        user_input
    )
    # display user message on screen 
    with st.chat_message("user"):
        st.write(user_input)

    # Generate the AI Agent's response
    response = agent.run(
        conversation.get_messages()
    )

    # Save and display the assistant's response
    conversation.add_message(
        "assistant",
        response
    )

    with st.chat_message("assistant"):
        st.write(response)