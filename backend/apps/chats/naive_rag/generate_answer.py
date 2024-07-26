from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from apps.chats.config import chat_config


class GenerateAnswerChain:
    def __init__(self) -> None:
        self.prompt = self.generate_answer_prompt()
        self.llm = ChatOpenAI(
            model=chat_config.MODEL_GPT, temperature=chat_config.TEMPERATURE
        )
        self.output_parser = StrOutputParser()
        self.chain = self.prompt | self.llm | self.output_parser
        self.streaming_chain = self.prompt | self.llm

    async def run(self, context, question):
        answer = await self.chain.ainvoke({"context": context, "question": question})

        return answer

    def run_sync(self, context, question):
        answer = self.chain.invoke({"context": context, "question": question})

        return answer

    def generate_answer_system_prompt(self):
        return """
            You are an intelligent AI language model assistant specializing in admissions support. Your name is Pengi.
            Instructions: Use the provided search results to compose a comprehensive and accurate reply to the question.
            - Compose a reply to the question using only the provided search results.
            - If no relevant search result is given, respond with "No Answer".
            - Do not use prior knowledge to answer.
            - Separate answers for multiple subjects with the same name.
            - Ignore irrelevant search results.
            - Provide a short and concise answer.
            - Ensure accuracy and avoid false content.
            """

    def generate_answer_user_prompt(self):
        return """
            Search result:
            ----
            {context}
            ---

            Question: {question}
            Answer:
            """

    def generate_answer_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    self.generate_answer_system_prompt()
                ),
                HumanMessagePromptTemplate.from_template(
                    self.generate_answer_user_prompt()
                ),
            ]
        )
