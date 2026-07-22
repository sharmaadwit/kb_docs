"""Test session-based identity fallback for anonymous CC Express users.

Runs _langfuse_user_context() with various param sets and prints the
resolved (trace_user_id, meta_user) so we can confirm:
  - authenticated users still resolve by email
  - anonymous CC Express (user_id=2) get sess:{session_id}@ccexpress.gupshup.io
  - two anonymous sessions get DISTINCT userIds (not collapsed)
  - session_id fallback only when no email and user_id==2
  - acct:N:unknown fallback preserved when no session_id
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "skill"))
from kb_answer import _langfuse_user_context  # noqa: E402


def run(label, params):
    tuid, meta = _langfuse_user_context(None, params)
    print(f"--- {label}")
    print(f"    params        = {params}")
    print(f"    trace_user_id = {tuid}")
    print(f"    meta_user     = {meta}")
    print()
    return tuid, meta


# 1. Authenticated user (email present) — unchanged behavior
run("authenticated (email)", {"user_email_id": "ananya.a@gupshup.io", "user_id": 456, "user_name": "Ananya A"})

# 2. Anonymous CC Express, session A
a_uid, a_meta = run("anon CC Express session A", {"user_id": 2, "session_id": "sess-AAA-111"})

# 3. Anonymous CC Express, session B (different session)
b_uid, b_meta = run("anon CC Express session B", {"user_id": 2, "session_id": "sess-BBB-222"})

# 4. Anonymous CC Express, camelCase sessionId
run("anon CC Express (camelCase sessionId)", {"user_id": 2, "sessionId": "sess-CCC-333"})

# 5. Anonymous CC Express but NO session_id — must fall back to acct:2:unknown
run("anon CC Express no session_id", {"user_id": 2})

# 6. Anonymous CC Express with session but ALSO email — email wins (no synth)
run("anon w/ email present", {"user_id": 2, "session_id": "sess-X", "user_email_id": "real@ccexpress.gupshup.io"})

# 7. Non-CC-Express account with session_id — should NOT synthesize (only user_id==2)
run("non-cc account w/ session", {"user_id": 34, "session_id": "sess-Z"})

# 8. user_id sent as string "2"
run("anon user_id string '2'", {"user_id": "2", "session_id": "sess-STR"})

# --- Assertions ---
errors = []
if a_uid != "sess:sess-AAA-111@ccexpress.gupshup.io":
    errors.append(f"session A wrong: {a_uid}")
if b_uid != "sess:sess-BBB-222@ccexpress.gupshup.io":
    errors.append(f"session B wrong: {b_uid}")
if a_uid == b_uid:
    errors.append("session A and B collapsed to same userId!")
if a_meta.get("identity_source") != "session_id":
    errors.append(f"session A missing identity_source marker: {a_meta}")
if a_meta.get("user_email") != a_uid:
    errors.append("meta user_email should equal synthesized identity")

# no-session anon must be acct:2:unknown
ns_uid, _ = _langfuse_user_context(None, {"user_id": 2})
if ns_uid != "acct:2:unknown":
    errors.append(f"no-session anon should be acct:2:unknown, got {ns_uid}")

# email must still win
em_uid, _ = _langfuse_user_context(None, {"user_id": 2, "session_id": "s", "user_email_id": "real@ccexpress.gupshup.io"})
if em_uid != "real@ccexpress.gupshup.io":
    errors.append(f"email should win, got {em_uid}")

# non-cc account not synthesized
nc_uid, nc_meta = _langfuse_user_context(None, {"user_id": 34, "session_id": "sess-Z"})
if nc_uid != "acct:34:unknown":
    errors.append(f"non-cc should be acct:34:unknown, got {nc_uid}")
if nc_meta.get("identity_source"):
    errors.append("non-cc should NOT have identity_source marker")

# string "2" also synthesizes
s2_uid, _ = _langfuse_user_context(None, {"user_id": "2", "session_id": "sess-STR"})
if s2_uid != "sess:sess-STR@ccexpress.gupshup.io":
    errors.append(f"string user_id '2' should synthesize, got {s2_uid}")

if errors:
    print("FAILURES:")
    for e in errors:
        print("  X", e)
    sys.exit(1)
print("ALL ASSERTIONS PASSED")
