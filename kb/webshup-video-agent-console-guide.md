source_url: https://webshup.gupshup.io/

<!-- kb-golden:v10 -->
# Webshup — Website Video/Voice/Chat Assistant Console

**Module**: Webshup

## Definition

Webshup is Gupshup's embeddable AI assistant widget for websites. It puts a
real-time assistant on a customer's site in three modes — chat, voice, and a
talking video avatar — configured through the Webshup Console and deployed
with a single `<script>` tag. Publishing a change in the console updates the
live widget instantly; no redeploy is needed.

## Architecture

The assistant's answers come from a connected "brain," set on the **AI &
brain** page. For the app inspected, the brain is **Gupshup Superagent**,
wired via:
```
https://superagent.smsgupshup.com/api/agents/chat/stream
```
This is the same SuperAgent streaming endpoint used elsewhere in this
project (`SUPERAGENT_API_URL` in `.env`) — Webshup widgets are SuperAgent
agents under the hood, with Webshup providing the embeddable
chat/voice/avatar front-end on top.

## The three modes

- **Chat** — a themed, streaming text widget.
- **Voice** — real two-way spoken calls with live captions; interruptible
  (talking over the assistant stops it mid-sentence).
- **Avatar** — a live, talking video avatar (a face) that answers out loud.
  The visitor's own camera stays off; only the assistant's face is shown.

## Console navigation

Per-app console sections (URL pattern:
`webshup.gupshup.io/app/<app_id>/<section>`):

| Section | URL slug | What it's for |
|---|---|---|
| Overview | `overview` | Live traffic dashboard for this app |
| Appearance | `appearance` | Widget look and feel |
| AI & brain | `ai` | Which AI agent answers (the "brain") |
| Voice calls | `voice` | Audio-only call configuration |
| Avatar | `avatar` | Video avatar face/voice/personality |
| Test | `playground` | Live test of the real, already-configured widget |
| Deploy & embed | `deploy` | Embed snippet, allowed origins, version rollback |
| Share | `share` | Not yet verified |
| Personalized links | `campaigns` | Not yet verified |
| Analytics | `analytics` | Not yet verified (Overview already shows summary metrics) |
| Team | `team` | Not yet verified |
| Plan & usage | `plan` | Not yet verified |
| Settings | `settings` | Application name, active/disabled status, Application ID |

## Overview dashboard

Shows live traffic only — message text itself is not surfaced unless
"Include test traffic" is toggled on. Metrics: conversations, visitors,
messages, voice minutes, video minutes, count stopped by caps, a
conversations-over-time chart (by hour), channel mix (text/voice/video
split), voice usage (characters heard/spoken), and a recent-conversations
list (channel, session ID, message count, duration, timestamp).

## Appearance

Controls the widget's visual theme, organized into tabs: **Style, Header,
Chat area, Typing area, Chat launcher, Badge.**

### Fields to configure

- **Base design** — a starting preset (examples seen: "Classic," "Zen
  Arches," "Warm Sandstone") or custom colors; changing the preset doesn't
  change the underlying layout.
- **Match my website** — point it at a URL on your own domain and it reads
  your name, logo, colour, and font to auto-build a matching look (review
  and apply — nothing changes until confirmed).
- **Ready-made styles** — one-click industry-ready looks (colours, fonts,
  background), previewable live before publishing.
- **Accent colour** — the one brand colour; affects the send button,
  visitor's own messages, suggestion chips, scene, and highlights.
  Overridable per-section.
- **Fonts & text** — separate controls for body text font and the brand
  name's own font. Options seen: System, Avenir, Humanist, Editorial,
  Arial, Mono, Poppins, Roboto, Raleway, Space Grotesk, Outfit, Lexend,
  Nunito, Klee One, Caveat, Architects Daughter, Oswald, Playfair, Dancing
  Script, Courier Prime. Text size: Small / Medium / Large / XL / XXL /
  XXXL.
- **Shape & surface** — roundedness/"lift" of the widget; "Theme default"
  keeps the preset's own look.
- **Window** — panel size (Small/Medium/Large) and an "allow expand to full
  screen" toggle.
- **Start fresh** — clears any applied style (colours, scene, icons,
  tagline, avatar, greeting) back to the base layout; brand name and wiring
  are preserved.

### Save / publish behavior

All changes show live in an on-page preview; nothing goes live to visitors
until **Publish** is pressed.

## AI & brain

Picks which AI agent answers visitor messages. Options seen: **Gupshup
Superagent** (Gupshup's own agent builder — the connected option for the
app inspected, showing its live API URL) or a generic demo brain, with an
option to connect a different brain.

## Voice calls

Audio-only calls — distinct from the Avatar's voice, which is set
separately on the Avatar page.

### Fields to configure

- **Voice calls** toggle — show/hide the mic button.
- **Languages** — which languages callers can speak.
- **Voice** — the assistant's spoken voice (example seen: "Simi — Female,
  Support specialist"), with a play-preview button.
- **More settings** — loudness and interruption behavior (defaults
  recommended for most).
- **Greeting** — spoken as soon as the call connects (120-character limit
  observed).
- **Captions** — show the assistant's words on screen while speaking.
- **Floating window** — shrinks the call to a small floating orb if the
  visitor switches browser tabs.
- **Start speaking sooner** — the assistant starts talking before its full
  reply finishes generating, for perceived speed.
- **Call layout** — Compact (call in the small panel) vs. Stage (wide panel
  with orb + text chat side by side).
- **Let people type during a call** — adds a chat button during a call for
  a hybrid voice+type experience; off = call-only.
- **Waiting card** — what visitors see when a page invites them directly
  into a voice call via `data-invite="voice"`: the call orb, a talk button,
  and a short greeting. Talk button text (≤24 chars, overridable per page
  via `data-talk-label`) and greeting bubble (≤80 chars, can be empty) are
  both configurable here.

### Save / publish behavior

Settings save to a draft automatically; **Publish** makes them live.

## Avatar

The live video avatar feature.

### Fields to configure

- **Live avatar** toggle — visitors speak to a talking AI face; their own
  camera stays off.
- **Face** — chosen from a large catalog (120+ faces observed), filterable
  by All / Women / Men / style (Realistic / Animated). Each face card shows
  a name, a short style label (e.g. "Studio," "Home," "Sofa," "Table,"
  "Lean," "Animated 3d," "Window sofa"), a one-line visual description, and
  tags (e.g. "professional," "casual," "indoor," "3d animated"). A play
  button previews the face in motion.
- **Voice** — the avatar's spoken voice, set independently from the Voice
  Calls page.
- **Language** — the avatar's spoken language.
- **Personality** — a tone/personality setting (default observed; other
  options not verified).

## Test (Playground)

A live test of the real, currently-configured widget — not a separate mock
environment. Offers Desktop and Mobile preview modes.

## Deploy & embed

### Embed snippet

Paste before the closing `</body>` tag:
```html
<script type="module" src="https://webshup-cdn.gupshup.io/v1/embed.js" data-app="app_01a1634d38db75bc8c43ed844d133a48"></script>
```

Note: a different CDN host (`webshup-cdn.smsgupshup.com`) has also been
observed on a separately-deployed Webshup widget. Both appear valid;
confirm with the platform team which is current/canonical if the two ever
produce different behavior.

### Fields to configure

- **Allowed origins** — a comma-separated allowlist of domains permitted to
  load the widget; must be saved explicitly.
- **Live version / rollback** — shows what's currently live; one-click
  restore to the previous published version if a publish causes a problem.
  Rolling back takes effect immediately and can itself be undone.

## Settings

Application-level properties, distinct from widget appearance/behavior:

- **Application name**
- **Status** — Active or Disabled (disabled presumably stops the widget
  from loading/responding entirely — not independently verified)
- **Application ID** — the same ID used in the embed snippet's `data-app`
  attribute (`app_01a1634d38db75bc8c43ed844d133a48` for the app inspected)

## Not yet verified

- **Pricing** — intentionally excluded from this doc, consistent with this
  project's policy that the skill does not answer pricing.
- **Share**, **Personalized links**, full **Analytics**, **Team**, and
  **Plan & usage** sections — visible in the console nav but not opened for
  this doc.
