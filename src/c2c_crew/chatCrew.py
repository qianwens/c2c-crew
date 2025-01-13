from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool
)
from pydantic import BaseModel

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ChatCrew():
	"""ChatCrew crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	docs_tool = DirectoryReadTool()
	file_tool = FileReadTool()
	search_tool = SerperDevTool()
	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	
	@agent
	def error_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['error_analyst'],
			verbose=True
		)
	
	@agent
	def customer_support(self) -> Agent:
		return Agent(
			config=self.agents_config['customer_support'],
			verbose=True,
			allow_delegation=True,
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def file_structure_analyze_task(self) -> Task:
		return Task(
			config=self.tasks_config['file_structure_analyze_task'],
			tools=[self.docs_tool],
		)

	@task
	def customer_support_task(self) -> Task:
		return Task(
			config=self.tasks_config['customer_support_task'],
			verbose=True
		)
	
	@task
	def error_message_analyze_task(self) -> Task:
		return Task(
			config=self.tasks_config['error_message_analyze_task'],
			tools=[self.docs_tool, self.file_tool],
			verbose=True
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the C2CCrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=[self.customer_support_task()],# Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)