from pydantic import BaseModel

from src.utils import read_file_as_dict


class ChartConfig(BaseModel):
  enable: bool = True
  height: int = 8
  width: int = 15
  tight_layout: bool = True


class ChartsConfig(BaseModel):
  first_name_repartition: ChartConfig = ChartConfig()
  last_name_repartition: ChartConfig = ChartConfig()
  nationalities_evolution: ChartConfig = ChartConfig()
  nationalities_repartition: ChartConfig = ChartConfig()
  sex_repartition: ChartConfig = ChartConfig()


class StatsConfiguration(BaseModel):
  folder_name: str = "stats"
  charts: ChartsConfig = ChartsConfig()
  
  @classmethod
  def from_dict(cls, dict_config: dict):
    return cls(**dict_config)

  @classmethod
  def from_path(cls, path: str | None):
    if path is None: dict_config = {}
    else: dict_config = read_file_as_dict(path)
    
    return cls.from_dict(dict_config)
  