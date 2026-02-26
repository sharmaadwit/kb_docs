# Pharma Vertical: AI-Native Org & Recipe Specification

## 1. Fundamentals
### Pharma Market Customers Goals
Customers (Pharma Brands, Hospitals, E-Pharmacies, Clinics) leverage conversational channels (WhatsApp, RCS, SMS) to:
*   **Patient Acquisition**: Driving leads for clinics and specialist centers via CTWA (Click-to-WhatsApp) ads.
*   **Patient Adherence (Retention)**: Educating chronic patients and ensuring they stick to their medication/lifestyle plans.
*   **HCP Engagement**: Enabling Medical Representatives (MRs) with instant product information to better serve Doctors (HCPs).
*   **Fulfillment & Sales**: Streamlining medicine ordering and lab test booking via rich interfaces like WhatsApp Flows.

### Market Knowledge: Segmentation
*   **Tier 1 (Enterprises)**: Focus on complex R&D enablement, Med-Rep AI Coaches, and patient support programs (PSPs). Requires high compliance (HIPAA/GDPR).
*   **Tier 2 (Mid-market/Clinics)**: Focus on high-volume appointment booking and automated lead qualification.
*   **Tier 3 (Retail Pharmacies)**: Focus on E-Pharmacy "Pic-to-Cart" (Prescription OCR) and home delivery.

---

## 2. Geography Wise Dynamics

### LATAM (e.g., Brazil)
*   **Market Dynamics**: Heavy reliance on visual/interactive ads. High trust in WhatsApp for healthcare service discovery.
*   **Top Use Cases**:
    *   **Clinic Lead Gen [Land]**: CTWA Ads leading to automated appointment scheduling (e.g., Dental, Cosmetic).
    *   **Patient Reminders [Must Have]**: Post-procedure follow-ups and medication alerts.
    *   **ROI Tracking [Must Have]**: Monitoring CPL (Cost Per Lead) vs. actual appointments booked.

### INDIA
*   **Market Dynamics**: Large-scale chronic disease populations (Diabetes, Respiratory). High penetration of E-pharmacies.
*   **Top Use Cases**:
    *   **E-Pharmacy Fulfillment [Land]**: Ordering medicines via Prescription OCR (Pic-to-Cart).
    *   **Med-Rep Enablement [Expand]**: AI Assistant for MRs to answer HCP queries on-the-field.
    *   **Chronic Care Journeys [Must Have]**: Multi-month journeys for diabetes/asthma management.

### MENA (e.g., UAE, KSA)
*   **Market Dynamics**: Expectation of premium, "VIP" service. High adoption of hybrid AI-Human support.
*   **Top Use Cases**:
    *   **Specialist Booking [Land]**: Coordination of appointments for high-value cosmetic/laser procedures.
    *   **E-Pharmacist Consultation [Expand]**: Video/Audio consultations embedded in the chat journey.
    *   **Multilingual Support [Must Have]**: Seamless Arabic/English switching for diverse expat populations.

---

## 3. Native AI-Org: Pharma Pod Framework

Following the Gupshup AI-Native Org principles, the Pharma vertical is organized into **Entrepreneurial Pods**.

### Revenue Pods (The Execution Layer)
*   **The Clinic/HCP Pod**: Owns the "HCP Enablement" and "Clinic Lead Gen" revenue targets.
    *   *SPOC*: [Name/Role]
    *   *Charter*: Maximize HCP engagement and clinic appointments booked.
*   **The Patient Care Pod**: Owns the "E-pharmacy" and "Patient Adherence" targets.
    *   *SPOC*: [Name/Role]
    *   *Charter*: Drive fulfillment volume and patient retention scores.

### Non-Revenue Pods (The Skill Layer)
*   **Pharma Compliance & Policy Pod**: A horizontal skill pod that builds and verifies the "Compliance Skill" (Adverse Event Detection, HIPAA-compliant storage).
*   **Core AIO Pod**: Provides the underlying SuperAgent orchestration and connects common skills like WhatsApp Flows and Personalize (CDP).

---

## 4. SuperAgent Pharma Recipe

The Pharma SuperAgent is defined as: `Context = Skills + Recipes + User Profile + Policies`.

### The Pharma Consultant Role
*   Understands Pharma behavior across regions (LATAM vs INDIA).
*   Maps Patient journeys: `Symptom -> Triage -> Doctor -> Prescription -> Ordering -> Adherence`.

### Core Skills (Built by Engineers)
1.  **Prescription OCR Skill**: Extracts drug names, dosage, and frequency from images.
2.  **Symptom Triage Skill**: Classifies user inputs into "Self-care", "Consult Doctor", or "Emergency".
3.  **Adverse Event (AE) Skill**: Detects potential side-effect mentions and triggers a Policy-mandated alert to the brand's safety team.
4.  **HCP Knowledge Base Skill**: RAG-based retrieval of medical literature and product specs.

### Recipes in Action (Built by GTM/CSM)
*   **The "Adherence" Recipe**:
    *   `Trigger`: Customer starts a treatment.
    *   `Action`: Call **Personalize Skill** to store patient profile -> Trigger **Automated Campaign Skill** for daily reminders -> Use **Feedback Skill** for weekly check-ins.
*   **The "Lead-to-Clinic" Recipe**:
    *   `Trigger`: CTWA Ad Click.
    *   `Action`: Call **Triage Skill** to qualify interest -> Call **WhatsApp Flows Skill** for booking -> Assign to **Agent Assist** if complex.

---

## 5. Entrepreneurship & Flux
*   **Leanness**: Each pod operates with a "Build Fast, Iterate Rapidly" mindset.
*   **Growth Mindset**: As AI models evolve (e.g., better reasoning for medical diagnosis), pods update their **Skills** without changing the **Recipe** structure.
*   **North Star**: Revenue and Patient Health Outcomes.
