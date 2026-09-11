> Source: https://console-docs.gupshup.io/docs/ace-agentic-llm-overview-copy
> Last updated: 2026-09-11

## **Introduction to ACE LLM**

ACE LLM by Gupshup is a family of generative models to automate **marketing, commerce & support** related conversations powered by Open & Closed source foundational models. It has been fine-tuned on industry & function-specific data to deliver a delightful customer experience. Enterprises get a head-start in delivering ACE LLM-powered conversational experiences.

The ACE LLM has been built keeping the focus on **compliance, accuracy** & **cost efficiency.** AI **guardrails** implemented in the ACE family ensure **ethical use**, **safety** in responses, **preventing harmful outputs** or biased information from delivering the **accurate results**.

Recently, We have upgraded our LLM models in to continuously improve the performance and accuracy of our AI systems.

| ACE Family Models (Till 11.0 release (6 Oct 24)) | ACE Family Models (12.0 -19.0 Release Starting from 7 Oct 24 - 10 Aug 25) | ACE Family Models (20.0 Release Starting from 11 Aug 25) |
| :----------------------------------------------- | :------------------------------------------------------------------------ | :------------------------------------------------------- |
| ACE LLM Lite (Flan t5, Llama 2)                  | ACE Lite: Llama-3.1-8b                                                    | ACE Lite: Qwen-3-4b                                      |
| ACE LLM Hybrid (Flan T5, Azure Open AI)          | ACE Pro: (Gemma-2-2b, Azure OpenAI GPT-4o-mini)                           | ACE Pro: (Gemma-2-2b, Azure OpenAI GPT-4o-mini)          |
| ACE LLM Hybrid v2 (Mistral, Azure Open AI)       | ACE Advanced: (Llama-3.1-8b, Azure OpenAI GPT-4o-mini)                    | ACE Advanced: (Qwen-3-4b, Azure OpenAI GPT-4o-mini)      |
| ACE LLM Classic (Azure Open AI)                  | ACE Premium: Azure OpenAI GPT-4o-mini                                     | ACE Premium: (Azure OpenAI GPT-4o-mini)                  |

<br />

**Use Case Handling**

<Table align={["left","left"]}>
  <thead>
    <tr>
      <th>
        ACE Family
      </th>

      <th>
        Imp. Use Case Served
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        **ACE Lite**
      </td>

      <td>
        * Qwen-3-4b: Intent & Entity Classification, FAQ Answering
      </td>
    </tr>

    <tr>
      <td>
        **ACE Pro**
      </td>

      <td>
        * Gemma-2-2b: Intent & Entity Classification
        * GPT-4o-mini: FAQ Answering
      </td>
    </tr>

    <tr>
      <td>
        **ACE Advanced**
      </td>

      <td>
        * Qwen-3-4b: Intent & Entity Classification
        * GPT-4o-mini: FAQ Answering
      </td>
    </tr>

    <tr>
      <td>
        **ACE Premium**
      </td>

      <td>
        * GPT-4o-mini: Intent & Entity Classification, FAQ Answering
      </td>
    </tr>
  </tbody>
</Table>

<br />

## **Introduction to Agentic LLM**

**Gemini** & **GPT** models are the core engines that drive the intelligence, response generation, and decision-making capabilities of your AI agents within the Gupshup AI Admin Module.

These models are used during both intent classification & skill execution and are configurable at both agent and skill level.

| Model                                       | Description                                                                                                                                    | Best For                                                                                      |
| :------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------- |
| GPT-4o (AI Agent Premium)                   | High-performance large language model from with strong reasoning & multi-modal capabilities                                                    | Complex use cases, longer replies, premium accuracy                                           |
| GPT-4o Mini (AI Agent Pro)                  | Lightweight variant offering faster responses at a lower compute cost                                                                          | Utility tasks, real-time replies, high-volume scenarios                                       |
| Gemini 2.0 Flash (ACE Flash Agent Premium)  | A powerful and versatile model with native multimodal input and a large 1M token context window for seamless, coherent conversations.          | Complex conversational flows, in-depth chat applications, and multi-turn interactions.        |
| Gemini 2.0 Flash-Lite (ACE Flash Agent Pro) | An optimized variant of Flash, designed for maximum speed and efficiency to deliver real-time, responsive conversational experiences at scale. | High-volume conversational tasks, real-time chatbots, and streamlined assistant applications. |