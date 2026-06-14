import puppeteer from 'puppeteer';
const SD = '/Users/Uni/Downloads';
async function main() {
    const browser = await puppeteer.launch({ headless: true });
    let p1 = await browser.newPage();
    await p1.setViewport({ width: 1440, height: 900 });
    await p1.goto('http://localhost:8080/', { waitUntil: 'domcontentloaded', timeout: 30000 });
    await p1.screenshot({ path: `${SD}/landing-desktop.png`, fullPage: true });
    console.log('Desktop done');
    let p2 = await browser.newPage();
    await p2.setViewport({ width: 375, height: 812 });
    await p2.goto('http://localhost:8080/', { waitUntil: 'domcontentloaded', timeout: 30000 });
    await p2.screenshot({ path: `${SD}/landing-mobile.png`, fullPage: true });
    console.log('Mobile done');
    let p3 = await browser.newPage();
    await p3.setViewport({ width: 768, height: 1024 });
    await p3.goto('http://localhost:8080/', { waitUntil: 'domcontentloaded', timeout: 30000 });
    await p3.screenshot({ path: `${SD}/landing-tablet.png`, fullPage: true });
    console.log('Tablet done');
    await browser.close();
}
main().catch(console.error);
