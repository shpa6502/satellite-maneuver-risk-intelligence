# Knowledge Base

## Satellite Maneuver Detection & Conjunction Risk Intelligence Platform

This document records the technical concepts, physics principles, data concepts, and engineering decisions learned while building this project.

The goal is to explain concepts in simple language so that every part of the project can be understood and defended during development, presentations, and interviews.

---

# Project Goal

Detect unusual satellite behavior and estimate conjunction-risk patterns using physics-informed features derived from public orbital telemetry data.

---

# Orbital Mechanics

## What Is An Orbit?

A satellite remains in orbit because gravity continuously pulls it toward Earth while its forward velocity causes it to keep missing Earth.

An orbit can be thought of as a continuous free fall around the planet.

---

## Altitude

Altitude is the distance between a satellite and Earth's surface.

General relationship:

* Higher altitude → slower orbit
* Lower altitude → faster orbit

Examples:

| Orbit Type | Approximate Altitude |
| ---------- | -------------------- |
| ISS        | ~400 km              |
| Starlink   | ~550 km              |
| GPS        | ~20,200 km           |
| GEO        | ~35,786 km           |

---

## Mean Motion

Mean motion describes how many complete orbits a satellite makes per day.

Examples:

* ISS ≈ 15.5 orbits/day
* GPS ≈ 2 orbits/day
* GEO ≈ 1 orbit/day

Units:

```text
revolutions per day
```

Why it matters:

Mean motion is one of the most important variables in the project because changes in mean motion often indicate changes in orbit.

---

## Orbital Period

Orbital period is the time required for one complete orbit.

Formula:

```text
orbital_period_minutes = 1440 / mean_motion
```

Why 1440?

There are 1440 minutes in one day.

Example:

```text
Mean Motion = 15

Orbital Period = 1440 / 15

≈ 96 minutes
```

---

## Inclination

Inclination is the angle between a satellite's orbital plane and Earth's equator.

Examples:

* 0° = Equatorial orbit
* 90° = Polar orbit

Why it matters:

Satellites with different inclinations travel through different regions of space.

Inclination is useful for:

* orbit classification
* congestion analysis
* conjunction-risk estimation

---

## Eccentricity

Eccentricity describes how circular or elliptical an orbit is.

Values:

* 0 = perfect circle
* close to 1 = highly stretched ellipse

Why it matters:

Changes in eccentricity may indicate orbital maneuvers or unusual behavior.

---

## Semi-Major Axis

The semi-major axis represents the average distance from Earth's center to a satellite.

It is one of the most important orbital parameters because many other orbital properties can be derived from it.

The semi-major axis can be estimated from mean motion using orbital mechanics.

---

## Altitude Estimate

Altitude is not always directly available in the dataset.

It can be estimated using:

1. Mean motion
2. Semi-major axis
3. Earth's radius

Altitude estimation will be used as one of the engineered features in this project.

---

## Perigee and Apogee

Perigee:

* closest point to Earth

Apogee:

* farthest point from Earth

For a perfectly circular orbit:

```text
Perigee = Apogee
```

For elliptical orbits:

```text
Perigee ≠ Apogee
```

---

## Orbit Bands

| Band | Approximate Altitude | Examples                 |
| ---- | -------------------- | ------------------------ |
| LEO  | < 2,000 km           | ISS, Starlink            |
| MEO  | 2,000–35,786 km      | GPS, Galileo             |
| GEO  | ~35,786 km           | Communication satellites |
| HEO  | > 35,786 km          | Specialized missions     |

---

## BSTAR Drag Term

BSTAR is a parameter that estimates the effect of atmospheric drag.

Interpretation:

* Higher BSTAR → more drag
* More drag → faster orbital decay

Why it matters:

BSTAR helps identify satellites whose orbits may be changing because of atmospheric effects.

---

# Satellite Maneuvers

## What Is A Maneuver?

A maneuver occurs when a satellite intentionally changes its orbit using onboard propulsion.

Reasons include:

* collision avoidance
* orbit maintenance
* station keeping
* mission operations

---

## Why Mean Motion Drift Matters

A sudden change in mean motion often indicates a change in orbital velocity.

A change in orbital velocity usually means:

```text
Thrusters fired
→ Orbit changed
→ Mean motion changed
```

This makes mean motion drift one of the most important maneuver indicators.

---

## What Is Drift?

Drift represents the change in a value over time.

Examples:

* inclination drift
* eccentricity drift
* mean motion drift
* altitude drift
* BSTAR drift

A single observation describes state.

Multiple observations describe behavior.

---

# Conjunction Risk

## What Is A Conjunction?

A conjunction occurs when two orbital objects pass unusually close to each other.

Important:

A conjunction is not necessarily a collision.

It is simply a close approach event.

---

## Orbital Density

Orbital density describes how crowded a region of space is.

Examples:

* LEO contains many active satellites and debris objects.
* Some altitude bands are significantly more congested than others.

Higher density generally implies greater operational risk.

---

## Risk Score

This project does not perform real collision prediction.

Instead, it estimates a simplified conjunction-risk proxy score using:

* orbital density
* orbital similarity
* anomaly indicators
* altitude bands
* drift behavior

---

# Data Concepts

## GP Data

GP (General Perturbations) data is the orbital data format provided by CelesTrak.

The project uses GP JSON data rather than manually parsing traditional TLE text files.

---

## TLE

TLE stands for Two-Line Element Set.

Historically, orbital data was distributed using two text lines containing orbital parameters.

Modern GP JSON data contains the same information in a more structured format.

---

## Epoch

Epoch is the timestamp associated with an orbital measurement.

It indicates when the orbital parameters were generated.

---

## Epoch Age

Epoch age measures how old an orbital record is.

Example:

```text
Current Time - Epoch Time
```

Older records generally provide less reliable estimates of current orbital position.

---

# Data Engineering Concepts

## Data Ingestion

Ingestion is the process of collecting data from external sources.

For this project:

```text
CelesTrak API
→ Raw JSON
→ Local Storage
```

---

## Data Cleaning

Data cleaning ensures the dataset is suitable for analysis.

Tasks include:

* removing duplicates
* handling missing values
* validating ranges
* standardizing formats

---

## Validation

Validation checks whether values fall within physically reasonable limits.

Examples:

* inclination between 0° and 180°
* eccentricity between 0 and 1
* positive mean motion

---

## Feature Engineering

Feature engineering transforms raw orbital data into more informative variables.

Examples:

* orbital period
* altitude estimate
* epoch age
* drift metrics

Feature engineering is often more important than model selection.

---

# Machine Learning Concepts

## Anomaly Detection

An anomaly is an observation that differs significantly from expected behavior.

In this project:

* Isolation Forest identifies unusual orbital patterns
* Rolling z-scores identify unusual temporal changes

---

## Why Anomaly Detection?

Most satellites do not maneuver frequently.

This makes maneuver events relatively rare.

Anomaly detection is therefore a natural approach because it focuses on identifying unusual behavior rather than classifying known maneuver types.

---

# Software Engineering Concepts

## Separation of Concerns

Each folder and script should have a single responsibility.

Examples:

```text
ingestion → fetch data
cleaning → validate data
features → engineer features
models → anomaly detection
risk → risk scoring
dashboard → visualization
```

---

## Why Save Raw Data?

Raw data should never be modified.

Benefits:

* reproducibility
* debugging
* auditing
* comparison against processed outputs

The original API response should always remain available.

---

## Reproducibility

A project is reproducible if the same input data and code produce the same output.

This is an important requirement for both scientific analysis and machine learning systems.
