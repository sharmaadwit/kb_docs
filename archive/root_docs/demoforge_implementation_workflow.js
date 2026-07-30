export const meta = {
  name: 'demoforge-video-integration',
  description: 'Replace YouTube with DemoForge videos: discover projects, implement selection logic, integrate into KB responses',
  phases: [
    { title: 'Discover', detail: 'List DemoForge projects/demos, draft manifest' },
    { title: 'Implement', detail: 'Code selection logic + API wrapper (parallel)' },
    { title: 'Integrate', detail: 'Wire into kb_answer.py response pipeline' },
    { title: 'Test', detail: 'Validate with real KB queries' },
  ],
};

// Phase 1: Discover all DemoForge projects and demos
phase('Discover');

const discoveryPrompt = `
List all DemoForge projects and demos accessible via the API.

API Credentials:
- Base URL: https://demoforge-api.gupshup.io
- PAT: ${process.env.DEMOFORGE_PAT || 'pat_GHOIyphtorBRclEv_gXpcfSKE4nMqNuZlHUue0Gq3jI'}
- Auth: Bearer token

Tasks:
1. Call GET /projects → list all projects with demo_count
2. For each project with demo_count > 0, call GET /projects/{id}/demos
3. Filter demos to status="complete" only
4. For each demo, extract: id, name, use_case, industry, persona

Output a JSON structure ready to be inserted into kb/demoforge_manifest.json:
{
  "projects": [
    {
      "id": "...",
      "name": "...",
      "demo_count": N,
      "demos": [
        {
          "id": "...",
          "name": "...",
          "use_case": "...",
          "industry": "...",
          "persona": "...",
          "status": "complete"
        }
      ]
    }
  ]
}

Include ALL projects found. Do NOT filter or sample.
`;

const discoveryResult = await agent(discoveryPrompt, {
  label: 'discover-demoforge-projects',
  phase: 'Discover',
  schema: {
    type: 'object',
    properties: {
      projects: {
        type: 'array',
        items: {
          type: 'object',
          properties: {
            id: { type: 'string' },
            name: { type: 'string' },
            demo_count: { type: 'integer' },
            demos: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  id: { type: 'string' },
                  name: { type: 'string' },
                  use_case: { type: 'string' },
                  industry: { type: 'string' },
                  persona: { type: 'string' },
                  status: { type: 'string' },
                },
              },
            },
          },
        },
      },
    },
  },
});

log(`Discovered ${discoveryResult.projects.length} projects with ${discoveryResult.projects.reduce((sum, p) => sum + p.demos.length, 0)} complete demos`);

// Phase 2: Implement in parallel
phase('Implement');

const implementSelectionLogic = async () =>
  agent(
    `Implement select_demoforge_demo() function in skill/kb_video.py.

Context:
- Current YouTube selection is in select_video() at lines 357-400
- DemoForge demos are organized by intent + module, not by KB page
- Function should return: {demo_id, name, industry, persona, share_token: None} or None

Implementation:
1. Add function select_demoforge_demo(query, intent, module, context) → dict | None
2. Load kb/demoforge_manifest.json from context
3. Map intent (how_to, overview, setup, etc) → demo_id
4. Map module → preferred demos
5. Return best matching demo or None

Use this pseudo-code:
\`\`\`python
def select_demoforge_demo(query: str, intent: str, module: str, context: dict) -> dict | None:
    manifest = context.get('demoforge_manifest', {})
    module_demos = manifest.get('module_to_demos', {}).get(module, {})

    intent_key = intent.lower().replace('-', '_')
    demo_id = module_demos.get(intent_key)

    if not demo_id:
        return None

    # Look up demo in manifest
    demo = manifest.get('demos_by_id', {}).get(demo_id)
    if not demo:
        return None

    return {
        'type': 'demoforge',
        'demo_id': demo_id,
        'name': demo['name'],
        'industry': demo.get('industry'),
        'persona': demo.get('persona'),
        'share_token': None,  # filled later via API
    }
\`\`\`

Do NOT call the API yet. Just selection logic.
Add the function to kb_video.py around line 400 (after select_video).
Include docstring with example usage.
`,
    { label: 'implement-selection-logic', phase: 'Implement' }
  );

const implementAPIWrapper = async () =>
  agent(
    `Implement DemoForge API wrapper in skill/kb_answer.py.

API Details:
- Endpoint: POST https://demoforge-api.gupshup.io/demos/{demo_id}/share
- Auth: Bearer {PAT from env DEMOFORGE_PAT}
- Response: {share_token: "uuid4", share_status: "active", ...}
- Share URL: https://demoforge-ui.gupshup.io/shared/{share_token}/autoplay

Implementation:
1. Create async function _mint_demoforge_share_link(client, demo_id, context)
2. Load PAT from context['secrets']['demoforge_pat']
3. POST to /demos/{demo_id}/share with 5s timeout, 3s connect
4. Extract share_token from response
5. Build URL: https://demoforge-ui.gupshup.io/shared/{token}/autoplay
6. Retry only on 429/5xx, max 2 retries with backoff
7. Return {share_token, share_status, share_url} or None on error

Use this code template:
\`\`\`python
async def _mint_demoforge_share_link(
    client: httpx.AsyncClient,
    demo_id: str,
    context: dict,
    max_retries: int = 2
) -> dict | None:
    """Mint share link for a DemoForge demo. Idempotent."""
    pat = context.get('secrets', {}).get('demoforge_pat')
    if not pat:
        return None

    url = f"https://demoforge-api.gupshup.io/demos/{demo_id}/share"
    headers = {"Authorization": f"Bearer {pat}"}

    for retry in range(max_retries + 1):
        try:
            r = await client.post(url, headers=headers, timeout=httpx.Timeout(5.0, connect=3.0))

            if r.status_code == 401:
                return None  # Auth failed, don't retry
            if r.status_code in (400, 404):
                return None  # Bad request, don't retry
            if r.status_code >= 500:
                if retry < max_retries:
                    await asyncio.sleep((250 * (2 ** retry)) / 1000)
                    continue
                return None

            r.raise_for_status()
            demo = r.json()
            return {
                "share_token": demo["share_token"],
                "share_status": demo.get("share_status"),
                "share_url": f"https://demoforge-ui.gupshup.io/shared/{demo['share_token']}/autoplay"
            }
        except httpx.TimeoutException:
            if retry < max_retries:
                await asyncio.sleep((250 * (2 ** retry)) / 1000)
                continue
            return None
        except Exception:
            return None

    return None
\`\`\`

Add to kb_answer.py around line 6100 (before _append_videos_section).
`,
    { label: 'implement-api-wrapper', phase: 'Implement' }
  );

const [selectionResult, apiResult] = await parallel([
  () => implementSelectionLogic(),
  () => implementAPIWrapper(),
]);

log(`Selection logic: ${selectionResult ? '✅' : '❌'}`);
log(`API wrapper: ${apiResult ? '✅' : '❌'}`);

// Phase 3: Integrate into response pipeline
phase('Integrate');

const integrateResult = await agent(
  `Update kb_answer.py to use DemoForge videos in the response pipeline.

Current flow (kb_answer.py:6112-6178):
- After answer composition, select videos by intent
- YouTube: use select_video() based on KB page match

New flow:
1. Try DemoForge first: call select_demoforge_demo(query, intent, module)
2. If DemoForge demo found:
   - Call _mint_demoforge_share_link(demo_id)
   - If success: use DemoForge URL
   - If fail: fallback to YouTube
3. If no DemoForge match: use YouTube as fallback

Update kb_answer.py kb_answer() function around lines 6129-6155:

Replace:
\`\`\`python
if intent == "overview" and is_platform_pitch_query:
    videos = kb_video.catalog_videos(...)
elif intent == "overview":
    videos = kb_video.select_videos(...)
else:
    videos = [kb_video.select_video(...)]
\`\`\`

With:
\`\`\`python
if intent != "overview":
    # Try DemoForge first
    demoforge_demo = kb_video.select_demoforge_demo(
        query=query, intent=intent, module=explicit_module, context=context
    )
    if demoforge_demo:
        share_link = await _mint_demoforge_share_link(
            client=context.get('http_client'), demo_id=demoforge_demo['demo_id'], context=context
        )
        if share_link:
            demoforge_demo.update(share_link)
            videos = [demoforge_demo]
        else:
            videos = [kb_video.select_video(...)]  # fallback
    else:
        videos = [kb_video.select_video(...)]  # no DemoForge match
else:
    # Overview: use YouTube catalog
    videos = kb_video.catalog_videos(...)
\`\`\`

Also update _append_videos_section() to handle demoforge type:
- If video['type'] == 'demoforge': use format "**See it in action:** {name} ({industry} · {persona})"
- Else: use YouTube format

Preserve telemetry: log demo_id, share_token, api_latency.
`,
  {
    label: 'integrate-demoforge',
    phase: 'Integrate',
  }
);

log(`Integration: ${integrateResult ? '✅' : '❌'}`);

// Phase 4: Test
phase('Test');

const testResult = await agent(
  `Test DemoForge integration with real KB queries.

Test cases (using idk_regression.py or similar):
1. Campaign Manager how-to query → should return DemoForge demo
   - Query: "How do I create a campaign?"
   - Expected: DemoForge link (Campaign Manager demo)
   - Check: share_url contains demoforge-ui.gupshup.io

2. Bot Studio overview query → should return YouTube (not DemoForge)
   - Query: "What is Bot Studio?"
   - Expected: YouTube catalog (overview path)
   - Check: no demoforge links

3. Unmapped module query → should return YouTube fallback
   - Query: "How do I set up webhooks?"
   - Expected: YouTube or no video
   - Check: graceful fallback

4. API timeout scenario → should fallback to YouTube
   - Manually test with fake demo_id
   - Expected: no crash, YouTube fallback
   - Check: error logged

Generate test script showing:
- Query executed
- Demo selected
- API call result
- Final video URL
- Success/failure status
`,
  {
    label: 'test-demoforge',
    phase: 'Test',
  }
);

log(`Testing: ${testResult ? '✅' : '❌'}`);

log('✅ DemoForge integration workflow complete');
