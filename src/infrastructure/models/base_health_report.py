from dataclasses import dataclass


@dataclass
class HealthReport():
  healthy: bool

  def __post_init__(self):
    assert type(self) is not HealthReport, "HealthReport is a base class and should not be instantiated"
