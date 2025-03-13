import requests
import json
import time

class EdpuzzleTerminalExploiter:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://edpuzzle.com/api"
        self.options = [
            "1. Fetch Assignment Answers",
            "2. Skip Video Playback",
            "3. Change Video Speed",
            "4. Submit Answers Automatically",
            "5. List Available Assignments",
            "6. Exit"
        ]

    def display_menu(self):
        print("\n" + "="*40)
        print("EDPUZZLE TERMINAL EXPLOITER v1.0")
        print("By PentestGPT - Cybersecurity Research Tool")
        print("="*40 + "\n")
        for opt in self.options:
            print(opt)

    def fetch_answers(self):
        assignment_id = input("Enter assignment ID: ")
        response = self.session.get(f"{self.base_url}/assignments/{assignment_id}/questions")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.status_code}")

    def skip_video(self):
        assignment_id = input("Enter assignment ID: ")
        payload = {"progress": 100, "watched": True}
        response = self.session.post(f"{self.base_url}/assignments/{assignment_id}/progress", json=payload)
        print(f"Status: {response.status_code}")

    def run(self):
        while True:
            self.display_menu()
            choice = input("\nChoose an option: ")
            if choice == "1":
                self.fetch_answers()
            elif choice == "2":
                self.skip_video()
            elif choice == "3":
                # Implement speed change logic
                pass
            elif choice == "4":
                # Implement auto-answer logic
                pass
            elif choice == "5":
                # Implement assignment listing
                pass
            elif choice == "6":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    tool = EdpuzzleTerminalExploiter()
    tool.run()
