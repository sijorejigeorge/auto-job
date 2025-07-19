from agent import get_page_content
from llm import send_to_llama
import json
from prompt_example import PROMPT_EXAMPLE

if __name__ == "__main__":
    while True:
        url = input("Enter the URL to visit (or 'exit' to quit): ")
        if url.lower() == "exit":
            break
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        prompt = input("Enter your job search instruction (e.g. 'Search for ML jobs and apply'): ")
        page_content, page, browser = get_page_content(url)

        # Feedback loop: keep asking LLM for next actions based on page state
        while True:
            # Extract visible text for context (can use page.content() for full HTML)
            visible_text = page.evaluate("document.body.innerText")
            full_prompt = (
                f"You are a browser assistant. Based on the current webpage and the user instruction '{prompt}', generate the next set of browser actions.\n"
                f"Respond ONLY with a JSON list of actions to perform. Example: {PROMPT_EXAMPLE}\n"
                "Here's the page text:\n" + visible_text[:2000]  # Limit to first 2000 chars for prompt size
            )
            print("Prompt sent to LLM:", full_prompt)
            print("Sending prompt to LLM...")
            result = send_to_llama(full_prompt)
            print("LLM response:", result)

            # Try to parse LLM response as JSON and execute actions
            try:
                cleaned_result = result.strip()
                if cleaned_result.startswith('```json'):
                    cleaned_result = cleaned_result[len('```json'):].strip()
                if cleaned_result.startswith('```'):
                    cleaned_result = cleaned_result[len('```'):].strip()
                if cleaned_result.endswith('```'):
                    cleaned_result = cleaned_result[:-3].strip()
                actions = json.loads(cleaned_result)
                if not actions:
                    print("No actions returned. Stopping loop.")
                    break
                for step in actions:
                    try:
                        if step["action"] == "type":
                            page.fill(step["selector"], step["value"])
                        elif step["action"] == "press_enter":
                            page.keyboard.press("Enter")
                        elif step["action"] == "click":
                            page.click(step["selector"])
                        elif step["action"] == "wait":
                            import time
                            time.sleep(step.get("duration", 1))
                        elif step["action"] == "scroll_down":
                            page.evaluate("window.scrollBy(0, arguments[0]);", step.get("amount", 1000))
                        # Add more actions as needed
                    except Exception as action_error:
                        print(f"Error executing action {step}: {action_error}")
                print("Actions performed. You can now inspect the browser.")
            except Exception as e:
                print("Could not parse LLM response as actions:", e)
                print("Raw LLM response:", result)
                break
            # Ask user if they want to continue or stop
            cont = input("Continue with next LLM step? (y/n): ").strip().lower()
            if cont != 'y':
                break
        print("Browser will remain open. Please close it manually when done.")
