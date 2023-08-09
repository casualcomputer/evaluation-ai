# evaluation-ai

Open repository of codes to train language models for program evaluations.


## Usage
### Clone the repository

```bash
git clone https://github.com/casualcomputer/evaluation-ai.git
```

### Navigate to the script location
you can use `-h` with the scripts to see the help messages.

```bash
cd evaluation-ai/src/data/
python 00_load_raw_data.py
python 01_extract_text.py
```

## Data Sources

| Source Name              | Source Link                                                                                                                                                | Number of Extracted Reports |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| ESDC                     | [Link](https://www.canada.ca/en/employment-social-development/corporate/reports/evaluations.html)                                                          |                         177 |
| CRA                      | [Link](https://www.canada.ca/en/revenue-agency/programs/about-canada-revenue-agency-cra/internal-audit-program-evaluation.html)                            |                         196 |
| Health Canada            | [Link](https://www.canada.ca/en/health-canada/corporate/transparency/corporate-management-reporting/evaluation.html)                                       |                         129 |
| Natural Resources Canada | [Link](https://natural-resources.canada.ca/transparency/reporting-and-accountability/plans-and-performance-reports/strategic-evaluation-division/year/782) |                         119 |

### Naming Convention

- Reports are named as `<department acronym>_<id>_<title>.<extension>`

