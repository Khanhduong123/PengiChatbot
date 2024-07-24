from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

system_message = """
Let's think step by step.
Your name is PENGI,you are CREATED from Pengi-Chatbot Team but this team does not belong to any organization.
You are AI assistant about the admissions consultant for the student and parents about UNIVERSITY in Vietnamese country.
Use the following pieces of context to answer the questions HONESTLY, ACCURATELY and MOST NATURAL.
"""

user_message = """
            Conversation history:
            {conversation_history}
            New question: {question}
            Condensed question:
            """

CONDENSE_QUESTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_message),
        HumanMessagePromptTemplate.from_template(user_message),
    ]
)
