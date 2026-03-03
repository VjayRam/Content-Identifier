### **Phase 1: Dataset Generation & Curation**

Sources:
- https://huggingface.co/datasets/PKU-Alignment/BeaverTails
- https://huggingface.co/datasets/PKU-Alignment/PKU-SafeRLHF
- https://huggingface.co/datasets/Anthropic/hh-rlhf

- [x]  **Generate/Curate Training Dataset:** Gather the primary data for the classifier.
    - [x]  Use a mix of published and synthetic datasets
- [x]  **Create Synthetic Eval Dataset:** Generate a separate set of 2k–4k synthetic samples.
- [x]  **Deliverable:** Upload the training set to **HuggingFace** and save the link.
- [x]  **Deliverable:** Prepare the evaluation dataset (as a `.json` or HF link).
- [x]  **Deliverable:** Clean up and include your generation/compilation code.

---

### **Phase 2: Model Training**

- [x]  **Train Model:** Fine-tune a binary classifier (e.g., using a **SmolLM** base).
    - [x]  RoBERTa
    - [x]  Gemma 3-1B-IT
- [x]  **Deliverable:** Export the training log file (tracking loss, steps, etc.).
    - [x]  WandB or MLFlow Experiment Tracking
- [x]  **Deliverable:** Finalize the training script/notebook.
    - [x]  Colab or Local
- [x]  **Deliverable:** Upload the trained model to **HuggingFace** and save the link.

---

### **Phase 3: Evaluation & Analysis**

- [x]  **Run Evaluation:** Calculate the following metrics on your eval set:
    - **AUPR** & **ROC**
    - **FPR at 90% Recall**
    - **FPR at 95% Recall**
- [x]  **Deliverable:** Include the evaluation code.
- [x]  **Deliverable:** Create a 10-sample subset showing "Sample | Prediction | Ground Truth."
- [ ]  **Deliverable:** Write the discussion of findings (analysis of performance and edge cases).
- [ ]  **Deliverable:** List the final evaluation metrics clearly.



## **Dataset Summary:**

### Dimensions

- **Labels (2):** `0` = Benign, `1` = Harmful
- **Categories (9):** CSAE, SHS, VC, IP, PII, DEF, SCAM, ESP, CBRN
- **Conversation Types (3):** `user_only`, `single_turn`, `multi_turn`
- **Target cells:** 2 x 9 x 3 = **54 unique combinations**

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

### **Test Dataset:**

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

### **Dataset Curation Algorithm:**

### Track 1: Training Data (`train_data_generator.ipynb`)

**Step 1 — Ingest & Compile** existing open-source datasets into a unified `{messages, label, source}` format:
- **BeaverTails** (PKU-Alignment) — single-turn prompt/response pairs with `is_safe` labels
- **PKU-SafeRLHF** — single-turn with two responses per prompt, each independently labeled safe/unsafe
- **Anthropic HH-RLHF** — multi-turn Human/Assistant conversations; `chosen` mapped to benign, `rejected` to harmful; parsed from Anthropic's custom text format into `[{role, content}]`

**Step 2 — Conversation Type Mutation.** Each sample is assigned a `conv_type`:
- Messages with > 2 turns become `multi_turn`
- Of the remaining single-turn pairs, ~20% are randomly **mutated to `user_only`** by dropping the assistant response
- The rest stay `single_turn`
- A `raw_text` column is built: `"USER: ...\nASSISTANT: ..."`

**Step 3 — vLLM Category Classification.** Qwen 2.5-7B-Instruct-AWQ classifies each sample into one of the 9 safety categories:
- A zero-shot system prompt lists all 9 category abbreviations with descriptions
- The model reads `raw_text` and returns the best-matching abbreviation
- Unclassified samples are filtered out
- Capped at 30,000 samples for GPU efficiency

**Step 4 — Hierarchical 3D Balancing.** A two-pass algorithm balances across all three dimensions:
- Computes target counts: `target_total / 2 labels / 9 categories / 3 types`
- **Pass 1:** For each (label, category, type) cell, take up to `target_per_type` samples
- **Pass 2:** Any shortfall in a type is backfilled from leftover samples in the same (label, category) group

**Step 5 — Gap Analysis & Generation-Based Filling.** After balancing, the `analyze_and_standardize` function:
1. **Analyzes** every (label, category, conv_type) cell and prints a BEFORE summary
2. **Computes** the target per cell (max count across all 54 cells)
3. **Generates** new samples for under-filled cells using vLLM (Qwen 2.5-7B-Instruct-AWQ):
   - For each (category, conv_type) with shortfall, builds a **contrastive generation prompt** that produces a JSON array of 2 items (1 harmful + 1 benign)
   - The prompt is tailored per `conv_type`: user_only requires exactly 1 message, single_turn requires user + assistant, multi_turn requires 4-6 alternating messages
   - Generated messages are normalized (handles `:role`/`-role` key quirks) and `raw_text` is populated
4. **Standardizes** — any residual shortfall is filled by sampling with replacement; excess cells are trimmed down
5. Prints an AFTER summary with final counts

**Step 6 — Gemma Formatting & Stratified Split:**
- Messages are normalized for Gemma's chat template (alternating user/assistant, merges consecutive same-role)
- `label` is cast to `ClassLabel(["benign", "harmful"])`
- A composite `stratify_key = "{label}_{category}"` enables **stratified train/val split** (90/10) that preserves proportions
- Final `DatasetDict` with `train` and `val` splits is saved and pushed to the Hub

---

### Track 2: Eval Data (`eval_data_generator.ipynb`)

**Step 1 — Bulk Synthetic Generation.** No existing datasets — everything is generated from scratch:
- 70 requests per (category, conv_type) combo = 70 x 9 x 3 = **1,890 vLLM calls**
- Each call uses the same contrastive prompt as Track 1, producing 2 samples (1 harmful + 1 benign)
- Target: ~3,780 synthetic samples

**Step 2 — Gap Analysis & Standardization.** Identical to Track 1's Step 5:
- Analyzes the 54 cells for imbalance (JSON parse failures cause uneven counts)
- Generates additional samples for under-filled cells
- Standardizes all cells to the same count

**Step 3 — Gemma Normalization:**
- Messages normalized for Gemma alternation, `raw_text` built
- Saved to disk and pushed to the Hub as the eval dataset

---

### Key Design Decisions

| Aspect | Choice |
|---|---|
| **Generation model** | Qwen 2.5-7B-Instruct-AWQ (fast, fits Colab T4) |
| **Target model** | Gemma 3-1B-IT (lightweight classifier to be trained) |
| **Prompt strategy** | Contrastive pairs — each call produces both a harmful and benign example on the same topic, ensuring the model learns the boundary |
| **Balancing** | Two-stage: coarse hierarchical balancing first, then fine-grained per-cell standardization with generation to minimize duplicate sampling |
| **Message normalization** | Handles Hub dataset quirks (`:role`, `-role` keys) and enforces alternating user/assistant for Gemma compatibility |

---

## **Repository Guide**

This section provides a high-level overview of the repository structure to help you navigate the files and understand their specific purposes:

### 📁 Root Directory
- `README.md`: The main documentation for the project, detailing methodology, datasets, and structure.
- `main.py` / `pyproject.toml`: Project entry points and dependency configurations for standard environment setups.

### 📁 scripts/
Contains all the Jupyter Notebooks used for data processing, model training, and evaluation.
- `train_data_generator.ipynb`: Code for curating, balancing, and synthetically generating the training dataset (Track 1).
- `eval_data_generator.ipynb`: Code for generating the purely synthetic evaluation dataset (Track 2).
- `data_processing.ipynb`: Utility notebook for testing out raw message parsing and standardization mappings.
- `model_trainer_roberta.ipynb`: Complete training pipeline for the RoBERTa model, including Optuna hyperparameter sweeps.
- `model_trainer_gemma.ipynb`: Complete training pipeline for the Gemma 3-1B-IT model, using a custom BCE Loss implementation for binary classification.
- `model_evaluation_roberta.ipynb`: Evaluation script for RoBERTa, producing test metrics (AUPR, ROC AUC, FPR) and False Positive/Negative reviews.
- `model_evaluation_gemma.ipynb`: Evaluation script for Gemma 3-1B-IT, producing identical test metrics.
- `model_inferencing.ipynb`: An inference sandbox providing single-sample and batch-processing wrapper functions for quick testing across both models.

### 📁 data/
Stores the raw datasets and generated files used throughout the project lifecycle.
- **raw/**: Starting raw imports (if saved locally).
- **train/**: Contains the final balanced subsets (`train_sampled.csv`, `val_sampled.csv`).
- **test/**: Contains the 100% synthetic eval set (`test_dataset.csv`).

### 📁 logs/
Stores output metrics, experimental runs, and result datasets generated during notebook execution.

> **Note:** Files with the suffix `_01` indicate results or outcomes from models trained using standard Cross-Entropy Loss (treated as multi-class classification), whereas files with the suffix `_02` represent outcomes from models properly trained using Binary Cross-Entropy (BCE) Loss (binaru classification).

- **experiments/**: Hyperparameter tracking runs (CSV logs).
- **metrics/**: JSON files containing the final output scores (AUPR, FPR, Latency) for each trained model.
- **outputs/**: Test prediction CSVs populated with model confidences (`test_predictions_gemma.csv`, `test_predictions_roberta.csv`).

### 📁 docs/
Holds PDF versions or Markdown extracts of completed run reports for easier review without re-executing notebooks.

### 📁 utils/
- `gpu_verify.py`: Quick diagnostic script to check GPU availability and CUDA bindings before running local training blocks.


