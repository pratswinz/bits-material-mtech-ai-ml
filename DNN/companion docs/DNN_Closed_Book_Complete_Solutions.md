# DNN Closed-Book Exam — Complete Step-by-Step Solutions
**Course:** AIMLCZG511 Deep Neural Networks | **Format:** Closed Book  
**Sources:** EC2 Mid-Sem 2025 (100 marks) + EC3 Mid-Sem 2026 (120 marks) + Mid QP 2024 (30 marks) + DNN_extra_notes (BCE/CCE derivations)  
**Visual guide:** `DNN_Visual_Study_Guide.html` (21 diagrams in `html_assets/`)

---

## PART 0 — FORMULA SHEET (Memorize Before Exam)

Write this on scrap paper in the first 5 minutes if allowed, or memorize cold.

| Topic | Formula | Notes |
|-------|---------|-------|
| Linear model | `z = wᵀx + b` | x includes bias column of 1s |
| Sigmoid | `σ(z) = 1/(1+e^(-z))` | Output in (0,1) |
| Step (perceptron) | `ŷ = 1 if z≥0 else 0` | EC2 uses 0/1 not ±1 |
| ReLU | `max(0, z)` | Derivative: 1 if z>0, else 0 |
| Softmax | `p_k = exp(z_k) / Σ_j exp(z_j)` | Subtract max before exp for stability |
| MSE | `(1/N) Σ(ŷ−y)²` | Linear regression loss |
| BCE | `−[y·log(ŷ) + (1−y)·log(1−ŷ)]` | Binary classification |
| CCE | `−Σ_k y_k·log(p_k)` | Multi-class; only true class contributes |
| **BCE gradient shortcut** | `∂L/∂z = ŷ − y` | **Most important — derive once, use forever** |
| Weight gradient | `∇w L = (ŷ−y)·x` | Single example |
| Perceptron update | `w ← w + η(y−ŷ)x` | Only when misclassified |
| GD update | `w ← w − η·∇w L` | Minimize loss |
| CNN output size | `(N − F + 2P)/S + 1` | N=input, F=filter, P=padding, S=stride |
| Precision | `TP / (TP + FP)` | Of predicted positives, how many correct |
| Recall | `TP / (TP + FN)` | Of actual positives, how many caught |
| Accuracy | `(TP + TN) / Total` | Misleading on imbalanced data |
| Conv params | `(F_h × F_w × C_in + 1) × C_out` | +1 is bias per filter |
| 2-layer backprop | `dZ₂=A₂−Y`, `dW₂=dZ₂·A₁ᵀ`, `dZ₁=(W₂ᵀdZ₂)⊙𝟙_{Z₁>0}` | ReLU hidden |

---

# PART 1 — EC2 MID-SEM 2025 (CLOSED BOOK) — FULL SOLUTIONS

---

## QUESTION 1 — PERCEPTRON

### Q1(a) — Numerical Perceptron [6 marks]

**Given:**
```
w = [w₀, w₁, w₂] = [0.5, 0.3, −0.4]
x₁ = 1,  x₂ = 2,  y = 1
η = 0.1,  step activation: ŷ = 1 if z≥0 else 0
Bias rule: x₀ = 1 always
```

**What the question is testing:** Can you compute the weighted sum, apply step function, and apply the perceptron learning rule?

---

#### Step (i) — Weighted sum z

The perceptron computes a dot product of weights with inputs (including bias):

```
z = w₀·x₀ + w₁·x₁ + w₂·x₂
  = w₀·1   + w₁·1   + w₂·2
  = 0.5(1) + 0.3(1) + (−0.4)(2)
  = 0.5 + 0.3 − 0.8
  = 0.0
```

**Answer (i): z = 0.0**

---

#### Step (ii) — Predicted output ŷ

Step function rule: output 1 if z ≥ 0, else 0.

```
z = 0.0  →  0 ≥ 0 is TRUE  →  ŷ = 1
```

**Answer (ii): ŷ = 1**

---

#### Step (iii) — Weight update (only if misclassified)

Perceptron learning rule:
```
IF ŷ ≠ y:
    w_j(new) = w_j(old) + η · (y − ŷ) · x_j
```

Check:
```
y = 1,  ŷ = 1  →  CORRECTLY CLASSIFIED
```

When correctly classified, **no update occurs**.

**Answer (iii): No update needed. Weights remain [0.5, 0.3, −0.4]**

---

**Exam tip:** Many students blindly apply the update rule. Always check ŷ vs y first. If they match, write "correctly classified, weights unchanged" — that IS the full answer.

---

### Q1(b)(i) — Which feature indicates spam? [2 marks]

**Given weights:** `[bias=0.2, suspicious_words=0.8, links=0.9, length=−0.5]`

**Explanation:**
- **Positive weight** → increasing that feature pushes z higher → toward class 1 (spam)
- **Negative weight** → increasing that feature pushes z lower → away from spam
- **Magnitude** → strength of influence

| Feature | Weight | Interpretation |
|---------|--------|----------------|
| suspicious_words | +0.8 | Strong spam indicator |
| **links** | **+0.9** | **Strongest spam indicator** |
| length | −0.5 | Longer emails → less spam |

**Answer:** **Links (weight = 0.9)** most strongly indicates spam — highest positive weight among features.

---

### Q1(b)(ii) — 75% accuracy plateau [4 marks]

**What 75% plateau means:**

1. **The perceptron has converged** — no misclassified training points remain that the current boundary can fix, OR it is cycling without improvement.

2. **Linear separability limit:** A single perceptron draws ONE straight line (hyperplane) in feature space. If 25% of data cannot be separated by any line, 75% is the **ceiling** for a perceptron.

3. **Not a data quantity problem** — adding more training epochs won't help because the model class (linear classifier) is too weak, not because training is insufficient.

4. **Perceptron limitation:** Cannot solve non-linearly separable problems (XOR, complex spam patterns). Need MLP with hidden layers for non-linear boundaries.

**Model answer (4 points):**
- Accuracy stuck at 75% → model has reached its best linear boundary
- Data is likely **not fully linearly separable** (~25% points on wrong side of any line)
- More epochs won't help — perceptron only updates on errors; if stuck, no further corrections possible
- Solution: use MLP, kernel methods, or more expressive features

---

### Q1(c) — Approach A vs B generalization [3 marks]

| Factor | Approach A (5 features) | Approach B (50 features) |
|--------|------------------------|--------------------------|
| Samples | 500 | 500 |
| Ratio | 500/5 = 100 samples/feature | 500/50 = 10 samples/feature |
| Overfitting risk | **Low** | **High** |
| Interpretability | **High** (sentiment words, rating) | Low (word counts) |

**Answer:** **Approach A generalizes better.**

**Reasoning:**
1. With only 500 samples, 50 features gives 10 samples per feature — classic overfitting territory. Both get 78% on training, but B likely memorized word combinations that won't appear in new reviews.
2. Approach A uses domain-meaningful features (sentiment counts, star rating) that transfer to new reviews regardless of exact vocabulary.
3. A's decision boundary is interpretable — you can explain why a review was classified negative.

---

### Q1(d) — Perceptron Code Blanks [5 marks]

```python
# Blank 1: compute weighted sum for example i
z = np.dot(X[i], weights)

# Blank 2: perceptron error (true - predicted)
error = y[i] - y_pred

# Blank 3: update rule (note: PLUS not minus — perceptron not gradient descent)
weights = weights + learning_rate * error * X[i]

# Blank 4: predictions on all examples
preds = np.array([1 if np.dot(x, w) >= 0 else 0 for x in X])

# Blank 5: accuracy
acc = np.mean(preds == y)
```

**Why Blank 3 uses `+` not `−`:** Perceptron rule adds correction when wrong. Gradient descent subtracts gradient. Different algorithms — don't mix them up.

---

## QUESTION 2 — LINEAR REGRESSION

### Q2(a) — One Batch Gradient Descent Iteration [6 marks]

**Given:**
```
X = [[1, 10],    y = [150, 250]
     [1, 20]]

w₀ = 50 (bias),  w₁ = 8 (area weight),  η = 0.01
N = 2 examples
```

**Model:** `ŷ = w₀·1 + w₁·area`

---

#### Step (i) — Predictions

```
ŷ₁ = w₀ + w₁·10 = 50 + 8(10) = 50 + 80 = 130
ŷ₂ = w₀ + w₁·20 = 50 + 8(20) = 50 + 160 = 210
```

**Answer (i): ŷ = [130, 210]**

---

#### Step (ii) — MSE Loss

```
MSE = (1/N) Σ(ŷᵢ − yᵢ)²
    = (1/2) [(130−150)² + (210−250)²]
    = (1/2) [(-20)² + (-40)²]
    = (1/2) [400 + 1600]
    = (1/2)(2000)
    = 1000
```

**Answer (ii): MSE = 1000**

---

#### Step (iii) — Gradient

For linear regression with MSE, the gradient is:
```
∇w = (1/N) · Xᵀ · (ŷ − y)
```

First compute error vector (prediction − actual):
```
ŷ − y = [130−150, 210−250] = [−20, −40]
```

Matrix form — Xᵀ is (2×2), error is (2×1):
```
Xᵀ = [[1,  1],
      [10, 20]]

Xᵀ(ŷ−y) = [[1,1], [10,20]] · [−20, −40]ᵀ
         = [1(−20)+1(−40),  10(−20)+20(−40)]
         = [−60, −1000]
```

Divide by N=2:
```
∇w₀ = −60/2 = −30   ← WAIT — let me recheck
```

Actually: `[1×(-20) + 1×(-40), 10×(-20) + 20×(-40)] = [-60, -200-800] = [-60, -1000]`

```
∇w = (1/2)[−60, −1000] = [−30, −500]
```

Hmm, let me recheck the standard formula. Some texts use (y - ŷ). The update is w ← w − η·gradient where gradient = ∂MSE/∂w.

∂MSE/∂w₀ = (2/N)Σ(ŷ−y) but with the (1/N) in MSE definition:
∂MSE/∂w = (2/N) Xᵀ(ŷ−y) ... 

Actually for MSE = (1/N)||Xw-y||²:
∇w MSE = (2/N) Xᵀ(Xw − y) = (2/N) Xᵀ(ŷ − y)

With ŷ−y = [-20, -40]:
Xᵀ(ŷ−y) = [-60, -1000]
∇w = (2/2)[-60, -1000] = [-60, -1000]

Or if using (1/N) without the factor of 2 (some courses use this convention):
∇w = (1/N) Xᵀ(ŷ−y) = [-30, -500]

The exam likely uses: `gradient = X.T @ (y_pred - y) / N` which gives [-30, -500].

**Answer (iii): gradient = [−30, −500]** (using code convention from Q2b)

---

#### Step (iv) — Weight update

```
w_new = w_old − η · gradient
w₀_new = 50 − 0.01(−30) = 50 + 0.30 = 50.30
w₁_new = 8  − 0.01(−500) = 8 + 5.0 = 13.0
```

**Answer (iv): New weights = [50.30, 13.0]**

**Why weights increased:** Predictions (130, 210) were **below** actual prices (150, 250). Negative gradient means we need to increase weights to raise predictions.

---

### Q2(b) — Linear Regression Code Blanks [5 marks]

```python
Blank 1:  np.dot(X, weights)
Blank 2:  np.mean((y_pred - y)**2)
Blank 3:  np.dot(X.T, error) / N
Blank 4:  weights - lr * gradient
Blank 5:  train_linear(X, y)
```

---

### Q2(c)(i) — Salary Prediction [3 marks]

```
Salary = w₀ + w₁(education) + w₂(experience)
       = 30000 + 2500(4) + 3000(2)
       = 30000 + 10000 + 6000
       = $46,000
```

**Reasonableness:** For 4 years education + 2 years experience, $46,000 is reasonable as an entry-to-mid level salary in many markets. The model assigns $2,500 per education year and $3,000 per experience year, which aligns with experience being valued slightly higher.

---

### Q2(c)(ii) — RMSE Acceptability [3 marks]

```
RMSE = √MSE = √5,000,000 ≈ $2,236
```

**Is $2,236 error acceptable?**

**Yes, generally acceptable** because:
- Typical salaries range $30,000–$150,000+
- Error of $2,236 is ~4–7% of predicted salaries — small relative to total
- For HR planning, being off by ~$2K is usable

**When it would NOT be acceptable:** If predicting hourly wages ($15–30/hr range), $2,236 error would be absurd. Context matters.

---

### Q2(d) — Normalized vs Original Features [3 marks]

**Answer: Model B (normalized features) trains faster.**

**Explanation:**

1. **Error surface shape:** With area ranging 400–2000, the loss surface is elongated (elliptical) — steep in w₁ direction, shallow in w₀ direction. Gradient descent zigzags slowly.

2. **After z-score normalization:** Features have mean≈0, std≈1. Error surface becomes more circular. Gradient points more directly toward minimum.

3. **Same final model:** Both converge to identical weights/predictions (normalization is invertible). Only **training speed** differs, not final accuracy.

4. **Same test MSE:** Confirms both found same solution — B just got there in fewer epochs.

---

## QUESTION 3 — LOGISTIC REGRESSION

### Q3(a) — Full Numerical Example [6 marks]

**Given:**
```
w = [w₀=0, w₁=0.6, w₂=0.8]
x = [1, 0.7, 0.5]   (bias, credit_score, income)
y = 1 (approve),  η = 0.1
```

---

#### Step (i) — Weighted sum z

```
z = w₀(1) + w₁(0.7) + w₂(0.5)
  = 0 + 0.6(0.7) + 0.8(0.5)
  = 0.42 + 0.40
  = 0.82
```

**Answer (i): z = 0.82**

---

#### Step (ii) — Sigmoid probability

```
ŷ = σ(z) = 1 / (1 + e^(−z))
         = 1 / (1 + e^(−0.82))
         = 1 / (1 + 0.4404)
         = 1 / 1.4404
         ≈ 0.694
```

**Answer (ii): ŷ ≈ 0.694 (69.4% approval probability)**

**Exam shortcut:** e^(−0.82) ≈ 0.44. If you can't compute exactly, show setup — partial credit.

---

#### Step (iii) — Gradient for single example

Using the golden formula (derived in Part 0):
```
∂L/∂w = (ŷ − y) · x
      = (0.694 − 1) · [1, 0.7, 0.5]
      = (−0.306) · [1, 0.7, 0.5]
      = [−0.306, −0.214, −0.153]
```

**Why negative?** Model predicted 0.694 but true label is 1 — under-predicting. Gradient is negative, so after subtracting (w − η·grad), weights **increase** — correct direction.

**Answer (iii): gradient = [−0.306, −0.214, −0.153]**

---

#### Step (iv) — Updated weights

```
w_new = w − η · gradient

w₀ = 0 − 0.1(−0.306) = 0.031
w₁ = 0.6 − 0.1(−0.214) = 0.621
w₂ = 0.8 − 0.1(−0.153) = 0.815
```

**Answer (iv): w_new ≈ [0.031, 0.621, 0.815]**

---

### Q3(b) — Logistic Regression Code Blanks [5 marks]

```python
Blank 1:  1 / (1 + np.exp(-z))
Blank 2:  sigmoid(z)
Blank 3:  np.dot(X_batch.T, (y_pred - y_batch)) / len(y_batch)
Blank 4:  weights - lr * gradient
Blank 5:  (sigmoid(np.dot(X, weights)) >= 0.5).astype(int)
```

---

### Q3(c)(i) — Imbalanced Accuracy [3 marks]

```
Accuracy = (TP + TN) / Total
         = (40 + 855) / 1000
         = 895 / 1000
         = 89.5% ≈ 89%
```

**Why misleading:**
- 950/1000 = **95% are healthy**
- A **dummy classifier** predicting "healthy" always → **95% accuracy**
- Our "smart" model (89%) is **worse than doing nothing!**
- Accuracy hides poor disease detection (80% recall means 20% missed)

---

### Q3(c)(ii) — Recall vs Precision, Threshold Change [3 marks]

**Why recall matters more for life-threatening disease:**
- **False Negative (miss disease)** → patient not treated → death
- **False Positive (false alarm)** → extra test → inconvenience but patient safe
- Cost of FN >> cost of FP in medicine

**Lowering threshold 0.5 → 0.3:**
- Model predicts "disease" more easily (lower bar)
- **(a) False Positives INCREASE** — more healthy patients flagged
- **(b) False Negatives DECREASE** — fewer diseased patients missed
- **Recall increases, precision decreases**

---

### Q3(d) — Fraud Detection Model Choice [3 marks]

**Given costs:** Missed fraud = $100, Investigation = $10

```
Model A: catches 300/500 frauds, misses 200
Model B: catches 375/500 frauds, misses 125
```

**Fraud loss comparison:**
```
A: 200 missed × $100 = $20,000 lost
B: 125 missed × $100 = $12,500 lost
B saves: $7,500 in fraud losses (75 extra frauds caught × $100)
```

**Overall accuracy:** B is only 1% better (96% vs 95%) — marginal.

**Recommendation: Deploy Model B** because:
1. 15% more fraud detected → $7,500 saved (dominates the 1% accuracy gap)
2. In fraud, **recall on minority class** matters more than overall accuracy
3. 20 features vs 3 is justified if investigation costs don't exceed $7,500 savings
4. Even if B flags more false positives, each costs only $10 vs $100 per missed fraud

---

## QUESTION 4 — SOFTMAX & METRICS

### Q4(a) — Softmax + CCE [6 marks]

**Given:**
```
z = [2.0, 1.0, 0.5]ᵀ   (classes: 0=negative, 1=neutral, 2=positive)
y = [0, 1, 0]ᵀ          (true class = 1 = neutral)
```

---

#### Step (i) — Softmax probabilities

**Step 1:** Compute exponentials
```
exp(2.0) = e² ≈ 7.389
exp(1.0) = e¹ ≈ 2.718
exp(0.5) = e^0.5 ≈ 1.649
```

**Step 2:** Sum
```
Σ = 7.389 + 2.718 + 1.649 = 11.756
```

**Step 3:** Normalize
```
p₀ = 7.389/11.756 = 0.629  (negative)
p₁ = 2.718/11.756 = 0.231  (neutral) ← TRUE CLASS
p₂ = 1.649/11.756 = 0.140  (positive)
```

**Answer (i): p = [0.629, 0.231, 0.140]**

---

#### Step (ii) — Categorical Cross-Entropy

```
L = −Σ_k y_k · log(p_k)
```

Only y₁=1 contributes (one-hot):
```
L = −log(p₁) = −log(0.231) = −(−1.469) = 1.47
```

**Answer (ii): L ≈ 1.47**

---

#### Step (iii) — Predicted class

```
argmax(p) = argmax([0.629, 0.231, 0.140]) = 0 (negative)
```

**Answer (iii): Predicted class = 0 (negative)**

---

#### Step (iv) — Correct?

```
Predicted: 0 (negative)
True:      1 (neutral)
→ INCORRECT
```

**Answer (iv): Prediction is wrong.**

---

### Q4(b) — Softmax Code Blanks [5 marks]

```python
Blank 1:  exp_Z / np.sum(exp_Z, axis=1, keepdims=True)
Blank 2:  np.dot(X_batch, W)
Blank 3:  np.dot(X_batch.T, (Y_pred - Y_batch)) / len(Y_batch)
Blank 4:  W - lr * gradient
Blank 5:  np.argmax(np.dot(X, W), axis=1)
```

**Note:** Softmax gradient `(Y_pred − Y_batch)` has same form as `(ŷ−y)` — beautiful symmetry across sigmoid/BCE and softmax/CCE.

---

### Q4(c)(i) — Bird Precision & Recall [3 marks]

**Confusion matrix (Bird = positive class):**

```
                Pred Cat   Pred Dog   Pred Bird
True Cat          280         15          5
True Dog           20        350         30
True Bird          10         40        250
```

**Extract for Bird class:**
```
TP = 250  (True Bird, Pred Bird)
FP = 10 + 40 = 50  (NOT Bird but Pred Bird: 10 cats + 40 dogs)
FN = 15 + 5 = 20   (True Bird but Pred Cat/Dog: 15→dog? wait)

FN = True Bird row, not Pred Bird = 10 + 40 = 50? 

Let me recheck:
- True Bird row: 10 predicted Cat, 40 predicted Dog, 250 predicted Bird
- FN = 10 + 40 = 50 (bird missed)
- Pred Bird column: 5 + 30 + 250 = 285 total predicted bird
- FP = Pred Bird but not Bird = 5 (cats) + 30 (dogs) = 35

Wait:
TP = 250
FP = cats wrongly called bird (5) + dogs wrongly called bird (30) = 35
FN = birds called cat (10) + birds called dog (40) = 50
```

```
Precision = TP/(TP+FP) = 250/(250+35) = 250/285 = 87.7%
Recall    = TP/(TP+FN) = 250/(250+50) = 250/300 = 83.3%
```

**Answer:**
- TP=250, FP=35, FN=50
- Precision ≈ 87.7%, Recall ≈ 83.3%

---

### Q4(c)(ii) — Bird-Dog Confusion Pattern [3 marks]

**Why birds misclassified as dogs (40/50 errors):**
- Model learned **shared visual features** between birds and dogs (fur texture, four-legged shape in some poses, similar backgrounds)
- Bird-specific features (wings, beak) not discriminative enough
- Classes are **semantically/visually similar** in the feature space

**Does 88% overall accuracy guarantee good per-class performance?**
- **NO.** Overall accuracy is weighted average. A class with few samples or high confusion (Bird recall 83%) can underperform while overall looks good.
- Must check **per-class precision/recall**, not just accuracy.

---

### Q4(d) — Hospital TB Model [3 marks]

**Answer: Deploy Model B (85% accuracy, 78% TB recall).**

1. **Missing TB is catastrophic** — contagious, fatal if untreated. 45% recall (Model A) misses **more than half** of TB cases.
2. **7% accuracy drop is acceptable** when it means catching 78% vs 45% of TB — the tradeoff saves lives.
3. **Ethical obligation:** Optimizing overall accuracy on imbalanced medical data is dangerous — majority class (healthy, 7000 images) dominates accuracy metric.
4. Model A looks better on paper (92%) but fails clinically on the rare, critical class.

---

## QUESTION 5 — DEEP FEEDFORWARD NEURAL NETWORK

### Q5(a) — Forward Propagation [6 marks]

**Architecture:** Input(2) → Hidden(2, ReLU) → Output(1, Sigmoid)

**Given:**
```
x = [0.5, 0.8]ᵀ

W¹ = [[ 1.0,  0.5],     b¹ = [ 0.2]
      [-0.5,  1.5]]           [-0.3]

w² = [1.2, 0.8]ᵀ,  b² = 0.1

y = 1
```

**Matrix convention:** z = x · W + b (row vector × matrix)

---

#### Step (i) — Hidden pre-activation Z¹

```
z₁⁽¹⁾ = x₁·W¹₁₁ + x₂·W²₁₁ + b₁ = 0.5(1.0) + 0.8(−0.5) + 0.2
      = 0.5 − 0.4 + 0.2 = 0.3

z₂⁽¹⁾ = x₁·W¹₁₂ + x₂·W²₂₁ + b₂ = 0.5(0.5) + 0.8(1.5) + (−0.3)
      = 0.25 + 1.2 − 0.3 = 1.15

Z¹ = [0.3, 1.15]
```

**Answer (i): Z¹ = [0.3, 1.15]**

---

#### Step (ii) — ReLU activation

```
ReLU(z) = max(0, z)

A¹ = [max(0, 0.3), max(0, 1.15)] = [0.3, 1.15]
```

Both positive → unchanged.

**Answer (ii): A¹ = [0.3, 1.15]**

---

#### Step (iii) — Output prediction

```
z² = A¹ · w² + b²
   = 0.3(1.2) + 1.15(0.8) + 0.1
   = 0.36 + 0.92 + 0.1
   = 1.38

ŷ = σ(1.38) = 1/(1 + e^(−1.38))
            = 1/(1 + 0.251)
            ≈ 0.799
```

**Answer (iii): ŷ ≈ 0.799**

---

#### Step (iv) — Binary Cross-Entropy Loss

```
L = −[y·log(ŷ) + (1−y)·log(1−ŷ)]
```

With y=1, second term vanishes:
```
L = −log(0.799) = −(−0.225) = 0.225
```

**Answer (iv): L ≈ 0.225**

---

### Q5(b) — Backpropagation Code Blanks [5 marks]

```python
Blank 1:  np.maximum(0, Z)                    # ReLU
Blank 2:  relu(Z1)                            # or np.maximum(0, Z1)
Blank 3:  np.dot(A1.T, dZ2) / N              # dW2
Blank 4:  np.dot(dZ2, W2.T)                  # dA1
Blank 5:  np.dot(X.T, dZ1) / N               # dW1
```

**Backprop logic (memorize the chain):**
```
Forward:  X → Z1 → A1 → Z2 → A2
Backward: dZ2 → dW2 → dA1 → dZ1 → dW1

dZ2 = A2 - Y           (sigmoid+BCE shortcut)
dW2 = A1.T @ dZ2 / N
dA1 = dZ2 @ W2.T
dZ1 = dA1 * (Z1 > 0)   (ReLU mask)
dW1 = X.T @ dZ1 / N
```

---

### Q5(c)(i) — Parameter Count [3 marks]

```
Architecture: Input(1000) → Hidden(8) → Output(5)

Layer 1 weights: 1000 × 8 = 8,000
Layer 2 weights: 8 × 5 = 40
Total (no bias) = 8,040 parameters
```

**Is 8,040 reasonable for 50,000 samples?**
- Ratio: 50,000/8,040 ≈ **6.2 samples per parameter**
- Rule of thumb: want 10–20+ samples per parameter
- **Borderline but reasonable** for a simple task — not severely overparameterized
- With bias terms (+8+5=13), still fine

---

### Q5(c)(ii) — High train acc, low test acc [3 marks]

**Cause 1 — Model too large (overfitting):**
- 8 hidden neurons may be too many if task is simple — model memorizes training noise
- Fix: reduce hidden neurons, add dropout, L2 regularization

**Cause 2 — Insufficient regularization for capacity:**
- 1000 input features with only 8 hidden units still allows memorization of specific word combinations in training set that don't generalize
- Fix: dropout, early stopping, data augmentation

---

### Q5(d) — Mobile Deployment Architecture [3 marks]

**Time calculation:**
```
Architecture A: 5 ms × 1,000,000 = 5,000,000 ms ≈ 1.39 hours/day
Architecture B: 45 ms × 1,000,000 = 45,000,000 ms ≈ 12.5 hours/day
Difference: ~11 hours extra processing per day
```

**Recommendation for mobile: Architecture A**

1. **2% accuracy gain (87%→89%) does NOT justify 9× slower inference** — 11 extra hours of processing daily
2. **Memory:** B needs 3.4 GB — exceeds most phone RAM budgets (4–6 GB shared with OS)
3. **Battery:** 9× compute = 9× power drain
4. **A is deployable; B is not practical on mobile**

**If cloud deployment:** Choose **Architecture B** — unlimited RAM/compute, 2% accuracy matters at scale, latency less critical with GPU clusters, no battery constraint.

---

# PART 2 — BCE GRADIENT DERIVATION (CLOSED BOOK MUST-KNOW)

**Exam question format:** "Derive ∂L/∂z for binary cross-entropy with sigmoid."

### Step 1 — Write the loss
```
L = −[y·log(ŷ) + (1−y)·log(1−ŷ)]
where ŷ = σ(z) = 1/(1+e^(−z))
```

### Step 2 — Differentiate L w.r.t. ŷ
```
∂L/∂ŷ = −[y/ŷ − (1−y)/(1−ŷ)]
```

### Step 3 — Differentiate ŷ w.r.t. z (sigmoid derivative)
```
∂ŷ/∂z = ŷ(1−ŷ)
```

### Step 4 — Chain rule
```
∂L/∂z = (∂L/∂ŷ)(∂ŷ/∂z)
      = −[y/ŷ − (1−y)/(1−ŷ)] · ŷ(1−ŷ)
```

### Step 5 — Simplify (multiply through)
```
= −y(1−ŷ) + (1−y)ŷ
= −y + y·ŷ + ŷ − y·ŷ
= ŷ − y
```

**Result: ∂L/∂z = ŷ − y** ← This is why backprop at output layer is so simple.

### Step 6 — Weight gradient (chain rule again)
```
z = wᵀx  →  ∂z/∂w = x
∇w L = (∂L/∂z)(∂z/∂w) = (ŷ−y)x
```

---

# PART 2B — CCE + SOFTMAX GRADIENT DERIVATION (from DNN_extra_notes 2)

**Exam format:** "Derive ∂L/∂z_j for Categorical Cross-Entropy with Softmax."

### Step 1 — Setup
```
Logits: z = [z₁, z₂, ..., z_K]ᵀ
Softmax: p̂_i = exp(z_i) / Σ_j exp(z_j)
One-hot target: y (only true class k has y_k = 1)
Loss: L = −Σ_i y_i · log(p̂_i) = −log(p̂_k)  [only true class contributes]
```

### Step 2 — ∂L/∂p̂_i
```
∂L/∂p̂_i = −y_i / p̂_i
```

### Step 3 — Softmax Jacobian
```
∂p̂_i/∂z_j = p̂_i(δ_ij − p̂_j)

where δ_ij = 1 if i=j, else 0
```

**Why this matters:** Softmax couples all outputs — changing one logit affects ALL probabilities.

### Step 4 — Chain rule
```
∂L/∂z_j = Σ_i (∂L/∂p̂_i)(∂p̂_i/∂z_j)
        = Σ_i (−y_i/p̂_i) · p̂_i(δ_ij − p̂_j)
        = Σ_i −y_i(δ_ij − p̂_j)
        = −y_j + p̂_j · Σ_i y_i
        = p̂_j − y_j        [since Σ y_i = 1]
```

**Vector form: ∇_z L = p̂ − y** — identical form to sigmoid+BCE!

### Step 5 — Weight gradient
```
z = Wx + b  →  ∂L/∂W = (p̂ − y)xᵀ,   ∂L/∂b = p̂ − y
```

**Key insight:** Both BCE+Sigmoid and CCE+Softmax give **Gradient = Prediction − Target**.

---

# PART 3 — MID QP 2024 (CLOSED BOOK) — FULL SOLUTIONS

## Q1 — MLP Design for Non-Linear Decision Boundary [6 marks]

**Task:** Design minimum hidden layers + nodes for 100% accuracy on a non-linear boundary (classes +1/−1, step activation).

### Standard pattern (concentric circles / ring boundary)

This is the classic "not linearly separable" geometry — same principle as XOR extended to 2D.

```
Architecture:
  Input(2) → Hidden(2) → Output(1)

Hidden Layer — 2 neurons:
  H1: Detects "inside inner circle"  — fires +1 if x²+y² < r₁²
  H2: Detects "inside outer circle"  — fires +1 if x²+y² < r₂²

  Each H node needs weights encoding distance from origin:
  z_H = w₁x + w₂y + w₀  with threshold T marked inside node

Output neuron:
  Combines H1, H2 to produce +1 for inner class, −1 for outer ring
  Example logic: ŷ = +1 if H1=+1 AND H2=+1 (inside inner)
                 ŷ = −1 otherwise
```

**Minimum architecture: 1 hidden layer, 2 hidden nodes.**

### Why 1 perceptron fails
Single perceptron = one linear boundary. Concentric circles need **two boundaries** (inner and outer radius) → requires hidden layer for non-linear feature composition.

### Step activation rule (exam format)
```
At each node: output = +1 if (weighted sum ≥ threshold inside node), else −1
Mention threshold value inside each node circle in your diagram
```

**Exam tip:** Draw the network diagram with thresholds labeled inside nodes. Show one worked example point from each region (+1 inner, −1 outer).

---

## Q2 — CNN Output Shapes [5 marks]

**Formula:** `Output size = (N − F + 2P) / S + 1`

### (a) Single 3×3 conv on 8×8, S=1, P=0
```
= (8 − 3 + 0) / 1 + 1 = 5 + 1 = 6
Shape: 6×6
```

### (b) 5 filters
```
Each filter produces one 6×6 feature map
Shape: 6×6×5
```

### (c) MaxPool 4×4, stride 2 on 6×6×5
```
Pool output = (6 − 4) / 2 + 1 = 2/2 + 1 = 2
Shape: 2×2×5
```

**Final Answer: (a) 6×6  (b) 6×6×5  (c) 2×2×5**

---

## Q4 — Gradient Descent on Quadratic [5 marks]

**Given:** `E(w₁,w₂) = 3w₁² + 4w₂² + 2w₁w₂`, point (0.5, 0.5), η=0.1

### (a) Gradients

Differentiate:
```
∂E/∂w₁ = 6w₁ + 2w₂
∂E/∂w₂ = 8w₂ + 2w₁
```

At (0.5, 0.5):
```
∂E/∂w₁ = 6(0.5) + 2(0.5) = 3 + 1 = 4
∂E/∂w₂ = 8(0.5) + 2(0.5) = 4 + 1 = 5
```

### (b) Weight update

```
w₁_new = 0.5 − 0.1(4) = 0.5 − 0.4 = 0.1
w₂_new = 0.5 − 0.1(5) = 0.5 − 0.5 = 0.0
```

**Answer: gradients = (4, 5), new weights = (0.1, 0.0)**

---

## Q3 — Transfer Learning [4 marks]

| | Rakesh (scratch, 100 samples) | Ram (pretrain 1M → fine-tune 100) |
|--|------|------|
| **Process** | Random init, train all weights on 100 examples | Learn general features on 1M, adapt top layers on 100 |
| **Advantage** | Simple, no dependency on source data | Leverages rich representations; needs far less target data |
| **Problem** | **Severe overfitting** — 100 samples insufficient to learn good features from scratch | Domain mismatch if source ≠ target distribution; catastrophic forgetting |
| **Fix** | Regularization, simpler model, collect more data | Freeze early layers, small LR, data augmentation |

**Rakesh's likely problem:** Overfitting — model memorizes 100 examples, poor generalization.

**Ram's fix:** Pretrained low-level features (edges, textures) transfer across tasks; only high-level classifier needs 100 examples to adapt.

---

## Q5 — CNN vs FC + Training Accuracy Drop [5 marks]

### (a) Two benefits of Conv over FC:
1. **Parameter sharing** — one 3×3 filter (9 params) applied across entire image vs FC connecting every pixel to every neuron (millions of params)
2. **Local connectivity / translation equivariance** — detects patterns (edges) wherever they appear in the image

### (b) Accuracy decreasing after few epochs:
- **NOT overfitting** (overfitting = train acc high, val acc drops)
- **Training accuracy itself decreasing** → model is **diverging**
- **Cause:** Learning rate too high — overshooting minimum, weights oscillate/explode
- **Fix:** Reduce learning rate η; use learning rate scheduler; check for data/label errors

---

## Q6 — Hyperparameters & CNN vs ANN [5 marks]

### (a) Hyperparameters:
Learning rate (η), batch size, number of epochs, number of layers, neurons per layer, activation function, optimizer (SGD/Adam), dropout rate, L2 penalty (λ), momentum coefficient

### (b) Why CNN over ANN for images:
- 50×50 image = 2,500 inputs; HD = 2 million inputs
- FC layer: 2500×1000 = 2.5M weights for ONE hidden layer
- CNN: 3×3×3 = 27 params per filter, shared across image
- CNN captures **spatial structure**; ANN treats pixels independently, loses location info

---

# PART 4 — EC3 MID-SEM 2026 — COMPLETE SOLUTIONS (All 7 Questions)

---

## EC3 QUESTION 1 — Hospital X-ray DFNN (10-class)

### Q1(a)(i) — Single Neuron ReLU Inference [2 marks]

**Given:** x=[0.8, −0.5, 0.2], w=[0.4, 0.1, −0.2], b=0.5

```
z = w·x + b
  = 0.4(0.8) + 0.1(−0.5) + (−0.2)(0.2) + 0.5
  = 0.32 − 0.05 − 0.04 + 0.5
  = 0.73

Output = ReLU(0.73) = max(0, 0.73) = 0.73
```

**Answer: 0.73**

---

### Q1(a)(ii) — Softmax for 10-class output [2 marks]

**Formula:**
```
p_i = exp(z_i) / Σ_{j=1}^{10} exp(z_j)    for i = 1,...,10
```

**Why appropriate:** Softmax converts 10 raw logits into a valid **probability distribution** (all values in (0,1), sum to 1) — required for mutually exclusive 10-class medical diagnosis.

---

### Q1(a)(iii) — Activation Functions [3 marks]

| Layer | Function | Formula |
|-------|----------|---------|
| Hidden 1 | ReLU | f(z) = max(0, z) |
| Hidden 2 | Leaky ReLU | f(z) = max(αz, z), α≈0.01 |
| Output | Softmax | p_i = exp(z_i)/Σexp(z_j) |

---

### Q1(b)(i) — Why Perceptron Cannot Do 10-class [4 marks]

1. **Single perceptron = one linear decision boundary** (hyperplane) — can only split data into two regions.
2. **10-class classification** requires partitioning feature space into **10 non-linear regions** — impossible with one linear boundary.
3. **XOR analogy:** XOR is the simplest case where one line fails — 10-class medical images are far more complex, with non-linear boundaries between disease categories.
4. **Multi-class needs:** Either one-vs-rest perceptrons (10 separate models) OR a DFNN with hidden layers + softmax to learn non-linear boundaries jointly.
5. **Linear separability:** Perceptron convergence theorem only guarantees convergence IF data is linearly separable — medical images are not.

---

### Q1(b)(ii) — Vanishing Gradients [4 marks]

**Cause:** Sigmoid/tanh saturation in deep layers → derivatives near 0 → gradients shrink exponentially as they backpropagate to early layers.

**Impact:** Early layers (near input) receive near-zero gradients → weights barely update → network fails to learn low-level features (edges, textures in X-rays).

**Fix 1 — ReLU activations:** Gradient = 1 for positive inputs → no saturation → gradient flows freely.

**Fix 2 — Residual/Skip connections (ResNet):** Add shortcut paths allowing gradient to bypass layers directly → gradient highway to early layers.

---

## EC3 QUESTION 2 — Churn Prediction DFNN

### Q2(a)(i) — Output Activation + Loss [3 marks]

| Component | Choice | Formula |
|-----------|--------|---------|
| Activation | **Sigmoid** | σ(z) = 1/(1+e^(−z)) |
| Loss | **Binary Cross-Entropy** | L = −[y·log(ŷ)+(1−y)·log(1−ŷ)] |

**Why paired:** Sigmoid outputs probability in (0,1) for binary churn (0=stay, 1=leave). BCE penalizes confident wrong predictions logarithmically. Combined gradient simplifies to **ŷ−y**.

---

### Q2(a)(ii) — Threshold 0.73 probability [2 marks]

```
P(churn) = 0.73 > 0.5  →  Predicted class: CHURN (1)
```

**Threshold meaning:** Decision boundary — customers above 0.5 churn probability are flagged for retention offers. 0.5 = equal cost of false positive/negative; can be adjusted based on business cost.

---

### Q2(b)(i) — Why DFNN beats Logistic Regression [2 marks]

1. **Non-linear feature interactions:** DFNN hidden layers learn combinations (e.g., high complaints AND low data usage) that logistic regression (linear in features) cannot capture.
2. **Hierarchical representations:** Hidden layers build abstract churn signals from raw behavioral features automatically — no manual feature engineering needed.

---

### Q2(b)(ii) — ReLU vs Leaky ReLU [3 marks]

| Layer | Choice | Justification |
|-------|--------|---------------|
| Hidden 1: **ReLU** | f(z)=max(0,z) | Computationally cheap (no exp); sparse activations; fast convergence |
| Hidden 2: **Leaky ReLU** | f(z)=max(0.01z,z) | Prevents **dying ReLU** — neurons in deeper layer that receive negative inputs still get small gradient (0.01) → continue learning |

---

### Q2(b)(iii) — Complete DFNN Architecture [5 marks]

```
Input(4) → Hidden1(64, ReLU) → Hidden2(32, Leaky ReLU) → Output(1, Sigmoid)
Loss: Binary Cross-Entropy | Optimizer: Adam | LR: 0.001
```

| Design choice | Justification |
|---------------|---------------|
| Input dim = 4 | Matches features: call duration, data usage, complaints, contract type |
| 2 hidden layers | Enough non-linearity for behavioral interactions without overfitting |
| 64 → 32 neurons | Tapering reduces params; 64 captures interactions, 32 compresses to decision |
| ReLU + Leaky ReLU | Speed + prevent dying neurons in layer 2 |
| Sigmoid output | Binary churn probability |
| BCE loss | Standard paired loss for binary classification |

---

## EC3 QUESTION 3 — Skin Cancer CNN + Edge Device

### Q3(a)(i) — Transfer Learning: YES [3 marks]

1. **Only 8,000 images / 7 classes** — too small to train deep CNN from scratch without overfitting.
2. **Melanoma severely underrepresented (600 vs 3,200 benign)** — pretrained ImageNet features help when melanoma samples are scarce.
3. **ResNet-50 already achieves 92%** — pretrained weights capture universal low-level features (edges, textures) transferable to dermoscopic images.

---

### Q3(a)(ii) — ResNet-50 FC Layer Parameter Change [4 marks]

**Original ImageNet FC:** 2048 → 1000
```
Removed = 2048×1000 + 1000 = 2,049,000
```

**New classifier:** 2048 → 512 → 7 (Dropout between, biases included)
```
Layer 1: 2048×512 + 512 = 1,049,088
Layer 2: 512×7 + 7 = 3,591
Added = 1,052,679
```

```
Net change = 1,052,679 − 2,049,000 = −996,321 parameters (reduction)
```

---

### Q3(b)(i) — CNN Layer Parameters [3 marks]

**Layer 1: Conv(32, 5×5, s=1, p=2), input 3 channels**
```
Params = (5×5×3 + 1) × 32 = 76 × 32 = 2,432
```

**Trace spatial dims:** 224→conv(p=2)→224→pool→112→conv→112→pool→56→conv→56→pool→**28×28×128**
```
Flatten size = 28×28×128 = 100,352

Layer 8 FC: 100,352 → 256
Params = 100,352×256 + 256 = 25,690,368
```

---

### Q3(b)(ii) — 4-channel input (infrared added) [3 marks]

```
New Layer 1 = (5×5×4 + 1) × 32 = 101×32 = 3,232
Increase = (3232−2432)/2432 × 100 = 32.9%
```

| Layer | Changes? | Why |
|-------|----------|-----|
| Layer 1 | **YES** | Directly connected to input channels |
| Layer 3 | **NO** | Depends on Layer 2 output channels (64), not raw input |
| Layer 8 | **NO** | FC input size (100,352) unchanged if spatial dims same |

---

### Q3(b)(iii) — Global Average Pooling Option A [3 marks]

**Choose Option A:** 28×28×128 → GAP → 128 → FC(128→10)

```
New FC params = 128×10 + 10 = 1,290
(vs original 25,690,368 — 99.995% reduction!)
```

| | |
|--|--|
| **Advantage** | Massive param reduction → fits edge device memory/power; less overfitting |
| **Disadvantage** | Loses spatial location information — may hurt if position of animal in frame matters |

---

### Q3(c)(i) — Accuracy drop on 128×128 crops [2 marks]

1. **Receptive field / context loss:** Full 512×512 images contain context (surrounding skin, borders). 128×128 crops lose this → model fails on partial views.
2. **Training-inference mismatch:** Model trained on full images never saw crop-scale inputs → poor generalization to different spatial scales.

---

### Q3(c)(ii) — Infrared channel increases receptive field? [2 marks]

**INCORRECT.**

Receptive field size depends on **network architecture** (kernel sizes, strides, depth) — NOT input channel count. Adding infrared adds information per pixel but does not change how many pixels each neuron "sees." RF computed by: RF_l = RF_{l−1} + (kernel−1)×stride_product.

---

## EC3 QUESTION 4 — RNN / GRU Factory Anomaly Detection

### Q4(a)(i) — Parameter Count [2 marks]

**Vanilla RNN** (d=10, h=20):
```
W_xh: 10×20 = 200
W_hh: 20×20 = 400
b_h:  20
Total = 620
```

**GRU** (3 gates):
```
Per gate: 10×20 + 20×20 + 20 = 620
Total = 3 × 620 = 1,860
```

---

### Q4(a)(ii) — Model Choice: GRU [3 marks]

**Choose GRU** over LSTM and Vanilla RNN because:
- **vs Vanilla RNN:** Gated memory prevents vanishing gradients for sequential anomaly patterns
- **vs LSTM:** GRU has **fewer parameters** (2 gates vs 3) → better for edge device memory/compute constraints
- **Anomaly signal:** Recent pattern changes need short-to-medium memory — GRU update gate selectively retains relevant history

---

### Q4(b)(i) — Vanilla RNN Step [2 marks]

```
pre_act = Whh·h_{t−1} + Whx·x_t
        = [0.6×0.5, 0.6×(−0.5)] + [0.4×2, 0.4×1]
        = [0.3, −0.3] + [0.8, 0.4]
        = [1.1, 0.1]

h_t = tanh([1.1, 0.1]) ≈ [0.80, 0.10]
```

---

### Q4(b)(ii) — GRU Step [3 marks]

Given Wz=I, Uz=0, Wh=0.5I, Uh=0, x_t=[2,1], h_{t−1}=[0.5,−0.5]:

**Update gate:**
```
z_t = σ(Wz·x_t + Uz·h_{t−1}) = σ([2,1]) ≈ [0.88, 0.73]
```

**Candidate state:**
```
h̃_t = tanh(Wh·x_t) = tanh(0.5·[2,1]) = tanh([1, 0.5]) ≈ [0.76, 0.46]
```

**Final hidden state:**
```
h_t = z_t ⊙ h_{t−1} + (1−z_t) ⊙ h̃_t

h_t[0] = 0.88(0.5) + 0.12(0.76) = 0.44 + 0.09 = 0.53
h_t[1] = 0.73(−0.5) + 0.27(0.46) = −0.365 + 0.124 = −0.24
```

**Answer: z_t≈[0.88,0.73], h̃_t≈[0.76,0.46], h_t≈[0.53,−0.24]**

---

### Q4(b)(iii) — GRU More Conservative [2 marks]

Vanilla RNN: h_t ≈ [0.80, 0.10] — large change from h_{t−1}=[0.5,−0.5] (Δ≈[0.30, 0.60])

GRU: h_t ≈ [0.53, −0.24] — smaller change (Δ≈[0.03, 0.26]) because update gate **blends** previous state (88% retained at dim 0) rather than fully replacing it.

---

### Q4(c)(i) — BPTT Gradient [1 mark]

```
∂L/∂h₂ = ∂L/∂h₃ · z₃ = 1 × 0.9 = 0.9
∂L/∂h₁ = ∂L/∂h₂ · z₂ = 0.9 × 0.9 = 0.81
```

---

### Q4(c)(ii) — GRU vs Long Dependencies [1 mark]

**Mitigation:** Update gate z≈0.9 preserves 90% of gradient per step vs RNN's repeated tanh squashing.

**GRU still struggles:** Very long sequences (1000+ steps) — even GRU gates saturate, gradient still decays over many steps.

---

### Q4(c)(iii) — RNN vs Transformer [1 mark]

**RNN preferred when:** Strict **online/streaming** processing required with **O(1) memory per step** — Transformer needs O(L²) for self-attention over full sequence, infeasible for continuous high-frequency sensor streams on edge device with limited RAM.

---

## EC3 QUESTION 5 — Attention Mechanisms

### Q5(a)(i) — Scaled Dot-Product Attention [3 marks]

```
q₃=[2,7], k₁=k₂=[3,1], k₃=[7,3], v₁=v₂=[3,1], v₃=[8,3], d_k=2, √d_k=1.414

s₁ = (2×3+7×1)/1.414 = 13/1.414 = 9.19
s₂ = 9.19
s₃ = (2×7+7×3)/1.414 = 35/1.414 = 24.74

Softmax (subtract max=24.74):
α₁≈0, α₂≈0, α₃≈1.0

context = 1.0×[8,3] = [8, 3]
```

---

### Q5(a)(ii) — Missing Mechanism [2 marks]

**Causal / Look-ahead masking missing.** Model attends to all positions including "future" items during training → learns to copy past purchases rather than predict next item. Need **causal mask** so position t only attends to positions ≤ t.

---

### Q5(b)(i) — Additive Attention [3 marks]

**Formula:** e_j = vᵀ tanh(W_q·q + W_k·k_j)

Using W_q=W_k=I, v=[1,1]ᵀ (simplified exam setup):

```
e₁: [1,1]·tanh([2+1,1+0]) = [1,1]·tanh([3,1]) ≈ 1.76
e₂: [1,1]·tanh([2,2]) ≈ 1.92
e₃: [1,1]·tanh([4,2]) ≈ 1.96

Softmax: α ≈ [0.28, 0.35, 0.37]
context = 0.28[1,0]+0.35[1,1]+0.37[3,1] ≈ [1.47, 0.72]
```

---

### Q5(b)(ii) — Attention Type Matching [2 marks]

| Scenario | Type | Why |
|----------|------|-----|
| Patient records + external drug DB | **Cross-attention** (encoder-decoder) | Query from patient record attends to external database keys/values |
| Diverse signals with long-range correlations | **Multi-head self-attention** | Different heads capture different correlation patterns (lab↔medication, imaging↔imaging) simultaneously |

---

### Q5(b)(iii) — Dot-Product vs Additive [2 marks]

| | Dot-Product | Additive |
|--|-------------|----------|
| Complexity | O(d·L²) — faster | O(d·L²) with extra W matrices — slower |
| Expressiveness | Less flexible | More flexible (learned W_q, W_k) |
| Prefer dot-product | Large d, long sequences, speed critical | — |
| Prefer additive | — | Small d, alignment quality critical |

---

### Q5(c)(i) — Multi-Head Dimensions [1 mark]

```
d_k = d_model / h = 512/8 = 64 per head
Each head Q/K/V projection: 512×64 = 32,768 params × 3 = 98,304
Output projection: 512×512 = 262,144
Total 8-head: ~360,448 vs single-head: ~262,144 (similar order, 8 heads add output projection overhead)
```

---

### Q5(c)(ii) — Multi-Head Benefit [1 mark]

Different heads learn **different attention patterns** — Head 1 may focus on recent lab results, Head 2 on medication history 3 months ago, Head 3 on imaging findings. Parallel attention prevents single-head bottleneck of only attending to most recent event.

---

### Q5(c)(iii) — Limitation + Mitigation [1 mark]

**Limitation:** 8 heads × L² attention scores = high memory/compute on long clinical sequences.

**Mitigation:** Reduce heads to 4, or use **Linformer/Performer** linear attention approximations — trade slight accuracy for O(L) complexity.

---

## EC3 QUESTION 6 — Transformers for Clinical NLP

### Q6(a)(i) — Positional Encoding [3 marks]

**What it does:** Injects **token order/position information** into embeddings — self-attention alone is permutation-invariant (treats "fever then cough" same as "cough then fever").

**Failure without it:** Clinical events appear in wrong temporal order → model cannot distinguish "medication given before symptom" vs "after" → incorrect summarization and missed causal relationships in discharge notes.

---

### Q6(a)(ii) — Architecture Matching [4 marks]

| Task | Architecture | Justification |
|------|-------------|---------------|
| (a) Clinical NER | **Encoder-only (BERT)** | Bidirectional context needed to label each token; no generation required |
| (b) Discharge note generation | **Decoder-only (GPT)** | Autoregressive text generation from prompt/context |
| (c) Medical report summarisation | **Encoder-Decoder (T5/BART)** | Encoder reads full note; decoder generates summary |

---

### Q6(b)(i) — Encoder Tensor Dimensions [3 marks]

```
Input:           (B, 128, 512)
Multi-head attn: (B, 128, 512)   [8 heads × 64 dim each]
Add & Norm:      (B, 128, 512)
FFN expand:      (B, 128, 2048)   [512 → 2048]
FFN contract:    (B, 128, 512)    [2048 → 512]
Add & Norm:      (B, 128, 512)
```

---

### Q6(b)(ii) — Encoder Layer Parameters [3 marks]

**Multi-Head Attention:**
```
Q, K, V: 3 × (512×512) = 786,432
Output projection: 512×512 = 262,144
Biases: 4×512 = 2,048
MHA subtotal ≈ 1,050,624
```

**Feed-Forward Network:**
```
W₁: 512×2048 + 2048 = 1,049,600
W₂: 2048×512 + 512 = 1,049,088
FFN subtotal ≈ 2,098,688
```

**Total per encoder layer ≈ 3,149,312 parameters**

---

### Q6(b)(iii) — Pre-LN vs Post-LN [3 marks]

| | Post-LN (original) | Pre-LN |
|--|-------------------|--------|
| Stability | Gradients can explode early — LayerNorm after residual | LayerNorm BEFORE sublayer → bounded inputs → **more stable early training** |
| Final performance | Slightly better at convergence with careful tuning | May need more epochs but converges reliably |
| Recommendation | Standard for fine-tuning pretrained | **Pre-LN for training from scratch / unstable early epochs** |

---

### Q6(c)(i) — BERT vs GPT vs T5 [2 marks]

| Model | Pre-training | Architecture | Summarisation suitability |
|-------|-------------|-------------|--------------------------|
| BERT | Masked LM (bidirectional) | Encoder-only | Poor — cannot generate text |
| GPT | Next-token prediction | Decoder-only | Moderate — can generate but no dedicated encoder for long input |
| T5 | Span corruption | Encoder-Decoder | **Best** — designed for seq2seq; fine-tune on note→summary pairs |

**Recommendation:** Fine-tune **T5 or BART** (encoder-decoder). With 50K pairs + 4 A100s, fine-tune pretrained T5-base — do NOT train from scratch.

---

### Q6(c)(ii) — O(L²) Bottleneck [2 marks]

**Problem:** L=2048 → attention matrix is 2048×2048 = 4M scores per head per layer → GPU memory and compute explode.

**Mitigation:** **Sliding window attention** — each token only attends to ±256 neighbors. Trade-off: loses global long-range dependencies but feasible for 2048-token notes.

---

## EC3 QUESTION 7 — Optimizers & Regularization

### Q7(a) — Optimizer Curve Matching [4 marks]

| Curve | Optimizer | Justification |
|-------|-----------|---------------|
| **A** | SGD | Smooth, monotonic, very slow — no momentum |
| **B** | SGD + Momentum | Fast start, oscillates around minimum, settles |
| **C** | RMSprop | Fast, adaptive per-param LR, plateaus at higher loss |
| **D** | Adam | Fastest convergence, smooth, reaches lowest loss (momentum + adaptive) |

---

### Q7(b)(i) — LR Schedule Matching [4 marks]

| Schedule | Type | Justification |
|----------|------|---------------|
| **X** | Constant high LR | Sharp rise then divergence/oscillation — LR too large |
| **Y** | Constant low LR | Steady rise, early plateau — LR too small to escape |
| **Z** | Cosine annealing with warm restarts | Steady rise, brief dip (restart), recovers to best accuracy |

---

### Q7(b)(ii) — Val↑ Train↓ [3 marks]

**Phenomenon: Overfitting**

**Optimizer-level fix:** Add **weight decay (L2 regularization)** to Adam — penalizes large weights in loss → reduces memorization. Alternative: reduce learning rate after epoch 60 (LR scheduler).

---

### Q7(b)(iii) — Regularization Diagnosis [4 marks]

| Run | Train | Val | Diagnosis |
|-----|-------|-----|-----------|
| 1 | 98% | 71% | **Overfitting** — large gap, memorizing training fraud patterns |
| 2 | 84% | 83% | **Underfitting** — model too weak / too much regularization |
| 3 | 91% | 90% | **Good fit** — optimal balance |
| 4 | 76% | 74% | **Underfitting + unstable** — LR too high or no normalization |

---

### Q7(b)(iv) — Fix Run 1 Overfitting [3 marks]

**Technique 1 — Dropout (p=0.5):** Randomly zeroes 50% of neurons during training → prevents co-adaptation → forces redundant representations → reduces memorization → closes train-val gap.

**Technique 2 — L2 Weight Decay (λ=0.01):** Adds λΣw² to loss → penalizes large weights → simpler decision boundary → better generalization to unseen fraud patterns.

---

### Q7(c) — Batch Normalization on Run 4 [2 marks]

**Prediction:** Training becomes **more stable**, converges **faster**, final accuracy **improves**.

**Mechanism:** BatchNorm normalizes activations to zero mean, unit variance within each mini-batch → prevents internal covariate shift → allows higher learning rate → smoother loss landscape → fixes unstable/noisy training in Run 4.

---

## Activation Functions Reference (All Papers)

| Function | Formula | Range | Derivative |
|----------|---------|-------|------------|
| Step | 1 if z≥0 else 0 | {0,1} | Undefined at 0 |
| Sigmoid | 1/(1+e^(-z)) | (0,1) | ŷ(1−ŷ) |
| ReLU | max(0,z) | [0,∞) | 1 if z>0 else 0 |
| Leaky ReLU | max(αz, z), α≈0.01 | (−∞,∞) | 1 or α |
| Softmax | exp(z_i)/Σexp(z_j) | (0,1), sums to 1 | Use p̂−y shortcut |
| Tanh | (e^z−e^(-z))/(e^z+e^(-z)) | (−1,1) | 1−tanh²(z) |

---

# PART 5 — EXAM STRATEGY (CLOSED BOOK)

### Time allocation (100 marks, 2 hours):
- **Q1 Perceptron:** 20 min
- **Q2 Linear Reg:** 20 min
- **Q3 Logistic:** 25 min (includes derivation if asked)
- **Q4 Softmax:** 20 min
- **Q5 DFNN:** 25 min
- **10 min buffer** for rechecking arithmetic

### Order of attack:
1. Scan all questions (2 min)
2. Do numerical questions first (guaranteed marks if arithmetic correct)
3. Code blanks last (quick if formulas memorized)
4. Theory/evaluation questions — use 5-point bullet format

### Common mistakes to avoid:
- ❌ Using `w + η·gradient` for logistic (should be `w − η·gradient`)
- ❌ Using `w − η·error·x` for perceptron (should be `w + η·(y−ŷ)·x`)
- ❌ Forgetting bias input x₀=1
- ❌ Softmax without subtracting max (overflow in code, but show stable version)
- ❌ Confusing precision and recall denominators
- ❌ Applying weight update when perceptron correctly classified

---

# PART 6 — PRACTICE WITHOUT NOTES (Self-Test)

Close this document and solve from scratch:

1. Perceptron: w=[0.2,−0.5,0.3], x=[1,2,1], y=0, η=0.1 → find z, ŷ, updated weights
2. Linear reg: X=[[1,5],[1,15]], y=[100,200], w=[10,5], η=0.01 → one batch GD step
3. Logistic: w=[0,1,−0.5], x=[1,0.8,0.6], y=0, η=0.1 → z, σ(z), gradient, new w
4. Softmax: z=[1,3,2], y=[0,0,1] → probabilities, CCE, predicted class
5. DFNN forward: x=[1,0], W¹=[[1,1],[0,1]], b¹=[0,0], w²=[1,−1]ᵀ, b²=0, ReLU+sigmoid
6. CNN: 32×32 input, 5×5 kernel, S=1, P=0 → output size? Then 2×2 pool S=2?
7. E=w₁²+w₂², (w₁,w₂)=(1,2), η=0.5 → gradient and new weights

**Answers at bottom of document.**

---

## SELF-TEST ANSWERS

1. z=0.2−1+0.3=−0.5, ŷ=0, correct, no update
2. ŷ=[35,85], MSE=1125, grad=[−25/2,...] → w=[10.125, 4.625] approx
3. z=0.8−0.3=0.5, σ≈0.622, grad=(0.622)(x), w increases toward 0
4. p=[0.090,0.665,0.245], L=−log(0.245)=1.41, pred=class 1 (wrong, true=2)
5. Z¹=[1,0], A¹=[1,0], z²=1, ŷ≈0.731, L≈0.313
6. Conv: (32−5)/1+1=28. Pool: (28−2)/2+1=14. Shape 14×14
7. grad=[2,4], w_new=[0,0]

---

*Generated for closed-book exam prep. Verify arithmetic once with calculator, then practice by hand.*
