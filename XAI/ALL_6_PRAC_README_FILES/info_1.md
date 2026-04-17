# Lab 1: Explainability in Intrinsically Explainable Models

## Notebook
**File:** `XAI_Ex_1.ipynb`

---

## Dataset Information

### 1. Cellphone Dataset (`Cellphone.csv`)
- **Type:** Regression
- **Samples:** 161 entries
- **Features (14 columns):**
  - `Product_id` (int64) — Unique product identifier (dropped before modeling)
  - `Price` (int64) — **Target variable** (cellphone price)
  - `Sale` (int64) — Number of sales
  - `weight` (float64) — Device weight
  - `resoloution` (float64) — Screen resolution
  - `ppi` (int64) — Pixels per inch
  - `cpu core` (int64) — Number of CPU cores
  - `cpu freq` (float64) — CPU frequency
  - `internal mem` (float64) — Internal memory
  - `ram` (float64) — RAM
  - `RearCam` (float64) — Rear camera megapixels
  - `Front_Cam` (float64) — Front camera megapixels
  - `battery` (int64) — Battery capacity
  - `thickness` (float64) — Device thickness
- **Preprocessing:** StandardScaler normalization on all features

### 2. MBA Admissions Dataset (`MBA.csv`)
- **Type:** Classification
- **Samples:** 6,194 entries (1,000 with admission labels)
- **Features (10 columns):**
  - `application_id` (int64) — Unique ID (dropped)
  - `gender` (object) — Male/Female
  - `international` (bool) — International student status
  - `gpa` (float64) — GPA score
  - `major` (object) — Academic major
  - `race` (object) — Race/ethnicity (4,352 non-null)
  - `gmat` (float64) — GMAT score
  - `work_exp` (float64) — Work experience (years)
  - `work_industry` (object) — Industry of work
  - `admission` (object) — **Target variable** (1,000 non-null)
- **Preprocessing:** One-hot encoding of categorical columns; rows with missing `admission` dropped

### 3. Wine Quality Dataset (`winequality-red.csv`)
- **Type:** Multi-class Classification
- **Samples:** 1,599 entries
- **Features (12 columns):** Fixed acidity, volatile acidity, citric acid, residual sugar, chlorides, free sulfur dioxide, total sulfur dioxide, density, pH, sulphates, alcohol
- **Target:** `quality` (integer score)
- **Split:** 80/20 train-test split

---

## Implementation Details

### Part 1: Multiple Linear Regression (Cellphone Dataset)
1. Loaded and inspected `Cellphone.csv`
2. Separated target (`Price`) from features; dropped `Product_id`
3. Applied `StandardScaler` for feature normalization
4. Trained `LinearRegression` from scikit-learn
5. Extracted model coefficients (`model.coef_`) to quantify each feature's contribution
6. Visualized absolute coefficient values as a bar chart using seaborn (`viridis` palette)

### Part 2: Decision Tree Classifier (MBA Dataset)
1. Loaded `MBA.csv` and filtered to rows with valid `admission` labels (1,000 samples)
2. One-hot encoded categorical features (gender, international, major, race, work_industry)
3. Trained `DecisionTreeClassifier` with `random_state=42`
4. Extracted `feature_importances_` (Gini importance) from the fitted tree
5. Visualized the full decision tree structure using `plot_tree` (filled, rounded nodes)
6. Plotted feature importance bar chart ranked by importance score

### Part 3: Random Forest with SHAP (Wine Quality Dataset)
1. Loaded `winequality-red.csv` and split into train/test (80/20)
2. Trained `RandomForestClassifier` with default hyperparameters
3. Used `shap.TreeExplainer` to compute SHAP values for the test set
4. Generated a SHAP summary plot showing feature contributions across all classes

---

## Interpretation & Explainability Analysis

### Linear Regression Explainability
The linear regression model is **intrinsically explainable** — each coefficient directly tells us how much the price changes when a feature increases by one standard deviation. Key findings:
- **`internal mem` (179.47)** and **`battery` (171.56)** have the largest positive coefficients, meaning they are the strongest predictors of higher cellphone prices
- **`thickness` (−161.06)** has a large negative coefficient — thinner phones tend to be more expensive
- **`resoloution` (−116.80)** also has a negative relationship, which may seem counterintuitive but could reflect multicollinearity with `ppi`
- Features like `Sale` (−35.07) and `weight` (−35.15) have relatively small impact on price

> **In plain language:** If you want to know why a phone costs more, this model says: "Look at the internal memory, battery, and RAM — those push the price up the most. Meanwhile, a thicker phone tends to cost less."

### Decision Tree Explainability
Decision trees are **white-box models** — we can literally trace the path of any prediction. Key findings:
- **`gpa` (0.200)** is the most important feature for MBA admission decisions
- **`gmat` (0.175)** is the second-most important, followed by **`work_exp` (0.118)**
- Demographic features like `gender` and `international` status have very low importance (<0.015)
- The tree visualization shows the exact split points and class distributions at each node

> **In plain language:** The decision tree tells us: "To predict if someone gets into an MBA program, first check their GPA. If it's above a certain threshold, then look at their GMAT score, then work experience. Gender and race play almost no role in the model's decision."

### Random Forest + SHAP Explainability
SHAP (SHapley Additive exPlanations) provides a principled way to explain predictions of any model:
- The summary plot shows that **`alcohol`**, **`volatile acidity`**, and **`sulphates`** are the most influential features for wine quality prediction
- Each dot represents one test sample, and its position on the x-axis shows whether that feature pushed the prediction higher or lower
- The color indicates the feature value (red = high, blue = low)

> **In plain language:** SHAP tells us: "For each wine, I can show you exactly which chemical properties made it score higher or lower. Wines with high alcohol content and high sulphates tend to get better quality ratings, while high volatile acidity hurts the score."

---

## Output Images
| Image | Description |
|-------|-------------|
| `images_1/output_1.png` | Feature importance bar chart from Linear Regression coefficients |
| `images_1/output_2.png` | Full Decision Tree visualization |
| `images_1/output_3.png` | Feature importance bar chart from Decision Tree |
| `images_1/output_4.png` | SHAP summary plot for Random Forest on wine quality |
