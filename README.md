# Cloud-Based Stroke Risk ETL & Analytics Pipeline

A cloud-native end-to-end data engineering project designed to collect, transform, store, and analyze healthcare data related to **stroke risk factors** using AWS and Python.

This project demonstrates how a scalable ETL pipeline can power public-health analytics — identifying trends, patterns, and risk correlations in real-world healthcare data.

---

## Overview

This project automates the ingestion and transformation of a stroke prediction dataset and stores it in a cloud-hosted PostgreSQL database.
The pipeline enables data scientists and analysts to efficiently query and visualize stroke-related risk patterns — such as the impact of **age, BMI, glucose level, hypertension, and lifestyle** on stroke occurrence.

The project is built with industry-standard practices: modular ETL scripts, centralized logging, environment-based configuration, versioned dependencies, and clear documentation.

---

## Business Problem

Stroke remains one of the leading causes of death and disability globally, with most cases being preventable through early identification of risk factors.
Healthcare organizations, insurers, and policy makers face challenges due to **fragmented and unstructured data**, which limits their ability to proactively identify and intervene in high-risk populations.

---

## Objective

To design and deploy a **cloud-based data pipeline** that:

1. Ingests stroke-related health data from a public dataset.
2. Cleans, transforms, and augments it with a calculated risk score.
3. Loads the processed data into a centralized PostgreSQL database (AWS RDS).
4. Enables analytics and visualization of stroke risk trends.

---

##  Business Value

| Sector                     | Application                                               | Example Outcome                            |
| -------------------------- | --------------------------------------------------------- | ------------------------------------------ |
| **Hospitals / Clinics**    | Integrate patient risk analytics into EHR systems.        | Early intervention for high-risk patients. |
| **Insurance Companies**    | Assess population-level stroke risk for policy modeling.  | Reduced long-term claim costs.             |
| **Public Health Agencies** | Monitor demographic risk patterns and health disparities. | Targeted prevention programs.              |
| **HealthTech Startups**    | Build stroke-prevention dashboards or wellness apps.      | Personalized health insights for users.    |

---

## Dataset

**Source:** [Kaggle – Stroke Prediction Dataset](https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset)

| Column              | Description                                                  |
| ------------------- | ------------------------------------------------------------ |
| `gender`            | Male / Female / Other                                        |
| `age`               | Age in years                                                 |
| `hypertension`      | 0 = No, 1 = Yes                                              |
| `heart_disease`     | 0 = No, 1 = Yes                                              |
| `ever_married`      | Yes / No                                                     |
| `work_type`         | Private / Self-employed / Govt_job / Children / Never_worked |
| `residence_type`    | Urban / Rural                                                |
| `avg_glucose_level` | Average glucose level                                        |
| `bmi`               | Body mass index                                              |
| `smoking_status`    | formerly smoked / never smoked / smokes / Unknown            |
| `stroke`            | 0 = No stroke, 1 = Stroke                                    |

---
## Architecture

```
+--------------------+
| Stroke Dataset     |
| (Kaggle)           |
+---------+----------+
          |
          v
+---------+----------+
| AWS S3 (Raw Layer) |
+---------+----------+
          |
          v
+---------+----------+
| Python ETL Scripts |
| (Ingest, Transform)|
+---------+----------+
          |
          v
+---------+----------+
| AWS RDS PostgreSQL |
| (Processed Layer)  |
+---------+----------+
          |
          v
+--------------------+
| Jupyter / Streamlit|
| (Visualization)    |
+--------------------+
```

---

## Tech Stack

| Component        | Tool / Service                                           |
| ---------------- | -------------------------------------------------------- |
| Cloud            | AWS (S3, RDS)                                            |
| Language         | Python 3.11                                              |
| Libraries        | pandas, boto3, psycopg2, SQLAlchemy, matplotlib, seaborn |
| Config & Secrets | `.env`, `python-dotenv`, `config.yaml`                   |
| Logging          | Python `logging` module (custom logger)                  |
| Orchestration    | Makefile                                                 |
| Version Control  | GitHub                                                   |
| Visualization    | Jupyter Notebook / Streamlit                             |

---

## Features

 End-to-end **ETL pipeline** (Ingest → Transform → Load)
 Automatic **logging system** for each step
 **AWS cloud integration** (S3 for storage, RDS for database)
 **Data cleaning and enrichment**, including a custom risk score
 **Reproducible analysis notebook** for visualization and insights
 Follows **industry best practices** for documentation, style, and security

---

## Risk Score Formula (Feature Engineering)

A derived metric to quantify potential stroke risk:

```python
risk_score = (age/100)*0.4 + hypertension*0.2 + heart_disease*0.2 + (avg_glucose_level/200)*0.2
```

This feature was added during the transformation stage to simulate how healthcare analysts might quantify patient risk profiles.

---

## Example Insights

| Insight            | Observation                                                  |
| ------------------ | ------------------------------------------------------------ |
| **Age Factor**     | 75% of stroke patients were aged 50 or older.                |
| **Hypertension**   | Doubles the likelihood of a stroke event.                    |
| **BMI**            | Overweight individuals (BMI > 30) showed a 3× higher risk.   |
| **Glucose Levels** | Average glucose > 150 mg/dL correlated strongly with stroke. |

*(Visuals in `/assets/`)*

---

## Repository Structure

```
stroke-risk-etl/
├── etl/
│   ├── ingest.py          # Fetch & upload raw data to S3
│   ├── transform.py       # Clean, enrich, and process data
│   ├── load.py            # Insert processed data into PostgreSQL
│   ├── logger.py          # Centralized logging configuration
│   └── utils.py           # Helper functions
├── infra/
│   ├── schema.sql         # Database table schema
│   ├── aws_setup.md       # AWS setup guide
│   └── config.yaml        # Pipeline config
├── notebooks/
│   └── stroke_analysis.ipynb
├── logs/
│   └── etl_YYYYMMDD.log
├── assets/
│   ├── architecture.png
│   ├── correlation_heatmap.png
│   └── dashboard.png
├── requirements.txt
├── Makefile
├── .env.example
└── README.md
```

---

## Resproducability

### 1️ Clone Repository

```bash
git clone https://github.com/<your-username>/stroke-risk-etl.git
cd stroke-risk-etl
```

### 2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3 Configure Environment

Copy `.env.example` → `.env` and fill in AWS & DB credentials.

### 4 Run Pipeline

```bash
make run-all
```

Or manually:

```bash
python etl/ingest.py
python etl/transform.py
python etl/load.py
```

### 5️⃣ Run Analysis

Open `notebooks/stroke_analysis.ipynb` or launch Streamlit dashboard (if applicable).

---

## Project Standards

| Category                  | Standard Followed                                    |
| ------------------------- | ---------------------------------------------------- |
| **Logging**               | Python `logging` with timestamped logs under `/logs` |
| **Code Style**            | PEP 8 & Google Python Style Guide                    |
| **Documentation**         | Google-style docstrings + structured README          |
| **Version Control**       | GitHub flow with branches & PRs                      |
| **Environment**           | `.env` for secrets, `config.yaml` for parameters     |
| **Dependency Management** | Pinned versions in `requirements.txt`                |
| **Reproducibility**       | Deterministic transformations & fixed random seeds   |
| **Automation**            | `Makefile` for orchestration                         |
| **Security**              | Least-privilege IAM roles for S3/RDS access          |

---

## Authors

**Amisha Das** – Data Scientist  
**Daniel Hakim** – Data Engineer
*(MSc Data Science, South East Technological University)*

---

## Future Work

* Deploy a flex dashboard dashboard publicly
* Add a lightweight API for querying risk scores
* Experiment with ML models for stroke prediction
* Automate pipeline orchestration using Prefect

