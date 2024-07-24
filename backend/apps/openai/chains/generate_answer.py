from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from apps.openai.config import chat_config
from apps.openai.prompts.generate_answer import GENERATE_ANSWER_PROMPT


class GenerateAnswerChain:
    def __init__(self, api_key) -> None:
        self.prompt = GENERATE_ANSWER_PROMPT
        self.llm = ChatOpenAI(model=chat_config.MODEL_GPT, temperature=0.1, api_key=api_key)
        self.output_parser = StrOutputParser()
        self.chain = self.prompt | self.llm | self.output_parser

    async def run(self, context, question):
        answer = await self.chain.ainvoke({"context": context, "question": question})

        return answer

    def run_sync(self, context, question):
        answer = self.chain.invoke({"context": context, "question": question})

        return answer
