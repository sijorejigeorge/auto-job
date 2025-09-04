import json
from agent import get_page_content
from llm import send_to_llama
from prompt_example import PROMPT_EXAMPLE
from browser_state import gather_browser_state
from action_executor import execute_actions
from history import AgentHistory

def run_agents(url_list, prompt):
    agent_histories = []
    for url in url_list:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        page_content, page, browser = get_page_content(url)
        agent_history = AgentHistory(url)
        step_number = 0
        max_steps = 20
        error_count = 0
        extracted_results = []
        visited_urls = [url]
        while True:
            state = gather_browser_state(page, browser, visited_urls)
            full_prompt = (
                "You are a browser automation agent.\n"
                f"User instruction: {prompt}\n"
                f"Current URL: {state['current_url']}\n"
                f"Page title: {state['title']}\n"
                f"Open tabs: {state['tabs_info']}\n"
                f"Viewport size: width={state['viewport_width']}, height={state['viewport_height']}\n"
                f"Scroll position: x={state['scroll_x']}, y={state['scroll_y']}\n"
                f"Page size: width={state['page_width']}, height={state['page_height']}\n"
                f"Pixels above viewport: {state['pixels_above']}\n"
                f"Pixels below viewport: {state['pixels_below']}\n"
                f"Clickable elements: {state['clickable_info'][:10]}\n"
                f"Page text (truncated):\n{state['visible_text'][:2000]}\n"
                f"Current TODO list (update this as you plan and execute):\n{state['todo_contents']}\n"
                f"Available files: {state['available_files']}\n"
                f"Step info: Step {step_number + 1} of {max_steps} max possible steps\n"
                f"Agent history:\n{agent_history.get_history_str()}\n"
                f"Filtered actions for current page: {state['filtered_actions']}\n"
                "Respond ONLY with a JSON object containing two keys: 'todo' (the updated todo list as markdown) and 'actions' (a JSON list of actions to perform, see example below).\n"
                f"Example: {{'todo': '# TODO\n- Step 1\n- Step 2', 'actions': {PROMPT_EXAMPLE}}}\n"
            )
            print("Prompt sent to LLM:", full_prompt)
            print("Sending prompt to LLM...")
            retry_attempts = 3
            result = None
            for attempt in range(retry_attempts):
                try:
                    result = send_to_llama(full_prompt)
                    print("LLM response:", result)
                    break
                except Exception as llm_error:
                    print(f"Error communicating with LLM (attempt {attempt+1}/{retry_attempts}): {llm_error}")
                    error_count += 1
                    if attempt == retry_attempts - 1:
                        print("Max LLM retry attempts reached. Stopping agent for this tab.")
                        break
            if result is None:
                print("LLM result was None. No response received from the model.")
                break
            try:
                cleaned_result = result.strip()
                if cleaned_result.startswith('```json'):
                    cleaned_result = cleaned_result[len('```json'):].strip()
                if cleaned_result.startswith('```'):
                    cleaned_result = cleaned_result[len('```'):].strip()
                if cleaned_result.endswith('```'):
                    cleaned_result = cleaned_result[:-3].strip()
                response_obj = json.loads(cleaned_result)
                new_todo = response_obj.get('todo', state['todo_contents'])
                actions = response_obj.get('actions', [])
                extracted = response_obj.get('extracted', None)
                if extracted:
                    extracted_results.append(extracted)
                try:
                    with open('todo.md', 'w', encoding='utf-8') as todo_file:
                        todo_file.write(new_todo)
                    print("Updated TODO list:")
                    print(new_todo)
                except Exception as todo_write_error:
                    print(f"Error writing updated todo list: {todo_write_error}")
                todo_lines = [line.strip() for line in new_todo.splitlines() if line.strip().startswith('-')]
                if todo_lines and all(line.startswith('- [x]') for line in todo_lines):
                    print("All tasks in TODO list are completed. Stopping loop.")
                    break
                if not actions:
                    print("No actions returned. Stopping loop.")
                    break
                agent_history.add_step(step_number + 1, actions)
                step_number += 1
                execute_actions(page, actions, error_count)
                print("Actions performed. You can now inspect the browser.")
            except Exception as e:
                print("Could not parse LLM response as actions and todo:", e)
                if result is not None:
                    print("Raw LLM response:", result)
                error_count += 1
                break
            cont = input("Continue with next LLM step? (y/n): ").strip().lower()
            if cont != 'y':
                break
        agent_history.finalize(visited_urls, error_count, extracted_results)
        agent_histories.append(agent_history)
        print("Browser will remain open. Please close it manually when done.")
    print("\n=== Agent Run Summary ===")
    for idx, hist in enumerate(agent_histories):
        print(f"Agent/Tab {idx+1}:")
        print(f"  Start URL: {hist.url}")
        print(f"  Visited URLs: {hist.visited_urls}")
        print(f"  Actions taken: {len(hist.actions)}")
        print(f"  Errors: {hist.errors}")
        print(f"  Extracted results: {hist.extracted_results}")
        print(f"  Step-by-step agent history:")
        for step in hist.actions:
            print(f"    {step}")
