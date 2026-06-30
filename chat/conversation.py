class ConversationManager:

    def __init__(self):
        # Store the complete conversation history
        self.messages = []

    def add_message(self, role, content):
        # Add a new message to the conversation
        self.messages.append(
            {
                "role": role,
                "content": content
            }
        )

    def get_messages(self):
        # Return the complete conversation history
        return self.messages

    def clear(self):
        # Reset the conversation history
        self.messages = []