from crewai import Agent
#from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq  # Import Groq client
from langchain_openai import ChatOpenAI
import os
from crewai_tools import SerperDevTool,WebsiteSearchTool, ScrapeWebsiteTool 
from tools.file_tools import FileReaderTool
from tools.sitemap_tools import SitemapProcessorTool



class ChatbotCrewAgents:

    def __init__(self):
        # Initialize tools if needed
        self.serper = SerperDevTool()
        self.web = WebsiteSearchTool()
        self.web_scrape=ScrapeWebsiteTool()
        self.file_reader = FileReaderTool()
        self.sitemap_processor = SitemapProcessorTool()


       # OpenAI Models
        self.gpt3 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.gpt4 = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.7)
        self.gpt3_5_turbo_0125 = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.7)
        self.gpt3_5_turbo_1106 = ChatOpenAI(model_name="gpt-3.5-turbo-1106", temperature=0.7)
        self.gpt3_5_turbo_instruct = ChatOpenAI(model_name="gpt-3.5-turbo-instruct", temperature=0.7)
        
        # Groq Models
        self.llama3_8b = ChatGroq(temperature=0.7, groq_api_key=os.environ.get("GROQ_API_KEY"), model_name="llama3-8b-8192")
        self.llama3_70b = ChatGroq(temperature=0.7, groq_api_key=os.environ.get("GROQ_API_KEY"), model_name="llama3-70b-8192")
        self.mixtral_8x7b = ChatGroq(temperature=0.7, groq_api_key=os.environ.get("GROQ_API_KEY"), model_name="mixtral-8x7b-32768")
        self.gemma_7b = ChatGroq(temperature=0.7, groq_api_key=os.environ.get("GROQ_API_KEY"), model_name="gemma-7b-it")
        
        # CHANGE YOUR MODEL HERE
        self.selected_llm = self.gpt4
    def context_researcher(self):
        return Agent(
            role='Context Researcher',
            goal='Process and analyze files and sitemap content to find relevant information for user queries',
            backstory="You are an expert at processing various data sources including documents and website content. You excel at understanding context and finding relevant information from multiple sources.",
            verbose=True,
            allow_delegation=False,
            llm=self.selected_llm,
            max_iter=3,
            tools=[self.file_reader, self.sitemap_processor, self.web_scrape],
        )

    def answer_formulator(self):
        return Agent(
            role='Answer Formulator',
            goal='Create comprehensive and accurate responses based on the gathered context',
            backstory="You are an expert at synthesizing information from multiple sources and creating clear, concise, and accurate responses that directly address user queries.",
            verbose=True,
            allow_delegation=False,
            llm=self.selected_llm,
            max_iter=3,
        )

    def fact_checker(self):
        return Agent(
            role='Fact Checker',
            goal='Verify the accuracy of information and provide source citations',
            backstory="You are a meticulous fact-checker who ensures all information is accurate and properly sourced. You verify claims against the provided documentation and website content.",
            verbose=True,
            allow_delegation=False,
            llm=self.selected_llm,
            tools=[self.file_reader, self.sitemap_processor],
            max_iter=3,
        )