# UX Lens AI

![UX Lens AI main screen](assets/header-image.png)

## Your idea in a nutshell

**UX Lens AI** is an AI-assisted tool that reviews screenshots of websites and mobile applications to detect potential issues in accessibility, visual clarity, and user experience.

The tool identifies elements such as insufficient contrast, small text, weak visual hierarchy, unclear calls to action, inconsistent components, and possible friction points within an interface. UX Lens AI is designed to support the work of designers and product teams, not to replace their professional judgment.

## Background

An interface can look attractive and still be difficult to use. Issues like poorly visible buttons, low-contrast text, too many competing actions, or poorly organized important information are frequent in digital products.

These problems can affect anyone, but they have a greater impact on users with visual impairments, the elderly, people using small screens, or users navigating in low-light conditions.

The motivation behind UX Lens AI is to make UX and accessibility reviews faster and more accessible. Often, teams do not have the time or resources to perform an exhaustive audit at every design stage. This tool aims to offer an initial visual review with actionable observations to help detect issues before they reach real users.

This topic is important because a good user experience is not just about a page looking good—it must also be clear, inclusive, understandable, and easy to use.

## AI Data and Techniques

UX Lens AI primarily works with interface images, such as screenshots of web pages, mobile apps, or digital designs.

Input data may include:

- Website screenshots.
- Mobile application screenshots.
- Designs exported from tools like Figma.
- Additional information about the type of audit to be performed.

The tool can focus on different aspects of an interface:

- Visual hierarchy.
- Accessibility.
- Navigation.
- Content clarity.
- Conversion experience.

To analyze the images, UX Lens AI utilizes artificial intelligence and computer vision techniques, such as:

- **Multimodal Models:** to interpret visual and textual elements present in an interface.
- **Optical Character Recognition (OCR):** to detect text, font sizes, labels, and calls to action.
- **Contrast Analysis:** to identify color combinations that could hinder readability.
- **Visual Component Detection:** to recognize buttons, cards, navigation bars, forms, and other interface elements.
- **Language Models:** to transform technical findings into clear, prioritized recommendations for designers.

The quality of the analysis depends on the quality of the screenshot. A blurry, incomplete, or low-resolution image may limit the detection of text, colors, and components.

## How is it used?

UX Lens AI is intended for UX/UI designers, frontend developers, product teams, digital agencies, and students who wish to review an interface before its publication or during its improvement process.

The workflow is as follows:

1. The user uploads a screenshot, a URL, or a design.
2. Selects the audit focus, for example: accessibility, visual hierarchy, navigation, or conversion.
3. UX Lens AI analyzes the interface and highlights areas that could cause problems.
4. The tool displays an overall score and prioritized recommendations based on their impact.
5. The designer reviews the suggestions and decides which ones to apply based on the product context and user needs.

The people affected by this solution include:

- **Designers and developers**, who can detect issues more quickly.
- **Product teams**, who can prioritize usability improvements.
- **End users**, who benefit from clearer and easier-to-use interfaces.
- **People with accessibility needs**, who may face fewer barriers when navigating digital products.

## Audit Examples

### 1. E-commerce Audit

In this example, UX Lens AI analyzes the home page of a fashion store called **Nova Atelier**.

![E-commerce Audit](assets/e-commerce-audit.png)

The audit identifies that several calls to action in the main hero section compete for the same visual attention. Buttons such as “Shop Women,” “Shop Men,” and “Explore Collection” have a similar hierarchy, which can make it difficult for the user to know which the primary action is.

**Key Findings:**

- Lack of a clearly prioritized primary call to action.
- Low visibility of the “Shop now” link.
- Product labels and badges that compete with names and prices.
- Secondary elements that may interrupt the navigation flow.

**Possible Recommendation:**

Define a primary action in the hero section and reduce the visual weight of secondary actions to better guide the user's decision.

### 2. Finance Application Audit

This example shows the audit of **Finova**, a mobile banking and personal finance application.

![Financial Application Audit](assets/finance-audit.png)

In a financial application, clarity and accessibility are especially critical because the user needs to interpret sensitive information such as balances, transactions, and payment actions.

**Key Findings:**

- Insufficient contrast on the “View details” button.
- Secondary text with low readability on light backgrounds.
- Small touch targets on some important actions.
- Improveable contrast in monthly spending charts.

**Possible Recommendation:**

Increase the contrast between text and backgrounds, especially on buttons and important financial content. It is also recommended to enlarge touch areas to facilitate mobile use.

### 3. Travel Page Audit

This example analyzes a travel discovery page called **Travelo.co**.

![Travel Page Audit](assets/travel-audit.png)

The page uses attractive imagery and a strong visual aesthetic, but UX Lens AI detects some elements that may affect comprehension and conversion.

Key Finding
