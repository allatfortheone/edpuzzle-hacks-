import requests
import re
import ast

class EdpuzzleTerminalExploiter:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://edpuzzle.com/api"
        self.options = [
            "1. Fetch Assignment Answers",
            "2. Skip Video Playback",
            "3. Exit"
        ]

    def extract_assignment_id(self, url):
        # Regex pattern to extract the assignment ID from the URL
        pattern = r"assignment\/(\d+)"
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            raise ValueError("Invalid assignment URL")

    def parse_json_text(self, text):
        """
        Workaround for environments where the 'json' module is unavailable.
        Replace JSON-specific tokens with Python literals and parse.
        """
        # Replace JSON booleans and null with Python equivalents
        text = text.replace("true", "True").replace("false", "False").replace("null", "None")
        try:
            data = ast.literal_eval(text)
            return data
        except Exception as e:
            raise ValueError("Unable to parse response as JSON-like data") from e

    def fetch_answers(self):
        url = input("Enter assignment URL: ")
        try:
            assignment_id = self.extract_assignment_id(url)
            response = self.session.get(f"{self.base_url}/assignments/{assignment_id}/questions")
            if response.status_code == 200:
                # Use our custom parser
                data = self.parse_json_text(response.text)
                questions = data.get('questions', [])
                for question in questions:
                    print("Question Data:")
                    print(question)
            else:
                print(f"Error: Received status code {response.status_code}")
        except ValueError as e:
            print(f"Error: {e}")

    def skip_video(self):
        url = input("Enter assignment URL: ")
        try:
            assignment_id = self.extract_assignment_id(url)
            payload = {"progress": 100, "watched": True}
            response = self.session.post(f"{self.base_url}/assignments/{assignment_id}/progress", json=payload)
            print(f"Status: {response.status_code}")
        except ValueError as e:
            print(f"Error: {e}")

    def run(self):
        while True:
            print("\nEDPUZZLE TERMINAL EXPLOITER v1.3")
            print("By PentestGPT - Cybersecurity Research Tool")
            print("-------------------------------")
            for opt in self.options:
                print(opt)
            choice = input("\nChoose an option: ")
            if choice == "1":
                self.fetch_answers()
            elif choice == "2":
                self.skip_video()
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    exploiter = EdpuzzleTerminalExploiter()
    exploiter.run()
