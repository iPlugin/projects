![alt text](screen/logo.png)
# Automatic Plant Watering System

This project is an **Automatic Plant Watering System** that monitors the light intensity and soil humidity levels to automate the watering process for plants. The system reads data from light and humidity sensors and controls a watering pump based on predefined thresholds. The project is developed using an Arduino board.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Components](#components)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

Maintaining the right moisture levels in soil is crucial for plant health. This project aims to automate the watering process, ensuring that plants receive water when they need it, based on real-time sensor data.

## Features

- **Light Sensor Monitoring**: Measures the intensity of ambient light.
- **Humidity Sensor Monitoring**: Tracks soil moisture levels.
- **Automatic Watering**: Activates a water pump if the light level is sufficient and the soil moisture is low.
- **Serial Monitoring**: Displays real-time sensor data on the Serial Monitor.

## Components

- Arduino Board Nano
- Light Sensor
- Humidity Sensor
- Water Pump
- Relay Module
- Wires
- Power Supply

## Installation

1. **Clone the repository**:
    ```bash
    $ git clone https://github.com/iPlugin/PROJ.git
    $ cd c_arduino_AquaGrow
    ```
2. **Open the project** in the Arduino IDE.
3. **Upload the code** to your Arduino board.

## Usage

1. **Power the Arduino board**.
2. **Monitor the Serial Monitor** in the Arduino IDE to observe the sensor readings.
3. **Observe the water pump**: It should turn on when the light level is above 40% and the soil moisture is below 60%.
    ```bash
    ----------------------------------------------------------
    Light - Analog value: 206	 Vol: 1.01V	 Perc: 80%
    Humidity - Analog value: 254	 Vol: 1.24V	 Perc: 76%
    Watering system: OFF
    ----------------------------------------------------------
    ```