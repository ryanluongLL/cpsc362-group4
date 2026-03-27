import puppeteer from 'puppeteer';
import fs from 'fs';

(async() => {
const browser = await puppeteer.launch({
	//userDataDir: '/Users/joel/.cache/puppeteer/chrome'}); // Headless 
	//userDataDir: '/Users/joel/.cache/puppeteer/chrome', Run non-headless, for debug
	 //headless: false});
});

const page = await browser.newPage();
await page.goto(`https://www.amazon.com/dp/${process.argv[2]}`);

let whole = await page.$eval('span.a-price-whole', w => w.innerText);
	//console.log(whole);
	//fs.writeFileSync('whole', `${whole}\n`)
let wholeMod = whole.split('\n',1)
let whole2 = wholeMod[0].replaceAll(",","")
	//console.log(wholeMod[0])
	//fs.writeFileSync('whole', `${wholeMod[0]}\n`)
let fraction = await page.$eval('span.a-price-fraction', f => f.innerText);
	//fs.writeFileSync('fraction', `${fraction}\n`)
	//console.log(fraction);
//console.log(`${wholeMod[0]}.${fraction}`)
process.stdout.write(`${whole2}.${fraction}`)
//console.log(whole.innerText);
//console.log(fraction.innerText);

browser.close();

})();
