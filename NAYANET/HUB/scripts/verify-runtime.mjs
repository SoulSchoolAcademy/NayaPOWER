import { chromium } from 'playwright';

const runtime = (process.env.NAYA_RUNTIME_URL || 'https://sparkling-shape-7ae5.smartnetpodcast.workers.dev').replace(/\/$/, '');
const forbidden = [
  'Collective',
  'Evidence',
  'Smart Mail New',
  'Source',
  'Understand',
  'Act',
  'Verify',
  'Learn',
  'Providence',
  'Truth',
  'Protection',
  'Source Separated',
  'What',
  'Human',
  'Simple',
  'Simplified',
  'Why',
  'Notice',
];
const boards = [
  'What Is Naya Power?',
  'What Is Naya?',
  'What Are Smart Notes?',
  'Your Intelligence Today',
  'Intelligence Reports',
  'What Is the Intelligent Library?',
  'Smart Lists',
  'Smart Spaces',
  'Smart Mail',
];
const sidebar = [
  'Your Intelligence Today',
  'Your Report',
  'Intelligent Library',
  'Smart Share',
  'Smart Ledger',
  'Your Connections',
  'Smart Lists',
  'Smart Spaces',
  'Smart Mail',
  'Settings',
];
const layers = [
  'In a Nutshell',
  'Human Note',
  'Child Note',
  'Grandma Note',
  'Naya Note',
  'Machine Note',
  'Learning Lesson',
  'What It Means',
  'How to Use',
  'What’s In It For You',
];
const viewports = [
  ['desktop', { width: 1440, height: 900 }],
  ['tablet', { width: 1024, height: 900 }],
  ['mobile', { width: 390, height: 844 }],
];

function fail(message) {
  console.error(`RUNTIME_ACCEPTANCE_FAIL: ${message}`);
  process.exitCode = 1;
}

async function requireVisibleExact(page, text, context) {
  const locator = page.getByText(text, { exact: true });
  if ((await locator.count()) === 0 || !(await locator.first().isVisible())) {
    fail(`${context}: missing visible exact text "${text}"`);
  }
}

async function requireForbiddenAbsent(page, text, context) {
  const locator = page.getByText(text, { exact: true });
  if ((await locator.count()) > 0) {
    const visible = await locator.evaluateAll((nodes) => nodes.some((node) => {
      const style = getComputedStyle(node);
      const rect = node.getBoundingClientRect();
      return style.visibility !== 'hidden' && style.display !== 'none' && rect.width > 0 && rect.height > 0;
    }));
    if (visible) fail(`${context}: forbidden legacy text visible: "${text}"`);
  }
}

const browser = await chromium.launch({ headless: true });
try {
  for (const [name, viewport] of viewports) {
    const page = await browser.newPage({ viewport });
    const response = await page.goto(runtime, { waitUntil: 'networkidle', timeout: 30000 });
    if (!response || !response.ok()) fail(`${name}: root HTTP response was not successful`);
    await page.waitForTimeout(250);

    for (const title of boards) await requireVisibleExact(page, title, name);
    for (const label of sidebar) await requireVisibleExact(page, label, name);
    for (const label of layers) await requireVisibleExact(page, label, name);
    for (const label of forbidden) await requireForbiddenAbsent(page, label, name);
    for (const label of ['Create Space', 'Favorite', 'Save']) await requireVisibleExact(page, label, name);

    const boardCount = await page.locator('[data-smart-board]').count();
    if (boardCount !== 9) fail(`${name}: expected 9 Smart Boards, found ${boardCount}`);

    const boardLayerCounts = await page.locator('[data-smart-board]').evaluateAll((boards) =>
      boards.map((board) => board.querySelectorAll('[data-smart-layer]').length)
    );
    if (boardLayerCounts.some((count) => count !== 10)) {
      fail(`${name}: every Smart Board must contain exactly 10 layers; got ${boardLayerCounts.join(',')}`);
    }

    const overflow = await page.evaluate(() => ({
      width: document.documentElement.scrollWidth,
      viewport: window.innerWidth,
    }));
    if (overflow.width > overflow.viewport + 2) fail(`${name}: horizontal overflow ${overflow.width} > ${overflow.viewport}`);

    console.log(`RUNTIME_ACCEPTANCE_PASS: ${name} ${viewport.width}x${viewport.height}`);
    await page.close();
  }
} finally {
  await browser.close();
}

if (process.exitCode !== 1) console.log(`RUNTIME_ACCEPTANCE_PASS: ${runtime}`);
