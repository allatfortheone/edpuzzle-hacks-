import requests
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
        """
        Extracts the assignment ID from the given URL by finding the substring 'assignment/'
        and reading the subsequent digits.
        """
        marker = "assignment/"
        index = url.find(marker)
        if index == -1:
            raise ValueError("Invalid assignment URL: missing 'assignment/'")
        # Get the part after "assignment/"
        id_part = url[index + len(marker):]
        assignment_id = ""
        for char in id_part:
            if char.isdigit():
                assignment_id += char
            else:
                break
        if not assignment_id:
            raise ValueError("Invalid assignment URL: no digits found after 'assignment/'")
        return assignment_id

    def parse_json_text(self, text):
        """
        Workaround for environments that don't support the json module.
        Replace some typical JSON tokens with Python literals and safely parse.
        """
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
            print("\nEDPUZZLE TERMINAL EXPLOITER v1.4")
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
