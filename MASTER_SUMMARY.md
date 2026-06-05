# MASTER SUMMARY — "Data Was Never the New Oil" (findings brief for the pitch)

Self-contained handoff for writing the video pitch. Every number below is either
**MEASURED** (we computed it from primary data), **REPORTED** (we quote a sourced figure),
or **MODELED** (we estimated it, assumptions shown). Tiers: **A** = primary/authoritative,
**B** = reputable secondary, **C** = aggregator (never cited as fact). Two figures are
flagged **DO-NOT-USE** / **NEEDS-DATA** — respect those or the rigor breaks.

All MEASURED numbers are reproducible from public data via a committed pipeline
(`bash run.sh`). Source IDs (SRC-0xx) are listed at the end.

---

## THE THESIS (what the film argues)

"Data is the new oil" gets the metaphor backwards, and the backwardness is the story.
**Oil is consumed — burn a barrel and it's gone. Data is copied — use a dataset and it's
still there.** By its nature data is the one resource you should never be able to exhaust.
Yet frontier AI is hitting a wall — but a strange one: **not a depleted stock, an exhausted
flow.** The machines have eaten essentially the entire public library of human text, and
humans don't write new high-quality text fast enough to feed the next model.

We've heard "we're running out" before — about oil, for a century — and a new extraction
technology made fools of the prophets every time (most recently fracking). **Data's
"fracking" is synthetic data and paid human data.** The open question the film lands on:
can you run out of something you never use up — and does the machine that refills the tank
end up poisoning it (model collapse)?

---

## THE HOOK (verified version)

> The platforms that harvest your data earn **tens of dollars per user per year** from it —
> Meta makes about **$56 a year off every daily user** — while a person's raw data sells on
> the broker market for **less than a dollar**. The most copyable resource ever created is
> somehow "running out." How?

⚠️ The pitch's old hook ("your data sells for 36 cents") is **DO-NOT-USE** — we could not
trace "$0.36" to any primary source. Use the **"< $1 / person"** framing (FT 2013), or lead
with the ARPU contrast above, which is fully sourced.

---

## THE STORY, CHAPTER BY CHAPTER (with the data)

**Ch 1-2 — The byproduct, and why data isn't oil.** Conceptual setup: data is non-rival
and copied; running out should be impossible. (No new stats needed; this is the hold-this-
contradiction beat.)

**Ch 3 — The exhaust economy.** How copyable "exhaust" became the most valuable business
model on earth, and how concentrated and quantified-you it is.
- **803 unique data brokers** are registered across the four public state registries
  (CA, VT, OR, TX); **166 of them (20.7%) are registered in all four states** — a national
  "professional" core (Acxiom, Claritas, Catalina, Babel Street, Blackbaud…). *(MEASURED, A)*
- Of California's 581 registered brokers: **18.9% admit collecting precise geolocation,
  5.3% say they sold or shared your data with a developer of a generative-AI system in the
  past year, 3.1% collect data on minors.** These are self-reported, so they are **lower
  bounds** ("at least"). *(MEASURED, A)* — **the 5.3% GenAI-sharing figure is the freshest,
  most novel stat in the film: a direct broker → AI-training link.**
- **The exhaust premium:** Alphabet earned **$402.8B** and Meta **$201.0B** in FY2025 —
  almost entirely from monetizing user data/attention. Per active user per year: **Meta
  ~$56, Reddit ~$18, Snap ~$13, Pinterest ~$7.** vs. raw data worth **< $1/person**.
  *(revenue + users MEASURED, A; data price REPORTED, B)*

**Ch 4-5 — The machines that eat data, and the strange wall.**
- Frontier language-model training sets have grown to **36 trillion tokens** (largest:
  Qwen3-Max, 2025), growing **~2.2×/year** at the frontier. *(MEASURED, A)*
- Epoch AI estimates the usable stock of human public text at **~4×10¹⁴ tokens**, growing
  only **0–10%/year**, fully used **2026–2032.** *(REPORTED, A)*
- **The hero finding (the crossover):** rebuilt from first-party data, the frontier trend
  meets that stock **around 2029** (modeled range 2027–2032) — independently landing
  *inside* Epoch's own window. The latest frontier model is already only **~1 order of
  magnitude below the entire usable stock of human text.** *(MODELED crossover on MEASURED
  + REPORTED inputs)* — **the stock line rises slowly while training explodes: exhausted
  flow, not depleted stock.**

**Ch 6 — We've seen this movie (oil).** The counterweight: scarcity prophets have been
wrong before.
- **M. King Hubbert predicted in 1956 that US oil would peak ~1970 — and it did** (actual
  conventional peak 1970 at **3.52 billion barrels/yr**, matching his curve). Production
  then declined to a **2008 trough (1.83 Gb/yr)** — exactly his shape.
- **Then fracking broke the forecast:** 2025 US production hit an **all-time record 4.96
  Gb/yr — about 12× what Hubbert's curve predicted for that year.** *(actual MEASURED, A;
  Hubbert's curve REPORTED+MODELED, B)*

**Ch 7 — Does the streak break?** The genuine open question, with the two "fracking"
candidates quantified.
- **Synthetic data defers the wall ~3 years per 10× of data** — so 10× → ~2032, 100× →
  ~2035, and even **1000× the entire human corpus only reaches ~2038**, because training
  grows exponentially. Synthetic *defers*, it cannot *abolish* without exponential supply.
  *(MODELED; the multiplier is a sweep, not a forecast)*
- **Paid human data is the other "fracking":** research on RLHF (paying humans to train
  models) exploded **~728× — from ~6 papers in 2021 to ~4,370 in 2024.** The industry is
  bifurcating: commodity labeling stagnates while expert data booms. *(MEASURED research
  PROXY, A/B; the dollar figures are REPORTED context — see flags)*
- **The one failure mode oil never had: model collapse** — a resource fed on its own copies
  can quietly degrade. *(This is a research-literature claim to cite, REPORTED — not
  something we measured.)* This is the honest landing: the era of free, infinite data is
  over, and the scramble (synthetic + paid human data) is the tell, whichever way it breaks.

---

## FINDINGS REFERENCE TABLE

| # | Headline | Key numbers | Type | Tier | Conf | Caveat |
|---|---|---|---|---|---|---|
| F-01 | CA brokers self-report | 18.9% geolocation · **5.3% GenAI-sharing** · 3.1% minors (n=581) | MEASURED | A | High | self-report = lower bound |
| F-02 | Four-state census | **803 unique · 166 in all 4 (20.7%)** · 437 in 2+ | MEASURED | A | Med-High | name-dedup; triangulates PRC/EFF ~750 |
| F-03 | Training-size growth | ~5×/yr (population); max 36T tokens | MEASURED | A | Med | crossover uses frontier ~2.2×/yr |
| F-04 | CCPA request load | top-10 = 67.7% of requests; ~99% fulfilled | MEASURED | A | Med | **supporting context** (pre-reported by Bloomberg); automated-signal inflation |
| F-05 | TX free-text AI scan | 0 substantive AI mentions | MEASURED | A | High | **REJECTED — negative result** |
| F-06 | Exhaust premium | Meta $56 / Reddit $18 / Snap $13 / Pinterest $7 per user/yr; rev Google $402.8B, Meta $201.0B; data < $1 | MEASURED + REPORTED | A / B | High | daily vs monthly users not strictly comparable |
| F-07 | The crossover (hero) | frontier meets ~4e14-token stock **~2029** (2027–2032) | MODELED on A+A | A | Med-High | crossover year is modeled; reproduces Epoch's window |
| F-08 | Deferral overlay | synthetic buys **~3 yr per 10×**; 1000× → ~2038 | MODELED | A+A | Robust leverage | multiplier is a sweep; model collapse caps it |
| F-09 | Hubbert vs actual | 1970 peak 3.52; 2008 trough 1.83; **2025 record 4.96 Gb/yr = 12× forecast** | MEASURED + REPORTED | A / B | High | EIA total-US vs Hubbert lower-48 |
| F-10 | Data-labor surge | **RLHF research ~728×** (6→4,370, 2021→2024) | MEASURED proxy + REPORTED | A/B | High (trend) | proxy for the field, **not jobs** |

---

## THE FOUR HERO VISUALS (built, reproducible)
1. **The crossover** — frontier LLM training size rising through the model cloud to meet the
   (slowly rising) human-text stock band ~2029, inside Epoch's 2026–2032 window.
2. **The deferral overlay** — the same chart with synthetic "+10× / +100×" stock lines and
   their crossover points marching right ~3 years per 10×.
3. **Hubbert vs. actual** — actual US oil tracks Hubbert's 1956 curve to the 1970 peak, then
   fracking rockets it to a 2025 record while his curve heads to zero.
4. **The data-labor signal** — RLHF publications' hockey-stick vs. the flat older
   labeling fields.

---

## RULES FOR THE PITCH (do not break these)

- **DO-NOT-USE:** "$0.36 / 36 cents per person." UNVERIFIED — no traceable primary. Replace
  with "< $1/person" (FT 2013) or the ARPU contrast.
- **NEEDS-DATA (don't invent a number):** a literal "AI-training jobs up X%." No occupation
  code exists; the big firms are private. Use the RLHF research proxy + attributed industry
  figures instead.
- **REPORTED, attribute on screen (never present as our finding):** the data-labeling
  market size and Scale AI / Mercor / Appen revenue & valuations (Tier B–C, mostly private);
  Epoch's stock estimate and window; Hubbert's 1956 parameters; "model collapse."
- **MODELED, say so:** the 2029 crossover year and the "3 years per 10×" deferral are
  estimates from a trend, not facts — their strength is that the crossover independently
  reproduces Epoch's published 2026–2032 window.
- **Self-report = lower bound:** phrase broker category stats as "at least X%."
- **F-02 framing:** the original cut is the **overlap (166 in all four states)**, not a
  "first national count" — Privacy Rights Clearinghouse + EFF already merged the registries
  (~750 groups, 2025); our 803 triangulates theirs.

---

## SOURCES (provenance, all logged)
- **SRC-001** Epoch AI model datasets (CC-BY) — training sizes/dates. Tier A.
- **SRC-002/003/004/005** California (CPPA), Vermont, Oregon, Texas data-broker registries. Tier A.
- **SRC-006** SEC EDGAR XBRL company facts (revenue). Tier A.
- **SRC-007** FY2025 10-K user metrics (Meta/Snap/Reddit/Pinterest). Tier A.
- **SRC-008** Epoch AI, "Will we run out of data?" (arXiv:2211.04325) — stock + growth + window. Tier A.
- **SRC-009** EIA — US crude oil production. Tier A.
- **SRC-010** Hubbert 1956 forecast parameters (secondary descriptions of his API paper). Tier B.
- **SRC-011** OpenAlex — publication counts (RLHF/annotation). Tier A/B.
- REPORTED context (attribute, not measured): FT 2013 data-value calculator; Bloomberg Law
  (CCPA requests); PRC/EFF broker merge; Scale/Mercor/Appen figures (CyberScoop/Sacra/
  PitchBook/market-research firms).

_Analysis complete through GATE 8 (approved 2026-06-05). Full traceability in FACTCHECK.md._
