#!/usr/bin/env python3
"""Extract success-story slides from internal PDF libraries into kb/case-studies/*.md."""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import pypdf

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "kb" / "case-studies"
PDF_2024 = ROOT / "_Master Success Stories Library_2024 (1).pdf"
PDF_2025 = ROOT / "Success Story Library 2025.pdf"

METRIC_VAL_RE = re.compile(
    r"^(?:\d+(?:\.\d+)?[xX%]|#\d+|\$\s?\d[\d,]*|\d+(?:\.\d+)?\s*(?:mn|million|k|cr|lakh|bn))$",
    re.I,
)
BULLET_RE = re.compile(r"^[●•]\s+")

COMPANY_INDUSTRY: Dict[str, str] = {
    "swiggy": "Food & Restaurant", "wow momo": "Food & Restaurant", "wow! momo": "Food & Restaurant",
    "chaayos": "Food & Restaurant", "zomato": "Food & Restaurant",
    "kotak bank": "Financial Services", "hdfc life": "Financial Services", "sbi life insurance": "Financial Services",
    "hdfc bank": "Financial Services", "icici lombard": "Financial Services", "canara bank": "Financial Services",
    "standard chartered bank": "Financial Services", "tonik bank": "Financial Services", "policybazaar": "Financial Services",
    "covercompare": "Financial Services", "creditwise capital": "Financial Services", "royal credit union": "Financial Services",
    "unifyn": "Financial Services", "unyfin": "Financial Services", "oto": "Financial Services",
    "no broker": "Real Estate", "nobroker": "Real Estate", "housing.com": "Real Estate",
    "emaar entertainment": "Real Estate", "emaar": "Real Estate", "eco world": "Real Estate",
    "treebo club": "Travel & Hospitality", "treebo": "Travel & Hospitality", "pumpumpum": "Travel & Hospitality",
    "red bus": "Travel & Hospitality", "redbus": "Travel & Hospitality", "cleartrip": "Travel & Hospitality",
    "ola": "Ride Hailing", "cityflo": "Ride Hailing", "blu": "Ride Hailing", "blusmart": "Ride Hailing",
    "bajaj auto": "Automotive", "bajaj": "Automotive", "tata motors": "Automotive", "cars24": "Automotive",
    "cars 24": "Automotive", "petromin": "Automotive", "ola electric": "Automotive",
    "orange": "Telecom", "youtube": "Entertainment", "vu sport": "Entertainment", "vusport": "Entertainment",
    "gujarat titans": "Entertainment", "mtv": "Entertainment", "dream11": "Entertainment", "dream 11": "Entertainment",
    "dewa": "Government", "khan academy": "Education", "doubtnut": "Education", "byju's": "Education", "byjus": "Education",
    "oralsin": "Healthcare", "oral sin": "Healthcare", "damas": "Healthcare",
    "tata cliq": "Retail & D2C", "bata": "Retail & D2C", "noise": "Retail & D2C",
    "lakme": "Retail & D2C", "lakmé": "Retail & D2C", "bombay shaving company": "Retail & D2C",
    "dmart": "Retail & D2C", "bigbasket": "Retail & D2C", "lenskart": "Retail & D2C", "myntra": "Retail & D2C",
    "snapdeal": "Retail & D2C", "6th street": "Retail & D2C", "schneider": "Retail & D2C", "vivo": "Retail & D2C",
    "akris": "Retail & D2C", "wolford": "Retail & D2C", "the sleep company": "Retail & D2C", "rupa rupa": "Retail & D2C",
    "ruparupa": "Retail & D2C", "sharaf dg": "Retail & D2C", "carl zeiss": "Retail & D2C", "max fashion": "Retail & D2C",
    "reserva": "Retail & D2C", "dream dubai": "Retail & D2C", "shipyari": "E-commerce Logistics", "ecom express": "E-commerce Logistics",
    "maggi": "CPG", "horlicks": "CPG", "surf excel": "CPG", "danone nutricia": "CPG", "dulux": "CPG",
    "kama sutra": "CPG", "pureit": "CPG", "vicco": "CPG", "love beauty & planet": "CPG", "akzo nobel": "CPG",
    "stelz": "CPG", "dubai insurance": "Financial Services", "tonik": "Financial Services",
}

USE_CASE_MODULES: Dict[str, List[str]] = {
    "ctwa": ["CTX", "Campaign Manager"], "marketing": ["Campaign Manager"],
    "commerce": ["Bot Studio", "Campaign Manager"], "qbm": ["Campaign Manager"],
    "support": ["Agent Assist"], "engagement": ["Bot Studio", "Campaign Manager", "Goals"],
    "onboarding": ["Bot Studio"], "rcs": ["Channels"], "whatsapp": ["Channels", "Campaign Manager"],
    "instagram": ["Channels"], "voice": ["Channels"], "ai": ["AI Admin", "Bot Studio"],
    "gen ai": ["AI Admin", "SuperAgent"], "payment": ["Wallet", "Integrations"],
    "end to end": ["Bot Studio", "Campaign Manager", "Agent Assist"],
    "flows": ["Bot Studio"], "ocr": ["AI Admin", "Integrations"],
}

ANON_BY_INDUSTRY: Dict[str, str] = {
    "Food & Restaurant": "Large food & restaurant company in India",
    "Financial Services": "Leading financial services company in India",
    "Real Estate": "Leading real estate platform in India",
    "Travel & Hospitality": "Leading travel & hospitality company in India",
    "Ride Hailing": "Leading ride-hailing company in India",
    "Automotive": "Leading automobile company in India",
    "Telecom": "Major telecom operator",
    "Entertainment": "Leading entertainment / sports brand",
    "Government": "Government / public-sector organization",
    "Education": "Leading ed-tech company in India",
    "Healthcare": "Healthcare provider",
    "Retail & D2C": "Leading retail / D2C brand",
    "CPG": "Leading consumer goods brand",
    "E-commerce Logistics": "E-commerce logistics company in India",
    "General": "Leading enterprise in its sector",
}

# Fix #3: regex patterns for stripping identifying phrases from anonymized content
_ANON_PHRASE_REPLACEMENTS = [
    (re.compile(r"\bthird[-\s]largest\b", re.I), "leading"),
    (re.compile(r"\bsecond[-\s]largest\b", re.I), "leading"),
    (re.compile(r"\b1st brand\b|\bfirst brand\b", re.I), "an early brand"),
    (re.compile(r"\boperating in \d+\s*countries\b", re.I), "operating across multiple countries"),
    (re.compile(r"\btop private bank\b", re.I), "leading bank"),
    (re.compile(r"\bIPL team\b", re.I), "professional sports team"),
    (re.compile(r"\bMP Election Commission\b", re.I), "state election authority"),
]

# Fix #7: quote pattern recognizing straight and Unicode smart quotes
_QUOTE_RE = re.compile(r'["\u201C\u201D]([^"\u201C\u201D]{30,400})["\u201C\u201D]')


@dataclass
class Story:
    story_id: str
    headline: str
    bullets: List[str]
    metrics: List[str]
    quote: str = ""
    company: str = ""
    industry: str = "General"
    use_cases: List[str] = field(default_factory=list)
    channels: List[str] = field(default_factory=list)
    confidential: bool = False
    source_library: str = ""
    source_page: int = 0
    raw_text: str = ""


def _slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return s[:90] or "case-study"


def _industry_slug(industry: str) -> str:
    """Convert an industry name to a filename-safe slug (Fix #1)."""
    s = unicodedata.normalize("NFKD", industry).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s.lower()).strip("-")
    return s or "general"


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def _is_noise(line: str) -> bool:
    low = line.lower().strip()
    if not low:
        return True
    if low in {"www.gupshup.io", "read the full story", "source: gupshup", "gupshup confidential"}:
        return True
    if re.match(r"^\*?\s*confidential", low):
        return True
    if low.isdigit() and len(low) <= 3:
        return True
    if re.match(r"^(food|restaurant|automotive|healthcare|telecom|government|ride hailing|entertainment|travel|hospitality|education|retail|cpg|fs)\s*&?", low):
        return True
    if low.startswith("use case outcome metric"):
        return True
    return False


def _page_confidential(text: str) -> bool:
    low = text.lower()
    if re.search(r"confidential(\s+information|\s+in\s+beta)?", low):
        return True
    if re.search(r"\bleading (ride|food|automobile|bus|sustainable|retail|bank|urban mobility)", low):
        return True
    if "operating in 6 countries" in low and "bus ticket" in low:
        return True
    return False


def _extract_metrics(lines: List[str]) -> Tuple[List[str], Set[int]]:
    metrics: List[str] = []
    used: Set[int] = set()
    i = 0
    while i < len(lines):
        if METRIC_VAL_RE.match(lines[i]):
            val = lines[i]
            label = ""
            if i + 1 < len(lines) and not METRIC_VAL_RE.match(lines[i + 1]) and not BULLET_RE.match(lines[i + 1]):
                label = lines[i + 1]
                used.add(i + 1)
            metrics.append(f"{val} — {label}".strip(" —") if label else val)
            used.add(i)
            i += 2 if label else 1
        else:
            i += 1
    return metrics, used


def _extract_bullets(raw_lines: List[str]) -> List[str]:
    bullets: List[str] = []
    current = ""
    for raw in raw_lines:
        line = re.sub(r"\s+", " ", raw.strip())
        if not line or _is_noise(line):
            continue
        if BULLET_RE.match(line):
            if current:
                bullets.append(current.strip())
            current = re.sub(r"^[●•]\s+", "", line)
        elif current and not METRIC_VAL_RE.match(line):
            current = f"{current} {line}"
        elif current:
            bullets.append(current.strip())
            current = ""
    if current:
        bullets.append(current.strip())
    return [b for b in bullets if len(b) > 20]


def _extract_headline(lines: List[str], used: Set[int], bullets: List[str], company: str) -> str:
    candidates: List[str] = []
    block: List[str] = []
    for idx, line in enumerate(lines):
        if idx in used or BULLET_RE.match(line):
            if block:
                candidates.append(" ".join(block))
                block = []
            continue
        if _is_noise(line) or line.startswith("www."):
            continue
        if len(line) < 8:
            continue
        if line.startswith('"') or "gupshup confidential" in line.lower():
            continue
        block.append(line)
    if block:
        candidates.append(" ".join(block))

    def score(c: str) -> int:
        s = 0
        c_low = c.lower()
        if re.search(r"\b(grows?|achiev|simplif|deliver|boost|make|launch|creat|reduce|increase|lead|transform)\b", c_low):
            s += 50
        if company and c.lower().startswith(company.lower()[:5]):
            s += 40
        if re.match(r"^leading ", c_low):
            s += 35
        if " etc." in c_low or "instagram worthy" in c_low:
            s -= 60
        if "www." in c_low or "confidential" in c_low:
            s -= 100
        s += min(len(c), 120)
        if any(b[:30].lower() in c_low for b in bullets):
            s -= 40
        return s

    best = max(candidates, key=score, default="")
    best = re.sub(r"\s+", " ", best).strip()
    best = re.sub(r"^www\.gupshup\.io\s*", "", best, flags=re.I)
    best = re.sub(r"\bGupshup Confidential\b", "", best, flags=re.I).strip()
    return best


def _extract_company(text: str, headline: str, bullets: List[str]) -> Tuple[str, str]:
    blob = _norm(f"{headline}\n{text}\n" + " ".join(bullets))
    for name, industry in sorted(COMPANY_INDUSTRY.items(), key=lambda x: -len(x[0])):
        if re.search(rf"\b{re.escape(name)}\b", blob):
            return name.title(), industry

    for b in bullets:
        m = re.match(r"^([A-Z][A-Za-z0-9'&.\-]+(?:\s+[A-Z][A-Za-z0-9'&.\-]+){0,3})\s+(?:used|took|launched|leveraged|sought|wanted|introduced|enabled|deployed|was facing|realised|realized|sought)", b)
        if m:
            comp = m.group(1).strip()
            return comp, COMPANY_INDUSTRY.get(comp.lower(), "General")

    m = re.match(r"^([A-Z][A-Za-z0-9'&.\-]+(?:\s+[A-Z][A-Za-z0-9'&.\-]+){0,4})\s+(?:grow|grows|achiev|deliver|simplif|boost|make|get|launch|creat)", headline)
    if m:
        comp = m.group(1).strip()
        if comp.lower() in {"brand", "the brand", "the organization", "the company", "company"}:
            return "", "General"
        return comp, COMPANY_INDUSTRY.get(comp.lower(), "General")

    m = re.search(r"(leading|major|top)\s+(.{5,70}?)\s+(company|brand|operator|platform|maker|retailer)", headline, re.I)
    if m:
        return _norm(m.group(0)), "General"

    return "", "General"


def _infer_industry_from_text(text: str) -> str:
    """Return the best industry label from page text when detection yields 'General' (Fix #4)."""
    low = text.lower()
    checks = [
        (["bus ", "hotel", "booking", "tourist", "hospitality"], "Travel & Hospitality"),
        (["ride ", "driver ", "commute", "cab ", "hailing"], "Ride Hailing"),
        (["bank", "loan", "credit", "insurance", "banking", "fintech"], "Financial Services"),
        (["food", "restaurant", "menu", "qsr", "dining"], "Food & Restaurant"),
        (["retail", "d2c", "fashion", "apparel", "jewelry", "catalog"], "Retail & D2C"),
        (["healthcare", "medical", "hospital", "clinic", "dental", "patient"], "Healthcare"),
        (["automotive", "car ", "vehicle", "automobile", "motorcycle"], "Automotive"),
        (["telecom"], "Telecom"),
        (["education", "edtech", "student", "learning"], "Education"),
        (["entertainment", "streaming", "sports", "gaming"], "Entertainment"),
        (["real estate", "housing", "property"], "Real Estate"),
        (["cpg", "consumer goods", "fmcg", "beauty", "nutrition"], "CPG"),
    ]
    for keywords, industry in checks:
        if any(kw in low for kw in keywords):
            return industry
    return "General"


def _infer_use_cases(text: str) -> List[str]:
    blob = text.lower()
    found: Set[str] = set()
    patterns = [
        ("CTWA", r"\bctwa\b|click to whatsapp|click-to-whatsapp|conversational advertising"),
        ("Marketing", r"\bmarketing\b|promotional|campaigns?\b|business messages"),
        ("Commerce", r"\bcommerce\b|ordering|checkout|cart\b|menu"),
        ("Support", r"\bsupport\b|helpdesk|call center|agent workload|complaint"),
        ("Engagement", r"\bengagement\b|retention|reactivat"),
        ("Onboarding", r"\bonboarding\b|rider registration|driver registration|new driver"),
        ("RCS", r"\brcs\b"),
        ("Gen AI", r"\bgen ai\b|generative ai\b|rammas"),
        ("AI", r"\bai\b|chatbot|virtual assistant"),
        ("Voice", r"\bvoice\b|click to call"),
        ("Payment", r"\bpayment\b|wallet\b"),
        ("Instagram", r"\binstagram\b"),
        ("WhatsApp Flows", r"\bwhatsapp flows?\b"),
    ]
    for label, pat in patterns:
        if re.search(pat, blob):
            found.add(label)
    return sorted(found)


def _infer_channels(text: str) -> List[str]:
    blob = text.lower()
    ch: Set[str] = set()
    if "whatsapp" in blob:
        ch.add("WhatsApp")
    if "rcs" in blob:
        ch.add("RCS")
    if "instagram" in blob:
        ch.add("Instagram")
    if "voice" in blob or "click to call" in blob:
        ch.add("Voice")
    return sorted(ch)


def _infer_modules(use_cases: List[str]) -> List[str]:
    mods: Set[str] = set()
    for uc in use_cases:
        for k, v in USE_CASE_MODULES.items():
            if k in uc.lower():
                mods.update(v)
    return sorted(mods) if mods else ["Campaign Manager"]


def _lift_metrics_from_bullets(bullets: List[str]) -> List[str]:
    """Extract up to 3 inline metrics from bullets when the metrics list is empty (Fix #6)."""
    inline_patterns = [
        re.compile(r"\b(\d+(?:\.\d+)?[xX])\b"),
        re.compile(r"\b(\d+(?:\.\d+)?)\s*(%)"),
        re.compile(r"\b(\d+(?:\.\d+)?)\s*(mn|million|k|cr|lakh|bn)\b", re.I),
    ]
    date_version_re = re.compile(r"^(?:20\d\d|v\d+|\d+\.\d+\.\d+)$", re.I)

    lifted: List[str] = []
    seen_vals: Set[str] = set()
    for bullet in bullets:
        if len(lifted) >= 3:
            break
        for pat in inline_patterns:
            m = pat.search(bullet)
            if not m:
                continue
            val_str = m.group(0).strip()
            if date_version_re.match(val_str):
                continue
            if val_str in seen_vals:
                continue
            rest = bullet[m.end():].strip()
            context = " ".join(rest.split()[:6]).strip(" .,;:")
            lifted.append(f"{val_str} — {context}" if context else val_str)
            seen_vals.add(val_str)
            break  # one metric per bullet
    return lifted


def _parse_story_page(text: str, page_num: int, library: str) -> Optional[Story]:
    if "Index (Click on the name" in text:
        return None
    raw_lines = [x for x in text.splitlines()]
    lines = [re.sub(r"\s+", " ", x.strip()) for x in raw_lines if not _is_noise(re.sub(r"\s+", " ", x.strip()))]
    if len(lines) < 3:
        return None

    bullets = _extract_bullets(raw_lines)
    metrics, used = _extract_metrics(lines)
    company, industry = _extract_company(text, "", bullets)
    headline = _extract_headline(lines, used, bullets, company)
    if company:
        m = re.search(
            rf"({re.escape(company)} .{{15,140}}?(?:messaging|whatsapp|platform|experience|ordering|engagement|commerce|banking|support|onboarding|results))",
            text,
            re.I | re.S,
        )
        if m:
            headline = re.sub(r"\s+", " ", m.group(1)).strip()
    if company and industry == "General":
        industry = COMPANY_INDUSTRY.get(company.lower(), "General")

    # Fix #4: reclassify "General" using keyword inference
    if industry == "General":
        industry = _infer_industry_from_text(text)

    if not headline and not bullets:
        return None
    if not bullets and len(metrics) < 2 and "Read the full story" not in text:
        return None
    if headline and len(headline) < 25 and not bullets:
        return None

    # Fix #7: quote extraction using regex with smart-quote support
    quote = ""
    joined_text = " ".join(lines)
    m_quote = _QUOTE_RE.search(joined_text)
    if m_quote:
        quote = m_quote.group(1).strip()

    company, industry = _extract_company(text, headline, bullets)
    if company and industry == "General":
        industry = COMPANY_INDUSTRY.get(company.lower(), "General")

    # Fix #4: reclassify again after final company extraction
    if industry == "General":
        industry = _infer_industry_from_text(text)

    use_cases = _infer_use_cases(text)
    channels = _infer_channels(text)
    confidential = _page_confidential(text)
    # Auto-anonymize when the slide already uses descriptor-style language ("Leading X", "Major Y").
    # These slides are usually internal-only even without a "Confidential" watermark.
    if not confidential and company and re.match(
        r"^(leading|major|top|large)\b", company.strip(), re.I,
    ):
        confidential = True

    # Fix #6: lift inline metrics from bullets when metrics list is empty
    if not metrics and bullets:
        metrics = _lift_metrics_from_bullets(bullets)

    story_id = f"{library}-p{page_num}"
    return Story(
        story_id=story_id,
        headline=headline or (bullets[0][:120] if bullets else "Success story"),
        bullets=bullets[:8],
        metrics=metrics[:6],
        quote=quote,
        company=company,
        industry=industry,
        use_cases=use_cases,
        channels=channels,
        confidential=confidential,
        source_library=library,
        source_page=page_num,
        raw_text=text,
    )


def _anonymize_story(story: Story) -> Story:
    if not story.confidential:
        return story
    descriptor = ANON_BY_INDUSTRY.get(story.industry, ANON_BY_INDUSTRY["General"])
    blob = story.raw_text.lower()
    if "india" in blob or "indian" in blob:
        if "in India" not in descriptor and "India" not in descriptor:
            descriptor = f"{descriptor} in India"
    elif any(x in blob for x in ("uae", "dubai")):
        descriptor = "Leading company in the UAE"
    elif "brazil" in blob:
        descriptor = "Leading retailer in Brazil"

    story.company = descriptor
    replace_patterns = sorted(COMPANY_INDUSTRY.keys(), key=len, reverse=True)
    replace_patterns += [
        "kotak mahindra bank", "kotak bank", "kotak", "hdfc", "icici", "sbi",
        "standard chartered", "canara bank", "dream11", "dream 11", "gujarat titans",
        "treebo", "ola", "zomato", "swiggy", "chaayos", "bajaj auto", "bajaj",
        "tata cliq", "tata motors", "cleartrip", "redbus", "red bus",
    ]
    for old in replace_patterns:
        pat = re.compile(re.escape(old), re.I)
        story.headline = pat.sub("the organization", story.headline)
        story.bullets = [pat.sub("The organization", b) for b in story.bullets]
        story.metrics = [pat.sub("", m).strip(" —") for m in story.metrics if pat.sub("", m).strip(" —")]

    # Fix #3: strip identifying phrases from anonymized headline, bullets, metrics
    def _clean_text(t: str) -> str:
        for pat, replacement in _ANON_PHRASE_REPLACEMENTS:
            t = pat.sub(replacement, t)
        return t

    story.headline = _clean_text(story.headline)
    story.bullets = [_clean_text(b) for b in story.bullets]
    story.metrics = [_clean_text(m) for m in story.metrics]

    story.headline = re.sub(r"\bGupshup Confidential\b", "", story.headline, flags=re.I)
    story.headline = re.sub(r"www\.gupshup\.io", "", story.headline, flags=re.I)
    story.headline = re.sub(r"\s+", " ", story.headline).strip()
    story.quote = ""
    if not story.headline or len(story.headline) < 20:
        story.headline = f"{descriptor} achieved measurable KPI improvements through conversational messaging"
    elif descriptor.lower() not in story.headline.lower()[: len(descriptor) + 8]:
        story.headline = f"{descriptor} — {story.headline}"

    # Fix #5: append use-case suffix to the anonymized descriptor (skip degenerate cases)
    if story.use_cases:
        first_uc = story.use_cases[0].strip().lower()
        if first_uc and len(first_uc) >= 2 and not story.company.lower().endswith(first_uc):
            candidate = f"{story.company} — {first_uc}"
            story.company = candidate[:80]

    return story


def _story_to_markdown(story: Story) -> str:
    """Convert a story to markdown with deterministic H1 and Outcome section (Fix #2)."""
    modules = _infer_modules(story.use_cases)
    display = story.company or ANON_BY_INDUSTRY.get(story.industry, "Enterprise customer")

    # Fix #2: deterministic H1 title
    if story.confidential:
        primary_uc = story.use_cases[0].lower() if story.use_cases else "conversational messaging"
        # display may already have " — {use_case}" appended by Fix #5; strip it to avoid duplication
        base_display = display
        uc_suffix = f" — {primary_uc}"
        if base_display.endswith(uc_suffix):
            base_display = base_display[: -len(uc_suffix)].strip()
        h1 = f"# {base_display} — {primary_uc} success story"
    else:
        h1 = f"# {display} — {story.industry} success story"

    tier = "internal_anonymized" if story.confidential else "public"
    lines = [
        h1,
        "",
        "**Content type**: case_study",
        f"**Company**: {display}",
        f"**Module**: {', '.join(modules)}",
        f"**Industry**: {story.industry}",
        f"**Sharing tier**: {tier}",
        "",
    ]

    # Fix #2: Outcome section (original PDF headline) before Summary
    outcome_text = story.headline.strip()
    if outcome_text:
        lines += ["## Outcome", outcome_text, ""]

    lines += [
        "## Summary",
        f"A {story.industry.lower()} organization used Gupshup conversational messaging to drive measurable business outcomes.",
        "",
    ]
    if story.metrics:
        lines += ["## Key results"] + [f"- {m}" for m in story.metrics] + [""]
    if story.bullets:
        lines += ["## What they did"] + [f"- {b}" for b in story.bullets] + [""]
    if story.use_cases:
        lines += ["## Gupshup capabilities used"] + [f"- {uc}" for uc in story.use_cases] + [""]
    if story.channels:
        lines += [f"**Channels**: {', '.join(story.channels)}", ""]
    if story.quote:
        lines += ["## Customer quote", f"> {story.quote}", ""]
    lines += [
        "## Good fit when",
        f"- You are in **{story.industry}** and want similar outcomes",
        f"- You need **{', '.join(story.use_cases[:3]) or 'conversational messaging'}** on **{', '.join(story.channels) or 'WhatsApp'}**",
        "",
    ]
    return "\n".join(lines)


def extract_pdf(path: Path, library: str) -> List[Story]:
    reader = pypdf.PdfReader(str(path))
    out: List[Story] = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if len(text.strip()) < 120:
            continue
        story = _parse_story_page(text, i + 1, library)
        if story:
            out.append(story)
    return out


def _similar(a: str, b: str) -> float:
    return SequenceMatcher(None, _norm(a), _norm(b)).ratio()


def merge_stories(stories: List[Story]) -> List[Story]:
    """Prefer 2025 when headline/company clearly duplicate."""
    kept: List[Story] = []
    for s in sorted(stories, key=lambda x: (x.source_library != "2025", x.source_page)):
        duplicate = False
        for i, k in enumerate(kept):
            same_co = s.company and k.company and _norm(s.company) == _norm(k.company)
            sim = _similar(s.headline, k.headline)
            if sim >= 0.72 or (same_co and sim >= 0.45):
                if s.source_library == "2025":
                    kept[i] = s
                duplicate = True
                break
        if not duplicate:
            kept.append(s)
    return kept


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    s2024 = extract_pdf(PDF_2024, "2024")
    s2025 = extract_pdf(PDF_2025, "2025")
    merged = merge_stories(s2024 + s2025)
    merged = [_anonymize_story(s) for s in merged]

    # Fix #5: descriptor deduplication — disambiguate duplicate company strings after merge
    company_counts: Dict[str, int] = {}
    for story in merged:
        company_counts[story.company] = company_counts.get(story.company, 0) + 1

    company_seen: Dict[str, int] = {}
    for story in merged:
        key = story.company
        if not key.strip() or key.startswith(" "):
            # Repair degenerate descriptors before dedup tagging
            descriptor = ANON_BY_INDUSTRY.get(story.industry, ANON_BY_INDUSTRY["General"])
            uc = (story.use_cases[0].lower() if story.use_cases else "")
            story.company = f"{descriptor} — {uc}".rstrip(" —") if uc else descriptor
            key = story.company
        if company_counts.get(key, 0) > 1:
            company_seen[key] = company_seen.get(key, 0) + 1
            if company_seen[key] > 1:
                tag = ""
                if story.metrics:
                    metric = story.metrics[0]
                    if "—" in metric:
                        val, label = metric.split("—", 1)
                        val = val.strip()
                        label = label.strip()
                        tag = f"{val} {label[:18]}".strip()[:24]
                    else:
                        tag = metric.strip()[:24]
                if not tag and story.use_cases and len(story.use_cases) > 1:
                    tag = story.use_cases[1].strip()[:18]
                if not tag and story.channels:
                    tag = story.channels[0].strip()[:18]
                tag = (tag or f"variant {company_seen[key]}").strip()
                story.company = f"{story.company} · {tag}"[:80]

    for f in OUT_DIR.glob("*.md"):
        f.unlink()
    if (OUT_DIR / "_manifest.json").exists():
        (OUT_DIR / "_manifest.json").unlink()

    manifest = []
    used_slugs: Set[str] = set()
    # Fix #1: per-industry counters for confidential slug generation
    industry_slug_counters: Dict[str, int] = {}

    for story in merged:
        if story.confidential:
            # Slug must NOT contain any brand token — use industry slug + counter
            ind_slug = _industry_slug(story.industry)
            industry_slug_counters[ind_slug] = industry_slug_counters.get(ind_slug, 0) + 1
            slug = f"{ind_slug}-{industry_slug_counters[ind_slug]}"
        else:
            # Public story: derive slug from company; refuse degenerate slugs.
            base_company = story.company or ""
            base_company = re.sub(r"\s*\(#\d+\)\s*$", "", base_company)
            base_company = re.sub(r"\s*·\s*.*$", "", base_company).strip()
            base = _slug(base_company)
            DEGENERATE = {"case-study", "to", "the", "for", "and"}
            if (
                not base
                or len(base) < 3
                or base.isdigit()
                or base in DEGENERATE
            ):
                ind_slug = _industry_slug(story.industry)
                industry_slug_counters[ind_slug] = industry_slug_counters.get(ind_slug, 0) + 1
                slug = f"{ind_slug}-public-{industry_slug_counters[ind_slug]}"
            else:
                slug = base
                n = 2
                while slug in used_slugs:
                    slug = f"{base}-{n}"
                    n += 1
        used_slugs.add(slug)
        path = OUT_DIR / f"{slug}.md"
        path.write_text(_story_to_markdown(story), encoding="utf-8")
        manifest.append({
            "file": path.name,
            "story_id": story.story_id,
            "company": story.company,
            "industry": story.industry,
            "confidential": story.confidential,
            "headline": story.headline[:100],
        })

    (OUT_DIR / "_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    total = len(manifest)
    anon_count = sum(1 for m in manifest if m["confidential"])
    pub_count = sum(1 for m in manifest if not m["confidential"])
    print(f"2024 pages parsed: {len(s2024)}")
    print(f"2025 pages parsed: {len(s2025)}")
    print(f"Merged unique stories: {total}")
    print(f"Anonymized: {anon_count}")
    print(f"Public: {pub_count}")


if __name__ == "__main__":
    main()
