/*
==== CONFIGURATION ====
*/
/*
== Mandatory Configuration ==
*/
// insert your apikey from https://openweathermap.org
const apikey = "apikey";
// insert the latidue and lonitude of the location you want to get the forecast for
// See the guide on how to get these values
const lat = "46";
const lon = "18";

/*
== Optional Configuration ==
*/
// Choose in which metric your forecast will be displayed. Available are: standard, metric or imperial
const units = "metric";
// From which temperature on should the respective color coding (via css) apply? Everything below mild will be threaten as cold.
const tempColorLimits = [
  { temp: 8, tempClass: "mild" },
  { temp: 20, tempClass: "warm" },
  { temp: 26, tempClass: "hot" },
];
/* Decide when you want to see additional weather information (if available at all).
I.e. "Clouds: 15" shows the Cloudiness (in %) if the value is available and equals or above 15
Set it to 0 if you want to show the value always (if available)

Please note: The "most important" additional information is shown only. So if i.e. both, wind_speed and
rain is available (and above your minimum), only rain is shown.
The priority is:  rain (mm) -> snow (mm) -> clouds (%) -> wind_speed (m/s or mi/s)
*/
const additionalInfoMinimums = {
  rain: 0,
  snow: 0,
  clouds: 15,
  wind_speed: 6,
};
/* = Time Span for Hourly Forecasts = */
// From which hour on (24h) do you want to get your hourly forecast? Mind that we can only request upcoming forecasts, so if you request the data AFTER your startTimeHour
// the script will start with the earliest hour possible
// Set to null to disable and get the first forecast available
const startTimeHour = 9;
// Until which hour on (24h) do you want to get your hourly forecast? Whatever comes first - the given count of forecasts or the given end time - ends the output.
// An example: If you request your forecast at 10:00 and want to get it until 18:00 with a gap of 2, you'll get 5 forecasts, even if your forecast count is set to 7.
// Set to null to disable and get forecasts until countOfForecasts is reached
const endTimeHour = 22;
/*
==== CONFIGURATION END ====
*/

// Default count for forecasts (can be overwritten with second parameter in function call)
const countOfForecasts = 9;
// Default gap for Forecasts (can be overwritten with third parameter in function call)
const gapBetweenForecasts = 2;

const weatherEndpoint = `https://api.openweathermap.org/data/2.5/onecall?lat=${lat}&lon=${lon}&appid=${apikey}&units=${units}&exclude=`;

function getWeatherAPIUrl(forecastType) {
  let excludes = ["current", "minutely", "hourly", "daily"];
  excludes = excludes.filter(type => type !== forecastType).reduce((prev, curr) => `${prev},${curr}`, "");

  return weatherEndpoint + excludes;
}

function getIcon(weatherIcon) {
  const weatherIconNo = weatherIcon.substr(0, 2);
  const iconmap = {
    "01": weatherIcon.endsWith("d") ? "☀" : "🌙",
    "02": "🌤",
    "03": "⛅",
    "04": "☁",
    "09": "🌧",
    10: "🌦",
    11: "🌩",
    13: "❄",
    50: "🌫",
  };

  return iconmap[weatherIconNo] || "?";
}

function getUnit(type) {
  const unitMap = {
    temp: {
      default: "K",
      metric: "°C",
      imperial: "°F",
    },
    wind_speed: {
      default: "m/s",
      metric: "m/s",
      imperial: "mi/s",
    },
  };

  return unitMap[type][units];
}

function getWeatherRendered(data, forecastType) {
  if (!data) return;

  if (forecastType === "minutely") {
    return `<div class="forecast">
    <div class="time"> ${formatDate(data, forecastType)} </div>
    <div class="precipitation"> ${data.precipitation} mm </div>
  </div>
  `;
  }

  return `
  <div class="forecast">
    <div class="time"> ${formatDate(data, forecastType)} </div>
    <div class="icon"> ${getIcon(data.weather[0].icon)} </div>
    ${getTemperature(data, forecastType)}
    <div class="additional"> ${getAdditionalRelevantInfo(data, forecastType)} </div>
  </div>
  `;
}

function getTemperature(data, forecastType) {
  if (forecastType === "daily") {
    return `<div class="temp"> 
    <span class="${getTempClass(data.temp.max)}"> ${Math.round(data.temp.max)} </span> / <span class="${getTempClass(
      data.temp.min
    )}"> ${Math.round(data.temp.min)} </span> ${getUnit("temp")} </div>`;
  } else {
    return `<div class="temp ${getTempClass(data.temp)}"> ${Math.round(data.temp)} ${getUnit("temp")} </div>`;
  }
}

function getAdditionalRelevantInfo(data, forecastType) {
  let additionalInfo = "";
  data.rain = forecastType === "hourly" && data.rain ? data.rain["1h"] : data.rain;
  data.snow = forecastType === "hourly" && data.snow ? data.snow["1h"] : data.snow;

  if (data.rain > additionalInfoMinimums.rain) {
    additionalInfo = `☂ ${Math.floor(data.pop * 100)}%<br/>${data.rain.toFixed(1)} mm`;
  } else if (data.snow > additionalInfoMinimums.snow) {
    additionalInfo = `⛄ ${data.snow.toFixed(1)} mm`;
  } else if (data.clouds > additionalInfoMinimums.clouds) {
    additionalInfo = `☁ ${data.clouds}%`;
  } else if (data.wind_speed >= additionalInfoMinimums.wind_speed) {
    additionalInfo = `🎐 ${data.wind_speed} ${getUnit("wind_speed")}`;
  }
  return additionalInfo;
}

function getDateOfForecast(data) {
  if (!data || !data.dt) return;
  let date;

  try {
    date = new Date(data.dt * 1000);
  } catch (err) {
    console.error("Could not convert date for forecast", data, err);
  }
  return date;
}

function formatDate(data, forecastType) {
  const date = getDateOfForecast(data);

  switch (forecastType) {
    case "minutely":
      return date.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
    case "daily":
      return date.toLocaleDateString(undefined, { weekday: "short", month: "2-digit", day: "2-digit" });
    default:
      const hours = date.getHours();
      return `${hours < 10 ? "0" : ""}${hours}:${date.getMinutes() || "00"}`;
  }
}

function getTempClass(temp) {
  let tempClass = "cold";

  for (i = 0; i < tempColorLimits.length; i++) {
    if (temp > tempColorLimits[i].temp && (i + 1 === tempColorLimits.length || temp < tempColorLimits[i + 1].temp)) {
      tempClass = tempColorLimits[i].tempClass;
    }
  }

  return tempClass;
}

function renderWeatherAlerts(alerts = []) {
  let output = "";

  for (alert of alerts) {
    output += `> [!caution] ${alert.event}
> **${new Date(alert.start * 1000).toLocaleString()} - ${new Date(alert.end * 1000).toLocaleString()}**
> ${alert.description}

`;
  }

  return output;
}

/**
 * Receives the weather for configured lot/lan via the OneCall Api of openweathermap.org
 * https://openweathermap.org/api/one-call-3
 * 
 * @param {*} forecastType type of forecast to receive. Defaults to hourly. Available: current, minutely, hourly, daily, alerts

 * @returns Weather data as HTML string
 */
async function getCurrentWeather(
  forecastType = "hourly",
  forecastCount = countOfForecasts,
  forecastGap = gapBetweenForecasts
) {
  try {
    if (!["current", "minutely", "hourly", "daily", "alerts"].includes(forecastType)) {
      console.warn(`Given forecast type "${forecastType}" is not supported. Falling back to hourly.`);
      forecastType = "hourly";
    }

    let weatherData = await callOpenWeatherMap(forecastType);
    let output = "";

    if (weatherData.alerts) {
      output += renderWeatherAlerts(weatherData.alerts);
    }

    if (forecastType === "alerts") {
      return output;
    }

    output += `<div class="weather ${forecastType}"><div class="forecasts">`;

    if (forecastType === "current") {
      output += getWeatherRendered(weatherData[forecastType], forecastType);
    } else {
      forecastCount = forecastCount * forecastGap;
      if (forecastCount > weatherData[forecastType].length) {
        forecastCount = weatherData[forecastType].length;
      }

      let i = 0;
      let dateOfEndTime = null;
      if (forecastType === "hourly") {
        if (startTimeHour) {
          i = weatherData.hourly.findIndex(h => getDateOfForecast(h).getHours() >= startTimeHour) || 0;
        }
        if (endTimeHour) {
          dateOfEndTime = new Date().setHours(endTimeHour);
        }
      }

      for (i; i < forecastCount; i = i + forecastGap) {
        let forecast = weatherData[forecastType][i];
        if (dateOfEndTime && getDateOfForecast(forecast) > dateOfEndTime) {
          break;
        }
        output += getWeatherRendered(forecast, forecastType);
      }
    }

    output += "</div></div>";
    return output;
  } catch (err) {
    console.error("Weather Script threw an error:", err);
    return "Could not render weather data... :(";
  }

  async function callOpenWeatherMap(forecastType) {
    const weatherData = await fetch(getWeatherAPIUrl(forecastType));

    return new Promise((resolve, reject) => {
      if (!weatherData.ok) {
        throw Error("Could not get weather data from openweathermap.org");
      }

      resolve(weatherData.json());
    });
  }
}

module.exports = getCurrentWeather;
