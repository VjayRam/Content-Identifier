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

### **Benign Content Categories (9 categories):**
- Child Sexual Abuse and Exploitation and Sex Crimes
- Self-Harm and Suicide
- Illegal Activities and Violent Crimes
- Intellectual Property or Copyright Violations
- Privacy or PII Violations
- Defamation, Libel, or Slander
- Defrauding, Scamming, Spamming, or Phishing
- Espionage, Spying, Stalking, Hacking, or Doxing
- Chemical, Biological, Radiological, and Nuclear (CBRN) Threats

### **Sources of Harmful Content:**
- https://huggingface.co/datasets/PKU-Alignment/BeaverTails
- https://huggingface.co/datasets/PKU-Alignment/PKU-SafeRLHF
- https://huggingface.co/datasets/Anthropic/hh-rlhf
- Synthetic dataset generated using Qwen model and vLLM

### **Sources of Benign Content:**
- https://huggingface.co/datasets/PKU-Alignment/BeaverTails
- https://huggingface.co/datasets/PKU-Alignment/PKU-SafeRLHF
- https://huggingface.co/datasets/Anthropic/hh-rlhf
- Synthetic dataset generated using Qwen model and vLLM

### **Training Dataset:**

| Conversation type | Samples |
|--------------------|---------|
| User query only | 5256 |
| Assistant response only | 5256 |
| Mixed Conversations | 5256 |

#### Label 0 (Benign): 15768 total
- CSAE: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- SHS: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- VC: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- IP: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- PII: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- DEF: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- SCAM: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- ESP: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- CBRN: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}

#### Label 1 (Harmful): 15768 total
- CSAE: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- SHS: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- VC: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- IP: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- PII: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- DEF: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- SCAM: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- ESP: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}
- CBRN: 1752 -> {'user_only': 584, 'single_turn': 584, 'multi_turn': 584}

Total samples: 31536  (expected 2 x 9 x 3 x 584 = 31536)

### **Evaluation Dataset:**

| Conversation type | Samples |
|--------------------|---------|
| User query only | 630 |
| Assistant response only | 630 |
| Mixed Conversations | 630 |


#### Label 0 (Benign): 1890 total
- CSAE: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- SHS: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- VC: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- IP: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- PII: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- DEF: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- SCAM: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- ESP: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- CBRN: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}

#### Label 1 (Harmful): 1890 total
- CSAE: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- SHS: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- VC: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- IP: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- PII: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- DEF: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- SCAM: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- ESP: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}
- CBRN: 210 -> {'user_only': 70, 'single_turn': 70, 'multi_turn': 70}

Total samples: 3780  (expected 2 x 9 x 3 x 70 = 3780)
