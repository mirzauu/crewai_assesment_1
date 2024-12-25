from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from mareting_dept.tools.search import SearchTools, generate_hashtags, scrape_targeted_emails
from crewai_tools import SerperDevTool, ScrapeWebsiteTool

@CrewBase
class MarketingDept:
    """Marketing Department crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def chief_creative_director(self) -> Agent:
        return Agent(
            config=self.agents_config['chief_creative_director'],
            verbose=True,
        )

    @agent
    def lead_market_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_market_analyst'],
            tools=[SearchTools.search_internet, SearchTools.open_page, ScrapeWebsiteTool(), SearchTools.analyze_competitors],
            verbose=True,
        )

    @agent
    def chief_marketing_strategist(self) -> Agent:
        return Agent(
            config=self.agents_config['chief_marketing_strategist'],
            tools=[SearchTools.search_internet, SearchTools.open_page, ScrapeWebsiteTool(), SearchTools.analyze_competitors],
            verbose=True,
        )

    @agent
    def creative_content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['creative_content_creator'],
            verbose=True,
        )

    @agent
    def email_marketer(self) -> Agent:
        return Agent(
            config=self.agents_config['email_marketer'],
            tools=[ScrapeWebsiteTool(), SearchTools.search_internet, SearchTools.open_page, scrape_targeted_emails],
            verbose=True,
        )

    @agent
    def social_media_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['social_media_specialist'],
            tools=[SearchTools.search_internet, SearchTools.open_page, SearchTools.search_instagram, generate_hashtags],
            verbose=True,
        )

    @task
    def analyze_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_strategy_task'],
            agent=self.lead_market_analyst(),
        )

    @task
    def project_understanding_task(self) -> Task:
        return Task(
            config=self.tasks_config['project_understanding_task'],
            agent=self.chief_marketing_strategist(),
        )

    @task
    def marketing_strategy_task(self) -> Task:
        return Task(
            config=self.tasks_config['marketing_strategy_task'],
            agent=self.chief_marketing_strategist(),
            output_file='marketing_strategy.md',
        )

    @task
    def campaign_idea_task(self) -> Task:
        return Task(
            config=self.tasks_config['campaign_idea_task'],
            agent=self.creative_content_creator(),
            output_file='campaign_idea.md',
        )

    @task
    def email_scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['email_scraping_task'],
            agent=self.email_marketer(),
            output_file='emails.md',
        )

    @task
    def email_content_task(self) -> Task:
        return Task(
            config=self.tasks_config['email_content_task'],
            agent=self.email_marketer(),
            output_file='email_content.md',
        )

    @task
    def email_response_task(self) -> Task:
        return Task(
            config=self.tasks_config['email_response_task'],
            agent=self.email_marketer(),
            output_file='email_response.md',
        )

    @task
    def instagram_content_task(self) -> Task:
        return Task(
            config=self.tasks_config['instagram_content_task'],
            agent=self.social_media_specialist(),
            output_file='instagram_content.md',
        )

    @task
    def image_prompt_task(self) -> Task:
        return Task(
            config=self.tasks_config['image_prompt_task'],
            agent=self.social_media_specialist(),
            output_file='image_prompts.md',
        )

    @task
    def content_strategy(self) -> Task:
        # Helper to load task output from files
        def load_task_output(filename):
            try:
                with open(filename, 'r') as file:
                    return file.read()
            except FileNotFoundError:
                return f"Error: {filename} not found."

        # Load outputs from other tasks
        email_addresses = load_task_output('emails.md')
        email_content = load_task_output('email_content.md')
        instagram_content = load_task_output('instagram_content.md')
        image_prompts = load_task_output('image_prompts.md')

        # Compile the final draft
        final_content = f"""
        # Marketing Campaign Final Draft

        ## Email Marketing
        ### Potential Client List
        {email_addresses}

        ### Cold Email Content
        {email_content}

        ## Social Media Strategy
        ### Instagram Content
        {instagram_content}

        ### Image Prompts
        {image_prompts}
        """

        # Write to the final draft file
        with open('final_draft.md', 'w') as file:
            file.write(final_content)

        return Task(
            config=self.tasks_config['content_strategy'],
            agent=self.creative_content_creator(),
            output_file='final_draft.md',
        )


    @crew
    def crew(self) -> Crew:
        """Creates the MarketingDept crew"""
        return Crew(
            agents=[
                self.lead_market_analyst(),
                self.chief_marketing_strategist(),
                self.creative_content_creator(),
                self.email_marketer(),
                self.social_media_specialist(),
            ],
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=self.chief_creative_director(),
        )
