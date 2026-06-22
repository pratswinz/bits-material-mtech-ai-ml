# Machine Learning — Topics Covered (All Slide Decks)

> `✓` = Example question(s) solved in the slides

---

## Module 1: Introduction (CS-1)
- What is Machine Learning? (T/P/E framework)
- Traditional Programming vs ML Approach *(spam filtering example solved)* ✓
- AI vs Data Science vs ML
- Common use cases (security, fraud detection, recommendation engines, customer support)
- When to use (and not use) ML
- Defining learning tasks *(4 examples given)* ✓
- Types of ML by supervision level:
  - Supervised Learning — Classification & Regression *(examples)* ✓
  - Unsupervised Learning *(clustering workflow example)* ✓
  - Reinforcement Learning
  - Semi-supervised Learning
- Types of ML by training data usage: Batch, Mini-batch, Online/Incremental learning
- Instance-based vs Model-based learning
- Open source ML tools (Scikit-learn, PyTorch, TensorFlow, Weka, Keras, etc.)
- ML Workflow overview (7 steps)

---

## Module 2: Machine Learning Workflow (CS-2)
- Role of Data
- Definition of Data: attributes, objects, instances
- Types of Attributes: Nominal, Ordinal, Interval, Ratio *(case study: bank customer data)* ✓
- Discrete vs Continuous Attributes
- Important Characteristics of Data: dimensionality, sparsity, resolution, size
- Data Types: Relational, Transactional, Document, Web/Social Network, Spatial, Time Series, Sequence
- Data Quality: noise, outliers, missing values, inconsistencies, duplicates
- **Data Pre-processing:**
  - Data Aggregation *(Python GroupBy example)* ✓
  - Data Cleansing: imputing missing values
  - Outlier Detection using IQR *(exercise with solution)* ✓
  - Outlier Detection using 3-Sigma / Z-score ✓
- **Instance Selection & Partitioning:**
  - Training / Validation / Test sets
  - Simple Random, Stratified, Clustered Sampling
  - Handling Imbalanced Training Sets (under-sampling / over-sampling)
- **Feature Scaling:**
  - Min-Max Normalization *(formula + worked example)* ✓
  - Z-score Standardization *(formula + worked example)* ✓
  - Normalization vs Standardization — when to use which
- **Feature Engineering:**
  - Feature Extraction (Curse of Dimensionality, PCA)
  - Feature Selection
  - Feature Construction *(example: Customer Lifetime feature)* ✓
  - Feature Transformation:
    - Discretization / Binning: Equal-width, Equal-depth
    - Encoding Numerical Features
    - Encoding Categorical Features: One-Hot / Dummy encoding, Label encoding

---

## Module 3: Linear Models for Regression (CS-3-4, CS-4, CS-5_LinearReg)
- Inductive Learning Hypothesis
- Supervised Learning: Regression — formal representation
- Simple vs Multiple Linear Regression
- Cost Function (Mean Squared Error / Least Squares)
- Intuition behind Cost Function — minima & maxima
- Convex Functions
- **Closed Form Solution (Normal Equation)** *(Problem Type 1: solved step-by-step)* ✓
  - Vectorization
- **Gradient Descent:**
  - Basic search procedure
  - Gradient Descent algorithm derivation
  - Gradient Descent for Linear Regression *(Problem Type 3: full worked example — coronary heart disease data)* ✓
  - Convergence guarantee (positive/negative derivative behavior)
  - Choosing Learning Rate *(Problem Type 2: interpretation of convergence / hyperparameter effect)* ✓
  - Effect of Feature Scaling on Gradient Descent
  - GD Variants: Batch, Mini-batch, Stochastic *(convergence comparison)* ✓
  - Closed Form Solution vs Gradient Descent — comparison
- **Evaluation Metrics for Regression:**
  - R-squared
- **Linear Basis Function Models:**
  - Polynomial Regression
  - Basis functions (Φ)
- **Bias-Variance Tradeoff:**
  - Quality of Fit — underfitting vs overfitting *(Problem Type 4: interpretation of model fit)* ✓
  - Effect of training set size on overfitting
  - How to experiment on model complexity
- **Handling Overfitting:**
  - Way 1: Increase training data size
  - Way 2: Reduce model complexity
  - Way 3: Early stopping
- **Regularization:**
  - Ridge Regression (L2) *(cost function + gradient update)* ✓
  - Lasso Regression (L1) *(cost function + gradient update)* ✓
  - Elastic Net
  - Choosing the right regularization (L1 vs L2 vs Elastic Net)
  - Numerical exercise: GD + Ridge + Lasso on coronary heart disease data ✓

---

## Module 4: Linear Models for Classification (CS-5_LogisticReg, CS-6)
- Decision Theory: objective of classification
- Types of classification: Discriminant, Probabilistic Generative, Probabilistic Discriminative
- Binary classification; decision regions; misclassification rate
- Logistic Regression vs Least Squares Regression
- Sigmoid / Logistic function
- Linear and Non-linear decision boundaries *(examples)* ✓
- **Cost Function for Logistic Regression (Cross-Entropy)**
- **Gradient Descent for Logistic Regression** *(worked example: job offer prediction using CGPA & IQ)* ✓
- Application: Sentiment Analysis with engineered features *(worked example)* ✓
- Logistic Regression — fit model using GD *(Problem: learning rate 0.3, initial weights)* ✓
- Regularization for Logistic Regression (same as M3, with interpretation)
- Controlling overfitting via regularization hyperparameter
- **Evaluation of Classification Models:**
  - Confusion Matrix *(examples with accuracy paradox)* ✓
  - Precision, Recall, F1 (implied via confusion matrix discussion)
  - ROC Curve *(construction step-by-step)* ✓
  - AUC — interpretation
  - Using ROC for model comparison ✓
- Class Imbalance problem
- Solution to class imbalance: SMOTE (Synthetic Minority Oversampling)
- **Multi-class Classification:**
  - One-vs-All (One-vs-Rest) strategy
  - One-vs-One strategy
- Logistic Regression summary

---

## Module 5: Decision Tree (CS-7)
- Decision Tree Classifier overview
- Decision Tree Construction: Hunt's Algorithm *(example)* ✓
- Decision Tree representation and expressiveness
- **Information Theory:**
  - Measure of Information
  - Entropy — definition and formula ✓
  - Entropy for binary classification ✓
  - Computing entropy of features *(EnjoySport dataset, step-by-step)* ✓
- **Information Gain** *(worked examples: Wind, Humidity, Outlook attributes)* ✓
- Attribute selection at each node *(full tree construction walkthrough — Problem Type 3)* ✓
- ID3 Algorithm (summary + pseudocode)
- Stopping conditions for partitioning
- Evaluating Decision Tree: Confusion Matrix *(Problem Type 4)* ✓
- Advantages and applications of Decision Trees
