# Example prompt for LLM browser agent
# This file contains the example JSON action list for job search automation.
# You can update or extend this example as needed.

PROMPT_EXAMPLE = (
    "["
    "{\"action\": \"type\", \"selector\": \"input[name='q']\", \"value\": \"Pluto\"}, "
    "{\"action\": \"click\", \"selector\": \"button.submit\"}, "
    "{\"action\": \"press_enter\"}, "
    "{\"action\": \"wait\", \"duration\": 2}, "
    "{\"action\": \"scroll_down\", \"amount\": 500}, "
    "{\"action\": \"select_option\", \"selector\": \"select#country\", \"value\": \"USA\"}, "
    "{\"action\": \"hover\", \"selector\": \".menu-item\"}, "
    "{\"action\": \"upload_file\", \"selector\": \"input[type='file']\", \"file_path\": \"/path/to/file.txt\"}"
    "]"
)
