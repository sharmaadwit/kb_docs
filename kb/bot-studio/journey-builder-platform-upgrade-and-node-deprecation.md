> Source: https://console-docs.gupshup.io/docs/journey-builder-platform-upgrade-node-deprecation
> Last updated: 2026-09-11

As part of our efforts to enhance the Journey Builder platform, Gupshup is transitioning all projects to a more modern and scalable infrastructure. This document outlines upcoming node updates, deprecations, user-facing changes, and next steps for all customers and partners.

## 📅 Effective From: Post Console 19.0 Release

A deprecation notice will begin appearing in the Console UI Journey listing page for the following legacy nodes:

| Node               | Action Required                                                                                         |
| :----------------- | :------------------------------------------------------------------------------------------------------ |
| Code Node          | Replace with **Expression Library** (for simple logic) or migrate to **JB Pro** (for complex functions) |
| Database Node      | Use supported integrations or migrate to JB Pro for external DB support                                 |
| Send Message Node  | Use dedicated message-type nodes (Audio, Sticker, Location, etc.)                                       |
| Clear Context Node | Used in limited cases, supported in JB Pro if required                                                  |

These nodes will continue to work temporarily, but will be fully deprecated in a future release. ***(Tentative Dates will be notified on the UI once decided)***. Sufficient time will be provided for migration.

## Sample Screenshots of the Notice:

<Image align="center" border={false} caption="Notice on the Journey Listing Page" src="https://files.readme.io/c0bc878406631e8842513b49561810a68722f2c9612939a1e589e3333d1fb076-image.png" />

<Image align="center" border={false} caption="After Clicking **View Effected Journeys**" src="https://files.readme.io/0009bcc075046e29600acd1adab62c19485cd2c60c61d1197b8c82751703519f-image.png" />

<br />

<Image align="center" border={false} caption="Journey Canvas with deprecated node" src="https://files.readme.io/d37ec3c37c4f0647310d27a4da103816b8245dc63e31d38a15737e87fcbe843e-image.png" />

<Image align="center" border={false} caption="Project that doesn't contain any deprecated node(s)" src="https://files.readme.io/592df24796f1f8d10cc54dfb76789551aac5b6c71543cf645133e56b5492b3db-image.png" />

<br />

**Note**: The notice will show on reload of the page even if the Project doesn't contain any deprecated nodes. Please ignore for such cases.

<br />

## 🔄 Migration Pathways

### 🧩 Use Alternate Nodes in JB V2

If your journey uses simple logic or API integrations, you can refactor your journeys using:

* Expression Library in Modify Variable node for manipulating runtime data
* JSON Handler node for parsing API responses or JSON Objects
* New Message-Type Nodes (Audio, Sticker, etc.) for sending WA specific message types

***These features are available within JB V2(Newer Version) and require no code or migration support. Reach out to* [console-support@gupshup.io](mailto:console-support@gupshup.io)  *for upgrading your project to JB V2*.**

<br />

## 🚀 Upgrading to JB Pro (For Advanced Use Cases)

Projects that rely on custom logic or backend execution (via Code Node) can be migrated to JB Pro.

### Key Notes:

* JB Pro supports Function Nodes built on Gupshup's Solutions Platform
* Migration is done only for projects managed by Gupshup Devs
* A migration script will be used to replace Code Nodes with Function Nodes
* Manual pre- and post-migration testing will be conducted by the Bot Solutions team
* Once migrated, projects cannot be reverted to JB V2
* JB Pro projects will be maintained and upgraded by Gupshup Bot Solutions only
* 📩 If your project is managed by Gupshup, please contact your Project Manager or CSM to initiate the JB Pro upgrade.
* ⚠️ Projects managed by customers directly are not eligible for JB Pro migration at this time.

<br />

## ✅ Next Steps for Users

* Review your journeys: Check for usage of deprecated nodes.
* Refactor using JB V2 nodes: Use Expression Library, JSON Handler, and message-type nodes wherever possible.
* Contact Support: If you require help with identifying deprecated node usage or migration options.

<br />

> Stay updated: Final deprecation timeline and enforcement dates will be shared soon!

<br />

### 📘 Need Help?

**Contact**: [console-support@gupshup.io](mailto:console-support@gupshup.io)

**For JB Pro upgrades: Reach out to your Project Manager or Customer Success Manager (CSM)**

We encourage you to begin reviewing and refactoring your journeys now to avoid last-minute migration or journey failures when the final deprecation goes live.

Thank you for your continued support.