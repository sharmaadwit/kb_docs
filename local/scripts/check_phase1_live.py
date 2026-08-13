#!/usr/bin/env python3
"""
Check if Phase 1 consulting-tone is live by inspecting latest traces for answer_mode field.
"""

import os
import sys
import json
import ssl
import urllib.request
import urllib.parse
import base64
from datetime import datetime, timedelta

def load_env():
    if os.path.exists('.env'):
        with open('.env') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split('=', 1)
                    if len(parts) == 2:
                        os.environ.setdefault(parts[0], parts[1])

def fetch_traces(days=1, limit=100):
    """Fetch recent traces from Langfuse."""
    load_env()

    host = os.environ.get('LANGFUSE_HOST', 'https://cloud.langfuse.com').rstrip('/')
    pub = os.environ.get('LANGFUSE_PUBLIC_KEY', '')
    sec = os.environ.get('LANGFUSE_SECRET_KEY', '')

    if not pub or not sec:
        print('❌ Missing Langfuse credentials in .env')
        return []

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)

    from_ts = start_time.isoformat() + 'Z'
    to_ts = end_time.isoformat() + 'Z'

    url = f"{host}/api/public/traces?fromTimestamp={urllib.parse.quote(from_ts)}&toTimestamp={urllib.parse.quote(to_ts)}&limit={limit}&page=1"

    auth_string = base64.b64encode(f'{pub}:{sec}'.encode()).decode()
    headers = {'Authorization': f'Basic {auth_string}', 'Content-Type': 'application/json'}

    try:
        req = urllib.request.Request(url, headers=headers)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
            data = json.loads(response.read().decode())
            return data.get('data', [])
    except Exception as e:
        print(f'❌ Fetch error: {e}')
        return []

def main():
    print('=' * 100)
    print('PHASE 1 LIVE STATUS CHECK')
    print('=' * 100)
    print()

    traces = fetch_traces(days=1, limit=150)

    if not traces:
        print('⚠️  No traces fetched (API error or no recent traffic)')
        return

    print(f'✅ Fetched {len(traces)} recent traces (last 24 hours)')
    print()

    consulting_count = 0
    standard_count = 0
    no_mode_count = 0

    consulting_traces = []
    standard_traces = []

    for trace in traces:
        metadata = trace.get('metadata', {})
        answer_mode = metadata.get('answer_mode')

        query = str(trace.get('input', {}).get('query', ''))[:80]
        module = metadata.get('module', 'unknown')
        intent = metadata.get('intent', '?')
        conf = metadata.get('confidence', 0)
        timestamp = trace.get('timestamp', '?')

        trace_info = {
            'query': query,
            'module': module,
            'intent': intent,
            'conf': conf,
            'timestamp': timestamp
        }

        if answer_mode == 'consulting':
            consulting_count += 1
            consulting_traces.append(trace_info)
        elif answer_mode == 'standard':
            standard_count += 1
            standard_traces.append(trace_info)
        else:
            no_mode_count += 1

    print('=' * 100)
    print('RESULTS')
    print('=' * 100)
    print()
    print(f'Total traces analyzed:  {len(traces)}')
    print(f'  ✅ Consulting mode:     {consulting_count} traces')
    print(f'     Standard mode:      {standard_count} traces')
    print(f'  ⚠️  No answer_mode:     {no_mode_count} traces')
    print()

    if consulting_count > 0:
        print('✅ PHASE 1 IS LIVE!')
        pct = consulting_count / (consulting_count + standard_count) * 100 if (consulting_count + standard_count) > 0 else 0
        print(f'   {pct:.1f}% of recent traffic in consulting-tone mode')
        print()
        print('SAMPLE CONSULTING TRACES:')
        for i, t in enumerate(consulting_traces[:5]):
            print(f'  {i+1}. Module: {t["module"]:15} | Intent: {t["intent"]:15} | Query: {t["query"][:50]}...')
        print()

    if standard_count > 0 and consulting_count == 0:
        print('⚠️  PHASE 1 NOT ACTIVE')
        print('   Standard-mode traces exist but NO consulting-mode traces')
        print('   Check: CONSULTING_TONE_CONFIG["enabled"] = True in skill/kb_answer.py')
        print('   Action: Restart SuperAgent skill service')
        print()

    if no_mode_count > 0:
        print(f'⚠️  {no_mode_count} traces missing answer_mode field')
        if consulting_count == 0 and standard_count == 0:
            print('   → Code may not be deployed or executed yet')
        print()

    # Module breakdown by mode
    if consulting_count > 0 or standard_count > 0:
        print('MODULE BREAKDOWN (Phase 1 Targets):')
        print('-' * 100)

        module_consulting = {}
        module_standard = {}

        for t in consulting_traces:
            m = t['module']
            module_consulting[m] = module_consulting.get(m, 0) + 1

        for t in standard_traces:
            m = t['module']
            module_standard[m] = module_standard.get(m, 0) + 1

        all_modules = set(module_consulting.keys()) | set(module_standard.keys())
        for mod in sorted(all_modules):
            cons = module_consulting.get(mod, 0)
            std = module_standard.get(mod, 0)
            total = cons + std
            pct = cons / total * 100 if total > 0 else 0
            print(f'  {mod:20} | consulting: {cons:3} | standard: {std:3} | ({pct:5.1f}% consulting)')
        print()

    print('=' * 100)

if __name__ == '__main__':
    main()
