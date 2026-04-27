# Insertional Mutagenesis Simulation

An interactive visualisation of how random insertional mutagenesis saturates a genome. Random insertions accumulate across a 30-gene window drawn from a chosen species' gene-size distribution; any insertion landing inside a gene body knocks it out.

## Pages

- **`index.html`** — the interactive simulation. Pick a species preset (*C. ruddii*, *E. coli*, *S. cerevisiae*, *A. thaliana*, *H. sapiens*, *P. japonica*, or a synthetic toy), press **Start**, and watch protein-coding and non-coding knockout curves rise against their theoretical expectations.
- **`explainer.html`** — a short derivation of why the expected curve follows `1 − (1 − p)ⁿ`, aimed at A-level / introductory-undergraduate readers.
- **`biology.html`** — the underlying biology and a cross-species table of gene density spanning roughly four orders of magnitude.
- **`checkpoints.html`** — a build-time snapshot of the project's commit history.
- **`about.html`** — short blurb and author link.

Pages share a single linked stylesheet (`shared.css`) for palette and chrome; everything else (controls, charts, prose, tables) is inline vanilla CSS + JS, no external scripts.

## Running

No build, no dependencies. Most pages work opened directly:

```sh
open index.html
```

`checkpoints.html` `fetch()`es `commits.json`, which browsers block under `file://`. For that page (or to test the whole site over HTTP), run:

```sh
./serve.sh        # python3 -m http.server on 127.0.0.1:8000
```

To refresh the commit history shown on the Checkpoints page, run `./build-commits.py` after committing.

## What the simulation shows

Each species preset sets the log-normal distributions for protein-coding and non-coding gene sizes, the proportion of genes that are non-coding, and the overall genic fraction of the genome. Gene bodies are drawn and laid out so the rendered window reflects realistic gene density — *E. coli* packs operons back-to-back, while the human preset spaces huge gene bodies across a much larger window.

The chart plots four lines as insertions accumulate:

- Observed knockout proportion (protein-coding and non-coding).
- Expected knockout proportion (protein-coding and non-coding), computed per gene as `1 − (1 − sᵢ/L)ⁿ` and averaged across the class.

The observed curves should track the expected curves closely; divergence is just sampling noise in a 30-gene window.

## Controls

- **Start / Pause / Step +1 / Reset** — standard simulation controls.
- **Speed** — insertions per second (1–500). Above ~60/s the simulation batches multiple insertions per animation frame.
- **Stop at** — halt automatically after *N* insertions (0 = no limit).

## License

No explicit license — all rights reserved by default. If you'd like to use this, open an issue.
