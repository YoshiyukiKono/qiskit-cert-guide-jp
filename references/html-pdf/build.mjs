import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";

import katex from "katex";
import MarkdownIt from "markdown-it";
import texmath from "markdown-it-texmath";
import { chromium } from "playwright-core";

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const REFERENCES_DIR = resolve(SCRIPT_DIR, "..");
const REPOSITORY_ROOT = resolve(REFERENCES_DIR, "..");
const SOURCE = join(REFERENCES_DIR, "qiskit-pocket-reference.md");
const OUTPUT = join(REFERENCES_DIR, "qiskit-pocket-reference-html.pdf");
const STYLESHEET = join(SCRIPT_DIR, "pocket-reference.css");
const require = createRequire(import.meta.url);
const KATEX_STYLESHEET = require.resolve("katex/dist/katex.min.css");

function commandPath(command) {
  const locator = process.platform === "win32" ? "where.exe" : "which";
  const result = spawnSync(locator, [command], { encoding: "utf8" });
  if (result.status !== 0) return null;
  return result.stdout.split(/\r?\n/).map((line) => line.trim()).find(Boolean) ?? null;
}

function browserFromArguments() {
  const index = process.argv.indexOf("--browser");
  if (index >= 0) {
    const supplied = process.argv[index + 1];
    if (!supplied) throw new Error("--browser requires an executable path.");
    return resolve(supplied);
  }
  const inline = process.argv.find((argument) => argument.startsWith("--browser="));
  return inline ? resolve(inline.slice("--browser=".length)) : null;
}

function findBrowser() {
  const explicit = browserFromArguments() || process.env.POCKET_REFERENCE_BROWSER;
  const candidates = [
    explicit,
    process.platform === "win32" ? "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" : null,
    process.platform === "win32" ? "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe" : null,
    process.platform === "win32" ? "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" : null,
    process.platform === "win32" ? "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe" : null,
    process.platform === "darwin" ? "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" : null,
    process.platform === "darwin" ? "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" : null,
    commandPath("google-chrome"),
    commandPath("chromium"),
    commandPath("chromium-browser"),
    commandPath("microsoft-edge"),
  ].filter(Boolean);

  const browser = candidates.find((candidate) => existsSync(candidate));
  if (!browser) {
    throw new Error(
      "Chrome or Edge was not found. Pass its executable path with --browser or POCKET_REFERENCE_BROWSER.",
    );
  }
  return browser;
}

function renderMarkdown(markdown) {
  const pageBreaks = markdown.replace(
    /<!--\s*pagebreak\s*-->/gi,
    '<div class="page-break" aria-hidden="true"></div>',
  );
  const parser = new MarkdownIt({ html: true, linkify: true, typographer: false }).use(texmath, {
    engine: katex,
    delimiters: "dollars",
    katexOptions: {
      output: "htmlAndMathml",
      strict: "warn",
      throwOnError: true,
      trust: false,
    },
  });
  return parser.render(pageBreaks);
}

function documentHtml(content) {
  const css = readFileSync(STYLESHEET, "utf8");
  const baseUrl = pathToFileURL(`${REFERENCES_DIR}/`).href;
  const katexCssUrl = pathToFileURL(KATEX_STYLESHEET).href;
  return `<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="author" content="qiskit-cert-guide-jp">
  <title>Qiskit v2.x ポケットリファレンス - HTML版</title>
  <base href="${baseUrl}">
  <link rel="stylesheet" href="${katexCssUrl}">
  <style>${css}</style>
</head>
<body>
  <main class="pocket-reference">${content}</main>
</body>
</html>`;
}

const footerTemplate = `
<div style="box-sizing:border-box;width:100%;margin:0 10mm;padding-top:1.2mm;border-top:0.35pt solid #c8d0dd;color:#526078;font-family:'BIZ UDPGothic','Noto Sans JP','Meiryo',sans-serif;font-size:6.5pt;display:flex;justify-content:space-between;">
  <span>Qiskit 2.5.2 / Runtime 0.49.0</span>
  <span class="pageNumber"></span>
</div>`;

async function build() {
  if (!existsSync(SOURCE)) throw new Error(`Markdown source was not found: ${SOURCE}`);
  const browserExecutable = findBrowser();
  const scratchRoot = join(REPOSITORY_ROOT, "tmp", "pdfs");
  mkdirSync(scratchRoot, { recursive: true });
  const scratch = mkdtempSync(join(scratchRoot, "pocket-reference-html-"));
  const htmlPath = join(scratch, "qiskit-pocket-reference.html");
  let browser;

  try {
    const markdown = readFileSync(SOURCE, "utf8");
    writeFileSync(htmlPath, documentHtml(renderMarkdown(markdown)), "utf8");
    browser = await chromium.launch({
      executablePath: browserExecutable,
      headless: true,
      args: ["--allow-file-access-from-files", "--disable-extensions", "--no-first-run"],
    });
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "networkidle" });
    await page.evaluate(() => document.fonts.ready.then(() => true));
    const katexErrors = await page.$$eval(".katex-error", (elements) =>
      elements.map((element) => element.textContent || "unknown KaTeX error"),
    );
    if (katexErrors.length) {
      throw new Error(`KaTeX rendering failed:\n${katexErrors.join("\n")}`);
    }
    await page.evaluate(() => {
      for (const container of document.querySelectorAll(".katex-display")) {
        const math = container.querySelector(":scope > .katex");
        if (!math) continue;
        const containerStyle = getComputedStyle(container);
        const availableWidth =
          container.clientWidth -
          Number.parseFloat(containerStyle.paddingLeft) -
          Number.parseFloat(containerStyle.paddingRight);
        const renderedWidth = math.getBoundingClientRect().width;
        if (renderedWidth > availableWidth) {
          const fontSize = Number.parseFloat(getComputedStyle(math).fontSize);
          math.style.fontSize = `${fontSize * (availableWidth / renderedWidth) * 0.98}px`;
        }
      }
    });
    await page.emulateMedia({ media: "print" });
    await page.pdf({
      path: OUTPUT,
      printBackground: true,
      preferCSSPageSize: true,
      displayHeaderFooter: true,
      headerTemplate: "<div></div>",
      footerTemplate,
      tagged: true,
      outline: true,
    });
    console.log(`Created ${OUTPUT}`);
  } finally {
    if (browser) await browser.close();
    rmSync(scratch, { recursive: true, force: true });
    try {
      rmSync(scratchRoot, { recursive: false });
      rmSync(dirname(scratchRoot), { recursive: false });
    } catch {
      // Preserve other temporary files when the directories are not empty.
    }
  }
}

await build();
