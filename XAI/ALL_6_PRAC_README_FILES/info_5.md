# Lab 5: Saliency Maps, Integrated Gradients & Grad-CAM

## Notebook
**File:** `XAI_Ex_5.ipynb`

---

## Dataset Information

### Flowers102 Dataset (`torchvision.datasets.Flowers102`)
- **Type:** Image Classification
- **Source:** Oxford 102 Flower Category Dataset
- **Model Used:** Pre-trained **ResNet-18** (ImageNet weights)
- **Input Resolution:** 448×448 pixels (resized from original)
- **Preprocessing:** Standard ImageNet normalization: `mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`
- **Test Sample:** Image at index 11 from the test split

---

## Implementation Details

### Part 1: Saliency Map
1. Loaded pre-trained `ResNet-18` from `torchvision.models`
2. Downloaded the Flowers102 test dataset and selected a flower image
3. Preprocessed the image: Resize → ToTensor → Normalize
4. Performed a **forward pass** and obtained the top predicted class score
5. **Backpropagated** the score to compute gradients w.r.t. the input image
6. Took absolute values of gradients and extracted the maximum across color channels
7. Applied spatial smoothing using `F.avg_pool2d` (kernel=7) for a cleaner visualization
8. Overlaid the saliency map on the original image with jet colormap and alpha blending

### Part 2: Integrated Gradients
1. Defined the **Integrated Gradients** function:
   - Baseline: black image (all zeros)
   - Steps: 100 interpolation steps between baseline and input
   - For each interpolated input: forward pass → backpropagate → collect gradients
   - Final attribution = mean of all gradients × (input − baseline)
2. Summed absolute attributions across color channels and normalized
3. Resized the attribution map to match the original image
4. Visualized as a side-by-side comparison: original image vs. Integrated Gradients overlay

### Part 3: Grad-CAM (Gradient-weighted Class Activation Mapping)
1. Implemented a **GradCAM class** that:
   - Registers forward hooks on the target layer (`layer4`) to capture activations
   - Registers backward hooks to capture gradients
   - Computes weights by global average pooling of gradients
   - Generates a weighted sum of activation maps followed by ReLU
2. Applied Grad-CAM to the same flower image targeting the predicted class
3. Resized the coarse Grad-CAM heatmap to the input resolution
4. Overlaid the heatmap on the original image with transparency

---

## Interpretation & Explainability Analysis

### Saliency Map
Saliency maps reveal which pixels had the **largest gradient magnitude**, indicating regions where small changes would most affect the model's prediction.

- The saliency map highlights the **flower petals and center** as the most salient regions
- Background regions (leaves, soil) have near-zero saliency — the model correctly ignores them
- The smoothing step removes pixel-level noise while preserving the overall attention pattern

> **In plain language:** "The saliency map answers: 'Which pixels does ResNet care about most when classifying this flower?' The answer is clearly the petals and the flower center — the same regions a human would look at."

### Integrated Gradients
Integrated Gradients provide a more **faithful attribution** than vanilla saliency maps by averaging gradients along a path from a baseline (black image) to the actual input.

- The attribution map shows a more distributed and robust highlighting of the flower
- Unlike vanilla saliency, Integrated Gradients satisfies the **completeness axiom**: the sum of all attributions equals the difference between the prediction on the input and the baseline
- It avoids the "gradient saturation" problem where vanilla gradients can miss important features

> **In plain language:** "Integrated Gradients says: 'I gradually revealed the image from black to full color. At each step, I measured how much the model's confidence changed. The regions that consistently mattered throughout this reveal are the truly important ones — not just the ones that happen to have a large gradient at the final image.'"

### Grad-CAM
Grad-CAM operates at a **deeper layer** (layer4 of ResNet), producing a coarser but more semantically meaningful heatmap.

- The Grad-CAM heatmap highlights the **entire flower region** rather than specific pixels
- It captures high-level semantic information — "this area contains a flower" rather than "these specific pixels have petals"
- The heatmap is inherently lower resolution (14×14 for ResNet's layer4) and is upsampled

> **In plain language:** "Grad-CAM looks at what the model's deep layers are focusing on. It says: 'The last convolutional layer is primarily activated by the flower in the center of the image. The model has learned to recognize the overall shape and structure of the flower, not just individual pixels.'"

### Comparison of Methods
| Method | Level | Strengths | Limitations |
|--------|-------|-----------|-------------|
| Saliency Map | Pixel-level | Fast, simple | Noisy, can miss saturated features |
| Integrated Gradients | Pixel-level | Theoretically sound (axioms satisfied) | Slower (requires multiple forward/backward passes) |
| Grad-CAM | Region-level | Semantically meaningful, class-discriminative | Lower resolution, misses fine-grained details |

---

## Output Images
| Image | Description |
|-------|-------------|
| `images_5/output_1.png` | Original flower image + smoothed saliency map overlay |
| `images_5/output_2.png` | Original flower image + Integrated Gradients attribution overlay |
| `images_5/output_3.png` | Original flower image + Grad-CAM heatmap overlay |
