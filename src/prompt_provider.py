from langchain.prompts import PromptTemplate


class PromptProvider:
    def get_rag_prompt_german(self):
        prompt_template = """
        You are a Legal Assistant and your purpose is to help you with legal questions.
        Give me only context based answers.
        Context: {context}
        Question: {query}
        Answer: """

        prompt = PromptTemplate(
            template=prompt_template, input_variables=["context", "query"]
        )
        return prompt

