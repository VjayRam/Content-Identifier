### **Phase 1: Dataset Generation & Curation**

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