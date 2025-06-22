# Interactive Threat Intelligence Dashboard 🛡️

A data visualization platform built with Python, Streamlit, and Pandas to analyze and display trends from cybersecurity threat data. This project acts as a strategic analysis layer on top of the "Vector-Threat" detection engine.


![alt text](https://i.imgur.com/cDOafwC.png)

![alt text](https://i.imgur.com/9slvmRv.png)


---

## 📖 Overview

While the "Vector-Threat" project is excellent at analyzing individual messages, security professionals need to see the bigger picture to understand attack campaigns. This "Threat-Intel Dashboard" solves that problem.

It's a full-stack data analytics platform that ingests the analysis results from the Vector-Threat API, stores them in a database, and presents the aggregated data in a dynamic, interactive web dashboard. This allows an analyst to move from single-instance threat detection to strategic trend analysis, answering questions like "What are the most common attack tactics this week?" or "Are we seeing a spike in high-risk alerts?".

---

## 🏛️ Architecture

This platform operates with a decoupled, two-part architecture, simulating a real-world data pipeline:

1.  **Vector-Threat API (The Engine):** The prerequisite project running on `localhost:5000`. It acts as a microservice responsible for analyzing message content.
2.  **Data Ingestion Pipeline (`ingest.py`):** A Python script that reads a dataset of messages, sends them to the Vector-Threat API for analysis, and stores the structured JSON results in a local SQLite database.
3.  **Threat-Intel Dashboard (`dashboard.py`):** The Streamlit application that reads from the SQLite database, processes the data with Pandas, and displays the interactive charts and filters.

---

## ✨ Key Features

*   **KPI Metrics:** High-level cards display key statistics like "Total Messages Analyzed," "Average Threat Score," and "Percentage of High-Risk Messages."
*   **Dynamic Visualizations:**
    *   **Top Threat Types:** A bar chart showing the most frequently occurring malicious findings.
    *   **Threats Over Time:** A line chart visualizing the number of threats detected per day.
*   **Interactive Filtering:** A powerful sidebar allows users to dynamically filter the entire dashboard by date range and threat score.
*   **Data Explorer:** A searchable, sortable table displays the raw, filtered data for in-depth review.

---

## 🛠️ Tech Stack

*   **Dashboard/Frontend:** Streamlit
*   **Data Processing & Analysis:** Pandas
*   **Database:** SQLite
*   **API for Ingestion:** Flask (from the `Vector-Threat` project)
*   **Language:** Python 3.9+
*   **Version Control:** Git & GitHub

---

## 🚀 How to Run This Project Locally

This project depends on the "Vector-Threat" API. You must run both projects simultaneously in separate terminals.

### Prerequisites
*   You have the `vector-threat` and `threat-intel-dashboard` project folders.
*   Both projects have their Python virtual environments set up and dependencies installed.

### Running the Application

1.  **Terminal 1: Start the Vector-Threat API**
    ```bash
    # Navigate to the vector-threat project
    cd path/to/vector-threat

    # Activate its virtual environment
    .\venv\Scripts\activate

    # Run the Flask server
    python app.py
    ```
    *Leave this terminal running.*

2.  **Terminal 2: Run the Data Ingestion (Only needs to be run once)**
    ```bash
    # Navigate to the threat-intel-dashboard project
    cd path/to/threat-intel-dashboard

    # Activate its virtual environment
    .\venv\Scripts\activate

    # Run the ingestion script to populate the database
    python ingest.py
    ```
    *You only need to do this the first time or when you want to add more data.*

3.  **Terminal 2 (or a new Terminal 3): Start the Dashboard**
    ```bash
    # In the threat-intel-dashboard project folder with venv active
    streamlit run dashboard.py
    ```
    A new tab will open in your browser displaying the interactive dashboard.
