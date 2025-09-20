from commit_messenger.chatbot.chatbot_utils import OllamaChatbot

model1 = 'codellama:7b' #this model is installed on my computer, the test will pass
model2 = 'nonExistingModelWithAWeirdName'


def test_valid_model():

    chatbot1 = OllamaChatbot(model1)
    # this test is a bit sketchy but I will run it anyway, any respectable model should be able to write this. If the test fails, then the model has a problem
    prompt_for_hello_world_test = 'write a one line code in python to print hello world to the terminal. The code should set hello world in single quotation marks'
    chatbot_response = chatbot1.run_ollama(prompt_for_hello_world_test)

    assert chatbot1.check_if_model_exists() == f"Running with model {model1}"
    assert 'print(\'hello world\')' in chatbot_response.lower()

def test_invalid_model():
    chatbot2 = OllamaChatbot(model2)
    assert chatbot2.check_if_model_exists() == f"Model {model2} not installed, please install to continue"








