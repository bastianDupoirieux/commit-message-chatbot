import ollama

class OllamaChatbot:
    def __init__(self, model):
        self.model = model

    def check_if_model_exists(self) -> str:
        """
        Runs a check to see if the model with which the chatbot is instantiated exists.
        :return: a validation string returning the
        """
        available_models = ollama.list().models
        model_names = [mod.model for mod in available_models]
        if self.model not in model_names:
            return f"Model {self.model} not installed, please install to continue"
        else:
            return f"Running with model {self.model}"


    def pull_model(self):
        ollama.pull(self.model)

    def run_ollama(self, prompt:str) -> str:
        """
        Prompts the installed ollama model and returns the response as a string.
        :param prompt: the prompt given to the model
        :return: response to the prompt
        """
        res = ollama.generate(model=self.model, prompt=prompt)

        return res['response']



