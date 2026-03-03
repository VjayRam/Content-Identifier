# Gemma Training Report for Content Identifier

## Vijay Ram Enaganti

# Model Training Summary

This document details the re-training of the Gemma 3 1B Instruction Tuned Model for a Sequence Classification task, specifically binary and multi-class classification, using the HuggingFace Transformers library within a Google Colab GPU Runtime (A100 80GB High RAM Instance).

**View Huggingface Model** \- [VijayRam1812/content-classifier-gemma · Hugging Face](https://huggingface.co/VijayRam1812/content-classifier-gemma)

# Key Model and Training Configuration:

* **Model:** Gemma 3.1B Instruction Tuned Model  
* **Training Method:** Re-Training  
* **Task:** Sequence Classification (Binary/Multiclass)  
* **Training Module:** HuggingFace Transformers  
* **Training Resource:** Google Colab GPU Runtime (A100 80GB High RAM Instance)  
* **Input Format:** Gemma Chat Template (Jinja2 Style)
* **Dataset:** Training dataset of 15,714 samples (balanced across 54 category combinations)[90/10 split for train and validation] with a separate evaluation dataset of 3,780 synthetic samples generated from scratch to prevent data leakage.

# Training and Optimization 

## Training Methodology:

* **Model Class:** AutoModelForSequenceClassification  
* **Implementation:** Hugging Face's Trainer API  
* **Loss Function:** 
  - *Run 1:* Standard **Cross-Entropy Loss** (default for single-label, num\_labels \> 1 classification in the Transformers library), as no custom loss function was specified.
  - *Run 2 (Corrected):* Implemented a custom `BCETrainer` class to utilize **Binary Cross-Entropy Loss** with `num_labels = 1`, which is more appropriate for binary classification tasks, ensuring numerical stability and correct logit assessment.

## Hyperparameter Tuning:

Hyperparameter optimization was conducted using **Optuna Bayesian Optimization** with the objective of **Maximizing AUPR** (Area Under the Precision-Recall Curve), which is suitable for potentially imbalanced or anomaly detection tasks (though the current dataset is balanced, AUPR is often a robust metric for classification).

**Parameters Optimized:**

| Parameter | Optimization Range/Values | Purpose |
| :---- | :---- | :---- |
| **learning\_rate** | 1e-6 to 5e-5 (log scale) | The primary control over the model weight updates. |
| **weight\_decay** | 0.0 to 0.1 | Regularization to prevent overfitting. |
| **batch\_size** | Categorical: \[4, 8, 16\] | Number of samples processed per weight update. |
| **warmup\_steps** | Integer: 0 to 500 | Steps to gradually increase the learning rate for training stabilization. |

# Results and Observations

## Optuna Bayesian Optimization Results

The hyperparameter tuning process, aimed at maximizing the Area Under the Precision-Recall Curve (AUPR), was conducted across 3 trials. The results from the 3 optimization and 1 final trials, including the final best model, are summarized below, focusing on the optimized parameters and key evaluation metrics.

*Run 1:*
| Trial Name | Learning  Rate | Weight Decay | Batch Size | Warmup Steps | Eval AUPR | Eval ROC AUC | Eval Loss | Test AUPR | Test ROC AUC | Test Loss |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **best\_model** | 1.05e-5 | 0.0426 | 16 | 292 | **0.940** | 0.943 | 0.965 | **0.982** | 0.982 | **0.423** |
| trial\_2 | 1.94e-6 | 0.0415 | 4 | 286 | 0.763 | 0.804 | 0.582 | \- | \- | \- |
| trial\_1 | 1.05e-5 | 0.0426 | 4 | 292 | 0.929 | 0.931 | 0.456 | \- | \- | \- |
| trial\_0 | 2.40e-6 | 0.0326 | 2 | 263 | 0.854 | 0.848 | 0.568 | \- | \- | \- |

*Run 2 (Corrected with Binary Cross-Entropy Loss):*
| Trial Name | Learning  Rate | Weight Decay | Batch Size | Warmup Steps | Eval AUPR | Eval ROC AUC | Eval Loss | Test AUPR | Test ROC AUC | Test Loss |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **best\_model** | 1.25e-5 | 0.0589 | 16 | 466 | **0.959** | 0.959 | **0.495** | **0.981** | 0.980 | **0.339** |
| trial\_2 | 1.88e-6 | 0.0048 | 2 | 321 | 0.810 | 0.806 | 0.573 | \- | \- | \- |
| trial\_1 | 1.25e-5 | 0.0589 | 4 | 466 | 0.946 | 0.944 | 0.458 | \- | \- | \- |
| trial\_0 | 1.95e-5 | 0.0075 | 2 | 410 | 0.946 | 0.946 | 0.753 | \- | \- | \- |

**Note on Metrics:** The "final\_best\_model" trial utilized a separate test set evaluation, whereas the other trials focused only on the development/validation set metrics for the hyperparameter search.

## Best Model Configuration

The best performing model, identified by the highest AUPR, was achieved with the following optimal hyperparameters after the second run with Binary Cross-Entropy Loss:

* **Learning Rate:** 1.25 x 10^-5  
* **Weight Decay:** 0.0589  
* **Per Device Train/Eval Batch Size:** 16 (Largest stable batch size)  
* **Warmup Steps:** 466  
* **Total Epochs:** 5  
* **Optimizer:** adamw\_torch\_fused

## Performance Analysis

The final model demonstrated strong generalization capabilities, achieving high performance metrics:

* **Train/Validation AUPR:** 0.959
* **Train/Validation ROC AUC:** 0.959
* **Train/Validation Loss:** 0.495

* **Test AUPR:** 0.9815  
* **Test ROC AUC:** 0.9807  
* **Test Accuracy:** 0.9399  
* **Test Precision:** 0.9541  
* **Test Recall:** 0.9243  
* **Test F1 Score:** 0.9390
* **Test FPR @ 95% TPR:** 0.0762
* **Test FPR @ 90% TPR:** 0.0344
* **Avg. Inference Latency:** 5.335 ms per sample

The high AUPR score, close to 1.0, indicates excellent precision and recall across all classification thresholds, confirming the model's effectiveness in identifying both Benign and Harmful content within the balanced dataset.

# References

- [Gemma3-1B-IT \- HuggingFace Model Docs](https://huggingface.co/google/gemma-3-1b-it)  
- [Gemma 3 Fine-Tuning for Classification Tasks \- Medium](https://medium.com/@sabaybiometzger/gemma-3-fine-tuning-for-classification-tasks-06e04eb6d0f6)  
- [Bayesian Hyperparameter Tuning with Optuna Tutorial Example \- Medium](https://medium.com/@avinashyadav16/bayesian-hyperparameter-tuning-with-optuna-a-beginner-friendly-guide-6a426f43c76e)