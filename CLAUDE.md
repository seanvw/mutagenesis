# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A two-page static web demo illustrating insertional mutagenesis saturation:

- `index.html` — interactive simulation. Random insertions accumulate across a 30-gene window drawn from a chosen species' gene-size distribution; any insertion landing in a gene body knocks it out.
- `explainer.html` — A-level-style derivation of the expected curve `1 − (1 − p)ⁿ` and why the observed KO curve follows it.

No build system, no dependencies, no tests. Pages use inline vanilla JS (no external scripts) and a single shared stylesheet (`shared.css`).

## Running

Most pages work opened directly (`open index.html`). `checkpoints.html` needs HTTP because it `fetch()`es `commits.json` — run `./serve.sh` (binds 127.0.0.1:8000) for that one.

## Architecture

### Stylesheets

`shared.css` holds everything common across pages: the core palette (`--bg`, `--panel`, `--ink`, `--muted`, `--accent`, `--good`), the `* { box-sizing }` reset, base `html, body`, the `.nav` block, and the `.panel` background/border/radius. Page-specific styles — including extra palette vars (`--gene`, `--nc`, `--insert`, `--hit`, `--extreme-hi`, etc.) and per-page `.panel` padding — live in each file's inline `<style>`. Pages link `shared.css` *before* their inline `<style>`, so inline rules and var declarations win on conflict. Colours are used semantically (e.g. `--gene` = protein-coding, `--nc` = non-coding, `--gene-ko`/`--nc-ko` = knocked out).

### `index.html` simulation model

The whole app lives inside a single IIFE at the bottom. Data flow:

1. **`PRESETS`** — per-species parameters (log-normal medians/sigmas for protein-coding and non-coding gene sizes, `ncFraction`, `genicFraction`, descriptive `note`). Adding a species = add an entry here + an entry in `SPECIES_COLORS` + an `<option>` in the `#preset` select.
2. **`buildGenes()`** — draws 30 gene sizes (log-normal via Box–Muller `randn()`), interleaves PC/NC kinds, then back-computes `DNA_LENGTH` from the preset's `genicFraction` so the rendered window reflects realistic gene density. Intergenic gaps are distributed log-normally across 31 slots.
3. **`step()`** — picks a uniform random bp, binary-searches the gene array (sorted by `start`) to detect hits, flips `knocked` + updates `koPC`/`koNC`, and appends to `state.timeline`.
4. **`redrawChart()`** — plots four lines: observed PC/NC (from `state.timeline`) and expected PC/NC curves computed as `1 − (1 − sᵢ/L)ⁿ` averaged over each class's gene sizes. The x-axis auto-grows via `chartMaxX`.
5. **`scheduleNext()`** — at speeds above ~60/s, batches multiple `step()` calls per animation frame rather than shrinking the `setTimeout` delay (avoids burning CPU on sub-16ms timers).

The DNA and chart SVGs are rebuilt from scratch on `reset()` (`renderDNABase()` / `renderChartBase()`) but insertions and KO state mutations update the existing SVG nodes in place via `setGeneKO()` and `drawInsertion()` — don't rebuild on every `step()`.

### `explainer.html`

Static prose explainer with small inline interactive widgets illustrating the same `1 − (1 − p)ⁿ` formula. It is linked from `index.html`'s subtitle, so if you rename or move it, update that link too.
