# Content Identifier: Training and Evaluation Report
Task Link: [Gray Swan Take Home Technical Task](https://you.ashbyhq.com/Gray%20Swan%20AI/assignment/d5de60e3-292d-446f-90d2-c1f61559afe2)

## 1. Summary
This report details the end-to-end process of building a binary classification model designed to identify harmful content within conversational data. The project involves comprehensive dataset curation, automated hyperparameter tuning, model training, and rigorous evaluation. 

**RoBERTa** was selected as the primary model for its strong performance in text classification tasks while remaining highly resource-efficient. To validate this choice, I also trained a **Gemma** Small Language Model (SLM) for comparison. The results demonstrate that RoBERTa achieves near state-of-the-art accuracy that is statistically comparable to the heavier Gemma model, offering significant advantages in inference speed, compute efficiency, and deployment feasibility for enterprise applications.

> For detailed approach and step by step thought process: [Approach and Thought Process](https://github.com/VjayRam/Content-Identifier/blob/main/docs/Approach%20and%20Thought%20Process.md)

---
## 2. Repository Guide
This section provides a high-level overview of the repository structure to help you navigate the files and understand their specific purposes:

### 📁 Root Directory
- `README.md`: The main documentation for the project, detailing methodology, datasets, and structure.
- `pyproject.toml`: Dependency configurations for standard environment setups.
- `main.py`: A streamlit app for interactive use of the trained content classifier models, allowing users to input prompts and receive real-time classifications. 
  - Terminal Command: `streamlit run main.py`

> **Note**: Use Gemma model in the Sreamlit UI only if you have the necessary GPU resources and are aware of the latency implications. RoBERTa is recommended for general use due to its efficiency. 

### 📁 scripts/
Contains all the Jupyter Notebooks used for data processing, model training, and evaluation.
- `train_data_generator.ipynb`: Code for curating, balancing, and synthetically generating the training dataset (Track 1). [Click to view](https://github.com/VjayRam/Content-Identifier/blob/main/scripts/train_data_generator.ipynb)
- `test_data_generator.ipynb`: Code for generating the purely synthetic evaluation dataset (Track 2). [Click to view](https://github.com/VjayRam/Content-Identifier/blob/main/scripts/test_data_generator.ipynb)
- `data_processing.ipynb`: Utility notebook for testing out raw message parsing and standardization mappings. [Click to view](https://github.com/VjayRam/Content-Identifier/blob/main/scripts/data_processing.ipynb)
- `model_trainer_roberta.ipynb`: Complete training pipeline for the RoBERTa model, including Optuna hyperparameter sweeps. [Click to view](https://github.com/VjayRam/Content-Identifier/blob/main/scripts/model_trainer_roberta.ipynb)
- `model_trainer_gemma.ipynb`: Complete training pipeline for the Gemma 3-1B-IT model, using a custom BCE Loss implementation for binary classification. [Click to view](https://github.com/VjayRam/Content-Identifier/blob/main/scripts/model_trainer_gemma.ipynb)
- `model_evaluation_roberta.ipynb`: Evaluation script for RoBERTa, producing test metrics (AUPR, ROC AUC, FPR) and False Positive/Negative reviews. [Click to view](https://github.com/VjayRam/Content-Identifier/blob/main/scripts/model_evaluation_roberta.ipynb)
- `model_evaluation_gemma.ipynb`: Evaluation script for Gemma 3-1B-IT, producing identical test metrics. [Click to view](https://github.com/VjayRam/Content-Identifier/blob/main/scripts/model_evaluation_gemma.ipynb)
- `model_inferencing.ipynb`: An inference sandbox providing single-sample and batch-processing wrapper functions for quick testing across both models. [Click to view](https://github.com/VjayRam/Content-Identifier/blob/main/scripts/model_inferencing.ipynb)

### 📁 data/
Stores the raw datasets and generated files used throughout the project lifecycle.
- **raw/**: Full dataset with all 31,536 samples split into train and validation sets balanced across 54 category combinations (`train_dataset.csv`, `val_dataset.csv`). 
- **train/**: Contains the final balanced subsets (`train_sampled.csv`, `val_sampled.csv`).
- **test/**: Contains the 100% synthetic eval set (`test_dataset.csv`).

### 📁 logs/
Stores output metrics, experimental runs, and result datasets generated during notebook execution.

> **Note:** Files with the suffix `_01` indicate results or outcomes from models trained using standard Cross-Entropy Loss (treated as multi-class classification), whereas files with the suffix `_02` represent outcomes from models properly trained using Binary Cross-Entropy (BCE) Loss (binary classification).

- **experiments/**: Hyperparameter tracking runs (CSV logs).
- **metrics/**: JSON files containing the final output scores (AUPR, FPR, Latency) for each trained model.
- **outputs/**: Test prediction CSVs populated with model confidences (`test_predictions_gemma.csv`, `test_predictions_roberta.csv`). 

> A small subset of these predictions (e.g., `sample_predictions_gemma.csv`, `sample_predictions_roberta.csv`) is also saved for manual review of False Positives/Negatives in the /outputs folder.

### 📁 docs/
Contains detailed reports and documentation on the dataset curation process, model training, and evaluation results.
- `Dataset Generation Report.md`: A comprehensive report on the dataset curation strategy, including the use of vLLM for balancing and synthetic generation. [(Click to view)](https://github.com/VjayRam/Content-Identifier/blob/main/docs/Dataset%20Generation%20Report.md)
- `Approach and Thought Process.md`: A detailed walkthrough of the entire project, from initial planning to final evaluation, including the rationale behind each decision and the methodologies implemented. [(Click to view)](https://github.com/VjayRam/Content-Identifier/blob/main/docs/Approach%20and%20Thought%20Process.md)
- `RoBERTa Training Report for Content Identifier.md`: A detailed report on the training process for the RoBERTa model, including hyperparameter tuning results and final performance metrics. [(Click to view)](https://github.com/VjayRam/Content-Identifier/blob/main/docs/RoBERTa%20Training%20Report%20for%20Content%20Identifier.md)
- `Gemma Training Report for Content Identifier.md`: A detailed report on the training process for the Gemma model, including the implementation of Binary Cross-Entropy Loss and final performance metrics. [(Click to view)](https://github.com/VjayRam/Content-Identifier/blob/main/docs/Gemma%20Training%20Report%20for%20Content%20Identifier.md)

### 📁 utils/
- `gpu_verify.py`: Quick diagnostic script to check GPU availability and CUDA bindings before running local training blocks.

---

## 3. Dataset Setup and Curation
The backbone of this classifier depends on a robust, balanced dataset covering 9 distinct safety categories (e.g., Self-Harm, Illegal Activities, PII Violations) across 3 conversation types (`user_only`, `single_turn`, `multi_turn`).

### 3.1 Training Data Strategy
- **Sourcing:** Aggregated samples from established open-source benchmarks, including PKU-Alignment (BeaverTails, PKU-SafeRLHF) and Anthropic (HH-RLHF). 
- **Balancing via vLLM:** Used Qwen 2.5-7B-Instruct-AWQ to classify, mutate, and synthetically generate missing data cells, ensuring a perfect equilibrium across:
  - Labels (Benign vs. Harmful)
  - 9 Safety Categories 
  - 3 Conversation Types
- **Full Set:** A highly refined and balanced dataset 31,536 samples cleanly stratified to prevent class or categorical imbalance.
- **Training Set and Validation Set:** A subset of the full dataset was used for training (14148 samples - 90%) and validation (1566 samples - 10%) with the same balanced structure, ensuring that the model learns from a representative distribution of all categories and labels.


### 3.2 Evaluation / Testing Data Strategy
- **Synthetic Generation:** To prevent data leakage and benchmark generalizability, the entire evaluation / testing set (~3,780 samples) was generated from scratch using a contrastive prompt mechanism (1 harmful + 1 benign pair per iteration).
- **Structure:** Identical hierarchical balance to the training set, yielding exact representations across all 54 target cells (2 labels x 9 categories x 3 conv types).

For the full dataset report: [Dataset Curation Report](https://github.com/VjayRam/Content-Identifier/blob/main/docs/Dataset%20Generation%20Report.md)

Link to the testing dataset: [VijayRam1812/safety_eval_dataset](https://huggingface.co/datasets/VijayRam1812/safety_eval_dataset)

Link to the full training dataset: [VijayRam1812/safety_dataset](https://huggingface.co/datasets/VijayRam1812/safety_dataset)

---

## 4. Infrastructure and Training Setup
The model training was orchestrated using Hugging Face's Trainer API, accelerated by Colab GPU runtimes. 

### 4.1 Hyperparameter Tuning
I incorporated **Optuna Bayesian Optimization** upon researching for optimal methods to intelligently explore the hyperparameter space and automatically converge on the optimal configurations. My primary optimization target was maximizing the Area Under the Precision-Recall Curve (AUPR). 

Parameters explored via Optuna:
- **Learning Rate:** `1e-6` to `5e-5` (log scale)
- **Weight Decay:** `0.0` to `0.1`
- **Batch Size:** `[8, 16, 32]` for RoBERTa, `[4, 8, 16]` for Gemma (due to memory constraints)
- **Warmup Steps:** `0` to `500`

* *Number of Trials for RoBERTa*: 10 Trials + 1 Final Run (with best hyperparameters)
* *Number of Trials for Gemma*: 3 Trials + 1 Final Run (with best hyperparameters) [* limited due to computational constraints *]
    
### 4.2 Loss Function Correction
During the initial training runs, I made a conceptual mistake: the Hugging Face Trainer API was set up using `num_labels = 2`. Because `num_labels` was strictly greater than 1, the Trainer defaulted to using standard multi-class Cross-Entropy Loss to treat the problem as multi-class classification. Realizing that the task is fundamentally binary classification, I corrected the setup. I updated the configuration to run with **Binary Cross-Entropy Loss** and `num_labels = 1`, ensuring the models correctly treated the problem as binary classification.

### 4.3 Model Configuration (RoBERTa - Primary)
RoBERTa was trained as a Sequence Classifier (`AutoModelForSequenceClassification`). Following the correction to the binary loss logic, I trained it successfully. As an encoder-only architecture, RoBERTa is explicitly optimized for full-context comprehension, which is necessary for nuanced content safety checks.


For RoBERTa Training Report: [RoBERTa Training Report](https://github.com/VjayRam/Content-Identifier/blob/main/docs/RoBERTa%20Training%20Report%20for%20Content%20Identifier.md)

Trained RoBERTa model: [Content Classifier - RoBERTa - HF](https://huggingface.co/VijayRam1812/content-classifier-roberta)

### 4.4 Model Configuration (Gemma - Comparative)
Gemma (e.g., 1B-IT/3B-IT) was loaded with a classification head. To fully implement the corrected shift to Binary Cross-Entropy Loss with `num_labels = 1`, adapting this SLM involved explicitly implementing a custom `BCETrainer` class to override Hugging Face's default loss behaviors, practically utilizing `nn.BCEWithLogitsLoss` to ensure numerical stability and correct binary logit assessment.

For Gemma Training Report: [Gemma Training Report](https://github.com/VjayRam/Content-Identifier/blob/main/docs/Gemma%20Training%20Report%20for%20Content%20Identifier.md)

Trained Gemma model: [Content Classifier - Gemma 3-1B-IT - HF](https://huggingface.co/VijayRam1812/content-classifier-gemma)

---

## 5. Evaluation and Results

The evaluation of both models was carried out on the fully synthetic 3,780-sample test set. 

### 5.1 Quantitative Metrics

Results on the Test Set with correct training (BCE Loss):

| Metric | RoBERTa (Primary) | Gemma (Comparative) |
| :--- | :--- | :--- |
| **Accuracy** | 95.44% | 93.99% |
| **Precision** | 95.54% | 95.41% |
| **Recall** | 95.34% | 92.43% |
| **F1 Score** | 0.9544 | 0.9389 |
| **PR-AUC** | 0.9882 | 0.9815 |
| **ROC-AUC** | 0.9889 | 0.9807 |
| **FPR @ 95% TPR** | 4.07% | 7.61% |
| **FPR @ 90% TPR** | 2.85% | 3.43% |
| **Avg. Latency per sample (ms)** | 0.335 ms | 5.33 ms |

### 5.2 Comparative Analysis & RoBERTa's Advantages

The results demonstrate that **RoBERTa is the superior choice for real-world deployment**. Not only did it outperform Gemma across virtually all metrics (unlike what was initially assumed), but its inherent structural characteristics multiply its advantages:

1. **Overall Performance:** 
  - RoBERTa achieved a comprehensively better metric profile: higher Accuracy (95.44% vs 93.99%), better ROC-AUC (0.9889 vs 0.9807), and significantly lower False Positive Rates (FPR @ 95% TPR is 4.07% for RoBERTa compared to Gemma's 7.61%). 
  - This indicates that its representational capacity perfectly managed to capture the complex nuances modeled during our high-quality synthetic data generation better than the heavier SLM architecture.
2. **Computational Efficiency:** 
  -  RoBERTa is an encoder-only model with roughly 125M - 355M parameters (depending on Base/Large), phenomenally smaller than the Gemma SLM (1B+ parameters). 
  - This translates to massively reduced VRAM footprints during both training and inference.
3. **Inference Latency:** 
  - Classifying incoming prompts or conversations requires real-time speed. 
  - As the metrics show, RoBERTa completely outclasses Gemma in inference latency, executing at **0.335 ms per sample** compared to Gemma's sluggish **5.33 ms per sample** - RoBERTa is nearly **16 times faster**. 
4. **Architectural Suitability:** 
  - The task is natively a sequence classification problem. 
  - By processing entire bidirectional contexts efficiently, RoBERTa avoids the generation-centric overhead and key-value caching limitations of decoder-only autoregressive models.
5. **Training Simplicity:** 
  - Fine-tuning the RoBERTa model was straightforward and faster, utilizing standard APIs without requiring custom loss implementations (`BCETrainer`) or complex template formatting adjustments necessary for instructional LLMs.

## 6. Learnings and Reflections
- **Data Quality is Paramount:** 
  - The meticulous curation and balancing of the dataset using vLLM was critical. 
  - The model's performance is directly tied to the quality and representativeness of the training data, especially in a nuanced task like content safety classification. 
  - This is the one phase of the task which consumed majority of the time and effort, but it paid off in the form of superior model performance.
- **Model Selection Matters:** 
  - While it was tempting to assume that the larger Gemma SLM would outperform the smaller RoBERTa, the results clearly demonstrated that model architecture and suitability to the task are more important than sheer size. 
  - RoBERTa's encoder-only design was inherently better suited for this classification task, while Gemma's generative architecture introduced unnecessary complexity and latency. 
  - There is a possibility of bigger sized complex Gemma models outperforming RoBERTa, but the latency and resource consumption trade-offs are something to discuss and consider when in real world deployment scenarios.
- **Hyperparameter Tuning is Essential:** 
  - The use of Optuna for automated hyperparameter optimization was a game-changer. 
  - It allowed for efficient exploration of the hyperparameter space and ensured that both models were trained under optimal conditions, maximizing their performance on the test set.
- **Loss Function Alignment is Critical:** 
  - The initial oversight in using Cross-Entropy Loss for a binary classification task highlighted the importance of aligning the loss function with the problem type. 
  - Correcting this to Binary Cross-Entropy Loss was essential for achieving the high performance observed in the final results.
- **Evaluation Metrics Must be Comprehensive:**
  - Relying solely on AUPR and ROC-AUC would have provided an incomplete picture of model performance. 
  - Incorporating additional metrics like Accuracy, Precision, Recall, F1 Score, and Inference Latency was crucial for a holistic evaluation and for making informed decisions about model deployment in real-world scenarios.
- **Possibility to extract more performance from RoBERTa and Gemma models**: 
  - While the current results are strong for the current training methods and dataset quality, I believe there are many other combinations of hyperparameters, training methods, and even dataset nuances that may affect the performance of both models. 
  - In the given scenario and scope of the task combined with the available resources and time, I believe that the current choices and decisions taken with respect to these aspects were optimal, but there is always room for further experimentation and improvement.


## 7. Conclusion
Through meticulously balanced dataset generation via vLLM and rigorous optimization using Optuna, I successfully established a highly accurate Content Identifier. **RoBERTa** decisively stands out as the optimal primary model. By delivering ~95.4% accuracy, a remarkable ROC-AUC of 0.9889, and blazing-fast inference (~0.335 ms/sample), it not only achieved superior classification capability but perfectly avoided the heavy deployment and latency costs inherent to SLMs, making it the most sensible and adaptable choice for enterprise infrastructure.


## 8. References and Appendix
- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers/index)

- [Optuna Hyperparameter Optimization](https://optuna.org/)

- [vLLM for Data Generation](https://docs.vllm.ai/en/latest/)

- [Google Colab for GPU Training](https://colab.research.google.com/)

- **Datasets**:
  - [BeaverTails](https://huggingface.co/datasets/PKU-Alignment/BeaverTails)
  - [PKU-SafeRLHF](https://huggingface.co/datasets/PKU-Alignment/PKU-SafeRLHF)
  - [Anthropic/hh-rlhf](https://huggingface.co/datasets/Anthropic/hh-rlhf)

- **Models**: 
  - [RoBERTa](https://huggingface.co/roberta-base)
  - [Gemma 3-1B-IT](https://huggingface.co/google/gemma-3-1b-it)
  - [Qwen 2.5-7B-Instruct-AWQ](https://huggingface.co/Qwen/Qwen-2.5-7B-Instruct-AWQ) [*used for dataset generation*]

- **AI Tools**:
  - ***Github Copilot (Gemini, Claude)***:
    -  For code suggestions, error fixes, optimization and documentation generation. Additionally, used for prompt engineering and template design for synthetic data generation.
  - ***Google Gemini***:
    - For brainstorming, finding data sources and research for best practices in dataset curation, model training, and evaluation. Additionally, used for prompt engineering and template design for synthetic data generation.
  - ***Perplexity AI***:
    - For finding credible sources for dataset and model training best practices, and for quick grounded clarifications on concepts related to the task.

- **Additional References**:
  - [vLLM LLM Engine Configuration](https://docs.vllm.ai/en/latest/configuration/engine_args/#modelconfig)
  - [Hugging Face AWQ Quantization](https://huggingface.co/docs/transformers/v5.2.0/quantization/awq)
  - [vLLM Sampling Parameters](https://docs.vllm.ai/en/v0.4.1/dev/sampling_params.html)
  - [Gemma Fine-Tuning for Classification Tasks - Medium](https://medium.com/@sabaybiometzger/gemma-3-fine-tuning-for-classification-tasks-06e04eb6d0f6)
  - [Optuna Bayesian Hyperparameter Tuning Guide - Medium](https://medium.com/@avinashyadav16/bayesian-hyperparameter-tuning-with-optuna-a-beginner-friendly-guide-6a426f43c76e)
