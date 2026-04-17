# Lab 4: LIME Explanation for Random Forest Classifier on Iris Dataset

## Notebook
**File:** `XAI_Ex_4.ipynb`

---

## Dataset Information

### Iris Dataset (`sklearn.datasets.load_iris`)
- **Type:** Multi-class Classification
- **Samples:** 150 (50 per class)
- **Features (4):**
  - `sepal length (cm)`
  - `sepal width (cm)`
  - `petal length (cm)`
  - `petal width (cm)`
- **Target Classes (3):**
  - 0 = Setosa
  - 1 = Versicolor
  - 2 = Virginica
- **Split:** 80/20 train-test split (`random_state=42`)

---

## Implementation Details

### Step 1: Model Training
1. Loaded the Iris dataset using `sklearn.datasets.load_iris`
2. Split data into training (120 samples) and test (30 samples) sets
3. Trained a `RandomForestClassifier` with 100 estimators (`random_state=42`)

### Step 2: Model Evaluation
1. Generated predictions on the test set
2. Produced a **classification report** showing precision, recall, and F1-score per class:
   - Setosa: 1.00 across all metrics
   - Versicolor: 1.00 across all metrics
   - Virginica: 1.00 across all metrics
   - **Overall accuracy: 100%**
3. Plotted a **confusion matrix** as a heatmap — perfect diagonal (no misclassifications)

### Step 3: LIME Explanations
1. Initialized `LimeTabularExplainer` with training data, feature names, and class names
2. For each of the 3 classes, selected 5 test samples belonging to that class
3. Generated LIME explanations for each sample using `explain_instance()`
4. Accumulated feature importance scores across samples per class
5. Plotted **per-class LIME feature importance** bar charts

---

## Interpretation & Explainability Analysis

### What is LIME?
LIME (Local Interpretable Model-agnostic Explanations) explains **individual predictions** of any black-box model by:
1. Perturbing the input around the sample of interest
2. Getting predictions from the black-box model on these perturbed samples
3. Fitting a simple, interpretable model (linear regression) locally
4. Using the local model's coefficients as feature importance scores

### Key Findings

**For Class Setosa (output_2.png):**
- **Petal length** and **petal width** are the dominant features — Setosa flowers have distinctly small petals, making these features highly discriminative
- Sepal features play a minor role

**For Class Versicolor (output_3.png):**
- All four features contribute to varying degrees
- **Petal length** and **petal width** remain important but in a middle range
- LIME shows that Versicolor is identified by having "medium" values — not too small (Setosa) and not too large (Virginica)

**For Class Virginica (output_4.png):**
- **Petal length** and **petal width** again dominate — Virginica flowers have the largest petals
- The importance pattern mirrors Setosa but in the opposite direction

> **In plain language:** "LIME explains the Random Forest's perfect predictions by saying: 'For each flower, I checked which features mattered most. Across all flowers, petal measurements (length and width) are by far the most important. Setosa flowers are easy to identify because their petals are tiny. Versicolor and Virginica are separated primarily by petal size — Virginica has the largest petals.'"

### Why LIME Matters
Even though a Random Forest is a **black-box ensemble** of 100 decision trees, LIME makes each prediction understandable:
- A doctor could be told: "This patient was diagnosed with X because features A and B were high"
- It provides **local faithfulness** — the explanation is accurate for that specific prediction, even if the global model is complex

---

## Output Images
| Image | Description |
|-------|-------------|
| `images_4/output_1.png` | Confusion matrix heatmap (perfect classification) |
| `images_4/output_2.png` | LIME feature importance for Class Setosa |
| `images_4/output_3.png` | LIME feature importance for Class Versicolor |
| `images_4/output_4.png` | LIME feature importance for Class Virginica |
