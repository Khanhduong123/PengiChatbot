from langchain.schema.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from apps.openai.config import chat_config
from apps.openai.prompts.condense_question import CONDENSE_QUESTION_PROMPT

import logging
from config import (
    SRC_LOG_LEVELS
)
log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["OPENAI"])

class CondenseQuestionChain:
    def __init__(self, api_key) -> None:
        self.prompt = CONDENSE_QUESTION_PROMPT
        self.llm = ChatOpenAI(model=chat_config.MODEL_GPT,api_key=api_key)
        self.output_parser = StrOutputParser()
        self.chain = self.prompt | self.llm | self.output_parser

    def format_conversation_history(self, conversation_history):
        buffer = []
        log.info(f"conversation_history: {conversation_history}")
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
