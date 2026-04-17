# Lab 3: GLM, GAM, Partial Dependence Plots, SHAP & ICE Plots

## Notebook
**File:** `XAI_Ex_3.ipynb`

---

## Dataset Information

### 1. Diabetes Dataset (`sklearn.datasets.load_diabetes`)
- **Type:** Regression
- **Samples:** 442
- **Features (10):** age, sex, bmi, bp (blood pressure), s1–s6 (blood serum measurements)
- **Target:** A quantitative measure of disease progression one year after baseline
- **Split:** 80/20 train-test split
- **Note:** Features are already normalized (zero mean, unit variance)

### 2. Breast Cancer Wisconsin Dataset (`sklearn.datasets.load_breast_cancer`)
- **Type:** Binary Classification
- **Samples:** 569 (212 malignant, 357 benign)
- **Features Used (10 of 30):** mean radius, mean texture, mean perimeter, mean area, mean smoothness, mean compactness, mean concavity, mean concave points, mean symmetry, mean fractal dimension
- **Target:** 0 = Malignant, 1 = Benign
- **Split:** 80/20 train-test split

---

## Implementation Details

### Part 1: Generalized Linear Model — GLM (Diabetes Dataset)
1. Loaded the diabetes dataset and visualized target distribution (histogram)
2. Identified data as positive and right-skewed → chose **Gamma family** with **Log link**
3. Added constant (intercept) using `sm.add_constant()`
4. Fitted GLM using `statsmodels.GLM(family=Gamma(link=log))`
5. Displayed GLM regression summary with coefficients, p-values, AIC
6. Visualized coefficients as positive (green) and negative (red) bars

### Part 2: Generalized Additive Model — GAM (Diabetes Dataset)
1. Set up `LinearGAM` with 10 spline terms `s(0) + s(1) + ... + s(9)` using pyGAM
2. Used `gridsearch()` to automatically find optimal smoothing parameters (lambdas)
3. Evaluated model: MSE = 2750.61, R² = 0.48
4. Displayed GAM summary with Effective Degrees of Freedom (EDoF) for each feature

### Part 3: Partial Dependence Plots — PDP (Diabetes + Cancer)
1. **Diabetes PDP:** For each of 10 features, generated grid and plotted partial dependence curves with 95% confidence intervals
2. **Cancer PDP:** Applied LogisticGAM to breast cancer data, then plotted partial dependence curves for each feature showing probability of benign diagnosis

### Part 4: GLM for Classification (Breast Cancer)
1. Visualized binary target distribution (bar plot)
2. Fitted GLM with **Binomial family** and **Logit link**
3. Displayed regression summary and coefficient bar plot

### Part 5: GAM for Classification (Breast Cancer)
1. Set up `LogisticGAM` with 10 spline terms
2. Achieved **96.49% accuracy** with confusion matrix: only 4 misclassifications out of 114
3. Displayed GAM summary with EDoF values

### Part 6: SHAP Analysis (Diabetes GAM)
1. Used `shap.KernelExplainer` on GAM model (since TreeExplainer doesn't support GAMs)
2. Computed SHAP values for 20 test samples
3. Generated SHAP summary plot and force plot for individual predictions

### Part 7: ICE Plots (Diabetes Dataset)
1. Re-initialized LinearGAM on diabetes data
2. Computed Individual Conditional Expectation curves for `bmi` and `s5` features
3. Plotted both standard ICE plots and **centered ICE plots** (c-ICE) that anchor curves to zero

---

## Interpretation & Explainability Analysis

### GLM Explainability
- **Log link function** means coefficients represent multiplicative effects: a coefficient of 0.5 means a one-unit increase in the feature multiplies the expected disease progression by e^0.5 ≈ 1.65
- **`bmi`** and **`s5`** show the highest positive coefficients — they are the strongest drivers of disease progression
- Negative coefficients indicate features that, when higher, correspond to lower disease progression

> **In plain language:** "The GLM tells us that Body Mass Index (bmi) and the s5 blood serum measurement are the biggest contributors to worsening diabetes. Because we used a Log link, these effects compound — a small increase in bmi doesn't just add to the risk, it multiplies it."

### GAM Explainability
- GAMs extend linear models by allowing **non-linear relationships** via spline functions
- **EDoF close to 1** → feature has a roughly linear relationship (e.g., `sex`)
- **EDoF > 3** → feature has a complex, curved relationship (e.g., `bmi`, `s5`)
- The R² of 0.48 is moderate, suggesting diabetes progression depends on factors beyond these 10 features

> **In plain language:** "The GAM says: 'Some features like bmi don't just increase disease progression in a straight line — there's a tipping point where the effect accelerates dramatically.' This is something a plain linear model would completely miss."

### PDP Interpretation
- **Diabetes PDPs:** Show the marginal effect of each feature. `bmi` shows a clear upward curve — higher bmi leads to sharply higher progression. Features like `age` are nearly flat, indicating minimal impact
- **Cancer PDPs:** Show probability of benign diagnosis. `mean radius` has a sharp downward curve — larger tumors are much more likely to be malignant. The confidence intervals (gray dashed lines) widen at extreme feature values where data is sparse

> **In plain language:** "PDPs show us the 'average story' of each feature. For breast cancer, as the tumor radius grows, the chance of it being benign drops dramatically — this matches medical intuition perfectly."

### SHAP Analysis
- The SHAP summary plot shows that `bmi` and `s5` have the widest spread of SHAP values, confirming they are the most impactful features
- The force plot for individual predictions shows how each feature pushes a specific prediction up or down from the baseline

> **In plain language:** "SHAP breaks down each individual patient's prediction. For Patient X, it might say: 'Your predicted disease progression is 200. The base prediction is 150, but your high bmi added +40 and your s5 level added +30, while your age subtracted -20.'"

### ICE Plot Interpretation
- ICE plots show that while the **average** (PDP) trend for `bmi` is upward, individual patients react differently — some show steep increases while others show flat responses
- **Centered ICE plots** make it easier to see this heterogeneity by removing the vertical offset between curves

> **In plain language:** "ICE plots reveal that not everyone responds to bmi changes the same way. Some patients see dramatic jumps in disease progression with small bmi increases, while others are relatively unaffected. This individual variation is hidden in the averaged PDP."

---

## Output Images
| Image | Description |
|-------|-------------|
| `images_3/output_1.png` | Diabetes target distribution histogram |
| `images_3/output_2.png` | GLM coefficient bar chart (Diabetes) |
| `images_3/output_3.png` | Partial Dependence Plots for all 10 features (Diabetes GAM) |
| `images_3/output_4.png` | Breast Cancer target distribution (binary bar plot) |
| `images_3/output_5.png` | GLM coefficient bar chart (Breast Cancer, Logit link) |
| `images_3/output_6.png` | Partial Dependence Plots for 10 features (Cancer LogisticGAM) |
| `images_3/output_7.png` | SHAP summary plot (Diabetes GAM) |
| `images_3/output_8.png` | SHAP force plot for single prediction |
| `images_3/output_9.png` | ICE plots for `bmi` and `s5` |
| `images_3/output_10.png` | Centered ICE (c-ICE) plots |
