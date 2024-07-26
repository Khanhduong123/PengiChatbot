from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from apps.chats.config import chat_config


class CondenseQuestionChain:
    def __init__(self) -> None:
        self.prompt = self.condense_question_prompt()
        self.llm = ChatOpenAI(model=chat_config.MODEL_GPT, temperature=0)
        self.output_parser = StrOutputParser()
        self.chain = self.prompt | self.llm | self.output_parser

    def format_conversation_history(self, conversation_history):
        buffer = []
        for chat in conversation_history:
            if chat['role'] == 'user':
                buffer.append(HumanMessage(content=chat['content']))
            elif chat['role'] == 'system':
                buffer.append(AIMessage(content=chat['content']))

        return buffer

    async def run(self, conversation_history, question):
        if not conversation_history:
            # Keep the question as is if there's no conversation context.
            return question

        conversation_history = self.format_conversation_history(
            conversation_history=conversation_history
        )

        new_question = await self.chain.ainvoke(
            {"question": question, "conversation_history": conversation_history}
        )

        return new_question

    def run_sync(self, chat_history, question):
        if not chat_history:
            # Keep the question as is if there's no conversation context.
            return question

        chat_history = self.format_conversation_history(
            conversation_history=chat_history
        )

        new_question = self.chain.invoke(
            {"question": question, "conversation_history": chat_history}
        )

        return new_question

    def condense_question_system_prompt(self):
        return """
            You are an intelligent AI language model assistant.
            Your task is to help condense follow-up questions by integrating them with the original question or previous context, keeping it in its original language.
            This will ensure that the condensed question is concise, clear, and suitable for RAG chatbot.
            If the question is new, retain the original question.
            """

    def condense_question_user_prompt(self):
        return """
            Conversation history:
            {conversation_history}
            New question: {question}
            Condensed question:
            """

    def condense_question_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(
                    self.condense_question_system_prompt()
                ),
                HumanMessagePromptTemplate.from_template(
                    self.condense_question_user_prompt()
                ),
            ]
        )
