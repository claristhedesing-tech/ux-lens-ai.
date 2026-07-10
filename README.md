# UX Lens AI

Building AI course project

## Summary

UX Lens AI is an AI-assisted accessibility and visual-clarity reviewer for websites and mobile applications. It analyzes interface screenshots and identifies possible design issues, including low contrast, weak visual hierarchy, small text, unclear calls to action, and inconsistent interface components. The tool is meant to support designers, not replace their professional judgment.

## Background

Designers often need to review many screens and interface states under time pressure. Accessibility and usability problems can be missed, especially in early design stages. These issues can make digital products harder to use for people with visual, cognitive, or motor disabilities.

As a graphic and UX/UI designer, I am interested in a tool that helps identify common visual and usability issues early in the design process. The project focuses on making inclusive design checks faster and easier to integrate into everyday workflows.

## How is it used?

A UX/UI designer uploads a screenshot of a website or mobile app screen. UX Lens AI analyzes the screen and presents a list of possible issues, ordered by priority.

For example, it could report:
- Text contrast may be too low against its background.
- A button is difficult to distinguish from nearby elements.
- Important information is not visually prominent.
- Text may be too small for comfortable reading.
- Labels such as “Continue” or “Submit” may not clearly explain the result of the action.

The primary users are UX/UI designers, graphic designers, product teams, and small organizations that do not have dedicated accessibility specialists.

## Data and AI techniques

The system would use annotated screenshots of websites and mobile applications. Each screenshot would include labels describing visual and accessibility issues.

Possible data sources could include:
- Public interface-design datasets.
- Open-source application screenshots.
- Synthetic interfaces created for training and testing.
- Accessibility guidelines such as WCAG, used as rules and evaluation criteria.

Possible AI techniques:
- Computer vision to detect interface elements such as buttons, fields, text blocks, and navigation.
- Optical character recognition (OCR) to extract visible text.
- Classification models to identify possible visual problems.
- Natural language processing to evaluate whether labels and calls to action are understandable.
- Rule-based checks for measurable criteria, such as contrast ratios and font sizes.

 ## Prototype

This repository includes a small prototype of UX Lens AI: a contrast checker for user-interface text and background colors.

The prototype calculates the contrast ratio between two colors and flags possible accessibility problems. It represents one small part of the proposed system.

A future version could use computer vision to identify text and background areas automatically from screenshots, OCR to read interface labels, and machine learning to prioritize possible usability issues.

## Challenges

The tool cannot fully understand a user’s goals, brand strategy, context, or emotional response to an interface. A visually unusual design is not necessarily bad design.

It could also make incorrect recommendations if screenshots are low quality, if text cannot be read accurately, or if training data does not represent a wide range of languages, cultures, devices, and accessibility needs.

The results should therefore be treated as suggestions for a designer to review, not as final decisions.

## What next?

A first prototype could analyze screenshots and check contrast, font size, and basic component consistency.

Later versions could:
- Integrate with Figma or design systems.
- Compare several screens for consistency.
- Offer feedback for responsive versions of a layout.
- Allow accessibility experts to give feedback that improves the model.
- Support several languages and local accessibility requirements.

## Acknowledgments

This project is inspired by accessibility standards such as the Web Content Accessibility Guidelines (WCAG), as well as the work of UX/UI designers and accessibility specialists. Any external datasets, code, images, or design resources used in a future prototype would be credited according to their licenses.
