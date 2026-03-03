# RoBERTa Training Report for Content Identifier

## Vijay Ram Enaganti

# Model Training Summary

This document details the fine-tuning of the RoBERTa base Model for a Sequence Classification task, specifically binary and multi-class classification, using the HuggingFace Transformers library within a Google Colab GPU Runtime (A100 80GB High RAM Instance).

**View Huggingface Model** \- [VijayRam1812/content-classifier-roberta · Hugging Face](https://huggingface.co/VijayRam1812/content-classifier-roberta)

# Key Model and Training Configuration:

* **Model:** RoBERTa base (BERT Variant)  
* **Training Method:** Fine-tuning  
* **Task:** Sequence Classification (Binary/Multiclass)  
* **Training Module:** HuggingFace Transformers  
* **Training Resource:** Google Colab GPU Runtime (A100 80GB High RAM Instance)  
* **Input Format:** Raw Text (Chat Style Messages Processed to Raw Text)
* **Dataset:** Training dataset of 14,148 samples (balanced across 54 category combinations)[90/10 split for train and validation] with a separate evaluation dataset of 3,780 synthetic samples generated from scratch to prevent data leakage.

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

The hyperparameter tuning process, aimed at maximizing the Area Under the Precision-Recall Curve (AUPR), was conducted across 10 trials. The results from the 10 optimization and 1 final trials, including the final best model, are summarized below, focusing on the optimized parameters and key evaluation metrics.

*Run 1:*
| Trial Name | Learning Rate | Weight Decay | Batch Size (Train/Device) | Warmup Steps | Eval AUPR | Eval ROC AUC | Eval Loss | Test AUPR | Test ROC AUC | Test Loss |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **best\_model** | **1.05e-5** | **0.0426** | **8 (16 Total)** | **292** | 0.918 | 0.915 | 0.551 | **0.982** | **0.982** | **0.423** |
| trial\_9 | 4.55e-5 | 0.0374 | 4 (4 Total) | 286 | 0.937 | 0.934 | 0.415 | \- | \- | \- |
| trial\_8 | 5.07e-6 | 0.0735 | 2 (2 Total) | 438 | 0.911 | 0.907 | 0.448 | \- | \- | \- |
| trial\_7 | 4.16e-6 | 0.0258 | 8 (8 Total) | 2 | 0.889 | 0.882 | 0.417 | \- | \- | \- |
| trial\_6 | 3.22e-6 | 0.0313 | 2 (2 Total) | 482 | 0.901 | 0.893 | 0.447 | \- | \- | \- |
| trial\_5 | 4.45e-5 | 0.0899 | 2 (2 Total) | 96 | 0.939 | 0.937 | 0.525 | \- | \- | \- |
| trial\_4 | 4.25e-5 | 0.0222 | 2 (2 Total) | 54 | 0.947 | 0.944 | 0.561 | \- | \- | \- |
| trial\_3 | 3.25e-6 | 0.0154 | 8 (8 Total) | 79 | 0.883 | 0.876 | 0.428 | \- | \- | \- |
| trial\_2 | 5.41e-6 | 0.0424 | 8 (8 Total) | 384 | 0.902 | 0.896 | 0.403 | \- | \- | \- |
| trial\_1 | 9.52e-6 | 0.0118 | 8 (8 Total) | 32 | 0.904 | 0.901 | 0.411 | \- | \- | \- |
| trial\_0 | 6.65e-6 | 0.0478 | 4 (4 Total) | 188 | 0.915 | 0.910 | 0.411 | \- | \- | \- |

*Run 2 (Corrected with Binary Cross-Entropy Loss):*
| Trial Name | Learning Rate | Weight Decay | Batch Size (Train/Device) | Warmup Steps | Eval AUPR | Eval ROC AUC | Eval Loss | Test AUPR | Test ROC AUC | Test Loss |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **best\_model** | **2.69e-5** | **0.071** | **8 (16 Total)** | **256** | **0.952** | **0.951** | **0.712** | **0.988** | **0.989** | **0.279** |
| trial\_9 | 9.37e-6 | 0.085 | 8 (16 Total) | 109 | 0.905 | 0.902 | 0.399 | \- | \- | \- |
| trial\_8 | 1.49e-6 | 0.021 | 2 (4 Total) | 434 | 0.872 | 0.866 | 0.462 | \- | \- | \- |
| trial\_7 | 1.42e-6 | 0.030 | 8 (16 Total) | 135 | 0.835 | 0.824 | 0.505 | \- | \- | \- |
| trial\_6 | 9.14e-6 | 0.050 | 8 (16 Total) | 175 | 0.912 | 0.908 | 0.385 | \- | \- | \- |
| trial\_5 | 1.08e-6 | 0.017 | 2 (4 Total) | 425 | 0.860 | 0.851 | 0.475 | \- | \- | \- |
| trial\_4 | 5.89e-6 | 0.060 | 4 (8 Total) | 148 | 0.907 | 0.904 | 0.407 | \- | \- | \- |
| trial\_3 | 2.69e-5 | 0.072 | 2 (4 Total) | 256 | 0.933 | 0.934 | 0.546 | \- | \- | \- |
| trial\_2 | 5.20e-6 | 0.053 | 2 (4 Total) | 171 | 0.913 | 0.909 | 0.432 | \- | \- | \- |
| trial\_1 | 1.54e-5 | 0.015 | 4 (8 Total) | 281 | 0.929 | 0.926 | 0.405 | \- | \- | \- |
| trial\_0 | 5.68e-6 | 0.005 | 4 (8 Total) | 367 | 0.904 | 0.899 | 0.414 | \- | \- | \- |


**Note on Metrics:** The "final\_best\_model" trial utilized a separate test set evaluation, whereas the other trials focused only on the development/validation set metrics for the hyperparameter search.

## Best Model Configuration

The best performing model, identified by the highest AUPR, was achieved with the following optimal hyperparameters after the second run with Binary Cross-Entropy Loss:

* **Learning Rate:** 2.69 x 10^-5  
* **Weight Decay:** 0.0717  
* **Per Device Train/Eval Batch Size:** 8  
* **Warmup Steps:** 256  
* **Total Epochs:** 5  
* **Optimizer:** adamw\_torch\_fused

## Performance Analysis

The final model demonstrated strong generalization capabilities, achieving high performance metrics:

* **Train/Validation AUPR:** 0.952
* **Train/Validation ROC AUC:** 0.951
* **Train/Validation Loss:** 0.712

* **Test AUPR:** 0.988  
* **Test ROC AUC:** 0.989  
* **Test Accuracy:** 0.954  
* **Test Precision:** 0.955  
* **Test Recall:** 0.953  
* **Test F1 Score:** 0.954
* **Test FPR @ 95% TPR:** 0.0407
* **Test FPR @ 90% TPR:** 0.0286
* **Avg. Inference Latency:** 0.335 ms per sample

The high AUPR score, close to 1.0, indicates excellent precision and recall across all classification thresholds, confirming the model's effectiveness in identifying both Benign and Harmful content within the balanced dataset.

# References

- [RoBERTa \- Huggingface Docs](https://huggingface.co/docs/transformers/v5.2.0/en/model_doc/roberta#roberta)  
- [Bayesian Hyperparameter Tuning with Optuna Tutorial Example \- Medium](https://medium.com/@avinashyadav16/bayesian-hyperparameter-tuning-with-optuna-a-beginner-friendly-guide-6a426f43c76e)