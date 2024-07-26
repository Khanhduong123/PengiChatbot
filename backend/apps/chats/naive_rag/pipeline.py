from typing import AsyncIterable

# from database import add_conversation, get_conversation_history
from apps.chats.config import chat_config
from apps.chats.naive_rag.condense_question import CondenseQuestionChain
from apps.chats.naive_rag.generate_answer import GenerateAnswerChain
from apps.chats.naive_rag.retrieval import DocumentRetrieval
from utils.logging import LOGGER


class NaiveRAGPipeline:
    def __init__(self):
        self.condense_question_chain = CondenseQuestionChain()
        self.generate_answer_chain = GenerateAnswerChain()

    async def execute(self, question):
        # Retrieve conversation from mongo database
        # conversation_history = await get_conversation_history(session_id=session_id)
        conversation_history = []

        question = await self.condense_question_chain.run(
            conversation_history=conversation_history, question=question
        )

        LOGGER.info(f"Condense question: {question}")

       
        query_result = await DocumentRetrieval.get_relevant_document(
            question=question
        )

        answer = await self.generate_answer_chain.run(
            context=query_result["context"], question=question
        )

        if "no answer" in answer.lower():
            answer = chat_config.PROMPT_NOT_FOUND
            relevant_docs = []

        else:
            relevant_docs = query_result["relevant_docs"]

        # Add conversation to mongo database
        # await add_conversation(
        #     session_id=session_id,
        #     conversation_id=conversation_id,
        #     question=question,
        #     answer=answer,
        #     relevant_docs=relevant_docs,
        # )

        LOGGER.info(f"Answer: {answer}")

        return {"question": question, "answer": answer, "relevant_docs": relevant_docs}

    def execute_sync(self, question):
       

        query_result = DocumentRetrieval.get_relevant_document_sync(
            question=question
        )

        answer = self.generate_answer_chain.run_sync(
            context=query_result["context"], question=question
        )

        if "no answer" in answer.lower():
            answer = chat_config.PROMPT_NOT_FOUND
            relevant_docs = []

        else:
            relevant_docs = query_result["relevant_docs"]

        LOGGER.info(f"Answer: {answer}")

        return {"question": question, "answer": answer, "relevant_docs": relevant_docs}

    async def execute_streaming(
        self, question
    ) -> AsyncIterable[str]:
        # Retrieve conversation from mongo database
        # conversation_history = await get_conversation_history(session_id=session_id)
        conversation_history = []

        question = await self.condense_question_chain.run(
            conversation_history=conversation_history, question=question
        )

        LOGGER.info(f"Condense question: {question}")

        query_result = await DocumentRetrieval.get_relevant_document(
            question=question
        )
        answer = ""
        async for stream in self.generate_answer_chain.streaming_chain.astream(
            {"context": query_result["context"], "question": question}
        ):
            # LOGGER.info(f"Token response: {stream.content}")
            answer += stream.content
            
            yield stream.content

        relevant_docs = query_result["relevant_docs"]

        LOGGER.info(f"Answer: {answer}")

        # Add conversation to mongo database
        # await add_conversation(
        #     session_id=session_id,
        #     conversation_id=conversation_id,
        #     question=question,
        #     answer=answer,
        #     relevant_docs=relevant_docs,
        # )
