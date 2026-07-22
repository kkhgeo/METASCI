# PDF Export

Onto decks ship as **HTML plus a PDF export**. The HTML is the authoring artifact; the PDF
is what gets emailed, attached to a report, or handed to a committee. Build both.

The fixed 1920×1080 canvas makes this nearly free — the same coordinate system that scales
to the viewport also maps directly to a PDF page.

## Print CSS

Add this to every Onto deck. It is the whole mechanism.

```css
@page{
  size: 1920px 1080px;
  margin: 0;
}

@media print{
  html,
  body{
    width: var(--fixed-slide-w);
    height: auto;
    overflow: visible;
    background: #fff;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  body::before,
  .slide-counter{ display: none; }

  .slide{
    position: relative;
    left: auto;
    top: auto;
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
    transform: none;
    page-break-after: always;
    break-after: page;
  }
  .slide:last-of-type{
    page-break-after: auto;
    break-after: auto;
  }
}
```

What each part does:

- `@page{size: 1920px 1080px; margin: 0}` makes the PDF page exactly one slide, edge to edge.
- Undoing `position:fixed` → `relative` and `transform:none` is the critical step. On screen
  every slide is stacked at the same fixed position and scaled; for print they must flow
  down the document so each lands on its own page.
- `opacity`/`visibility`/`pointer-events` resets defeat the `.slide.active` visibility rule,
  so **all** slides print, not just the active one.
- `print-color-adjust: exact` preserves dark slides and accent fills. Without it browsers
  drop backgrounds and the cover, contents, and closing slides print white.
- Hiding `.slide-counter` and `body::before` removes screen-only chrome.
- The `:last-of-type` rule prevents a trailing blank page.

## Exporting

Chrome/Edge headless produces the cleanest output:

```bash
chrome --headless --disable-gpu \
  --print-to-pdf="Deck.pdf" \
  --no-pdf-header-footer \
  "file:///absolute/path/to/Deck.html"
```

Or print from the browser: Ctrl+P, destination "Save as PDF", margins **None**, and
"Background graphics" **on**.

Wait for webfonts before printing. `font-display: swap` means a headless run can rasterize
Paperlogy as the fallback face if it prints too early. If Korean text renders in the wrong
face, add a delay or preload the fonts.

## Verify

Check the PDF, not just the HTML:

- Page count equals slide count. A count that is double usually means a `.slide` is
  overflowing 1080px and spilling onto a second page.
- Page size is 16:9 and uniform across every page. A PDF stores this in points, so
  `@page{size: 1920px 1080px}` shows up as a MediaBox of `0 0 1440 810` — that is the
  correct result, not a scaling error (1920 px × 72/96 = 1440 pt). Any other ratio, or a
  MediaBox that varies page to page, means `@page` did not apply.
- Fonts embedded in the PDF are all intended ones. A system Korean face (Gulim, Batang,
  Dotum, Malgun) in the list means some stack is missing its Korean fallback — see
  `onto-tokens.md`. Latin webfaces that are silently absent mean the deck fell back; decide
  whether to fix the load or drop the dependency.
- Dark slides are still dark. White backgrounds mean `print-color-adjust` was dropped or
  "Background graphics" was off.
- Korean text is Paperlogy, not a fallback.
- No slide counter, no navigation chrome.
- Video posters appear on slides that use video. Video elements themselves do not print —
  give any `<video>` a `poster` so the printed page is not blank.

## Naming

Keep the export beside the HTML with a matching name and the aspect ratio in it, e.g.
`Deck.html` → `Deck_merged_16x9.pdf`. Report both paths in the final response.

If the deck also needs a lighter file for email, export a second reduced PDF rather than
degrading the primary one, and say which is which.
