# evaluation-ai

Open repository of codes to train language models for program evaluations.

1.  **Find data sources**

    a\. scrape and save full evaluation reports from various government departments

    b\. scrape and save the recommendation sections of the evaluation reports in the previous step

2.  **Perform NLP tasks**

    a\. train/fine-tune word/sentence/document embeddings

    open-source models: Word2Vec, GloVe, FastText, ELMo, InferSent, Setence-BERT

    proprietary models: OpenAI's ADA

    b\. cluster similar recommendations (extracted from 1.b.) using embeddings from 2.a.

    c\. summarize types of recommendations (extracted from 1.a.)

    open-source models: [models on HuggingFace](https://huggingface.co/models?pipeline_tag=summarization), like flan-T5

    proprietary models: gpt-3.5/4, [Cohere](https://cohere.com/summarize)

    d\. train sequence models to generate recommendations (RNN, LSTM, GRU, and transformers)

    e\. many more

## Data Sources

| Source Name              | Source Link                                                                                                                                                | Number of Extracted Reports |
|:------------|:----------------------------------------------|------------:|
| ESDC                     | [Link](https://www.canada.ca/en/employment-social-development/corporate/reports/evaluations.html)                                                          |                         TBD |
| CRA                      | [Link](https://www.canada.ca/en/revenue-agency/programs/about-canada-revenue-agency-cra/internal-audit-program-evaluation.html)                            |                         196 |
| Health Canada            | [Link](https://www.canada.ca/en/health-canada/corporate/transparency/corporate-management-reporting/evaluation.html)                                       |                         126 |
| Natural Resources Canada | [Link](https://natural-resources.canada.ca/transparency/reporting-and-accountability/plans-and-performance-reports/strategic-evaluation-division/year/782) |                         TBD |

### Naming Convention

-   Reports are named as `<department acronym>_<id>_<title>.txt`
-   Concatenated reports are named as `<department acronym>_all.txt`
