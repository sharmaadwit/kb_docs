---
title: Advanced Configuration
description: Model infrastructure settings and voice tuning parameters
source: https://voiceagents.gupshup.io/developer-docs
---

# Advanced Configuration

## Advanced Tab

The Advanced tab provides a read-only view of the underlying model infrastructure configuration for the selected agent. Voice-specific tuning parameters are managed from the Agent tab, not here.

### Model Infrastructure Details

| Parameter | Value (Example) | Description |
|---|---|---|
| Provider | Model-1 | The voice AI platform provider stack in use |
| TTS Engine | Turbo v2.5 | Text-to-Speech engine version handling speech synthesis |
| ASR Provider | Built-in | Automatic Speech Recognition provider transcribing caller audio |

> ℹ NOTE Advanced settings — including voice stability, similarity boost, and speed parameters — are configured in the Agent tab under Voice Settings. This tab is read-only and reflects the infrastructure assigned to your account model.
