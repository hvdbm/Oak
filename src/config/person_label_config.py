class PersonLabelConfig():
  def __init__(self,
    show_nationalities: bool = False,
    show_nickname: bool = True,
    upper_last_name: bool = False
  ):
    self.show_nationalities = show_nationalities
    self.show_nickname = show_nickname
    self.upper_last_name = upper_last_name