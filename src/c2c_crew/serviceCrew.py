from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool
)

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ServiceCrew():
	"""C2CCrew crew"""
	docs_tool = DirectoryReadTool()
	file_tool = FileReadTool()
	search_tool = SerperDevTool()
	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def code_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['code_analyst'],
			tools=[self.docs_tool, self.file_tool, self.search_tool],
			verbose=True
		)

	@agent
	def azure_architect(self) -> Agent:
		return Agent(
			config=self.agents_config['azure_architect'],
			verbose=True
		)
	
	@agent
	def error_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['error_analyst'],
			verbose=True
		)


	@task
	def service_code_analyze_task(self) -> Task:
		return Task(
			config=self.tasks_config['service_code_analyze_task'],
			async_execution=True
		)
	
	@task
	def environment_variables_detect_task(self) -> Task:
		return Task(
			config=self.tasks_config['environment_variables_detect_task'],
			async_execution=True
		)

	@task
	def dependencies_detect_task(self) -> Task:
		return Task(
			config=self.tasks_config['dependencies_detect_task'],
			async_execution=True
		)

	@task
	def dependencies_analyze_task(self) -> Task:
		return Task(
			config=self.tasks_config['dependencies_analyze_task'],
			context=[self.dependencies_detect_task(), self.environment_variables_detect_task()],
		)

	@task
	def azure_services_recommend_task(self) -> Task:
		return Task(
			config=self.tasks_config['azure_services_recommend_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the C2CCrew crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=[self.service_code_analyze_task(), self.dependencies_detect_task(), self.environment_variables_detect_task(), self.dependencies_analyze_task()], # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)