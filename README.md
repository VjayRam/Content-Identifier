### **Phase 1: Dataset Generation & Curation**

Sources:
- https://huggingface.co/datasets/LLM-LAT/harmful-dataset
- https://huggingface.co/datasets/LLM-LAT/benign-dataset
- https://huggingface.co/datasets/mteb/ToxicChatClassification
- https://huggingface.co/datasets/Anthropic/hh-rlhf
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

- [ ]  **Generate/Curate Training Dataset:** Gather the primary data for the classifier.
    - [ ]  Use a mix of published and synthetic datasets
    - [ ]  DVC for Dataset Tracking
- [ ]  **Create Synthetic Eval Dataset:** Generate a separate set of 2k–4k synthetic samples.
- [ ]  **Deliverable:** Upload the training set to **HuggingFace** and save the link.
- [ ]  **Deliverable:** Prepare the evaluation dataset (as a `.json` or HF link).
- [ ]  **Deliverable:** Clean up and include your generation/compilation code.

---

### **Phase 2: Model Training**

- [ ]  **Train Model:** Fine-tune a binary classifier (e.g., using a **SmolLM** base).
    - [ ]  BERT
    - [ ]  SmolLM
- [ ]  **Deliverable:** Export the training log file (tracking loss, steps, etc.).
    - [ ]  WandB or MLFlow Experiment Tracking
- [ ]  **Deliverable:** Finalize the training script/notebook.
    - [ ]  Colab or Local
- [ ]  **Deliverable:** Upload the trained model to **HuggingFace** and save the link.

---

### **Phase 3: Evaluation & Analysis**

- [ ]  **Run Evaluation:** Calculate the following metrics on your eval set:
    - **AUPR** & **ROC**
    - **FPR at 90% Recall**
    - **FPR at 95% Recall**
- [ ]  **Deliverable:** Include the evaluation code.
- [ ]  **Deliverable:** Create a 10-sample subset showing "Sample | Prediction | Ground Truth."
- [ ]  **Deliverable:** Write the discussion of findings (analysis of performance and edge cases).
- [ ]  **Deliverable:** List the final evaluation metrics clearly.



## **Dataset Summary:**

### **Harmful Content Categories (9 categories):**
- Child Sexual Abuse and Exploitation and Sex Crimes
- Self-Harm and Suicide
- Illegal Activities and Violent Crimes
- Intellectual Property or Copyright Violations
- Privacy or PII Violations
- Defamation, Libel, or Slander
- Defrauding, Scamming, Spamming, or Phishing
- Espionage, Spying, Stalking, Hacking, or Doxing
- Chemical, Biological, Radiological, and Nuclear (CBRN) Threats

### **Benign Content Categories (2 categories):**
- Mildly Harmful
- General Query and Response

### **Sources of Harmful Content:**
- https://huggingface.co/datasets/LLM-LAT/harmful-dataset
- https://huggingface.co/datasets/mteb/ToxicChatClassification
- https://huggingface.co/datasets/Anthropic/hh-rlhf
- Synthetic dataset generated using Qwen model and vLLM

### **Sources of Benign Content:**
- https://huggingface.co/datasets/LLM-LAT/benign-dataset
- https://huggingface.co/datasets/Anthropic/hh-rlhf
- https://huggingface.co/datasets/mteb/ToxicChatClassification
- Synthetic dataset generated using Qwen model and vLLM

### **Training Dataset:**

#### **Total Harmful Samples: 9000**

#### **Conversation type distribution of Harmful Samples:**

| Conversation type | Samples |
|--------------------|---------|
| User query only | 3000 |
| Assistant response only | 3000 |
| Mixed Conversations | 3000 |

#### **Source wise distribution of Harmful Samples:**

| Source | Samples per category | Samples per source |
|--------|----------------------|----------------------|
| LLM-LAT/harmful-dataset | 250 | 2250 |
| LLM-LAT/benign-dataset | 250 | 2250 |
| mteb/ToxicChatClassification | 250 | 2250 |
| Anthropic/hh-rlhf | 250 | 2250 |
| Synthetic | 250 | 2250 |

#### **Total Benign Samples: 9000**

#### **Conversation type distribution of Benign Samples:**

| Conversation type | Samples |
|--------------------|---------|
| User query only | 3000 |
| Assistant response only | 3000 |
| Mixed Conversations | 3000 |

#### **Source wise distribution of Benign Samples:**

| Source | Samples per category | Samples per source |
|--------|----------------------|----------------------|
| LLM-LAT/benign-dataset | 1500 | 3000 |
| mteb/ToxicChatClassification | 1500 | 3000 |
| Synthetic | 1500 | 3000 |

### **Evaluation Dataset:**

#### **Total Harmful Samples: 1800**

#### **Conversation type distribution of Harmful Samples:**

| Conversation type | Samples |
|--------------------|---------|
| User query only | 600 |
| Assistant response only | 600 |
| Mixed Conversations | 600 |


#### **Source wise distribution of Harmful Samples:**

| Source | Samples per category | Samples per source |
|--------|----------------------|----------------------|
| LLM-LAT/harmful-dataset | 50 | 450 |
| LLM-LAT/benign-dataset | 50 | 450 |
| mteb/ToxicChatClassification | 50 | 450 |
| Anthropic/hh-rlhf | 50 | 450 |
| Synthetic | 50 | 450 |


#### **Total Benign Samples: 1800**

#### **Conversation type distribution of Benign Samples:**
| Conversation type | Samples |
|--------------------|---------|
| User query only | 600 |
| Assistant response only | 600 |
| Mixed Conversations | 600 |


#### **Source wise distribution of Benign Samples:**
| Source | Samples per category | Samples per source |
|--------|----------------------|----------------------|
| LLM-LAT/benign-dataset | 300 | 600 |
| mteb/ToxicChatClassification | 300 | 600 |
| Synthetic | 300 | 600 |
