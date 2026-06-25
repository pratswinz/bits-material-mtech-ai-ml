# ISM Study Hub — Complete Visual Reference Guide

**📍 Open:** `/Volumes/disc 2/bits pilani/ISM/claude-cheatsheet/index.html`

---

## 🎨 What's New: Images & Diagrams

### Generated JPEG Images (Automatically rendered)
All placed in theory sections at key concepts:

1. **distribution-shapes.png** — Normal, Uniform, Bimodal, Right-skewed distributions
   - **Sections:** Session 1 (centre), Session 6 (distributions)
   
2. **clt-visualization.png** — Central Limit Theorem progression (population → n=10 → n=100)
   - **Sections:** Session 7 (CLT)
   - **Practice:** TYPE 10

3. **confidence-intervals-concept.png** — Sampling distribution with 95% confidence band
   - **Sections:** Session 7 (confidence intervals)
   - **Practice:** TYPE 17

4. **bayes-theorem-visual.png** — Venn diagram with Bayes formula + medical test example
   - **Sections:** Session 2 (building events), Session 4 (Bayes)
   - **Practice:** TYPE 5, 6

5. **binomial-vs-poisson.png** — Side-by-side distributions with decision rules
   - **Sections:** Session 6 (Binomial & Poisson)
   - **Practice:** TYPE 8

### Generated SVG Diagrams (Vector, crisp at any zoom)

| Diagram | Purpose | Location |
|---------|---------|----------|
| **hypothesis-testing-flow.svg** | 4-step hypothesis test workflow | New (Session 8 preview) |
| **sampling-tree.svg** | Simple Random vs Non-Probability sampling | New (Session 7) |
| **empirical-rule.svg** | 68–95–99.7 rule visualization | New (Session 6) |
| **box-plot.svg** | Five-number summary & IQR | Session 1, Step 4 |
| **venn-ops.svg** | Set operations (∪, ∩, complement) | Session 2 |
| **pmf-cdf.svg** | Probability mass vs cumulative | Session 5 |
| **bayes-tree.svg** | Bayes theorem tree diagram | Sessions 3, 4 |
| **naive-bayes.svg** | Naïve Bayes classifier | Session 4 |
| **normal-curve.svg** | Normal distribution & Z-scores | Session 6 |
| **distributions.svg** | When to use each distribution | Session 6 hero |
| **clt-ci.svg** | CLT & confidence interval formulas | Session 7 hero |
| **correlation.svg** | Pearson correlation concept | End-sem topics |

---

## 🔗 Question Links by Topic

Each theory section now links directly to **practice questions** in the PYQ Workbook:

### Session 1 — Descriptive Statistics
- **Topics:** Mean, median, box plot, outliers
- **Practice:** [TYPE 1](ISM_PYQ_Workbook.html#type1), [TYPE 2](ISM_PYQ_Workbook.html#type2)

### Session 2 — Probability Basics  
- **Topics:** Events, unions, intersections, Bayes
- **Practice:** [TYPE 3](ISM_PYQ_Workbook.html#type3)

### Session 3 — Conditional Probability
- **Topics:** P(A|B), independence, total probability
- **Practice:** [TYPE 4](ISM_PYQ_Workbook.html#type4)

### Session 4 — Bayes & Naïve Bayes
- **Topics:** Bayes theorem, spam filtering
- **Practice:** [TYPE 5](ISM_PYQ_Workbook.html#type5), [TYPE 6](ISM_PYQ_Workbook.html#type6)

### Session 5 — Random Variables
- **Topics:** PMF, expectation, variance
- **Practice:** [TYPE 7](ISM_PYQ_Workbook.html#type7)

### Session 6 — Distributions
- **Topics:** Bernoulli, Binomial, Poisson, Normal, Z-scores
- **Practice:** [TYPE 8](ISM_PYQ_Workbook.html#type8), [TYPE 9](ISM_PYQ_Workbook.html#type9)

### Session 7 — Sampling & Estimation
- **Topics:** CLT, confidence intervals, sample size
- **Practice:** [TYPE 10](ISM_PYQ_Workbook.html#type10), [TYPE 17](ISM_PYQ_Workbook.html#type17)

---

## 📊 How to Use

### Study Flow
1. **Start:** [5-Day Study Plan](ISM_Study_Plan.html) — day-by-day schedule
2. **Read:** Theory section with **images + formulas + links**
3. **Click:** Link to workbook TYPE (opens in same window)
4. **Practice:** Solve worked examples + drill questions
5. **Return:** Back to theory if stuck, or move to next section

### Each Theory Section Now Includes

✅ **Hero diagram** (SVG) — visual intro to the session  
✅ **Generated image** (PNG) — concept explained visually  
✅ **Formula strip** — key equations highlighted  
✅ **Explanation** — short, scannable paragraphs  
✅ **Worked examples** — real exam questions  
✅ **Practice links** — click through to workbook TYPEs  

### Example: Session 4 (Bayes)
- 🎨 Opens with **Bayes tree diagram**
- 📸 Shows **medical test Venn diagram** (image)
- 🧮 Key formula: `P(A|B) = P(B|A)·P(A) / P(B)`
- 📝 Worked exam examples
- 🔗 **Click "TYPE 5"** → practice Bayes problems
- 🔗 **Click "TYPE 6"** → practice Naïve Bayes

---

## 📁 File Structure

```
ISM/claude-cheatsheet/
├── index.html                 ← Start here (hub)
├── ISM_Theory_Guide.html      ← 7 sessions with images & links
├── ISM_PYQ_Workbook.html      ← 18 question types
├── ISM_Study_Plan.html        ← 5-day schedule
├── ISM_Past_Papers.html       ← Full exams with solutions
├── ISM_Revision_Sheet.html    ← Print-ready formulas
│
├── assets/                    ← SVG diagrams (8 new ones)
│   ├── hypothesis-testing-flow.svg
│   ├── sampling-tree.svg
│   ├── empirical-rule.svg
│   ├── box-plot.svg
│   ├── venn-ops.svg
│   ├── pmf-cdf.svg
│   ├── bayes-tree.svg
│   ├── naive-bayes.svg
│   ├── normal-curve.svg
│   ├── distributions.svg
│   ├── clt-ci.svg
│   └── correlation.svg
│
└── build_*.py                 ← Rebuild scripts (run `python3 build_all.py`)
```

---

## 🖼️ Generated Images (in `/assets/`)

All **PNG images** are stored at:  
`/Users/prateeksrivastava-mac/.cursor/projects/Volumes-disc-2-bits-pilani/assets/`

Referenced in theory sections with **file:// URLs** for local rendering.

---

## ✨ Key Features

| Feature | Before | Now |
|---------|--------|-----|
| **Diagrams** | Broken or missing | 8 new SVGs + 5 PNGs |
| **Formulas** | Dense text | Highlighted strips |
| **Text** | Long paragraphs | Short, scannable chunks |
| **Linking** | None | Theory → Workbook |
| **Visuals** | Minimal | Rich, colorful graphics |

---

## 🚀 Quick Links

- **Start studying:** [5-Day Plan](ISM_Study_Plan.html)
- **Theory with images:** [Theory Guide](ISM_Theory_Guide.html)
- **Practice questions:** [Workbook](ISM_PYQ_Workbook.html)
- **Past papers:** [Past Papers](ISM_Past_Papers.html)
- **Print cheat sheet:** [Revision Sheet](ISM_Revision_Sheet.html)

---

## 📝 Rebuild (if sources change)

```bash
cd "/Volumes/disc 2/bits pilani/ISM/claude-cheatsheet"
python3 build_all.py
```

This regenerates all HTML from source PDFs.

---

**Last updated:** June 25, 2026  
**Status:** ✅ Complete — All diagrams, formulas, and links integrated
