from dataclasses import dataclass
from enum import StrEnum

from haco.capabilities import Capability
from haco.control import Control
from haco.uom import Uom
from haco.utils import ConvertersString


class DeviceClass(StrEnum):
    """

    Sourced from: https://www.home-assistant.io/integrations/sensor/#device-class

    """

    APPARENT_POWER = "apparent_power"  # Apparent power in VA.
    AQI = "aqi"  # Air Quality Index (unitless).
    ATMOSPHERIC_PRESSURE = "atmospheric_pressure"  # Atmospheric pressure in cbar, bar, hPa, inHg, kPa, mbar, Pa, or psi.
    BATTERY = "battery"  # Battery percentage in %.
    CARBON_DIOXIDE = "carbon_dioxide"  # CO₂ in ppm.
    CARBON_MONOXIDE = "carbon_monoxide"  # CO in ppm.
    CURRENT = "current"  # Current in A or mA.
    DATA_RATE = "data_rate"  # Data rate in bit/s, kbit/s, Mbit/s, Gbit/s, B/s, kB/s, MB/s, GB/s, KiB/s, MiB/s, or GiB/s.
    DATA_SIZE = "data_size"  # Data size in bit, kbit, Mbit, Gbit, B, kB, MB, GB, TB, PB, EB, ZB, YB, KiB, MiB, GiB, TiB, PiB, EiB, ZiB, or YiB.
    DATE = "date"  # ISO 8601 date string.
    DISTANCE = "distance"  # Distance in km, m, cm, mm, mi, yd, or in.
    DURATION = "duration"  # Duration in d, h, min, or s.
    ENERGY = "energy"  # Energy in Wh, kWh, MWh, MJ, or GJ.
    ENERGY_STORAGE = "energy_storage"  # Stored energy in Wh, kWh, MWh, MJ, or GJ.
    ENUM = "enum"  # Limited set of non-numeric states.
    FREQUENCY = "frequency"  # Frequency in Hz, kHz, MHz, or GHz.
    GAS = "gas"  # Gas volume in m³, ft³, or CCF.
    HUMIDITY = "humidity"  # Humidity in %.
    ILLUMINANCE = "illuminance"  # Light level in lx.
    IRRADIANCE = "irradiance"  # Irradiance in W/m² or BTU/(h⋅ft²).
    MOISTURE = "moisture"  # Water content in %.
    MONETARY = "monetary"  # Monetary value (ISO 4217).
    NITROGEN_DIOXIDE = "nitrogen_dioxide"  # NO₂ in µg/m³.
    NITROGEN_MONOXIDE = "nitrogen_monoxide"  # NO in µg/m³.
    NITROUS_OXIDE = "nitrous_oxide"  # N₂O in µg/m³.
    OZONE = "ozone"  # O₃ in µg/m³.
    PH = "ph"  # pH value.
    PM1 = "pm1"  # Particulate matter <1µm in µg/m³.
    PM25 = "pm25"  # Particulate matter <2.5µm in µg/m³.
    PM10 = "pm10"  # Particulate matter <10µm in µg/m³.
    POWER_FACTOR = "power_factor"  # Power factor (unitless or %).
    POWER = "power"  # Power in W or kW.
    PRECIPITATION = "precipitation"  # Accumulated precipitation.
    PRECIPITATION_INTENSITY = "precipitation_intensity"  # Precipitation rate.
    PRESSURE = "pressure"  # Pressure in Pa, kPa, hPa, bar, cbar, mbar, mmHg, inHg, or psi.
    REACTIVE_POWER = "reactive_power"  # Reactive power in var.
    SIGNAL_STRENGTH = "signal_strength"  # Signal strength in dB or dBm.
    SOUND_PRESSURE = "sound_pressure"  # Sound pressure in dB or dBA.
    SPEED = "speed"  # Speed in ft/s, in/d, in/h, km/h, kn, m/s, mph, or mm/d.
    SULPHUR_DIOXIDE = "sulphur_dioxide"  # SO₂ in µg/m³.
    TEMPERATURE = "temperature"  # Temperature in °C, °F, or K.
    TIMESTAMP = "timestamp"  # Datetime object or ISO 8601 string.
    VOLATILE_ORGANIC_COMPOUNDS = "volatile_organic_compounds"  # VOC in µg/m³.
    VOLATILE_ORGANIC_COMPOUNDS_PARTS = "volatile_organic_compounds_parts"  # VOC in ppm or ppb.
    VOLTAGE = "voltage"  # Voltage in V or mV.
    VOLUME = "volume"  # Volume in L, mL, gal, fl. oz., m³, ft³, or CCF.
    VOLUME_STORAGE = "volume_storage"  # Stored volume.
    WATER = "water"  # Water consumption in L, gal, m³, ft³, or CCF.
    WEIGHT = "weight"  # Mass in kg, g, mg, µg, oz, lb, or st.
    WIND_SPEED = "wind_speed"  # Wind speed in ft/s, km/h, kn, m/s, or mph.


@dataclass(kw_only=True)
class Sensor(Control):
    DATA = dict(
        platform='sensor'
    )
    converters = ConvertersString

    unit_of_measurement: Uom | None = None
    device_class: DeviceClass | None = None

    def command(self, value):
        raise NotImplementedError()

    def state(self, value):
        raise NotImplementedError()

    @classmethod
    def get_capabilities(cls):
        return [
            Capability(name=None, command=None)
        ]
