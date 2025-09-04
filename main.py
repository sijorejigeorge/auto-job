from agent_runner import run_agents

if __name__ == "__main__":
    while True:
        urls = input("Enter one or more URLs to visit (comma separated, or 'exit' to quit): ")
        if urls.lower() == "exit":
            break
        url_list = [u.strip() for u in urls.split(',') if u.strip()]
        if not url_list:
            continue
        prompt = input("Enter your job search instruction (e.g. 'Search for ML jobs and apply'): ")
        run_agents(url_list, prompt)
