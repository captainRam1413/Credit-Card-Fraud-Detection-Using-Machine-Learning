# [Credit Card Fraud Detection Using Machine Learning](https://credit-card-fraud-detection-using-7wmf.onrender.com/)

## Overview
This project implements a machine learning-based system for detecting fraudulent credit card transactions. With the increasing volume of online transactions, credit card fraud has become a significant concern. This system analyzes transaction patterns to differentiate between legitimate and fraudulent activities, helping to prevent financial losses for cardholders.

## Problem Statement
Credit card fraud occurs when unauthorized individuals use card details to make illegitimate transactions, resulting in financial losses for the legitimate cardholder. The challenge is to accurately identify these fraudulent transactions among millions of legitimate ones, with fraudulent transactions constituting only a small percentage of the total (highly imbalanced dataset).

## Dataset
The dataset used in this project is from Kaggle, containing credit card transactions made by European cardholders over two days. Due to confidentiality issues, the original features have been transformed using PCA:

- **Number of transactions**: 284,807  
- **Number of fraudulent transactions**: 492 (0.172% of total)  
- **Features**: 31 (V1, V2, ..., V28, Time, Amount, Class)  
  - `V1`–`V28`: PCA-transformed numerical values  
  - `Time`: Seconds elapsed between transactions  
  - `Amount`: Transaction amount  
  - `Class`: Target variable (1 for fraud, 0 for legitimate)  

## Methodology
The project implements and compares several machine learning algorithms for fraud detection:

- Logistic Regression  
- Random Forest  
- Naïve Bayes Classifier  
- Decision Tree (Entropy and Gini Index)  
- Support Vector Machine (SVM)

Each algorithm is evaluated using various performance metrics:

- Accuracy  
- Precision  
- Recall  
- F1-Score

Different train-test splits were used: **20/80, 40/60, 80/20**

## Results
Based on experimental results, **Random Forest** consistently provides the best overall performance:

| Test Size | Model         | Accuracy | Recall | F1-Score | Precision |
|-----------|---------------|----------|--------|----------|-----------|
| 20%       | Random Forest | 99.95%   | 0.74   | 0.84     | 0.97      |
| 40%       | Random Forest | 99.95%   | 0.74   | 0.84     | 0.95      |
| 80%       | Random Forest | 99.93%   | 0.67   | 0.77     | 0.90      |

## Implementation
The implementation follows these steps:

### 1. Data Loading and Exploration  
### 2. Data Preprocessing  
- Handling class imbalance  
- Feature scaling  

### 3. Model Training and Evaluation  
- Training multiple ML algorithms  
- Hyperparameter tuning  
- Performance evaluation  

### 4. Results Analysis and Visualization  

## Requirements
- `numpy>=1.19.5`  
- `pandas>=1.3.0`  
- `scikit-learn>=0.24.2`  
- `matplotlib>=3.4.2`  
- `seaborn>=0.11.1`  
- `imbalanced-learn>=0.8.0`
- `stripe api key` 

## Usage

### Clone the repository:
```bash
git clone https://github.com/yourusername/credit-card-fraud-detection.git
cd credit-card-fraud-detection
pip install -r requirements.txt
```
- get raw data from [csv](https://drive.google.com/file/d/1X60-SwAzMSp6wvEisY2h0WOv_HFfj6vX/view?usp=sharing)
- run notebooks to get model's [pre-train](https://drive.google.com/drive/folders/1S-hraeZMrRBpHXIFowe1NDFGB9pgxq5r?usp=drive_link)
- check [Demo](https://credit-card-fraud-detection-using-7wmf.onrender.com/)

```bash
python app.py
```
  
  
