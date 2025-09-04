def execute_actions(page, actions, error_count):
    for step in actions:
        retry_action_attempts = 2
        for action_attempt in range(retry_action_attempts):
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
                elif step["action"] == "select_option":
                    page.select_option(step["selector"], step["value"])
                elif step["action"] == "hover":
                    page.hover(step["selector"])
                elif step["action"] == "upload_file":
                    page.set_input_files(step["selector"], step["file_path"])
                break
            except Exception as action_error:
                print(f"Error executing action {step} (attempt {action_attempt+1}/{retry_action_attempts}): {action_error}")
                error_count += 1
                if action_attempt == retry_action_attempts - 1:
                    print(f"Max retry attempts for action {step} reached. Skipping.")
