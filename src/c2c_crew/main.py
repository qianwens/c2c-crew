#!/usr/bin/env python
import sys
import warnings
import os
import json

from c2c_crew.crew import C2CCrew
from c2c_crew.serviceCrew import ServiceCrew
from c2c_crew.chatCrew import ChatCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    print("Chatbot: Hi! Give me your folder path and I will analyze it for you.")
    folder = input("User: ")
    codetocloud_path = os.path.join(folder, '.codetocloud')
    azure_json_path = os.path.join(codetocloud_path, 'azure.json')
    if os.path.exists(azure_json_path):
        print("Chatbot: The .codetocloud/azure.json exists in the provided folder. Reply Yes to continue or ask me any questions.")
        while True:
            user_input = input("User: ")
            if user_input.lower() == "yes":
                break
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Chatbot: Goodbye! It was nice talking to you.")
                return
            with open(azure_json_path, 'r') as file:
                azure_data = json.load(file)
                chatResult = ChatCrew().crew().kickoff(inputs={"folder": folder, "question": user_input, "bicep": os.path.join(folder, 'infra')})
                print("Chatbot:", chatResult)
    inputs = {
        'folder': 'C:\\Users\\qianwens\\testrepo\\dvpwa'
    }
    folderResult = C2CCrew().crew().kickoff(inputs=inputs)
    print(folderResult)
    folders_dict_list = [folder.dict() for folder in folderResult.pydantic.folders]
    async_results = ServiceCrew().crew().kickoff_for_each(inputs=folders_dict_list)
    for async_result in async_results:
        print(async_result)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        C2CCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        C2CCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        C2CCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
