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
    "tata cliq": "Retail & D2C", "tata cliq": "Retail & D2C", "bata": "Retail & D2C", "noise": "Retail & D2C",
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
        return comp, COMPANY_INDUSTRY.get(comp.lower(), "General")

    m = re.search(r"(leading|major|top)\s+(.{5,70}?)\s+(company|brand|operator|platform|maker|retailer)", headline, re.I)
    if m:
        return _norm(m.group(0)), "General"

    return "", "General"


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

    if not headline and not bullets:
        return None
    if not bullets and len(metrics) < 2 and "Read the full story" not in text:
        return None
    if headline and len(headline) < 25 and not bullets:
        return None

    quote = ""
    for x in lines:
        if (x.startswith('"') and x.endswith('"')) or ("CTO" in x and '"' in x):
            quote = x.strip('"“"')
            break

    company, industry = _extract_company(text, headline, bullets)
    if company and industry == "General":
        industry = COMPANY_INDUSTRY.get(company.lower(), "General")

    use_cases = _infer_use_cases(text)
    channels = _infer_channels(text)
    confidential = _page_confidential(text)

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
    # Common multi-word brand patterns in confidential slides
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
    story.headline = re.sub(r"\bGupshup Confidential\b", "", story.headline, flags=re.I)
    story.headline = re.sub(r"www\.gupshup\.io", "", story.headline, flags=re.I)
    story.headline = re.sub(r"\s+", " ", story.headline).strip()
    story.quote = ""
    if not story.headline or len(story.headline) < 20:
        story.headline = f"{descriptor} achieved measurable KPI improvements through conversational messaging"
    elif descriptor.lower() not in story.headline.lower()[: len(descriptor) + 8]:
        story.headline = f"{descriptor} — {story.headline}"
    return story


def _story_to_markdown(story: Story) -> str:
    modules = _infer_modules(story.use_cases)
    display = story.company or ANON_BY_INDUSTRY.get(story.industry, "Enterprise customer")
    title = story.headline
    tier = "internal_anonymized" if story.confidential else "public"
    lines = [
        f"# {title}",
        "",
        "**Content type**: case_study",
        f"**Company**: {display}",
        f"**Module**: {', '.join(modules)}",
        f"**Industry**: {story.industry}",
        f"**Sharing tier**: {tier}",
        "",
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

    for f in OUT_DIR.glob("*.md"):
        f.unlink()
    if (OUT_DIR / "_manifest.json").exists():
        (OUT_DIR / "_manifest.json").unlink()

    manifest = []
    used: Set[str] = set()
    for story in merged:
        base = _slug(story.company if story.company else story.headline)
        slug = base
        n = 2
        while slug in used:
            slug = f"{base}-{n}"
            n += 1
        used.add(slug)
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
    print(f"2024 pages parsed: {len(s2024)}")
    print(f"2025 pages parsed: {len(s2025)}")
    print(f"Merged unique stories: {len(merged)}")
    print(f"Anonymized: {sum(1 for m in manifest if m['confidential'])}")


if __name__ == "__main__":
    main()
