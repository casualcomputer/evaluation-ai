# Evaluation-AI: A LLM for Assessing Government Programs

The Evaluation-AI repository is dedicated to building a comprehensive collection of program evaluation reports and leveraging state-of-the-art techniques in large language models (LLMs) to create a powerful tool for assessing government programs. Our mission is to develop a model that can effectively understand and analyze policy frameworks using retrieval-augmented generation (RAG) and a hybrid search strategy. We are committed to transparency and open-source fairness measurement to ensure the reliability and equity of our models.

## Objectives
Repository of Program Evaluation Reports: 
- Curate and maintain a rich collection of program evaluation reports, serving as a valuable resource for researchers and practitioners.
- Advanced LLM Training: Utilize the latest advancements in LLMs to train a model that comprehensively understands policy frameworks and program evaluation contexts.
- Retrieval-Augmented Generation (RAG): Employ a hybrid search strategy combining traditional retrieval methods with generative capabilities to enhance information extraction and comprehension.
- Contextual Application: Develop and tailor the tool for various tasks within the program evaluation context, ensuring its relevance and effectiveness in real-world applications.

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

