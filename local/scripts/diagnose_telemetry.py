#!/usr/bin/env python3
"""
Diagnose why traces have empty metadata.
Checks: Langfuse credentials, trace structure, metadata fields.
"""

import os, json, urllib.request, base64, ssl
from datetime import datetime, timedelta

def load_env():
    env = {}
    for line in open('.env'):
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, _, v = line.partition('=')
            env[k.strip()] = v.strip()
    return env

def check_langfuse_creds():
    env = load_env()
    print("=== LANGFUSE CREDENTIALS ===")
    print(f"LANGFUSE_HOST: {env.get('LANGFUSE_HOST', 'MISSING')}")
    print(f"LANGFUSE_PUBLIC_KEY: {env.get('LANGFUSE_PUBLIC_KEY', 'MISSING')[:20]}..." if env.get('LANGFUSE_PUBLIC_KEY') else "MISSING")
    print(f"LANGFUSE_SECRET_KEY: {env.get('LANGFUSE_SECRET_KEY', 'MISSING')[:20]}..." if env.get('LANGFUSE_SECRET_KEY') else "MISSING")

    if not all([env.get('LANGFUSE_HOST'), env.get('LANGFUSE_PUBLIC_KEY'), env.get('LANGFUSE_SECRET_KEY')]):
        print("❌ Missing credentials!")
        return False
    print("✅ Credentials present")
    return True

def check_recent_traces():
    env = load_env()
    host = env.get('LANGFUSE_HOST', '').rstrip('/')
    pub = env.get('LANGFUSE_PUBLIC_KEY', '')
    sec = env.get('LANGFUSE_SECRET_KEY', '')

    print("\n=== RECENT TRACES ===")

    creds = base64.b64encode(f"{pub}:{sec}".encode()).decode()
    import certifi
    ctx = ssl.create_default_context(cafile=certifi.where())

    frm = (datetime.utcnow() - timedelta(minutes=5)).strftime('%Y-%m-%dT%H:%M:%SZ')
    params = f"page=1&limit=10&fromTimestamp={frm}"
    url = f"{host}/api/public/traces?{params}"

    try:
        req = urllib.request.Request(url, headers={'Authorization': f'Basic {creds}'})
        body = json.loads(urllib.request.urlopen(req, timeout=30, context=ctx).read())
        traces = body.get('data', [])
        print(f"Found {len(traces)} traces in last 5 minutes")

        if not traces:
            print("⚠️  No recent traces. Issue might be upstream (skill not sending).")
            return

        # Check metadata in each trace
        empty_meta_count = 0
        for t in traces:
            meta = t.get('metadata', {})
            trace_id = t.get('id', '')

            # Count empty metadata fields
            empty_fields = [k for k,v in meta.items() if v is None or v == '']
            has_query = bool(meta.get('query'))
            has_answer = bool(meta.get('answer_preview'))

            if not has_query or not has_answer:
                empty_meta_count += 1
                print(f"\n❌ Trace {trace_id[:30]}...")
                print(f"   Has query: {has_query} | Has answer: {has_answer}")
                print(f"   Empty fields: {len(empty_fields)}/{len(meta)}")
                if empty_fields[:5]:
                    print(f"   Missing: {', '.join(empty_fields[:5])}")

        if empty_meta_count == 0:
            print("✅ All recent traces have metadata")
        else:
            print(f"\n⚠️  {empty_meta_count}/{len(traces)} traces have missing metadata")
            print("\nPossible causes:")
            print("1. Skill code not reaching _send_langfuse() calls")
            print("2. Early return/exception before telemetry")
            print("3. Context.get_secret() failing (LANGFUSE_ not in skill secrets)")

    except Exception as e:
        print(f"❌ Error fetching traces: {e}")

def check_skill_code():
    print("\n=== SKILL CODE CHECK ===")
    try:
        with open('skill/kb_answer.py') as f:
            content = f.read()
            has_send_langfuse = '_send_langfuse' in content
            has_metadata = 'metadata = {' in content
            has_context_secret = 'context.get_secret' in content

            print(f"Has _send_langfuse(): {has_send_langfuse}")
            print(f"Has metadata dict: {has_metadata}")
            print(f"Has context.get_secret(): {has_context_secret}")

            if all([has_send_langfuse, has_metadata, has_context_secret]):
                print("✅ Skill code looks correct")
            else:
                print("⚠️  Code might be missing telemetry")
    except Exception as e:
        print(f"❌ Error reading skill code: {e}")

if __name__ == '__main__':
    check_langfuse_creds()
    check_recent_traces()
    check_skill_code()

    print("\n=== NEXT STEPS ===")
    print("If traces are empty, check:")
    print("1. Skill environment has LANGFUSE_HOST, PUBLIC_KEY, SECRET_KEY secrets")
    print("2. Run a test query and re-check with this script")
    print("3. Check skill logs for exceptions before _send_langfuse() calls")
