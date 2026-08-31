# Wiki / Knowledge Base HTML Explainer

Use this when the user asks for an HTML explainer but explicitly wants it to feel like a wiki, glossary, handbook, docs site, or searchable knowledge base rather than a slide-like or step-by-step explainer.

## When to choose this pattern

- Source material is a long Markdown glossary, curriculum note, FAQ, handbook, or reference document.
- The user says “위키처럼”, “용어집”, “사전”, “문서 사이트”, “검색되게”, or “기존 템플릿 말고”.
- The primary action is lookup and navigation, not a linear walkthrough.

## Recommended single-file architecture

1. Parse the source Markdown into structured data:
   - `#` top-level sections become major wiki pages or category groups.
   - `##` headings become term/doc pages when the document is glossary-like.
   - Repeated field bullets (a `- <field>:` pattern consistent across terms) become explicit wiki fields.
2. Embed the structured data as JSON inside the HTML:
   - `<script id="wikiData" type="application/json">...</script>`
   - Keep rendering logic separate from the data blob.
3. Use hash routing so the file works locally without a server:
   - `#home`, `#category/<slug>`, `#term/<slug>`, `#prompts`.
4. Provide wiki affordances:
   - sticky left navigation with categories and term links
   - search box with live results and Enter-to-open-first-result
   - term detail page with field sections
   - related documents from the same category
   - optional right-side “On this page” mini TOC
   - dark/light toggle and random term button only if they help browsing
5. Keep the artifact self-contained. Avoid a build step and avoid CDN dependencies unless the interaction model truly needs React.

## Design guidance

- Do not force the default html-explainer visual/interactive templates when the user asked for a wiki. A custom single-file HTML is acceptable if verified.
- A wiki should prioritize scan speed, stable navigation, and dense but readable pages over big hero sections.
- Good visual direction for technical glossary wikis: editorial reference book, restrained dark docs, warm paper encyclopedia, or compact command-center docs.
- Avoid fake metrics, generic feature cards, and slide-deck rhythm.

## Verification

기본 확인은 `open` 후 사용자 브라우저 육안이다(SKILL.md 워크플로와 동일). 아래 체크는 사용자가 CDP 검수를 요청했을 때 수행한다.

- Open the file in a browser using `file://`.
- Verify the app shell renders: left nav, home page, category page, term detail page.
- Verify search: type a known term, check results, press Enter to open first result.
- Verify at least one direct hash route such as `#term/api`.
- Verify special pages such as prompt templates or comparison pages if present.
- Add an in-page error collector during development if browser console output is vague:

```html
<script>
window.__wikiErrors = [];
window.addEventListener('error', e => window.__wikiErrors.push({
  message: e.message,
  source: e.filename,
  line: e.lineno,
  col: e.colno
}));
window.addEventListener('unhandledrejection', e => window.__wikiErrors.push({
  message: String(e.reason),
  source: 'promise'
}));
</script>
```

Then inspect `window.__wikiErrors` after navigation and interactions.

## Common pitfalls

- Python string generation can accidentally turn JavaScript `\n` into literal line breaks inside string literals or regexes. Inspect the generated JS around `split('\n')`, `join('\n')`, and regex literals before browser verification.
- When regenerating a local file, browser automation can show a cached version. Add a query suffix such as `?v=2` or navigate fresh before judging CSS/JS fixes.
- `navigator.clipboard` may fail on `file://`. Use a fallback textarea plus `document.execCommand('copy')`, and report copy verification separately if the browser blocks clipboard access.
- Inline `code` styling can bleed into `pre code`. Add a specific rule such as `.md-content pre code { display: block; background: transparent !important; padding: 0; }`.
- Long left navs need their own scrolling area and mobile drawer behavior; otherwise the main content becomes hard to use.
