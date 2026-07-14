# UX Lens AI

Building AI course project

![UX Lens AI Dashboard](/header-image.png)

## Summary

UX Lens AI is an AI-assisted accessibility and visual-clarity reviewer for websites and mobile applications. It analyzes interface screenshots and identifies possible design issues, including low contrast, weak visual hierarchy, small text, unclear calls to action, and inconsistent interface components. The tool is meant to support designers, not replace their professional judgment.

## Background

Designers often need to review many screens and interface states under time pressure. Accessibility and usability problems can be missed, especially in early design stages. These issues can make digital products harder to use for people with visual, cognitive, or motor disabilities.

As a graphic and UX/UI designer, I am interested in a tool that helps identify common visual and usability issues early in the design process. The project focuses on making inclusive design checks faster and easier to integrate into everyday workflows.

## How is it used?

A UX/UI designer uploads a screenshot of a website or mobile app screen. UX Lens AI analyzes the screen and presents a list of possible issues, ordered by priority.

### Real-world Audit Examples:

**1. Finance App Accessibility Audit**
Testing color contrast, touch targets, and readability in complex data environments.
![Finance Audit](/finance-full-ux-audit.png)

**2. E-commerce Visual Hierarchy Audit**
Identifying competing calls-to-action and cluttered product information.
![E-commerce Audit](/e-commerce-full-ux-audit.png)

**3. Travel Discovery UX Audit**
Evaluating text readability over dynamic background imagery and copy clarity.
*(See header image at the top of this page)*

## Data and AI techniques

The system would use annotated screenshots of websites and mobile applications. Each screenshot would include labels describing visual and accessibility issues.

Possible AI techniques:
- **Computer Vision:** To detect interface elements such as buttons, fields, text blocks, and navigation.
- **OCR (Optical Character Recognition):** To extract visible text for analysis.
- **Classification Models:** To identify possible visual problems and prioritize them.
- **NLP (Natural Language Processing):** To evaluate whether labels and calls to action are understandable.
- **Rule-based Logic:** For measurable criteria like WCAG contrast ratios.

## Prototype

This repository includes an original functional prototype: `contrast_checker.py`. 

This script replicates the core logic of the UX Lens "Actionable Insights" panel. It calculates color contrast ratios between text and backgrounds, evaluates them against **WCAG 2.1 AA** standards, and generates a prioritized report with severity labels (**HIGH**, **MEDIUM**, **LOW**).

The code includes pre-configured audit tests for the three examples showcased in this project (Finova, Nova Atelier, and Travelo.co).

## Challenges

The tool cannot fully understand a user’s goals, brand strategy, or emotional response to an interface. A visually unusual design is not necessarily bad design. Results should be treated as suggestions for a designer to review, not as final decisions.

## What next?

- **Figma Integration:** Developing a plugin to audit designs directly in the workspace.
- **Design System Sync:** Comparing interface states for consistency.
- **Expert Feedback Loop:** Allowing accessibility experts to refine the AI's recommendations.

## Acknowledgments

Inspired by the **Web Content Accessibility Guidelines (WCAG)** and the **Building AI** course.
