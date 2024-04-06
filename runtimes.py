# runtimes.py
import time

class RuntimeAlpha:
    @staticmethod
    def load():
        """
        Simulates the loading time for RuntimeAlpha.
        """
        time.sleep(1)

    @staticmethod
    def generate(args):
        """
        Simulates the processing time for RuntimeAlpha and generates a response based on the input prompt.
        Returns the generated response.
        """
        time.sleep(0.75)
        prompt = args["prompt"]
        return f"Given your question: {prompt}. I think the best answer is to buy ice cream."

class RuntimeBeta:
    @staticmethod
    def load():
        """
        Simulates the loading time for RuntimeBeta.
        """
        time.sleep(2)

    @staticmethod
    def generate(args):
        """
        Simulates the processing time for RuntimeBeta and generates a response based on the input prompt.
        Returns the generated response.
        """
        time.sleep(1.75)
        prompt = args["prompt"]
        return f"Given your question: {prompt}. I think the best answer is to get a hamburger."