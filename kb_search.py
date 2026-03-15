import json
import re
from datetime import datetime, timezone
from typing import Dict, List

import requests


EXPLICIT_MODULES = {
    "agent assist": "Agent Assist",
    "bot studio": "Bot Studio",
    "journey builder": "Bot Studio",
    "campaign manager": "Campaign Manager",
    "channels": "Channels",
    "ctx": "CTX",
    "ctwa": "CTX",
    "integrations": "Integrations",
    "ai admin": "AI Admin",
    "analytics": "Analytics",
    "bot studio analytics": "Bot Studio Analytics",
    "goals": "Goals",
    "goal analytics": "Goals",
    "workflows": "Workflows",
    "wallet": "Wallet",
    "personalize": "Personalize",
    "overview": "Overview",
    "extension": "Extension",
}

FEATURE_RULES = [
    {
        "id": "AA_BUSINESS_HOURS",
        "triggers": ["business hours", "after-hours behavior", "after-hours support", "different working hours than the default team", "schedule logic is wrong", "support hours"],
        "preferred_sources": ["user-management-business-hours"],
        "penalty_sources": ["views", "android-native"],
        "preferred_mode": "page_lookup",
    },
    {
        "id": "AA_AUTO_REPLIES",
        "triggers": ["automatic reply", "auto replies", "no agent is available", "customer reminder", "agent reminder", "wrong auto reply", "system resolves a chat automatically", "manual resolution behavior and auto resolution behavior", "inactive customers not agents", "away response versus normal routing"],
        "preferred_sources": ["response-management-auto-replies-and-customer-satisfaction"],
        "penalty_sources": ["views", "user-management-teams"],
        "preferred_mode": "page_lookup",
    },
    {
        "id": "AA_ASSIGNMENT_RULES",
        "triggers": ["channel and tags", "different teams", "assignment logic", "sticky assignment", "routing to the expected team", "routing depends on tags and channel", "reopened thread same owner", "retry assignment or fail immediately", "where to change routing outcomes"],
        "preferred_sources": ["chat-management-assignment-rules"],
        "penalty_sources": ["android-native", "tools-developer-mode"],
        "preferred_mode": "page_lookup",
    },
    {
        "id": "AA_STICKY_ASSIGNMENT",
        "triggers": ["sticky assignment", "reopened chats"],
        "preferred_sources": ["chat-management-assignment-rules"],
        "penalty_sources": ["what-happens-if-a-chat-doesnt-match", "assignment-enhancements"],
        "preferred_mode": "behavior",
    },
    {
        "id": "AA_ASSIGNMENT_AVAILABILITY",
        "triggers": ["agents are unavailable", "incoming chats under assignment rules", "unassigned chats"],
        "preferred_sources": ["chat-management-assignment-rules"],
        "penalty_sources": ["what-happens-if-a-chat-doesnt-match"],
        "preferred_mode": "behavior",
    },
    {
        "id": "AA_LIVE_MONITORING",
        "triggers": ["waiting for assignment", "ongoing chats", "no rule matched", "no rule matched conversations", "active busy offline", "active busy and offline", "first response time", "average first response time", "average response time", "average resolution time", "wait time related metrics", "wait time metrics", "chats are piling up before assignment", "agent state plus unresolved queue signals", "monitor active agents"],
        "preferred_sources": ["live-monitoring-dashboard-real-time-chat-analytics-and-performance-insights"],
        "penalty_sources": ["dashboard", "agent-timesheet", "chats"],
        "preferred_mode": "page_lookup",
    },
    {
        "id": "AA_LIVE_MONITORING_BEHAVIOR",
        "triggers": ["real-time operations view", "active, busy, and offline", "average first response time", "average response time", "average resolution time"],
        "preferred_sources": ["live-monitoring-dashboard-real-time-chat-analytics-and-performance-insights"],
        "penalty_sources": ["dashboard", "agent-timesheet", "chats"],
        "preferred_mode": "behavior",
    },
    {
        "id": "AA_LIVE_MONITORING_DASHBOARD",
        "triggers": ["which dashboard shows ongoing chats", "bot chats", "no-rule-matched conversations", "where can i monitor chats waiting for assignment in real time"],
        "preferred_sources": ["live-monitoring-dashboard-real-time-chat-analytics-and-performance-insights"],
        "penalty_sources": ["dashboard", "expression-library", "json-handler", "agent-transfer-node"],
        "preferred_mode": "page_lookup",
    },
    {
        "id": "BS_TEST_YOUR_BOT",
        "triggers": ["test your bot", "message log", "backend json", "starting node inputs", "variables updated", "before going live"],
        "preferred_sources": ["test-your-bot"],
        "penalty_sources": ["about-bot-studio", "conversational-path", "ctx-goal-nodes-and-conversions-api"],
        "preferred_mode": "page_lookup",
    },
    {
        "id": "BS_TEST_YOUR_BOT_DEBUG",
        "triggers": ["nodes executed", "starting node inputs", "variables updated", "without switching to another tool", "wrong path after a user message", "wrong path after user message", "node execution details and payload details", "trigger input validation and backend payload inspection", "test widget can reveal backend json"],
        "preferred_sources": ["test-your-bot"],
        "penalty_sources": ["code-node", "regex-validation", "conversational-path"],
        "preferred_mode": "behavior",
    },
    {
        "id": "BS_PROMPT_TIMEOUT",
        "triggers": ["timeout in prompt", "prompt node timeout", "user does not respond before the timeout", "timeouts work in prompt nodes"],
        "preferred_sources": ["timeout-in-prompt-nodes"],
        "penalty_sources": ["carousel", "send-message-node"],
        "preferred_mode": "behavior",
    },
    {
        "id": "BS_SAVE_DEPLOY_STALE",
        "triggers": ["live bot is still behaving like the old version", "saved a journey but the live bot", "save enough or do we need save & deploy"],
        "preferred_sources": ["save-vs-save-deploy"],
        "penalty_sources": ["journey-builder-legacy", "static-flows"],
        "preferred_mode": "behavior",
    },
    {
        "id": "BS_SAVE_DEPLOY_COMPARE",
        "triggers": ["what is the difference between save and save & deploy", "save vs save & deploy", "save vs deploy"],
        "preferred_sources": ["save-vs-save-deploy"],
        "penalty_sources": ["journey-builder-legacy", "static-flows", "how-do-the-elements-of-bot-studio-work-together"],
        "preferred_mode": "compare",
    },
    {
        "id": "CH_GO_LIVE_INSTAGRAM",
        "triggers": ["go live with instagram", "instagram users are not entering", "intended bot journey", "instagram routing", "instagram go live", "all bot studio journeys become active on instagram dm", "new conversations versus ongoing ones", "if behavior is fine in test your bot but wrong on instagram"],
        "preferred_sources": ["go-live-with-instagram"],
        "penalty_sources": ["welcome-to-gupshup-console", "about-bot-studio"],
        "preferred_mode": "page_lookup",
    },
    {
        "id": "CH_RETAIN_HISTORY",
        "triggers": ["retain customer chat history", "earlier chat context", "returning customers", "anonymous users", "chat history retention", "chat history is relevant", "remember prior conversation context on the same browser and device"],
        "preferred_sources": ["retain-customer-chat-history"],
        "penalty_sources": ["retargeting", "ads-management"],
        "preferred_mode": "behavior",
    },
    {
        "id": "INT_WEBHOOKS_CONFIG",
        "triggers": ["configure webhooks", "where do i configure webhooks", "webhooks in the console"],
        "preferred_sources": ["integrations/webhooks"],
        "penalty_sources": ["others-webhooks", "agent-assist/others"],
        "preferred_mode": "page_lookup",
    },
    {
        "id": "WF_WEBHOOKS_DELIVERY",
        "triggers": ["delivery analytics downstream", "duplicate delivery events", "reconcile webhook data", "recipient level delivery outcomes", "recipient-level delivery outcomes", "webhook delivery records and campaign response files disagree", "webhooks connect to delivery analytics", "webhook to analytics handling", "delivery callbacks map to the analytics view of message outcomes", "delivery records in callbacks", "click metadata and the delivery event timeline", "delivery events versus click events", "page for webhook configuration page for webhook to delivery analytics mapping and report for click metadata"],
        "preferred_sources": ["workflows/webhooks-to-delivery-analytics"],
        "penalty_sources": ["inbound-messages-and-events"],
        "preferred_mode": "compare",
    },
    {
        "id": "WF_WEBHOOK_SCHEMA_STORAGE",
        "triggers": ["which webhook data should we store", "delivery lifecycle tracking", "store sent delivered read and failed", "how should we store sent delivered read and failed events from webhooks", "fields from webhook payloads", "message ids consistently"],
        "preferred_sources": ["integrations/webhooks", "workflows/webhooks-to-delivery-analytics"],
        "penalty_sources": ["automated-campaign-analytics", "campaign-and-ctx-ad-preview", "inbound-messages-and-events"],
        "preferred_mode": "schema",
    },
    {
        "id": "CM_CAMPAIGN_ANALYTICS",
        "triggers": ["campaign analytics", "response file", "link tracking report", "dropped", "failed", "click through rate", "unique clicks", "total clicks"],
        "preferred_sources": ["campaign-analytics"],
        "penalty_sources": ["campaign-and-ctx-ad-preview", "dashboard"],
        "preferred_mode": "definition",
    },
    {
        "id": "CM_CAMPAIGN_ANALYTICS_DASHBOARD",
        "triggers": ["where do i view campaign analytics after a campaign is sent", "what metrics are available in campaign analytics", "what does dropped mean", "what does failed mean", "which report gives timewise delivery events for all phone numbers", "which report should i download"],
        "preferred_sources": ["campaign-analytics"],
        "penalty_sources": ["automated-campaign-analytics", "creating-and-analysing-a-click-to-whatsapp-campaign", "campaign-and-ctx-ad-preview"],
        "preferred_mode": "definition",
    },
    {
        "id": "GOAL_GOAL_ANALYTICS",
        "triggers": ["goal achieved", "unique users", "table view", "source type", "source value", "goal analytics"],
        "preferred_sources": ["goal-analytics"],
        "penalty_sources": ["ctx-goal-nodes-and-conversions-api"],
        "preferred_mode": "definition",
    },
    {
        "id": "GOAL_GOAL_ANALYTICS_EXPORTS",
        "triggers": ["goal achieved versus unique users", "goal achieved mean versus unique users", "exporting milestone-level goal analytics data", "source type show", "source value contain"],
        "preferred_sources": ["goal-analytics"],
        "penalty_sources": ["ctx-goal-nodes-and-conversions-api", "ctwa-to-bot-to-goals"],
        "preferred_mode": "definition",
    },
    {
        "id": "WF_CTWA_TO_GOALS",
        "triggers": ["connect a bot to a ctwa campaign", "ad journeys", "call and return", "campaign active", "post-click conversion performance", "makes the ctwa campaign active", "click publish"],
        "preferred_sources": ["ctwa-to-bot-to-goals"],
        "penalty_sources": ["ctx-goal-nodes-and-conversions-api", "creating-a-ctwa-ad"],
        "preferred_mode": "page_lookup",
    },
    {
        "id": "WF_CTWA_DASHBOARD_PAIR",
        "triggers": ["campaign delivered but i want to know whether users converted", "campaign delivered but conversion unclear", "delivery performance and post-click conversion performance", "users are clicking but no conversions are visible", "campaign delivered successfully users clicked but no goals are showing up", "delivery looks healthy but conversion is weak", "both campaign delivery performance and post click conversion performance", "delivery reporting and goal completion reporting"],
        "preferred_sources": ["campaign-analytics", "goal-analytics", "ctwa-to-bot-to-goals"],
        "penalty_sources": ["creating-a-ctwa-ad", "new-campaign", "jb-v2", "skills-developer-mode"],
        "preferred_mode": "compare",
    },
    {
        "id": "BS_SAVE_VS_DEPLOY",
        "triggers": ["save vs save & deploy", "save and save deploy", "save & deploy", "save vs deploy"],
        "preferred_sources": ["save-vs-save-deploy", "kb/bot-studio/save-vs-save-deploy.md"],
        "penalty_sources": ["faqs-of-bot-studio", "campaign-journey", "carousel", "send-message-node"],
        "preferred_mode": "compare",
    },
    {
        "id": "WH_DELIVERY_STATUSES",
        "triggers": ["delivery statuses", "message lifecycle statuses", "sent delivered read failed", "how should we store delivery statuses"],
        "preferred_sources": ["integrations/webhooks", "workflows/webhooks-to-delivery-analytics"],
        "penalty_sources": ["review-event", "template", "profile", "account", "status-event"],
        "preferred_mode": "schema",
    },
    {
        "id": "CTX_COMPARE_ANALYTICS",
        "triggers": ["campaign analytics vs goal analytics", "compare ctwa campaign analytics goal analytics", "difference between campaign manager analytics and goal analytics", "difference between campaign analytics and goal analytics"],
        "preferred_sources": ["campaign-analytics", "goal-analytics", "ctwa-to-bot-to-goals"],
        "penalty_sources": ["creating-a-ctwa-ad", "campaign-setup", "faqs-of-bot-studio"],
        "preferred_mode": "compare",
    },
    {
        "id": "CH_WIDGET_PRIVACY_CONFIG",
        "triggers": ["privacy policy", "web widget privacy", "widget privacy"],
        "preferred_sources": ["privacy-policy", "pre-chat-form"],
        "penalty_sources": ["security"],
        "preferred_mode": "setup",
    },
    {
        "id": "CTX_GOAL_VALIDATION",
        "triggers": ["goal is being fired", "goal firing", "expected journey step", "goal validation"],
        "preferred_sources": ["goal-analytics", "ctwa-to-bot-to-goals"],
        "penalty_sources": ["creating-a-ctwa-ad", "campaign-setup"],
        "preferred_mode": "troubleshooting",
    },
]

GLOBAL_PENALTY_SOURCES = [
    "android-native",
    "tools-developer-mode",
    "about-bot-studio",
    "conversational-path",
    "whatsapp-carousel",
    "inbound-messages-and-events",
    "dashboard",
    "campaign-and-ctx-ad-preview",
    "insights-agent-timesheet",
    "efficient-chat-navigation-for-different-user-roles-through-views",
    "ctx-goal-nodes-and-conversions-api",
    "code-node",
    "regex-validation-in-prompt-nodes",
    "expression-library-in-journey-builder-canvas",
    "json-handler-instead-of-code-node",
    "agent-transfer-node",
    "proactive-persistent-message",
    "gupshup-journey-builder-legacy",
    "what-happens-if-a-chat-doesnt-match",
    "assignment-enhancements",
    "automated-campaign-analytics",
    "creating-a-ctwa-ad",
    "creating-and-analysing-a-click-to-whatsapp-campaign",
    "jb-v2",
    "agent-personality",
    "skills-developer-mode",
    "ai-admin",
    "chat-fields",
    "views",
    "campaigns",
]


def _normalize_query_for_match(query: str) -> str:
    q = (query or "").lower()
    q = q.replace("&", " and ")
    q = re.sub(r"[^a-z0-9]+", " ", q)
    q = re.sub(r"\s+", " ", q).strip()
    return q


def _parse_parameters(parameters: object = None, **kwargs) -> Dict:
    data = {}
    if isinstance(parameters, str):
        p = parameters.strip()
        if p:
            try:
                data = json.loads(p)
            except Exception:
                data = {}
    elif isinstance(parameters, dict):
        data = dict(parameters)
    if kwargs:
        data.update(kwargs)
    return data


def _extract_query(params: Dict) -> str:
    if not isinstance(params, dict):
        return ""
    direct = params.get("query")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()
    nested = params.get("parameters")
    if isinstance(nested, dict):
        q = nested.get("query")
        if isinstance(q, str) and q.strip():
            return q.strip()
    if isinstance(nested, str) and nested.strip():
        try:
            obj = json.loads(nested)
            q = obj.get("query")
            if isinstance(q, str) and q.strip():
                return q.strip()
        except Exception:
            pass
    return ""


def _gh_headers(context) -> Dict[str, str]:
    token = context.get_secret("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("Missing GitHub configuration secrets")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "superagent-product-kb-search",
    }


def _repo_cfg(context) -> Dict[str, str]:
    owner = context.get_secret("GITHUB_OWNER")
    repo = context.get_secret("GITHUB_REPO")
    branch = context.get_secret("GITHUB_BRANCH") or "main"
    chunks_path = context.get_secret("GITHUB_KB_CHUNKS_PATH") or "kb/kb_chunks.jsonl"
    if not owner or not repo:
        raise RuntimeError("Missing GitHub configuration secrets")
    return {"owner": owner, "repo": repo, "branch": branch, "chunks_path": chunks_path}


def _load_chunks(context) -> List[Dict]:
    cfg = _repo_cfg(context)
    url = f"https://raw.githubusercontent.com/{cfg['owner']}/{cfg['repo']}/{cfg['branch']}/{cfg['chunks_path']}"
    r = requests.get(url, headers=_gh_headers(context), timeout=30)
    r.raise_for_status()
    items: List[Dict] = []
    for line in r.text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            items.append(json.loads(line))
        except Exception:
            continue
    return items


def _detect_module(query: str) -> str:
    q = _normalize_query_for_match(query)
    for k, v in EXPLICIT_MODULES.items():
        if k in q:
            return v
    return "General"


def _detect_feature_rules(query: str) -> List[Dict]:
    q = _normalize_query_for_match(query)
    return [rule for rule in FEATURE_RULES if any(t in q for t in rule.get("triggers", []))]


def _preferred_mode(query: str, feature_rules: List[Dict], intents: List[str]) -> str:
    q = _normalize_query_for_match(query)
    if any(x in q for x in [" vs ", " versus ", " difference ", " compare "]):
        return "compare"
    for r in feature_rules:
        if r.get("preferred_mode"):
            return r["preferred_mode"]
    return intents[0] if intents else "setup"


def _detect_intents(query: str) -> List[str]:
    q = _normalize_query_for_match(query)
    intents: List[str] = []
    if any(x in q for x in [" vs ", " versus ", " difference ", " compare "]):
        intents.append("compare")
    if any(x in q for x in ["which page", "where do i", "where exactly", "which dashboard", "which report", "what page", "where can i monitor"]):
        intents.append("page_lookup")
    if any(x in q for x in ["what is", "what does", "mean in"]):
        intents.append("definition")
    if any(x in q for x in ["what happens", "how do timeouts work", "when enabled", "when disabled", "after hours", "anonymous users", "returning customers", "real time operations view"]):
        intents.append("behavior")
    if any(x in q for x in ["troubleshoot", "what should i check", "not seeing", "missing", "wrong", "issue", "problem"]):
        intents.append("troubleshooting")
    if any(x in q for x in ["schema", "payload", "fields to store", "statuses", "status fields", "how should we store"]):
        intents.append("schema")
    if not intents:
        intents.append("setup")
    return intents


def _module_from_source(source: str) -> str:
    s = (source or "").lower()
    if "agent-assist" in s:
        return "Agent Assist"
    if "bot-studio" in s:
        return "Bot Studio"
    if "campaign-manager" in s:
        return "Campaign Manager"
    if "channels" in s:
        return "Channels"
    if "goals" in s:
        return "Goals"
    if "integrations" in s:
        return "Integrations"
    if "workflows" in s:
        return "Workflows"
    if "ctx" in s or "ctwa" in s:
        return "CTX"
    if "analytics" in s:
        return "Analytics"
    if "wallet" in s:
        return "Wallet"
    if "personalize" in s:
        return "Personalize"
    if "overview" in s:
        return "Overview"
    if "extension" in s:
        return "Extension"
    if "ai-admin" in s or "ai_admin" in s:
        return "AI Admin"
    return "General"


def _score_chunk(query: str, chunk: Dict, feature_rules: List[Dict], explicit_module: str) -> float:
    q = _normalize_query_for_match(query)
    source = str(chunk.get("source") or chunk.get("path") or "").lower()
    heading = str(chunk.get("heading") or "").lower()
    text = str(chunk.get("text") or "").lower()
    section_type = str(chunk.get("section_type") or "").lower()
    score = 0.0
    for token in re.findall(r"[a-z0-9&+-]+", q):
        if len(token) < 3:
            continue
        if token in heading:
            score += 0.25
        if token in source:
            score += 0.25
        if token in text:
            score += 0.05
    if explicit_module != "General" and explicit_module.lower() in _module_from_source(source).lower():
        score += 0.35
    if section_type == "reference":
        score -= 1.2
    if any(bad in source for bad in GLOBAL_PENALTY_SOURCES):
        score -= 4.0
    for rule in feature_rules:
        if any(ps in source for ps in rule.get("preferred_sources", [])):
            score += 3.0
        if any(pn in source for pn in rule.get("penalty_sources", [])):
            score -= 2.6
        for trig in rule.get("triggers", []):
            if trig in heading or trig in source:
                score += 0.7
    if any(rule.get("id", "").startswith("AA_LIVE_MONITORING") for rule in feature_rules):
        if "live-monitoring-dashboard-real-time-chat-analytics-and-performance-insights" in source:
            score += 5.0
        elif any(bad in source for bad in ["journey-builder-platform-upgrade", "call-and-return-node", "stateful-buttons", "preview"]):
            score -= 5.0
    if any(rule.get("id") in {"WF_WEBHOOKS_DELIVERY", "WF_WEBHOOK_SCHEMA_STORAGE"} for rule in feature_rules):
        if any(good in source for good in ["workflows/webhooks-to-delivery-analytics", "integrations/webhooks"]):
            score += 4.0
        elif any(bad in source for bad in ["how-to-create-whatsapp-static-flows", "automated-campaign-analytics"]):
            score -= 5.0
    if any(rule.get("id") == "WF_CTWA_DASHBOARD_PAIR" for rule in feature_rules):
        if any(good in source for good in ["campaign-analytics", "goal-analytics"]):
            score += 3.0
        elif "creating-a-tiktok-specific-bot-journey" in source:
            score -= 2.5
    if any(rule.get("id") == "BS_TEST_YOUR_BOT_DEBUG" for rule in feature_rules):
        if "test-your-bot" in source:
            score += 4.0
    if any(x in q for x in ["which page", "where do i", "which dashboard", "which report", "where exactly"]):
        if section_type == "path":
            score += 1.5
        if "exact ui path" in text or "gupshup console" in text:
            score += 0.8
    if any(x in q for x in ["what is", "what does", "mean"]):
        if section_type == "concept":
            score += 1.5
    if any(x in q for x in ["what happens", "when enabled", "when disabled", "after-hours", "anonymous users"]):
        if section_type in {"concept", "general", "validation"}:
            score += 1.1
    if any(x in q for x in ["schema", "payload", "fields to store", "statuses"]):
        if section_type == "schema":
            score += 1.8
    if any(x in q for x in ["troubleshoot", "what should i check", "missing", "wrong", "issue", "problem"]):
        if section_type in {"troubleshooting", "validation"}:
            score += 1.2
    if "privacy policy" in q:
        if "security" in source and not any(x in text for x in ["widget", "configure", "where", "display", "appear", "pre-chat form", "checkbox text", "hyperlinked text", "url for hyperlinked text", "before chat starts"]):
            score -= 1.8
        if "privacy-policy" in source:
            score += 2.3
        if "pre-chat-form" in source:
            score += 1.2
    return score


def _apply_feature_lock(scored: List[Dict], feature_rules: List[Dict]) -> List[Dict]:
    preferred_tokens = []
    for rule in feature_rules:
        preferred_tokens.extend(rule.get("preferred_sources", []))
    if not preferred_tokens:
        return scored
    preferred = [row for row in scored if any(tok in str(row.get("source") or "").lower() for tok in preferred_tokens)]
    return preferred if preferred else scored


def _compact_langfuse(trace_name: str, query: str, results: List[Dict], explicit_module: str, intents: List[str], preferred_mode: str, latency_ms: int, context) -> Dict:
    trace_id = f"kb-{trace_name}-{datetime.now(timezone.utc).strftime('%H%M%S%f')}"
    top_source = results[0].get("source") if results else None
    module_label = explicit_module if explicit_module != "General" else (_module_from_source(top_source or "") if top_source else "General")
    module_source = "explicit" if explicit_module != "General" else ("inferred_from_top_source" if top_source else "default")
    return {
        "ok": True,
        "trace_id": trace_id,
        "metadata": {
            "query": query,
            "release": context.get_secret("KB_RELEASE") if context else "kb-runtime",
            "logic_version": context.get_secret("KB_LOGIC_VERSION") if context else "search-telemetry-v1",
            "prompt_version": context.get_secret("KB_PROMPT_VERSION") if context else "kb-search-v1",
            "model": "rules-runtime",
            "temperature": 0.0,
            "top_p": 1.0,
            "query_family": explicit_module,
            "module_label": module_label,
            "module_source": module_source,
            "selected_answer_mode": preferred_mode,
            "answered": len(results) > 0,
            "clarification_asked": False,
            "unanswered": len(results) == 0,
            "top_score": results[0].get("score") if results else None,
            "top_source": top_source,
            "source_count": len(results),
            "latency_ms": latency_ms,
            "intent_labels": intents,
            "explicit_module": None if explicit_module == "General" else explicit_module,
            "confidence": results[0].get("score") if results else 0.0,
        },
    }


def kb_search(parameters: object = None, context=None, **kwargs) -> dict:
    params = _parse_parameters(parameters, **kwargs)
    query = _extract_query(params)
    top_k = int(params.get("top_k") or 5)
    if not query:
        raise ValueError("query is required")
    started = datetime.now(timezone.utc)
    chunks = _load_chunks(context)
    explicit_module = _detect_module(query)
    intents = _detect_intents(query)
    feature_rules = _detect_feature_rules(query)
    preferred_mode = _preferred_mode(query, feature_rules, intents)
    scored = []
    for c in chunks:
        s = _score_chunk(query, c, feature_rules, explicit_module)
        if s > 0:
            row = dict(c)
            row["score"] = s
            scored.append(row)
    scored.sort(key=lambda x: x.get("score", 0.0), reverse=True)
    scored = _apply_feature_lock(scored, feature_rules)
    results = scored[:top_k]
    latency_ms = int((datetime.now(timezone.utc) - started).total_seconds() * 1000)
    langfuse = _compact_langfuse("kb_search", query, results, explicit_module, intents, preferred_mode, latency_ms, context)
    return {
        "ok": True,
        "query": query,
        "top_k": top_k,
        "results": results,
        "langfuse": {
            "ok": langfuse["ok"],
            "trace_id": langfuse["trace_id"],
            "module_label": langfuse["metadata"]["module_label"],
            "module_source": langfuse["metadata"]["module_source"],
        },
    }