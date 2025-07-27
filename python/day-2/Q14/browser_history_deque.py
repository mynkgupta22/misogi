
from collections import deque
from typing import List

class BrowserHistory:
    def __init__(self, max_size: int = 5):
        self.history = deque(maxlen = max_size)
        self.forward_stack = deque()    

    def add_page(self, url: str):
        """Add a new page to the history."""
        self.history.append(url)
        print(f"Added page: {url}")
        print(f"Current history: {list(self.history)}")

    def go_back(self):
        """Go back to the last page."""
        if self.history:
            last_page = self.history.pop()
            self.forward_stack.append(last_page)
            print(f"Going back from: {last_page}")
        else:
            print("No pages to go back to.")
        print(f"Current history: {list(self.history)}")
        print(f"Forward stack: {list(self.forward_stack)}")

    def go_forward(self):
        """Go forward to the next page."""
        if self.forward_stack:
            next_page = self.forward_stack.pop()
            self.history.append(next_page)
            print(f"Going forward to: {next_page}")
        else:
            print("No pages to go forward to.")
        print(f"Current history: {list(self.history)}")
        print(f"Forward stack: {list(self.forward_stack)}")

     def current_state(self) -> List[str]:
        """Return the current history and forward stack."""
        return list(self.history), list(self.forward_stack)

    def print_history(self):
        """Print the current history."""
        print("Current History:", list(self.history))
        print("Forward Stack:", list(self.forward_stack))

                   
