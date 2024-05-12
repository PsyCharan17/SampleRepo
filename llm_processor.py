from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser



OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")

class prompts():
    def _init_(self) -> None:
        pass

    def notes_maker_prompt(self):
        prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an expert notes compiler and summarizer"),
                ("user", """You will be provided with some data and you are to remove uneccesary data and summarize the data and make it look meaningful. Here is the data: 
                {input}
                 
                PROVIDE THE SUMMARIZED MEANINGFUL NOTES, ANYTHING ELSE IS NOT REQUIRED""")
            ])
        return prompt
    def process_recieved_notes(self):
        prompt = ChatPromptTemplate.from_messages([
                ("system", "You are an expert teacher who corrects notes and data"),
                ("user", """You will be provided with a paragraph which lacks some context and might not seem continous. You are to correct that data by rearranging the sentences meaningfully, in the end the paragraph should be completely. Remove sentence which you feel are unwanted: 
                {input}
                 
                PROVIDE MEANINGFUL NOTES, ANYTHING ELSE IS NOT REQUIRED""")
            ])
        return prompt
    

class llm_invoker:
    def _init_(self) -> None:
        self.prompts = prompts()
        self.llm =  ChatOpenAI(api_key=OPEN_AI_KEY)
        self.output_parser = StrOutputParser()
    
    def process_chunks(self, chunk_data):
        chain = self.prompts.notes_maker_prompt() | self.llm | self.output_parser
        processed_data = chain.invoke({"input": chunk_data})
        return processed_data
    
    def process_notes(self, notes_data):
        chain = self.prompts.process_recieved_notes() | self.llm | self.output_parser
        data = chain.invoke({"input": notes_data})
        return data