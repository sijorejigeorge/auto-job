def gather_browser_state(page, browser, visited_urls):
    # Gather browser state and return as a dict
    tabs_info = []
    if hasattr(browser, 'contexts') and browser.contexts:
        for tab in browser.contexts[0].pages:
            try:
                tab_id = id(tab)
                tab_url = tab.url
                tab_title = tab.title()
                tabs_info.append({'id': tab_id, 'url': tab_url, 'title': tab_title})
                if tab_url not in visited_urls:
                    visited_urls.append(tab_url)
            except Exception:
                continue
    viewport = page.viewport_size
    scroll_y = page.evaluate('window.scrollY')
    scroll_x = page.evaluate('window.scrollX')
    page_height = page.evaluate('document.body.scrollHeight')
    page_width = page.evaluate('document.body.scrollWidth')
    viewport_height = viewport['height'] if viewport and 'height' in viewport else None
    viewport_width = viewport['width'] if viewport and 'width' in viewport else None
    pixels_above = scroll_y
    pixels_below = page_height - (scroll_y + viewport_height) if viewport_height else None
    visible_text = page.evaluate("document.body.innerText")
    clickable_elements = page.query_selector_all('a,button,input[type="submit"],input[type="button"]')
    clickable_info = []
    for el in clickable_elements:
        try:
            selector = el.evaluate('el => el.outerHTML')
            text = el.inner_text()
            clickable_info.append({'selector': selector, 'text': text})
        except Exception:
            continue
    try:
        with open('todo.md', 'r', encoding='utf-8') as todo_file:
            todo_contents = todo_file.read()
    except Exception:
        todo_contents = '[Current todo.md is empty, fill it with your plan when applicable]'
    import os
    available_files = [f for f in os.listdir(os.path.dirname(__file__)) if os.path.isfile(os.path.join(os.path.dirname(__file__), f))]
    filtered_actions = [el['text'] for el in clickable_info if el['text']]
    return {
        'current_url': page.url,
        'title': page.title(),
        'tabs_info': tabs_info,
        'viewport_width': viewport_width,
        'viewport_height': viewport_height,
        'scroll_x': scroll_x,
        'scroll_y': scroll_y,
        'page_width': page_width,
        'page_height': page_height,
        'pixels_above': pixels_above,
        'pixels_below': pixels_below,
        'visible_text': visible_text,
        'clickable_info': clickable_info,
        'todo_contents': todo_contents,
        'available_files': available_files,
        'filtered_actions': filtered_actions
    }
