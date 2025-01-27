import os
from decouple import config
from crewai import Crew, Process
from agents import ChatbotCrewAgents
from tasks import ChatbotCrewTasks

class ChatbotCrew:
    def __init__(self, file_paths, sitemap_urls):
        self.file_paths = file_paths
        self.sitemap_urls = sitemap_urls
        self.agents = ChatbotCrewAgents()
        self.tasks = ChatbotCrewTasks()

    def process_query(self, query):
        # Initialize agents
        researcher = self.agents.context_researcher()
        formulator = self.agents.answer_formulator()
        checker = self.agents.fact_checker()

        # Initialize tasks
        research_task = self.tasks.research_context_task(
            researcher, query, self.file_paths, self.sitemap_urls
        )
        formulation_task = self.tasks.formulate_answer_task(
            formulator, [research_task]
        )
        verification_task = self.tasks.verify_answer_task(
            checker, [formulation_task], [research_task]
        )

        # Form the crew
        crew = Crew(
            agents=[researcher, formulator, checker],
            tasks=[research_task, formulation_task, verification_task],
            process=Process.sequential
        )

        # Execute the crew
        return crew.kickoff()

if __name__ == "__main__":
    # Example configuration
    file_paths = ["./data/doc1.txt", "./data/doc2.pdf"]
    sitemap_urls = ["https://example.com/sitemap.xml"]
    
    chatbot = ChatbotCrew(file_paths, sitemap_urls)
    
    while True:
        query = input("\nEnter your question (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
            
        print("\nProcessing your question...")
        response = chatbot.process_query(query)
        print("\nResponse:")
        print(response)
