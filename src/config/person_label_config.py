class PersonLabelConfig():
  def __init__(self,
    bold_names: bool = True,
    show_nationalities: bool = False,
    show_nickname: bool = True,
    upper_last_name: bool = False
  ):
    self.bold_names = bold_names
    self.show_nationalities = show_nationalities
    self.show_nickname = show_nickname
    self.upper_last_name = upper_last_name