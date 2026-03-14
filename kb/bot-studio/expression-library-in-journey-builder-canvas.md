source_url: https://console-docs.gupshup.io/docs/expression-library-in-journey-builder-canvas

<!-- kb-golden:v10 -->
# Expression Library in Journey builder Canvas

**Module**: Bot Studio

## Definition
The Expression Library enhancement in the Modify Variable node is designed to empower bot designers with advanced data manipulation capabilities. By offering a robust set of pre-built functions, this feature eliminates the need for custom code nodes, enabling efficient and seamless variable operations directly within the Journey Builder Canvas. This enhancement introduces a dedicated interface for creating and testing expressions, providing an intuitive experience for designers to achieve complex data transformations with ease.

## Procedure
### Exact UI path
Gupshup Console → Bot Studio → Journey Builder

### Prerequisites
- Access to the relevant bot/project in Gupshup Console.
- A journey/app where you can test the configuration.

### Fields to configure
- Validation rules
- sample values for testing the expression

### Steps
1. Open Gupshup Console.
2. Navigate to the Modify Variable node and open the Modifier dropdown.
3. Test Expression Functionality: Designers can test expressions with sample values to verify results. Outputs or errors are displayed instantly, allowing iterative testing and corrections.
4. Save Validation: Expressions must pass validation before saving. Invalid expressions or mismatched data types disable the Save button, ensuring error-free runtime execution.
5. Select the Expression option at the bottom of the list.
6. Click on Build Expression open the editor.
7. Add sample values for testing the expression.
8. Click the play icon to execute the test.
9. Ensure the "Store in Variable" selection matches the output data type.
10. Select the Expression option from the Modifier dropdown.

### Validation / where to check
- Test Expression Functionality: Designers can test expressions with sample values to verify results. Outputs or errors are displayed instantly, allowing iterative testing and corrections.
- Designers can test expressions with sample values to verify results.
- Ease of Use: A clean and intuitive interface designed for bot designers of all experience levels. Comprehensive documentation and test functionality to ensure a smooth user experience.
- Comprehensive documentation and test functionality to ensure a smooth user experience.
- Testing the Expression: Add sample values for testing the expression. Click the play icon to execute the test. Review the output or error feedback in the Output Box.
- Click the play icon to execute the test.
- Follow the intuitive interface to create, test, and save expressions.
- Is real-time typo detection available? Not yet. However, the Test Expression functionality provides feedback for correcting errors.

### Troubleshooting
- Save Validation: Expressions must pass validation before saving. Invalid expressions or mismatched data types disable the Save button, ensuring error-free runtime execution.
- Invalid expressions or mismatched data types disable the Save button, ensuring error-free runtime execution.
- Error Feedback: Comprehensive error messages for invalid syntax or data mismatches. Suggestions for corrections to guide bot designers.
- Comprehensive error messages for invalid syntax or data mismatches.
- Error-Free Execution: Built-in validation and error feedback prevent runtime errors. Designers can confidently deploy expressions with guaranteed stability.
- Built-in validation and error feedback prevent runtime errors.
- Testing the Expression: Add sample values for testing the expression. Click the play icon to execute the test. Review the output or error feedback in the Output Box.
- Review the output or error feedback in the Output Box.
- # Error Handling

### Save / publish / deploy behavior
- Click **Save** (or **Save & Deploy**) to apply changes.

### Setup path
- Navigate to the Modify Variable node and open the Modifier dropdown.

## Options / variants
- Select the Expression option at the bottom of the list.
- Add sample values for testing the expression.
- Select the Expression option from the Modifier dropdown.

## Field mapping / schemas
- No explicit payload/schema details were identified in the source for this page.

## Field/payload examples
- No explicit payload examples were identified in the source.

## Cross-module workflow docs
- Bot Studio journey → Channel go-live (WhatsApp/Instagram/Web)
- Bot Studio journey → Observability via Webhooks

## Module disambiguation docs
- **Save** stores changes; **Save & Deploy** publishes to live channels.
- Node configuration happens in **Bot Studio**; delivery/engagement metrics are typically in **Analytics/Insights**.

## Reference (from source)
<!-- procedural:v2 -->
# Expression Library in Journey builder Canvas

**Module**: Bot Studio

## Overview
The Expression Library enhancement in the Modify Variable node is designed to empower bot designers with advanced data manipulation capabilities. By offering a robust set of pre-built functions, this feature eliminates the need for custom code nodes, enabling efficient and seamless variable operations directly within the Journey Builder Canvas. This enhancement introduces a dedicated interface for creating and testing expressions, providing an intuitive experience for designers to achieve complex data transformations with ease.

## When to use
_Add the primary scenarios and personas._

## Setup path
- Navigate to the Modify Variable node and open the Modifier dropdown.
Navigate to the Modify Variable node and open the Modifier dropdown.

## Step-by-step configuration
# Introduction

The Expression Library enhancement in the Modify Variable node is designed to empower bot designers with advanced data manipulation capabilities. By offering a robust set of pre-built functions, this feature eliminates the need for custom code nodes, enabling efficient and seamless variable operations directly within the Journey Builder Canvas. This enhancement introduces a dedicated interface for creating and testing expressions, providing an intuitive experience for designers to achieve complex data transformations with ease.

# Key Features

- Expression Modifier Option: A new Expression option in the Modify Variable dropdown menu, fixed at the bottom for easy access. Available even when no search results match other modifier options.
- A new Expression option in the Modify Variable dropdown menu, fixed at the bottom for easy access.
- Available even when no search results match other modifier options.
- Expression Box: A dedicated editor for creating and editing expressions. Supports approximately 180 pre-built functions for manipulating different data types. Enables nesting of functions for advanced data operations. Includes a variable icon to insert variables and a play icon to execute expressions.
- A dedicated editor for creating and editing expressions.
- Supports approximately 180 pre-built functions for manipulating different data types.
- Enables nesting of functions for advanced data operations.
- Includes a variable icon to insert variables and a play icon to execute expressions.
- Test Expression Functionality: Designers can test expressions with sample values to verify results. Outputs or errors are displayed instantly, allowing iterative testing and corrections.
- Designers can test expressions with sample values to verify results.
- Outputs or errors are displayed instantly, allowing iterative testing and corrections.
- Save Validation: Expressions must pass validation before saving. Invalid expressions or mismatched data types disable the Save button, ensuring error-free runtime execution.
- Expressions must pass validation before saving.
- Invalid expressions or mismatched data types disable the Save button, ensuring error-free runtime execution.
- Error Feedback: Comprehensive error messages for invalid syntax or data mismatches. Suggestions for corrections to guide bot designers.
- Comprehensive error messages for invalid syntax or data mismatches.
- Suggestions for corrections to guide bot designers.
# Key Benefits

- Enhanced Efficiency: Reduces dependency on custom code nodes, enabling faster journey development.
- Reduces dependency on custom code nodes, enabling faster journey development.
- Ease of Use: A clean and intuitive interface designed for bot designers of all experience levels. Comprehensive documentation and test functionality to ensure a smooth user experience.
- A clean and intuitive interface designed for bot designers of all experience levels.
- Comprehensive documentation and test functionality to ensure a smooth user experience.
- Robust Functionality: Pre-built functions simplify complex operations. Support for nesting allows flexibility for advanced use cases.
- Pre-built functions simplify complex operations.
- Support for nesting allows flexibility for advanced use cases.
- Error-Free Execution: Built-in validation and error feedback prevent runtime errors. Designers can confidently deploy expressions with guaranteed stability.
- Built-in validation and error feedback prevent runtime errors.
- Designers can confidently deploy expressions with guaranteed stability.
# How It Works

- Accessing the Expression Library: Navigate to the Modify Variable node and open the Modifier dropdown. Select the Expression option at the bottom of the list.
Accessing the Expression Library:

- Navigate to the Modify Variable node and open the Modifier dropdown.
Navigate to the Modify Variable node and open the Modifier dropdown.

- Select the Expression option at the bottom of the list.
Select the Expression option at the bottom of the list.

- Creating an Expression: Click on Build Expression open the editor. Use the available functions, insert variables, and nest operations as needed.
Creating an Expression:

- Click on Build Expression open the editor.
Click on Build Expression open the editor.

- Use the available functions, insert variables, and nest operations as needed.
Use the available functions, insert variables, and nest operations as needed.

- Testing the Expression: Add sample values for testing the expression. Click the play icon to execute the test. Review the output or error feedback in the Output Box.
Testing the Expression:

- Add sample values for testing the expression.
Add sample values for testing the expression.

- Click the play icon to execute the test.
Click the play icon to execute the test.

- Review the output or error feedback in the Output Box.
Review the output or error feedback in the Output Box.

- Saving the Expression: Once validated, click Use Expression to apply the expression to the node. Ensure the "Store in Variable" selection matches the output data type.
Saving the Expression:

- Once validated, click Use Expression to apply the expression to the node.
Once validated, click Use Expression to apply the expression to the node.

- Ensure the "Store in Variable" selection matches the output data type.
Ensure the "Store in Variable" selection matches the output data type.

# Supported Functionalities

- 180+ Pre-Built Functions: Handle strings, numbers, dates, arrays, and more.
- Handle strings, numbers, dates, arrays, and more.
- Nesting Support: Combine multiple functions for advanced data manipulations.
- Combine multiple functions for advanced data manipulations.
- Validation Rules: Max character limit: 1000. Up to 10 sample values for testing. Data type compatibility checks for "Store in Variable."
- Max character limit: 1000.
- Up to 10 sample values for testing.
- Data type compatibility checks for "Store in Variable."
# Error Handling

- Syntax Errors: Detected and displayed in the Output Box during testing. Clear guidance provided for corrections.
- Detected and displayed in the Output Box during testing.
- Clear guidance provided for corrections.
- Data Type Mismatches: Prevent saving of invalid expressions. Output Box highlights mismatches and suggests appropriate fixes.
- Prevent saving of invalid expressions.
- Output Box highlights mismatches and suggests appropriate fixes.
# Getting Started

To explore the Expression Library enhancement:

- Open the Modify Variable node in the Journey Builder Canvas.
- Select the Expression option from the Modifier dropdown.
- Follow the intuitive interface to create, test, and save expressions.
# FAQs

- What happens if I enter an invalid expression? Errors will be displayed in the Output Box during testing. The Save button will remain disabled until the expression is corrected.
- Errors will be displayed in the Output Box during testing. The Save button will remain disabled until the expression is corrected.
- Can I use this feature for all data types? Yes, the Expression Library supports all standard data types, including strings, numbers, arrays, and dates.
- Yes, the Expression Library supports all standard data types, including strings, numbers, arrays, and dates.
- Is real-time typo detection available? Not yet. However, the Test Expression functionality provides feedback for correcting errors.
- Not yet. However, the Test Expression functionality provides feedback for correcting errors.
This enhancement transforms the Modify Variable node into a powerful tool, offering unparalleled flexibility and ease for bot designers to manipulate data.

Updated 10 months ago

- List of Functions

## Business hours vs after-hours behavior
_Not applicable / not specified._

## Save/publish behavior
Key notes found in source:

- - Save Validation: Expressions must pass validation before saving. Invalid expressions or mismatched data types disable the Save button, ensuring error-free runtime execution.
- - Invalid expressions or mismatched data types disable the Save button, ensuring error-free runtime execution.
- - Error-Free Execution: Built-in validation and error feedback prevent runtime errors. Designers can confidently deploy expressions with guaranteed stability.
- - Designers can confidently deploy expressions with guaranteed stability.
- - Follow the intuitive interface to create, test, and save expressions.
- - What happens if I enter an invalid expression? Errors will be displayed in the Output Box during testing. The Save button will remain disabled until the expression is corrected.
- - Errors will be displayed in the Output Box during testing. The Save button will remain disabled until the expression is corrected.
