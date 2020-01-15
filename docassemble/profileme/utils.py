from docassemble.base.util import action_button_html, url_action

def edit_link(variable):
  return action_button_html(url_action(variable))

