# Sales Engineering (SE) Evaluation Framework: "The Global Standard"

This framework defines the "World-Class" standard for Pre-sales and Sales Engineering query responses. It is designed to evaluate whether an AI agent acts as a technical advisor and strategic partner by leveraging the full depth of the Gupshup Conversation Cloud.

## I. Core Evaluation Rubric (1-5 Scale)

### 1. Technical Accuracy & Precision
*   **The Standard**: Does it specify exact module names (e.g., "Bot Studio > Journeys") and node types (e.g., "Prompt Node" vs. "Action Node")?
*   **Module-Specific Check**:
    *   **Journey Builder**: References to modular microservices architecture, API/Code blocks, and Variable types (Local/Global/System).
    *   **AI Admin**: References to Intent/Entity mapping, Precision Thresholds, and LLM Config (GPT-4o vs 4o-mini).
    *   **Campaign Manager**: References to Dynamic Link Tracking, Recurring Schedules, and Response Files.

### 2. Business Resonance (The "So-What?")
*   **The Standard**: Maps technical features to outcomes like ROI, CPL (Cost Per Lead), or RTO (Return to Origin) reduction.
*   **Example**: "Using WhatsApp Flows doesn't just collect data—it reduces drop-offs in the symptomatic triage phase by 30%."

### 3. Consultative Depth & Strategic Insight
*   **The Standard**: Provides a "Point of View" (POV) on implementation. 
*   **Instruction**: Suggest "Modular Journeys" (Microservices style) for maintainability rather than monolithic flows.

### 4. Industry Contextualization
*   **The Standard**: Uses vertical-specific terminology.
    *   **Pharma**: Patient Adherence, HCP Engagement, Adverse Event (AE) Detection.
    *   **Retail**: Abandoned Cart Recovery, Pic-to-Cart (OCR), COD Management.

### 5. Clarity & "Next Step" Actionability
*   **The Standard**: Scalable structure (Bullets/Headers) with a proactive recommendation (e.g., "Next step: Let's configure a 'Test Bot' in Developer Mode to verify this logic").

---

## II. Detailed Module Instructions for SE Responses

### A. Journey Builder (Standard: Modular & Logic-Heavy)
*   **Instruction**: Always recommend **Modular Architecture**. 
*   **Detail**: Explain the use of **Call & Return** nodes to connect separate journeys (e.g., connecting a "Balance Inquiry" journey to an "Authentication" block).
*   **Variable Usage**: If a user asks about data persistence, specify **System Variables** (e.g., `userChannelID` for automatic phone number fetching) to reduce user friction.

### B. AI Admin & Agents (Standard: Personality & Guardrails)
*   **Instruction**: Define the **AI Personality** (Professional, Clever, Respectful, etc.) and **Language Style**.
*   **Technical Detail**: Always mention the **Precision Threshold** (default 30%) and how to tune it for strictness vs. flexibility.
*   **Tools**: Explain that **AI Tools** are the agentic equivalent of API integrations in structured journeys.

### C. Campaign Manager (Standard: Analytics & Personalization)
*   **Instruction**: Emphasize **Dynamic Link Tracking** for ROI visibility.
*   **Detail**: Explain the use of **Fallback Values** in templates to ensure a seamless experience even when subscriber data (like a name) is missing.
*   **Example**: Show how to use the **Response File** to analyze failure reasons (e.g., Meta validation vs. delivery failure).

---

## III. Scoring Key & Feedback Loop

| Score | Descriptor | Description |
| :--- | :--- | :--- |
| **5** | **World-Class** | Includes specific node recommendations, industry ROI proof-points, and instructions on using System Variables. |
| **4** | **Expert** | Technically sound with good business alignment; uses correct module terminology but misses the "Modular Architecture" advice. |
| **3** | **Functional** | Accurate but reactive. Explains how to find a feature but not how to use it strategically. |
| **1-2** | **Below Standard** | Vague, omits technical constraints, or fails to mention mandatory Meta approval processes for templates. |

## IV. Testing AI Responses
For every response, evaluate:
1.  **Did it mention a specific Node?** (e.g., API Block, Prompt Node).
2.  **Did it offer an Industry Example?** (e.g., "Abandoned Cart for Retail").
3.  **Did it specify a Step-by-Step path?** (e.g., "Bot Studio > AI Admin > Content > Scrapers").
