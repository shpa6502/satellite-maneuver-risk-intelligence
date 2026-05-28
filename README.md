# Orbital Intelligence Platform

## Project Title

Satellite Maneuver Detection & Conjunction Risk Intelligence Platform

---

## Overview

This project builds an end-to-end data analytics and machine learning pipeline for satellite maneuver detection and conjunction-risk analysis using real CelesTrak GP JSON orbital data.

The system processes public satellite orbital records, cleans and validates the data, engineers physics-based features, detects anomalous orbital behavior, computes simplified conjunction-risk scores, and presents the results in a Streamlit dashboard.

---

## Problem

Earth orbit is becoming increasingly crowded with active satellites and orbital debris.

This project focuses on:
- detecting unusual orbital behavior
- identifying anomalous satellite maneuvers
- analyzing orbital congestion patterns
- estimating conjunction-risk proxy scores

using public orbital telemetry data.

---

## Data Source

Primary source:
- CelesTrak GP JSON API

Example endpoint:

```text
https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json
```

Planned groups:
- active
- starlink
- debris

---

## Pipeline

```text
ingestion
→ cleaning
→ feature engineering
→ anomaly detection
→ risk scoring
→ Streamlit dashboard
→ deployment
```

---

## Planned Features

The project will engineer:

- inclination
- eccentricity
- mean motion
- orbital period
- altitude estimate
- BSTAR drag proxy
- epoch age
- drift versions of orbital features over time

---

## Models

Initial models:

- Isolation Forest for anomaly detection
- rolling z-scores for drift flags

---

## Dashboard

The Streamlit dashboard will include:

- object search
- anomaly table
- risk score ranking
- orbit band density chart

---

## Goal

The goal is to build a serious portfolio project demonstrating:

- data cleaning
- pipeline design
- physics-informed feature engineering
- anomaly detection
- risk analytics
- deployment
