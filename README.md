# UX Lens AI - Accessibility and Visual Clarity Auditor

![Header Image](/header-image.png)

*Building AI course project*

## Summary
**UX Lens AI** is a conceptual tool designed to assist UX/UI designers in identifying common accessibility and usability issues in digital interfaces. It uses AI to analyze screenshots or prototypes, highlighting problems like low contrast, poor visual hierarchy, and ambiguous labeling.

## Background
As a designer, checking every single state of a complex interface for accessibility (WCAG) compliance is time-consuming. Issues like small touch targets or insufficient contrast are often missed. 

My motivation is to bridge the gap between creative design and inclusive technical standards, making sure products are accessible to everyone from the start of the design process.

## How is it used?
1. **Upload:** A designer uploads a screenshot or links a Figma frame.
2. **Analysis:** The AI identifies interactive elements and measures visual properties.
3. **Feedback:** The tool provides a prioritized list of design suggestions directly on the UI.

### Example 1: Finance app accessibility audit

![Finance app accessibility audit](/examples/finance-accessibility-audit.png)

### Example 2: E-commerce hierarchy audit

![E-commerce visual hierarchy audit](/examples/ecommerce-hierarchy-audit.png)

## Data and AI Techniques
- **Computer Vision:** To detect UI components (buttons, text fields, icons).
- **OCR:** To read and analyze microcopy for clarity.
- **Rule-based Logic & ML:** To compare design properties against WCAG standards and usability heuristics.

## Prototype
This repository includes a small original Python script (`contrast_checker.py`) that demonstrates the logic behind one of the tool's core features: **Automatic Contrast Evaluation**. 

You can run it to see how the system calculates the contrast ratio between two colors to ensure readability.

## Challenges
- AI cannot replace human empathy or understand brand-specific aesthetic choices.
- Designing for diverse cultural contexts or non-standard UI patterns remains a challenge for automated tools.

## What next?
- Developing a Figma plugin integration.
- Training the model to recognize "dark patterns" in UX.

## Acknowledgments
Inspired by the Building AI course and WCAG 2.1 guidelines.
