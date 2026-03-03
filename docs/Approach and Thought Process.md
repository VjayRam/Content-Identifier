# Thoughts and Reflections on the Content Identifier Task

## 1. Initial Brainstorming 
Upon going through the task details and requirements, I identified **3 critical choices** that I needed to make:
1. **Dataset Design** 
2. **Model Selection**
3. **Infrastructure Setup and Model Training**
4. **Evaluation Metrics** *(Added as a 4th critical choice later)*

This instinctively led to the decision to divide the workflow into **4 well-defined phases**:
1. Data Curation and Generation
2. Model Training 
3. Model Evaluation 
4. Result Analysis and Documentation 

---

## 2. Doubts and Clarifications 

### Initial Doubts
1. Does the final solution need to be a **single model**, or is an **ensemble** of multiple models working together acceptable?
2. Are there specific requirements for the model **architecture**? For example, should I focus on traditional ML models (LSTMs, CNNs) or more modern approaches (Transformers, LLMs, SLMs)?
3. Regarding **dataset generation**, am I permitted to use tools other than vLLM, such as Ollama or LM Studio? 
4. For the **input data samples**, is it an open choice to use either a single message (either from user or assistant) or a full conversation between user and assistant?

### Clarifications Received
1. **A single model is preferred.** While ensembles can perform better in theory, they come with significant disadvantages for enterprise and real-world deployment (complexity, latency, maintainability, etc.).
2. **No specific requirements on architecture** — I was encouraged to lean toward state-of-the-art approaches, reflecting day-to-day operations in the role.
3. **No restrictions on tooling** for dataset generation. I was free to use whatever worked best (vLLM was just an option).
4. The model should be able to handle **all three formats**: user prompt only, single-turn, and multi-turn conversations.

---

## 3. Dataset Design
I browsed and searched for existing benchmarked datasets using Gemini and Perplexity Search. Initial candidates among existing datasets included:
- [LLM-LAT - Harmful](https://huggingface.co/datasets/LLM-LAT/harmful-dataset)
- [LLM-LAT - Benign](https://huggingface.co/datasets/LLM-LAT/benign-dataset)
- [PKU-Alignment - BeaverTails](https://huggingface.co/datasets/PKU-Alignment/BeaverTails)
- [PKU-Alignment - PKU-SafeRLHF](https://huggingface.co/datasets/PKU-Alignment/PKU-SafeRLHF)
- [Anthropic - HH RLHF](https://huggingface.co/datasets/Anthropic/hh-rlhf)

In terms of conversational inputs, I chose **BeaverTails**, **PKU-SafeRLHF**, and **Anthropic HH RLHF** to be included in the training set. Since the testing and evaluation criteria for the task is based on *synthetic data samples*, I decided to include a small percentage of synthetic data in the training set as well.

To maintain the balance of the distribution in the dataset across conversation types, labels, categories, and sources, I came up with a rigorous curation strategy.

### 3.1 Training Dataset Curation Strategy

- **Step 1 — Ingest & Compile:** Combined existing open-source datasets into a unified `{messages, label, source}` format:
  - **BeaverTails**: single-turn prompt/response pairs with `is_safe` labels.
  - **PKU-SafeRLHF**: single-turn with two responses per prompt, properly leveled.
  - **Anthropic HH-RLHF**: multi-turn Human/Assistant conversations; `chosen` mapped to benign, `rejected` to harmful.
- **Step 2 — Conversation Type Mutation:** Each sample was assigned a `conv_type`:
  - Messages with > 2 turns became `multi_turn`.
  - Of the remaining single-turn pairs, ~20% were randomly mutated to `user_only` by dropping the assistant response.
  - The rest stayed `single_turn`.
- **Step 3 — vLLM Category Classification:** Used **Qwen 2.5-7B-Instruct-AWQ** to classify each sample into one of the 9 safety categories via zero-shot prompting.
- **Step 4 — Hierarchical 3D Balancing:** Executed a two-pass algorithm to balance the target counts across labels, categories, and types (`target_total / 2 labels / 9 categories / 3 types`).
- **Step 5 — Gap Analysis & Generation-Based Filling:** Computed the target per cell (max count across all 54 cells) and generated new samples for under-filled cells using **vLLM contrastive generation prompts**. It standardized the remainders to match evenly.
- **Step 6 — Final Formatting & Stratified Split:** Normalized messages for chat templates, cast `label` to `ClassLabel`, and conducted a stratified `train/val` split (90/10) to preserve proportions.

> **Result:** A perfectly balanced dataset across conversation types, labels, sources, and categories. 
> 🔗 **Find the dataset:** [VijayRam1812/safety_dataset](https://huggingface.co/datasets/VijayRam1812/safety_dataset)

### 3.2 Testing Dataset Curation Strategy

- **Step 1 — Bulk Synthetic Generation:** No existing datasets — everything generated from scratch (Target: ~3,780 synthetic samples via **1,890 vLLM contrastive calls**).
- **Step 2 — Gap Analysis & Standardization:** Identical to Track 1's Step 5, checking the 54 cells for imbalance and fixing it. 
- **Step 3 — Normalization:** Normalized for standard alternations and pushed to the Hub as the eval dataset.

> 🔗 **Find the dataset:** [VijayRam1812/safety_eval_dataset](https://huggingface.co/datasets/VijayRam1812/safety_eval_dataset)

---

## 4. Model Selection
- My initial choice for text classification tasks led me towards **BERT** or BERT variant models. 
- I verified my decisions with Gemini. According to Gemini, an encoder-only model is a strong performer for this task, but I assumed an older architecture may fail to capture complex, modern conversational nuances. 
- For a robust alternative, it was suggested to use **RoBERTa** (a modernized BERT variant) for low resource capacity, and for higher resource capacity, **SLMs (Gemma, SmolLM, Phi)** to capture significant nuances. 
- As a side quest out of curiosity, I decided to try **both model options** due to the availability of GPU resources via Colab. 
- While researching fine-tuning methods for binary classification, I discovered that the Hugging Face `Transformers` module can easily load an SLM like Gemma for classification tasks using the `AutoModelForSequenceClassification` class, loading a classification head directly onto a causal model natively.

---

## 5. Infrastructure Setup and Model Training
- I decided to use **Hugging Face's Trainer API** for training both the **RoBERTa** and **Gemma** models. 
- For the training of Gemma, I found that the API defaults to using standard multi-class *Cross-Entropy Loss* for classification tasks when `num_labels` > 1. I made an initial mistake of using `num_labels = 2`. I eventually realized that using **Binary Cross-Entropy (BCE) loss** with `num_labels = 1` was the correct methodology. 
- To achieve this for the SLM, I implemented a custom `BCETrainer` class that inherited from `Trainer` and overrode the `compute_loss` method to use `nn.BCEWithLogitsLoss`. 
- All operations were executed in **Colab GPU Runtimes** for faster training and inference.

### 5.1 Automated Hyperparameter Tuning (Optuna)
- I sought an automated process for hyperparameter tuning and found **Optuna's Bayesian Optimization** to be highly powerful and efficient. 
- It allows for intelligent exploration of the hyperparameter space by using past evaluation results to inform future trials, driving faster convergence compared to traditional grid/random searches. 
- I implemented Optuna in my training loop to optimize key hyperparameters: `learning_rate`, `weight_decay`, `batch_size`, and `warmup_steps`. 
- **Objective Goal:** Maximizing the Area Under the Precision-Recall Curve (**AUPR**).
- Post optimization, I trained the final models with the best hyperparameters and evaluated their performance.

---

## 6. Evaluation Metrics
I chose to evaluate the models using a comprehensive set of metrics that capture different aspects of performance, combining the required metrics with standard supplementary insights.

**Recommended Metrics:**
- **AUPR** (Area Under the Precision-Recall Curve)
- **ROC-AUC** (Area Under the Receiver Operating Characteristic Curve)
- **FPR @ 95% TPR** (False Positive Rate at 95% True Positive Rate)
- **FPR @ 90% TPR** (False Positive Rate at 90% True Positive Rate)

**Additional Metrics:**
- **Accuracy**, **Precision**, **Recall**, and **F1 Score**
- **Inference Latency** (ms per sample)

> **Reasoning:** While AUPR, ROC-AUC, and FPR at specific TPR thresholds are crucial for understanding the model's performance in imbalanced classification scenarios (common in safety tasks), metrics like Accuracy, Precision, Recall, and F1 Score provide a more holistic view of performance. **Inference Latency** is deeply critical for real-time applications where classification needs to happen in milliseconds. This directly enabled my comprehensive comparison of the trade-offs between model complexity and performance for real-world enterprise architectures.

## 7. Results Analysis and Documentation
- After training and evaluating both the RoBERTa and Gemma models, I conducted a detailed analysis of their performance across all metrics.
- I documented the entire process, including the rationale behind each decision, the methodologies implemented, and the insights gained from the results.
- I also reflected on the trade-offs between the two models, considering factors like performance, inference latency, and resource requirements, to provide a well-rounded conclusion on their suitability for real-world deployment in safety classification tasks.








