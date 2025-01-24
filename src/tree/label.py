def bold(text: str) -> str:
  return f"<B>{text}</B>"

def newline() -> str:
  return "<BR/>"

def replace_newline(text: str) -> str:
  newline_symbol = newline()
  return text.replace("\n", newline_symbol)