# Comprehensive KB Analytics Dashboard — Locked Structure

**Status:** LOCKED (2026-06-16)  
**Last Modified:** 2026-06-16  
**Rule:** Never remove, rename, or significantly alter any of these 8 report sections

---

## The 8 Locked Report Sections

### 1. 📋 Query Family Analysis (Top Modules)
**Purpose:** Module-level breakdown of query volume and performance  
**Columns:** Module | Query Count | % of Total | Avg Confidence  
**Data Source:** Live Langfuse  
**Shows:** Which product areas drive the most queries and confidence levels  
**Locked:** Yes - critical for identifying product-specific improvement areas

### 2. 🎯 Intent Distribution
**Purpose:** Intent-level analysis of user question types  
**Columns:** Intent | Queries | % of Total | Answered (%)  
**Data Source:** Live Langfuse  
**Shows:** What users are asking about (setup, overview, definition, etc)  
**Locked:** Yes - essential for understanding user needs

### 3. 👥 User Segmentation (Top 10 Internal)
**Purpose:** Track performance across internal Gupshup team members  
**Columns:** User | Queries | Answer Rate | Avg Confidence | Video Attached %  
**Data Source:** Live Langfuse  
**Shows:** Which team members use the KB and their success rates  
**Locked:** Yes - critical for presales/support team productivity metrics  
**Count:** Must show TOP 10 (not fewer, not more without explicit approval)

### 4. 🌐 External Users
**Purpose:** Track external customer/partner usage patterns  
**Columns:** User Email | Domain | Queries | Answer Rate | Avg Confidence | Video Attached %  
**Data Source:** Live Langfuse  
**Shows:** How external customers interact with the KB  
**Locked:** Yes - essential for understanding customer satisfaction  
**Note:** Separate table from internal users

### 5. 🎥 Video Analytics
**Purpose:** Track video attachment and caption metrics  
**Columns:** Metric | Value  
**Metrics:**
- Overall Video Attachment Rate
- Videos Appended to Answer
- Captions Enabled  
**Data Source:** Live Langfuse  
**Shows:** Video content strategy effectiveness  
**Locked:** Yes - video is a key product differentiator

### 6. 🎯 Multi-Intent & Cross-Module Questions
**Purpose:** Understand question complexity (single vs multi-intent)  
**Columns:** Intent Count | Queries | Answer Rate  
**Data Source:** Live Langfuse  
**Shows:** How many questions are simple vs complex  
**Locked:** Yes - identifies complexity distribution in user queries

### 7. 🎬 Intent-based Video Triggers
**Purpose:** See which intents have highest video attachment rates  
**Columns:** Intent | Queries | Video Attached %  
**Data Source:** Live Langfuse  
**Shows:** Which question types benefit most from video content  
**Locked:** Yes - identifies content gaps and video opportunities

### 8. ❌ Sample of Remaining IDK Queries (Top 20)
**Purpose:** Show real examples of questions the KB still can't answer  
**Columns:** Query | Module | Top Score  
**Data Source:** Live Langfuse  
**Shows:** Next optimization targets and failure cases  
**Locked:** Yes - critical for planning next improvements

---

## What's Allowed

### ✅ Data Refresh
- Update with fresh Langfuse data anytime
- Run: `python3 local/scripts/generate_analytics_dashboard.py`

### ✅ Styling & Layout Improvements
- Better CSS, colors, typography
- Responsive design enhancements
- Improved visual hierarchy

### ✅ Add Video Parameters
- Include video metrics anywhere they make sense
- Already in: User Segmentation, External Users, Intent-Video Triggers
- Can add to: Intent Distribution, Query Family Analysis

### ✅ Add New Columns
- New metrics/data to existing sections
- Example: Add "Video Attach Count" column to User Segmentation

### ✅ Adjust Display Count
- Change "Top 10" to "Top 15" if data exists
- Keep minimum of 10 for User Segmentation
- Can adjust counts for other tables

### ✅ Minor Wording Changes
- Clarify column headers
- Improve section descriptions
- Example: "Internal Domains" → "Gupshup Team" if more clear

---

## What's Forbidden

### ❌ Never Remove Sections
- All 8 sections must always be present
- Cannot hide/collapse by default
- Cannot make optional

### ❌ Never Rename Fundamentally
- Keep emoji and core meaning consistent
- Minor clarifications OK (e.g., "Internal" → "Gupshup Team")
- Cannot change to completely different names

### ❌ Never Merge Sections
- Each section stands alone
- Internal Users ≠ External Users (separate tables)
- Video Analytics ≠ Intent-Video Triggers (different purposes)

### ❌ Never Replace with Charts
- Tables are the format for these reports
- Visualizations can supplement, not replace
- Data accessibility is paramount

### ❌ Never Remove Columns
- Keep all existing columns
- Can add new columns
- Cannot remove core metrics

---

## Why This Structure?

Each section answers a critical question for optimization:

| Section | Question | Use Case |
|---------|----------|----------|
| Modules | Which products need help? | Product-specific improvements |
| Intents | What do users ask about? | Content planning |
| Internal Users | How is the team using it? | Presales/support metrics |
| External Users | How are customers using it? | Customer satisfaction |
| Video | Does video help? | Content strategy |
| Complexity | How hard are questions? | Effort estimation |
| Intent-Video | Which content gaps exist? | Video creation priorities |
| IDK Samples | What's still broken? | Next optimization targets |

**Removing any one of these blinds a critical dimension of decision-making.**

---

## The Generator Script

**File:** `local/scripts/generate_analytics_dashboard.py`

This script:
- Generates all 8 sections from live Langfuse data
- Includes all required columns
- Preserves the exact structure
- Cannot be modified to skip or remove sections

**To regenerate:**
```bash
cd /Users/adwit.sharma/kb_docs
python3 local/scripts/generate_analytics_dashboard.py
```

---

## History

**2026-06-16:** 
- Locked all 8 report sections permanently
- Documented in `.cursor/rules/dashboard-report-sections.md`
- Enforced via generator script

---

## Questions?

Before removing, renaming, or significantly altering any section:
1. Read this document
2. Check the rule file: `.cursor/rules/dashboard-report-sections.md`
3. Verify the action is in the "What's Allowed" section
4. If not, ask for explicit user approval with rationale

