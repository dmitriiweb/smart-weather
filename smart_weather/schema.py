from dataclasses import dataclass

from pydantic import BaseModel, Field


class WeatherLocationFormatResult(BaseModel):
    city_name: str = Field(description="The name of the city")
    country_code: str = Field(
        description="The country code of the city, use ISO 3166 country codes only"
    )
    state_code: str | None = Field(
        default=None, description="The state code of the state, use for US only"
    )

    def __str__(self) -> str:
        if self.state_code:
            return f"{self.city_name},{self.state_code},{self.country_code}"
        return f"{self.city_name},{self.country_code}"


@dataclass
class Coordinates:
    latitude: float
    longitude: float


class WeatherForecast(BaseModel):
    today: str
    upcoming: str
