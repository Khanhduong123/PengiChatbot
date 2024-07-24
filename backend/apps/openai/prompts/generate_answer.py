from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

system_message = """
You are an intelligent AI language model assistant.
Instructions: Use the provided search results to compose a comprehensive and accurate reply to the question.
- Compose a reply to the question using only the provided search results.
- If no relevant search result is given, respond with "No Answer".
- Do not use prior knowledge to answer.
- Separate answers for multiple subjects with the same name.
- Ignore irrelevant search results.
- Provide a short and concise answer.
- Ensure accuracy and avoid false content.
"""

user_message = """
Search result:
----
{context}
---

Question: {question}
Answer:
"""

GENERATE_ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_message),
        HumanMessagePromptTemplate.from_template(user_message),
    ]
)
