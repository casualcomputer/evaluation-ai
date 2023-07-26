- [ ] **Find data sources**

  - [X] scrape and save full evaluation reports from various government departments
  - [ ] scrape and save the recommendation sections of the evaluation reports in the previous step
- [ ] **Perform NLP tasks**

  - [ ] train/fine-tune word/sentence/document embeddings
    open-source models: Word2Vec, GloVe, FastText, ELMo, InferSent, Setence-BERT 
    proprietary models: OpenAI's ADA
  - [ ] cluster similar recommendations (extracted from 1.b.) using embeddings from 2.a.
  - [ ] summarize types of recommendations (extracted from 1.a.)

  open-source models: [models on HuggingFace](https://huggingface.co/models?pipeline_tag=summarization), like flan-T5

  proprietary models: gpt-3.5/4, [Cohere](https://cohere.com/summarize)

  - [ ] train sequence models to generate recommendations (RNN, LSTM, GRU, and transformers)
  - [ ] many more
