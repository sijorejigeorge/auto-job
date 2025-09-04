class AgentHistory:
    def __init__(self, url):
        self.url = url
        self.visited_urls = [url]
        self.actions = []
        self.errors = 0
        self.extracted_results = []

    def add_step(self, step_number, actions):
        self.actions.append(f"Step {step_number}: Actions: {actions}")

    def finalize(self, visited_urls, errors, extracted_results):
        self.visited_urls = visited_urls
        self.errors = errors
        self.extracted_results = extracted_results

    def get_history_str(self):
        return '\n'.join(self.actions)
