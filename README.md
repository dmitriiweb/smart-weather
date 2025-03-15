# smart-weather

## Requirements

- Python >= 3.11
- Local installation of Ollama
- OpenWeatherMap API key

## Installation

You can install `smart-weather` directly from GitHub using pip:

```sh
pip install git+https://github.com/dmitriiweb/smart-weather.git
```

## Usage

To use the `smart-weather` CLI, simply run:

```sh
smart-weather -l "your location here"
```


## Example of Usage

this is example of usage of smart-weather with local installation of Ollama (qwwen 2.5 7b)

```sh
$ smart-weather -l "London"
The current weather in London is clear with minimal cloud cover. The temperature is at 277.31 Kelvin (which converts to approximately 5°C), and it feels like 273.91 Kelvin (-3.26°C) due to the prevailing conditions. The minimum and maximum temperatures for today are expected to be around 276.51 Kelvin (4.19°C) and 278.45 Kelvin (10.32°C), respectively.

Wind speed is recorded at 4.12 meters per second, coming from the northwest with a direction of 70 degrees. Visibility is good with 10,000 meters. The air pressure is stable at 1024 hPa and humidity at 66%.

Given the weather forecast for London, which describes clear skies but low temperatures, here are some suggestions for what to wear and activities you might enjoy:

### What to Wear:
- **Layers**: Since it feels like -3.26°C, dressing in layers is key. Start with a lightweight thermal or woolen base layer.
- **Outerwear**: A down jacket or insulated coat will help keep you warm during the colder periods.
- **Footwear**: Opt for thick, waterproof boots that can handle cold conditions and some snow if present.
- **Accessories**: Wear a scarf, mittens, and a beanie to keep your extremities warm.
- **Hands and Feet**: Gloves or mittens are essential.

### Best Activities:
1. **Snowshoeing** - If there’s any light snowfall, this can be a great activity in parks like Richmond Park.
2. **Ice Skating** - Head over to a nearby frozen pond or local ice rink for some fun skating.
3. **Cross-Country Skiing** - Find trails with moderate difficulty and enjoy the winter scenery.
4. **Photography**: With clear skies, this is an excellent opportunity to capture beautiful frosty landscapes.
5. **Hot Drinks at Café** - After your outdoor activities, warm up with a hot chocolate or coffee inside a cozy café.

These suggestions should help you stay warm and enjoy your day in the cool weather!

Based on the weather forecast for London:

- **Temperature:** While the actual temperature of approximately 5°C might feel colder due to low humidity, ensure you dress warmly as the perceived temperature drops to around -3.26°C.
- **Wind:** The wind is coming from the northwest at a speed of 4.12 meters per second, which could make it feel even cooler (chill factor).
- **Visibility:** Good visibility with 10,000 meters suggests clear skies which might also contribute to a drop in perceived temperature.
- **Humidity and Air Pressure:** With humidity around 66% and stable air pressure at 1024 hPa, moisture shouldn't be making the conditions particularly uncomfortable.

Given this forecast, it's advisable to dress warmly, especially if you plan to spend time outdoors.
```
