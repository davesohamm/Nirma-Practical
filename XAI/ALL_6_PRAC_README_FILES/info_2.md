# Lab 2: Explainability in Logistic Regression and Support Vector Machines

## Notebook
**File:** `XAI_Ex_2.ipynb`

---

## Dataset Information

### 1. Synthetic Customer Churn Dataset
- **Type:** Binary Classification (generated using `make_classification`)
- **Samples:** 1,000
- **Features (5):**
  - `feature_1` through `feature_5` — All informative, no redundant features
- **Target:** `churn` (0 or 1)
- **Class Distribution:** Approximately balanced (binary)
- **Generation Parameters:** `n_informative=5`, `n_redundant=0`, `random_state=42`

### 2. Iris Dataset (Binary Subset)
- **Type:** Binary Classification
- **Source:** `sklearn.datasets.load_iris` (only classes 0 and 1 used — Setosa and Versicolor)
- **Features Used (2):**
  - `sepal length (cm)`
  - `petal length (cm)`
- **Target:** `species` (0 = Setosa, 1 = Versicolor)
- **Samples:** 100 (50 per class)

---

## Implementation Details

### Part 1: Logistic Regression Explainability (Customer Churn)
1. Generated a synthetic binary classification dataset with 5 informative features
2. Trained `LogisticRegression` using `liblinear` solver with `random_state=42`
3. Extracted model coefficients for each feature:
   - `feature_1`: −0.7461
   - `feature_2`: +0.8422
   - `feature_3`: +0.6936
   - `feature_4`: −0.3051
   - `feature_5`: −0.7187
   - Intercept: 0.7327
4. Visualized absolute coefficient magnitudes as a sorted bar chart (viridis palette)

### Part 2: SVM Explainability (Iris Binary Classification)
1. Loaded the Iris dataset and filtered to only two classes (Setosa vs Versicolor)
2. Selected 2 features (`sepal length`, `petal length`) for 2D visualization
3. Trained a linear SVM (`SVC(kernel='linear')`)
4. Plotted the decision boundary, margin boundaries, and support vectors:
   - Data points colored by class
   - Support vectors highlighted with circles
   - Decision hyperplane and margin lines drawn using weight vector (`w`) and intercept (`b`)

---

## Interpretation & Explainability Analysis

### Logistic Regression Explainability
Logistic Regression is an **intrinsically interpretable** model. The coefficients directly represent the log-odds contribution of each feature:

- **`feature_2` (+0.8422)** has the strongest positive effect — increasing this feature makes churn **more likely**
- **`feature_1` (−0.7461)** and **`feature_5` (−0.7187)** have strong negative effects — higher values make churn **less likely**
- **`feature_3` (+0.6936)** also contributes positively to churn probability
- **`feature_4` (−0.3051)** has the weakest effect

> **In plain language:** This model says: "To predict whether a customer will leave (churn), `feature_2` is the biggest red flag — if it's high, the customer is likely leaving. On the other hand, if `feature_1` or `feature_5` are high, the customer is more likely to stay. The model can quantify exactly how much each factor matters through the coefficient values."

### SVM Explainability
Linear SVMs offer explainability through their **decision boundary** and **support vectors**:

- The **weight vector** (`w`) defines the orientation of the decision boundary — it tells us the relative importance of each feature in separating the classes
- **Support vectors** are the critical data points closest to the boundary. They are the most informative samples — if removed, the boundary would shift
- The **margin** (distance between the dashed lines) shows how confident the model is. A wider margin indicates better class separation

> **In plain language:** The SVM draws a line between Setosa and Versicolor flowers. It says: "I found the best possible dividing line by focusing on the flowers that are hardest to classify (the support vectors). The line is positioned to be as far as possible from both groups. The petal length is the primary separator — Setosa flowers have much shorter petals."

---

## Output Images
| Image | Description |
|-------|-------------|
| `images_2/output_1.png` | Logistic Regression coefficient magnitudes bar chart |
| `images_2/output_2.png` | SVM decision boundary visualization with support vectors and margins |
