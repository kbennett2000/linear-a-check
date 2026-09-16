// Cycle 3, Part C, step 1.
//
// Load Strong's Hebrew dictionary with Node's own require() -- the file ends in
// module.exports, so it is a plain CommonJS module -- and write it out as JSON
// for the Python steps.  No regular expressions are used to read it.
//
//   node scripts/18_dump_hebrew.js
//
// in:  data/raw/strongs-hebrew-dictionary.js
// out: data/derived/strongs_hebrew.json

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const root = path.resolve(__dirname, '..');
const src = path.join(root, 'data', 'raw', 'strongs-hebrew-dictionary.js');
const out = path.join(root, 'data', 'derived', 'strongs_hebrew.json');

const bytes = fs.readFileSync(src);
console.log('file:   data/raw/strongs-hebrew-dictionary.js');
console.log('bytes:  ' + bytes.length);
console.log('sha256: ' + crypto.createHash('sha256').update(bytes).digest('hex'));

const dict = require(src);
const keys = Object.keys(dict);
console.log('entries: ' + keys.length);
console.log('fields on the first entry: ' + Object.keys(dict[keys[0]]).join(', '));

fs.writeFileSync(out, JSON.stringify(dict, null, 1), 'utf8');
console.log('wrote data/derived/strongs_hebrew.json');
