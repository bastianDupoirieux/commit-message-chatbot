import sys
import yaml
import click
from commit_messenger.utils.utils import Config, GitUtils
from commit_messenger.chatbot.chatbot_utils import OllamaChatbot
from git import Repo
from pathlib import Path

permitted_commit_modes = ['standard', 'yolo']

BASE_DIR = Path(__file__).resolve().parent

config_path = BASE_DIR / 'config.yml'

with open(config_path, 'r') as stream:
    config = yaml.safe_load(stream)



def main():
    # start by running checks on the config and the project
    config_class = Config(config)

    config_class.run_config_checks() #run checks if the config is passed correctly

    #Get the git diff
    repo = Repo('.', search_parent_directories=True)
    git_utils = GitUtils(repo)

    added_files_list = git_utils.see_added_files()
    if len(added_files_list) == 0:
        print('No files added')
        sys.exit(0)

    # reject if any of the files to be ignored are staged and throw an error
    git_diff_list = []

    for file in added_files_list:
        config_class.create_error_if_file_should_be_ignored(file)
        git_diff_list.append(git_utils.get_diff_from_staged_files(file))

    diff_str = '\n'.join(git_diff_list)

    prompt = config['base_prompt'] + diff_str

    #if everything is fine: call the chatbot
    #model = config['model']
    chatbot = OllamaChatbot(config["model"])

    model_existence = chatbot.check_if_model_exists()
    if not model_existence:
        user_input = input("Do you want to install the model? (y/n): ")
        if user_input.lower() == 'y':
            print("Installing model...")
            chatbot.pull_model()
            #model_existence = chatbot.check_if_model_exists()
        else:
            print("Exiting...")
            sys.exit(-1) # Exit with code -1 means the model is not installed and won't be installed

    commit_msg = chatbot.run_ollama(prompt)

    commit_mode = config['commit_mode'].lower()

    if commit_mode == 'yolo':
        git_utils.commit_added_files(commit_msg)

    else:
        user_input = input(f"The following message was generated: {commit_msg}\n Do you want to commit with this message? (y/n): ")
        input_counter = 0
        while user_input.lower() != 'y' and input_counter<config["max_retries"]:
            commit_msg = chatbot.run_ollama(config["retry_prompt"])
            user_input = input(f"The following message was generated: {commit_msg}\n Do you want to commit with this message? (y/n): ")
            input_counter += 1

        if input_counter == config["max_retries"]:
            sys.exit(-2) # Exit with code -2 means the max retries for commiting with the messenger has been reached and no commit has been made

        else:
            git_utils.commit_added_files(commit_msg)

        sys.exit(0)

@click.command()
def cli():
    main()

if __name__ == '__main__':
    cli()

    #then depending on the commit mode: directly get the output from the chatbot and commit or ask if the message is fine (y,n).
    # If yes, then ask if it should be commited (y,n). If not, then reask the chatbot to formulate.
    # Also add an option to output the message so it can be edited manually (how could that work?)