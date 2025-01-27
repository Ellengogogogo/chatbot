from crewai import Task

class ChatbotCrewTasks:
    def research_context_task(self, agent, query, file_paths, sitemap_urls):
        return Task(
            agent=agent,
            description=f"""
            Research query: {query}
            1. Process the following file paths: {file_paths}
            2. Process the following sitemaps: {sitemap_urls}
            3. Extract relevant information related to the query
            4. Organize the findings in a structured format
            """,
            expected_output="A structured collection of relevant information from all sources"
        )

    def formulate_answer_task(self, agent, context):
        return Task(
            agent=agent,
            context=context,
            description=f"""
            Based on the provided context: {context}
            1. Create a comprehensive answer
            2. Ensure the response is clear and concise
            3. Structure the response in a user-friendly format
            """,
            expected_output="A clear, well-structured response to the user's query"
        )

    def verify_answer_task(self, agent, answer, context):
        return Task(
            agent=agent,
            context=context,
            description=f"""
            Verify the following answer: {answer}
            Using the context: {context}
            1. Check all facts and claims
            2. Verify source citations
            3. Ensure accuracy of information
            4. Flag any inconsistencies or uncertainties
            """,
            expected_output="A verified answer with source citations and confidence levels"
        )




