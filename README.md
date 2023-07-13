# evaluation-ai

Open repository of codes to train language models for program evaluations.

1. Find data sources (scrape reports from various government departments)
2. Define NLP tasks of interest
   - extraction/summarization of recommendations from all program evaluation reports across departments
   - cluster similar recommendations
   - train a generative language model with LSTM, GRU, and transfromers

## Data Sources

| Source Name              | Source Link                                                                                                                                             | Number of Extracted Reports |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------: |
| ESDC                     | [Link](https://www.canada.ca/en/employment-social-development/corporate/reports/evaluations.html)                                                          |                         TBD |
| CRA                      | [Link](https://www.canada.ca/en/revenue-agency/programs/about-canada-revenue-agency-cra/internal-audit-program-evaluation.html)                            |                          19 |
| Health Canada            | [Link](https://www.canada.ca/en/health-canada/corporate/transparency/corporate-management-reporting/evaluation.html)                                       |                         126 |
| Natural Resources Canada | [Link](https://natural-resources.canada.ca/transparency/reporting-and-accountability/plans-and-performance-reports/strategic-evaluation-division/year/782) |                         TBD |

### Naming Convention

- Reports are named as `<department acronym>_<id>_<title>.txt`
- Concatenated reports are named as `<department acronym>_all.txt`
