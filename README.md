# Candidate Profile Transformer

## Overview

Candidate Profile Transformer is a configurable data processing pipeline that ingests candidate information from multiple heterogeneous sources, normalizes and merges the data into a canonical profile, tracks provenance and confidence, and produces runtime-configurable output schemas.


### Supported Source Types

#### Structured Sources

* ATS JSON
* Recruiter CSV

#### Unstructured Sources

* Resume PDF

---

# Architecture

```
ATS JSON
          \
Resume PDF ---> Parsing ---> Normalization ---> Entity Matching
          /                                      |
Recruiter CSV                                    |
                                                 v
                                          Merge Engine
                                                 |
                                                 v
                                           Provenance
                                                 |
                                                 v
                                           Confidence
                                                 |
                                                 v
                                   Canonical Candidate Profile
                                                 |
                                                 v
                                        Projection Layer
                                                 |
                                                 v
                                        Schema Validator
                                                 |
                                                 v
                                            JSON Output
```

---

# Features

## Multi-Source Ingestion

Supports ingestion from:

* ATS exports (JSON)
* Recruiter spreadsheets (CSV)
* Candidate resumes (PDF)

---

## Data Normalization

### Phone Numbers

Normalized to E.164 format.

Example:

```
9876543210
```

becomes

```
+919876543210
```

### Country Codes

Normalized to ISO-3166 Alpha-2.

Example:

```
India -> IN
United States -> US
```

### Skills

Canonicalized using a skill normalization layer.

Examples:

```
js -> JavaScript
reactjs -> React
py -> Python
```

---

## Entity Matching

Candidates are matched using:

1. Exact email match
2. Exact phone match
3. Name similarity using SequenceMatcher

---

## Merge Strategy

Source priority:

```
ATS JSON > Resume PDF > Recruiter CSV
```

Conflict resolution:

* Name -> highest priority source
* Email -> highest priority source
* Phone -> highest priority source
* Skills -> union + deduplication

---

## Provenance

Every selected field records:

* field
* source
* method

Example:

```json
{
  "field": "full_name",
  "source": "ATS_JSON",
  "method": "source_priority"
}
```

---

## Confidence Scoring

Source confidence:

| Source        | Confidence |
| ------------- | ---------- |
| ATS JSON      | 0.95       |
| Resume PDF    | 0.85       |
| Recruiter CSV | 0.75       |

The final profile includes:

* per-skill confidence
* overall confidence

---

# Canonical Profile Schema

```json
{
  "candidate_id": "string",
  "full_name": "string",
  "emails": [],
  "phones": [],
  "location": {
    "city": "string",
    "region": "string",
    "country": "string"
  },
  "links": {},
  "headline": "string",
  "years_experience": 0,
  "skills": [],
  "experience": [],
  "education": [],
  "provenance": [],
  "overall_confidence": 0.0
}
```

---

# Runtime Configurable Output

The pipeline supports runtime projection without code changes.

Capabilities:

* Field selection
* Field renaming
* Confidence toggle
* Provenance toggle
* Missing-value policies

Supported missing-value policies:

```
null
omit
error
```

Example:

```json
{
  "fields": [
    {
      "path": "candidate_name",
      "from": "full_name"
    },
    {
      "path": "primary_email",
      "from": "emails[0]"
    }
  ],
  "include_confidence": true,
  "include_provenance": true,
  "on_missing": "null"
}
```

The projection layer supports:

- Field selection
- Field remapping
- Confidence inclusion/exclusion
- Provenance inclusion/exclusion
- Missing value handling (null / omit / error)

---

# Installation

## Clone Repository

```bash
git clone https://github.com/avantgarde-rk/candidate-profile-transformer.git
cd candidate-transformer
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

## CLI Usage

```bash
python main.py --ats data/ats/sample_ats.json --resume data/resumes/RakeshResume.pdf --csv data/recruiter/sample_recruiter.csv --config configs/custom_config.json
```

---

# Sample Output

```json
{
  "candidate_name": "Rakesh R",
  "primary_email": "rakesh@example.com",
  "primary_phone": "+919876543210",
  "overall_confidence": 0.95
}
```

---

# Running Tests

Run all tests:

```bash
pytest -v
```

Expected:

```
7 passed
```

---

# Test Coverage

The project includes both unit tests and evaluator-style robustness tests.

### Unit Tests

- Entity Matching
- Name Similarity Matching
- Phone Normalization
- Skill Normalization
- Merge Engine
- Projection Engine
- Schema Validation

### Robustness Tests

The following real-world edge cases were tested:

| Test Case | Result |
|------------|---------|
| Resume without email | Passed |
| Resume without phone | Passed |
| Resume without skills | Passed |
| Corrupted PDF | Passed |
| Empty CSV | Passed |
| Missing CSV columns | Passed |
| Missing projection field | Passed |
| Country normalization | Passed |
| Deterministic ID generation | Passed |
| Skill union across sources | Passed |
| Source-priority conflict resolution | Passed |

All tests completed successfully.

# Example Commands

### Default Run

```bash
python main.py --ats data/ats/sample_ats.json --resume data/resumes/RakeshResume.pdf --csv data/recruiter/sample_recruiter.csv --config configs/custom_config.json
```

### Run with Custom ATS

```bash
python main.py --ats my_ats.json --resume my_resume.pdf --csv my_recruiter.csv --config configs/custom_config.json
```

# Edge Cases Covered

* Missing email
* Missing phone
* Missing skills
* Corrupted PDF
* Empty CSV
* Missing CSV columns
* Missing projection fields
* Country normalization
* Name similarity matching

---

# Assumptions

* ATS data is considered the most reliable source.
* Resume PDF may contain incomplete or noisy information.
* Unknown values are never invented.
* Missing values become null, omitted, or errors based on configuration.
* Country normalization is limited to supported mappings.

---

# Deliberately Out of Scope

To keep the solution focused and deterministic:

* LinkedIn scraping
* LLM-based extraction
* OCR for scanned resumes
* Distributed processing
* Advanced NLP experience extraction
* External API enrichment

---

# Project Structure

```
candidate-transformer/
│
├── configs/
├── data/
│   ├── ats/
│   ├── recruiter/
│   └── resumes/
│
├── src/
│   ├── confidence/
│   ├── matching/
│   ├── merger/
│   ├── models/
│   ├── normalizers/
│   ├── parsers/
│   ├── projection/
│   ├── provenance/
│   ├── utils/
│   └── validation/
│
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

---

# Author

Rakesh R

