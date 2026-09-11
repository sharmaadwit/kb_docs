> Source: https://console-docs.gupshup.io/docs/script-node
> Last updated: 2026-09-11

# Script Node in Journey Builder V2

Use the Script Node in Journey Builder V2 to run lightweight JavaScript for data transformation, variable updates, and migrated Legacy Code Node logic.

## Overview

The Script Node gives bot designers a controlled way to write custom JavaScript inside Journey Builder V2. It is useful when a journey requires logic that is difficult or inefficient to build with the Expression Library, JSON Handler, Modify Variable, or multiple no-code nodes.

Use the Script Node to reduce canvas complexity, support migration from Legacy Code Nodes, and handle advanced transformation use cases within a safe execution model.

***

## Why the Script Node was introduced

The Script Node addresses these Journey Builder V2 migration and authoring challenges:

* Some legacy Code Node logic is too complex to convert into Expression Library functions.
* Some API response handling and data transformation use cases require multiple JSON Handler, Modify Variable, or conditional nodes.
* Bot designers need a lightweight scripting option without depending on the full Legacy Code Node experience.
* Legacy projects using Code Nodes need a smoother migration path into Journey Builder V2.
* Migrated projects should retain existing logic without forcing bot designers to manually rewrite scripts using alternate nodes.

With the Script Node, bot designers can keep advanced logic while using the improved stability, scalability, and user experience of Journey Builder V2.

***

## What the Script Node supports

The Script Node allows bot designers to write custom JavaScript for lightweight logic execution.

Common use cases include:

* modifying local, global, or other supported variables;
* transforming API responses;
* preparing payloads;
* formatting strings, numbers, dates, or JSON values;
* handling calculations;
* simplifying logic that would otherwise require multiple nodes;
* preserving migrated logic from Legacy Code Nodes.

The Script Node can also support selected libraries that are explicitly allowed by the Journey Builder backend.

***

## Important limitation

The Script Node is not a full-fledged Code Node. It is a lightweight JavaScript execution node for controlled scripting use cases in Journey Builder V2.

Only libraries allowed by the Journey Builder backend can be used inside the Script Node. If a bot designer requires an additional library, they should raise a request with the Support team.

The Journey Builder Engineering team will evaluate each request and enable the library only if it is feasible, secure, and not process-intensive. Unsupported or high-risk libraries may not be enabled.

***

## Runtime behavior

The Script Node executes scripts asynchronously.

Each script execution has a maximum runtime threshold of 30 seconds.

If the script execution takes more than 30 seconds:

* the Script Node execution fails;
* the configured fallback path is triggered;
* the journey continues based on the fallback configuration.

Keep scripts minimal and optimized to avoid the 30-second timeout window.

Recommended practices:

* avoid unnecessary heavy loops;
* avoid large in-memory transformations unless required;
* avoid blocking or long-running logic;
* keep scripts focused on data manipulation;
* use JSON Handler or Expression Library where they are sufficient;
* use the Script Node only when low-code alternatives become too complex.

***

## Phase 1 scope

Phase 1 of the Script Node is migration-centric. Its primary goal is to support the migration of Legacy Journey Builder projects that currently use Code Nodes.

In Phase 1:

* Legacy Code Nodes will be migrated to Script Nodes in Journey Builder V2.
* Code written inside Legacy Code Nodes will be copied as-is into the new Script Node.
* Existing supported libraries used in Code Nodes will be migrated where applicable.
* Projects containing Legacy Code Nodes will be moved to Journey Builder V2 with Script Nodes.
* Runtime guardrails will be applied to ensure safer execution.
* Advanced scripting UX enhancements will be introduced incrementally in later phases.

This approach means bot designers do not need to manually convert complex Code Node logic into JSON Handler or Expression Library workflows during migration.

***

## Legacy Code Node migration

During migration from Legacy Journey Builder to Journey Builder V2:

1. The migration engine identifies journeys containing Legacy Code Nodes.
2. Each Legacy Code Node is converted into a Script Node.
3. The code inside the Legacy Code Node is copied as-is into the Script Node.
4. Node placement, connections, and execution flow are preserved where feasible.
5. Library dependencies are reviewed and migrated based on supportability.
6. **Unsupported libraries used in the Legacy Code Node may be allowed for migrated projects only. They cannot be used or found in other projects.**
7. Bot designers can review and continue using the migrated scripts from the Script Node editor.

This preserves custom logic and keeps journeys functional, subject to runtime compatibility.

***

## Library handling during migration

For newly created Journey Builder V2 projects, only the officially supported set of Script Node libraries will be available.

However, for migrated projects, there may be cases where a Legacy Code Node used a library that is not supported for new Script Node usage.

In such cases:

* the unsupported library may still be allowed only for that specific migrated project;
* this exception is provided to ensure a seamless migration;
* the library will not be available in new projects;
* the library cannot be newly requested for general usage;
* the library will appear with a `Legacy` tag in the Manage Library section of the Script Node editor;
* legacy-tagged libraries will be read-only or restricted based on implementation.

This allows migrated journeys to continue functioning while ensuring that deprecated or unsupported libraries are not introduced into new projects.

***

## Supported libraries

The Script Node supports only libraries that are approved and enabled by the Journey Builder backend.

If a required library is not available:

1. Raise a request with the Support team.
2. Provide the library name, version, and use case.
3. The Journey Builder Engineering team will evaluate the request.
4. If the library is feasible and safe to support, it may be enabled.
5. If the library is process-intensive, unsafe, unsupported, or unsuitable for the Script Node runtime, the request may be rejected.

Library enablement is subject to engineering review.

***

## Recommended usage

Use the Script Node when:

* Expression Library functions are insufficient;
* JSON Handler mappings would require too many nodes;
* complex transformations are required;
* migrated Code Node logic needs to be preserved;
* lightweight JavaScript can simplify the journey canvas.

Avoid using the Script Node when:

* the same logic can be handled with Expression Library;
* the same response can be parsed with JSON Handler;
* the script requires long-running execution;
* the script requires unsupported libraries;
* the script performs heavy computation that may exceed the 30-second threshold;
* the logic belongs in an external backend service rather than Journey Builder.

<br />

<Callout icon="📘" theme="info">


  **Note:** _Journey Builder V2 is designed for conversational automation use cases that require a moderate level of logic handling and computational processing. It should not be treated as an IDE, application server, or compute environment for process-intensive or memory-intensive operations._

  _For requirements that exceed the intended scope of Journey Builder V2, such processing should be performed outside the platform using an appropriate external service or backend system. The processed result can then be passed back into Journey Builder through API Nodes. This approach ensures that heavy computation is handled reliably outside the conversation runtime, while the user journey continues smoothly without performance degradation or runtime interruptions._ 
</Callout>

***

## Example use cases

### 1. Complex variable transformation

Use Script Node when a variable needs to be transformed using custom logic that is difficult to represent through Expression Library.

Example use cases:

* advanced string formatting;
* custom date calculation;
* conditional JSON restructuring;
* multi-field transformation;
* dynamic payload preparation.

***

### 2. Complex API response handling

Use Script Node when an API response requires multiple transformations that would otherwise need many JSON Handler and Modify Variable nodes.

Example use cases:

* combining multiple API fields;
* filtering nested arrays;
* calculating totals from object arrays;
* converting payload structures;
* preparing response-specific variables.

***

### 3. Legacy Code preservation

Use Script Node when a Legacy Code Node has been migrated into Journey Builder V2.

The migrated code will be available in the Script Node editor and can continue to execute, subject to runtime compatibility.

***

## Fallback behavior

If the Script Node fails during execution, the fallback path configured for the node will be triggered.

Common failure reasons include:

* script execution timeout greater than 30 seconds;
* runtime exception;
* unsupported operation;
* invalid variable reference;
* incompatible migrated code;
* library-related issue;
* syntax or execution error.

Configure fallback paths wherever appropriate to ensure the journey continues gracefully.

***

## Best practices

Follow these best practices while using the Script Node:

* Keep scripts short and focused.
* Avoid heavy computation inside journeys.
* Use JSON Handler for straightforward JSON extraction.
* Use Expression Library for standard transformations.
* Use Script Node only when alternate nodes make the canvas too complex.
* Test scripts thoroughly before deployment.
* Handle errors using try/catch where required.
* Avoid relying on unsupported libraries.
* Ensure variable names are valid and already created where required.
* Avoid long-running loops or unbounded operations.
* Use fallback paths for safer runtime handling.

***

## Phase 1 limitations

Phase 1 focuses on migration and foundational Script Node execution.

The following advanced capabilities may be enhanced in later phases:

* advanced reusable script management;
* richer script library management;
* enhanced variable dependency reconciliation;
* cross-journey script reuse improvements;
* deeper validation and debugging experience;
* improved handling of legacy library versions;
* more seamless scripting UX for bot designers.