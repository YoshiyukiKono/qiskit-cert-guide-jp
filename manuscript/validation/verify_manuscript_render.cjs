// Syntax and table-structure checks; this does not perform visual layout review.
// Reuses the pinned dependencies in references/html-pdf/package.json.
// Run from any directory: node manuscript/validation/verify_manuscript_render.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {createRequire} = require('node:module');

const root = path.resolve(__dirname, '../..');
const req = createRequire(path.join(root, 'references/html-pdf/package.json'));
const MarkdownIt = req('markdown-it');
const texmath = req('markdown-it-texmath');
const katex = req('katex');
let formulas = 0;
const engine = {
    renderToString(source, options) {
        formulas++;
        return katex.renderToString(source, {...options, throwOnError: true, strict: 'error'});
    },
};
const md = new MarkdownIt({html: true}).use(texmath, {engine, delimiters: 'dollars'});

for (const name of ['01-quantum-operations.md', '02-visualization-measurement.md', '06-estimator.md']) {
    const source = fs.readFileSync(path.join(root, 'manuscript/ja', name), 'utf8');
    const lines = source.split(/\r?\n/);
    const tokens = md.parse(source, {});
    const tables = tokens.filter(token => token.type === 'table_open');
    for (const table of tables) {
        const rows = lines.slice(...table.map);
        // A raw ket bar in a table is a Markdown column delimiter. Use \lvert instead.
        const cells = row => row.trim().replace(/^\|/, '').replace(/\|$/, '').split(/(?<!\\)\|/).length;
        const width = cells(rows[1]);
        for (const [offset, row] of rows.entries()) {
            assert.equal(cells(row), width, `${name}:${table.map[0] + offset + 1}: table column mismatch`);
        }
    }
    assert.equal((source.match(/^\$\$\r?$/gm) || []).length % 2, 0, `${name}: display math delimiters`);
    assert.equal((source.match(/^```[^\r\n]*\r?$/gm) || []).length % 2, 0, `${name}: code fences`);
    const before = formulas;
    const html = md.renderer.render(tokens, md.options, {});
    assert(!/katex-error|class="texmath"/.test(html), `${name}: math rendering error`);
    console.log(`PASS ${name}: ${formulas - before} formulas, ${tables.length} tables`);
}
console.log(`PASS total: ${formulas} rendered formulas`);
