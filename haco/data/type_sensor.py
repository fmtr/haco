class DeviceClassSensor:
    """

    Sourced from:
    https://www.home-assistant.io/integrations/sensor/#device-class

    """
    NONE: type(None) = None  # Generic sensor. This is the default and doesn’t need to be set.
    APPARENT_POWER: str = "apparent_power"  # Apparent power in VA.
    AQI: str = "aqi"  # Air Quality Index (unitless).
    ATMOSPHERIC_PRESSURE: str = "atmospheric_pressure"  # Atmospheric pressure in cbar, bar, hPa, inHg, kPa, mbar, Pa, or psi.
    BATTERY: str = "battery"  # Percentage of battery that is left in %.
    CARBON_DIOXIDE: str = "carbon_dioxide"  # Carbon Dioxide in CO2 (Smoke) in ppm.
    CARBON_MONOXIDE: str = "carbon_monoxide"  # Carbon Monoxide in CO (Gas CNG/LPG) in ppm.
    CURRENT: str = "current"  # Current in A or mA.
    DATA_RATE: str = "data_rate"  # Data rate in bit/s, kbit/s, Mbit/s, Gbit/s, B/s, kB/s, MB/s, GB/s, KiB/s, MiB/s, or GiB/s.
    DATA_SIZE: str = "data_size"  # Data size in bit, kbit, Mbit, Gbit, B, kB, MB, GB, TB, PB, EB, ZB, YB, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, or YiB.
    DATE: str = "date"  # Date string (ISO 8601).
    DISTANCE: str = "distance"  # Generic distance in km, m, cm, mm, mi, yd, or in.
    DURATION: str = "duration"  # Duration in d, h, min, or s.
    ENERGY: str = "energy"  # Energy in Wh, kWh, MWh, MJ, or GJ.
    ENERGY_STORAGE: str = "energy_storage"  # Stored energy in Wh, kWh, MWh, MJ, or GJ.
    ENUM: str = "enum"  # Has a limited set of (non-numeric) states.
    FREQUENCY: str = "frequency"  # Frequency in Hz, kHz, MHz, or GHz.
    GAS: str = "gas"  # Gas volume in m³, ft³, or CCF.
    HUMIDITY: str = "humidity"  # Percentage of humidity in the air in %.
    ILLUMINANCE: str = "illuminance"  # The current light level in lx.
    IRRADIANCE: str = "irradiance"  # Irradiance in W/m² or BTU/(h⋅ft²).
    MOISTURE: str = "moisture"  # Percentage of water in a substance in %.
    MONETARY: str = "monetary"  # The monetary value (ISO 4217).
    NITROGEN_DIOXIDE: str = "nitrogen_dioxide"  # Concentration of Nitrogen Dioxide in µg/m³.
    NITROGEN_MONOXIDE: str = "nitrogen_monoxide"  # Concentration of Nitrogen Monoxide in µg/m³.
    NITROUS_OXIDE: str = "nitrous_oxide"  # Concentration of Nitrous Oxide in µg/m³.
    OZONE: str = "ozone"  # Concentration of Ozone in µg/m³.
    PH: str = "ph"  # Potential hydrogen (pH) value of a water solution.
    PM1: str = "pm1"  # Concentration of particulate matter less than 1 micrometer in µg/m³.
    PM25: str = "pm25"  # Concentration of particulate matter less than 2.5 micrometers in µg/m³.
    PM10: str = "pm10"  # Concentration of particulate matter less than 10 micrometers in µg/m³.
    POWER_FACTOR: str = "power_factor"  # Power factor (unitless), unit may be None or %.
    POWER: str = "power"  # Power in W or kW.
    PRECIPITATION: str = "precipitation"  # Accumulated precipitation in cm, in, or mm.
    PRECIPITATION_INTENSITY: str = "precipitation_intensity"  # Precipitation intensity in in/d, in/h, mm/d, or mm/h.
    PRESSURE: str = "pressure"  # Pressure in Pa, kPa, hPa, bar, cbar, mbar, mmHg, inHg, or psi.
    REACTIVE_POWER: str = "reactive_power"  # Reactive power in var.
    SIGNAL_STRENGTH: str = "signal_strength"  # Signal strength in dB or dBm.
    SOUND_PRESSURE: str = "sound_pressure"  # Sound pressure in dB or dBA.
    SPEED: str = "speed"  # Generic speed in ft/s, in/d, in/h, km/h, kn, m/s, mph, or mm/d.
    SULPHUR_DIOXIDE: str = "sulphur_dioxide"  # Concentration of sulphur dioxide in µg/m³.
    TEMPERATURE: str = "temperature"  # Temperature in °C, °F, or K.
    TIMESTAMP: str = "timestamp"  # Datetime object or timestamp string (ISO 8601).
    VOLATILE_ORGANIC_COMPOUNDS: str = "volatile_organic_compounds"  # Concentration of volatile organic compounds in µg/m³.
    VOLATILE_ORGANIC_COMPOUNDS_PARTS: str = "volatile_organic_compounds_parts"  # Ratio of volatile organic compounds in ppm or ppb.
    VOLTAGE: str = "voltage"  # Voltage in V or mV.
    VOLUME: str = "volume"  # Generic volume in L, mL, gal, fl. oz., m³, ft³, or CCF.
    VOLUME_STORAGE: str = "volume_storage"  # Generic stored volume in L, mL, gal, fl. oz., m³, ft³, or CCF.
    WATER: str = "water"  # Water consumption in L, gal, m³, ft³, or CCF.
    WEIGHT: str = "weight"  # Generic mass in kg, g, mg, µg, oz, lb, or st.
    WIND_SPEED: str = "wind_speed"  # Wind speed in ft/s, km/h, kn, m/s, or mph.
