from src.utils import read_file_as_dict

class ChartConfig():
  def __init__(self,
    enable: bool = True,
    height: int = 8,
    width: int = 15,
    tight_layout: bool = True,
  ):
    self.enable = enable
    self.height = height
    self.width = width
    self.tight_layout = tight_layout


DEFAULT_CHARTS_CONFIGS: dict[str, ChartConfig] = {
  "first_name_repartition": ChartConfig(),
  "last_name_repartition": ChartConfig(),
  "nationalities_evolution": ChartConfig(),
  "nationalities_repartition": ChartConfig(),
  "sex_repartition": ChartConfig(),
}


class StatsConfiguration():
  # def __set_charts_configs(self, charts_configs: dict[str, ChartConfig]) -> None:
  #   self.charts_configs = DEFAULT_CHARTS_CONFIGS

  #   for key, config in charts_configs.values():
  #     if key not in charts_configs.keys: continue
  #     for values in 
  #       charts_configs[key] =

  def __init__(self,
    folder_name: str = "stats",
    charts_configs: dict[str, ChartConfig] = {}
  ):
    self.folder_name = folder_name
    self.__set_charts_configs(charts_configs)
  
  @classmethod
  def from_path(cls, path: str | None):
    if path is None: dict_config = {}
    else: dict_config = read_file_as_dict(path)
    
    return cls(**dict_config)
  