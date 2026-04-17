# Lab 6: What-If Tool for Image Classification (Smile Detection)

## Notebook
**File:** `XAI_What_If_Classification.ipynb`

---

## Dataset Information

### CelebA Smile Detection Subset
- **Source:** [CelebA Dataset](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html) — Large-scale CelebFaces Attributes Dataset
- **Type:** Binary Image Classification (Smiling vs Not Smiling)
- **Model Architecture:** Custom CNN (Convolutional Neural Network):
  - Input shape: `(78, 64, 3)` — Resized celebrity face images
  - Conv2D(32, 5×5) → MaxPool(2×2)
  - Conv2D(64, 5×5) → MaxPool(2×2)
  - Flatten → Dense(256, ReLU) → Dense(2, Softmax)
- **Pre-trained Weights:** `smile-model.hdf5` (downloaded from Google Cloud Storage)
- **Test Subset:** 250 celebrity face images with associated metadata
- **Metadata Attributes:** Gender, age (Young/Not Young), smiling (ground truth), attractiveness scores, and other facial attributes from CelebA

---

## Implementation Details

### Step 1: Environment Setup
1. Patched `protobuf` for compatibility (`safe_MessageToJson` wrapper)
2. Installed `witwidget` (Google's What-If Tool widget for Colab/Jupyter)

### Step 2: Data Preparation
1. Downloaded pre-trained CNN model (`smile-model.hdf5`)
2. Downloaded a subset of CelebA test images (`test_subset.zip`)
3. Loaded CSV metadata into a pandas DataFrame
4. Converted data into `tf.Example` protobuf format:
   - Each example contains image bytes (PNG-encoded) in `image/encoded` field
   - Additional metadata fields (gender, age, smiling label, etc.) are stored as features

### Step 3: Model Definition & Loading
1. Defined a Sequential CNN in TensorFlow/Keras matching the pre-trained architecture
2. Loaded weights from `smile-model.hdf5`

### Step 4: Custom Prediction Function
1. Defined `custom_predict()` function that:
   - Extracts image bytes from `tf.Example` protobuf
   - Decodes images using PIL
   - Converts to numpy arrays and normalizes to [0.0, 1.0] range
   - Runs batch inference through the CNN
   - Returns softmax probabilities for [Not Smiling, Smiling]

### Step 5: What-If Tool Visualization
1. Configured `WitConfigBuilder` with:
   - 250 test examples
   - Custom prediction function
   - Label vocabulary: ["Not Smiling", "Smiling"]
2. Launched interactive `WitWidget` in notebook

---

## Interpretation & Explainability Analysis

### What is the What-If Tool (WIT)?
Google's What-If Tool is an **interactive visual interface** for probing machine learning models. It allows practitioners to:
- Explore model performance across different data slices
- Compare individual predictions and find counterfactual examples
- Analyze fairness across demographic groups
- Understand model behavior without writing code

### Key Explorations Performed

**1. Performance Analysis:**
- Set ground truth feature to "Smiling" in the Performance tab
- Analyzed inference correctness across different slices (e.g., Young vs Not Young, Male vs Female)
- Identified any systematic biases in the smile detector

**2. Counterfactual Analysis:**
- Selected individual celebrity images and clicked "Show nearest counterfactual datapoint"
- The tool finds the most similar image (by average pixel color) that has a **different prediction**
- This helps understand: "What minimal change would flip the model's decision?"

**3. Fairness Exploration:**
- Compared model accuracy across gender groups
- Investigated whether the smile detector performs equally well on different demographics
- Scatter plots of features vs inference correctness reveal potential biases

> **In plain language:** "The What-If Tool lets us interactively investigate: 'Is this smile detector fair? Does it work equally well for men and women? For young and old people?' By comparing images with different predictions, we can see what the model considers a 'smile' — sometimes discovering it relies on confounding factors like lighting or face shape rather than the actual smile."

### Important Notes
- This model uses **only images** as input, so partial dependence plots for metadata features (age, gender) are flat — these features aren't part of the model's input
- The metadata features are provided purely for **slicing and analysis** of model fairness
- The WIT is an interactive tool — no static output images are generated in the notebook

### Why This Matters for XAI
The What-If Tool represents a shift from **algorithmic explainability** (like SHAP or LIME) to **interactive exploratory explainability**:
- It empowers non-technical stakeholders to explore model behavior
- It surfaces fairness issues that automated methods might miss
- It provides counterfactual reasoning: "What if this person were different?"

---

## Output Images
| Image | Description |
|-------|-------------|
| *(No output images)* | The What-If Tool is an interactive widget — its visualizations are rendered in the notebook at runtime and are not captured as static images |

> **Note:** To view the WIT interface, run the notebook in Google Colab or a Jupyter environment with `witwidget` installed.
