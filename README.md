# evaluation-ai
Open repository of codes to train language models for program evaluations.

1. Find data sources (scrape reports from various government departments)
2. Define NLP tasks of interest
   - extraction/summarization of recommendations from all program evaluation reports across departments
   - cluster similar recommendations
   - train a generative language model with LSTM, GRU, and transfromers

## Data Sources
- [ESDC](https://www.canada.ca/en/employment-social-development/corporate/reports/evaluations.html)
- [CRA](https://www.canada.ca/en/revenue-agency/programs/about-canada-revenue-agency-cra/internal-audit-program-evaluation.html)
- [Health Canada](https://www.canada.ca/en/health-canada/corporate/transparency/corporate-management-reporting/evaluation.html)
- [Natural Resources Canada](https://natural-resources.canada.ca/transparency/reporting-and-accountability/plans-and-performance-reports/strategic-evaluation-division/year/782)
