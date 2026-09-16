// Load LinearAInscriptions.js in a real JS runtime (Node's vm module) and dump
// its Maps to JSON. No regex parsing of the source.
// Note: objects built inside the vm context belong to that context's realm, so
// the Map->object conversion is done inside the context too.
const fs = require('fs');
const vm = require('vm');

const SRC = 'data/raw/LinearAInscriptions.js';
const OUT_DIR = 'data/derived';

const code = fs.readFileSync(SRC, 'utf8');
const sandbox = {};
vm.createContext(sandbox);
vm.runInContext(code, sandbox, { filename: SRC });

const names = ['inscriptions', 'lexicon', 'sequences', 'wordsInCorpus', 'ligatures'];
const summary = {};
for (const n of names) {
  const isMap = vm.runInContext(`typeof ${n} !== 'undefined' && ${n} instanceof Map`, sandbox);
  if (!isMap) { summary[n] = 'MISSING or not a Map'; continue; }
  summary[n] = vm.runInContext(`${n}.size`, sandbox);
  const json = vm.runInContext(
    `JSON.stringify(Object.fromEntries(${n}.entries()), null, 1)`, sandbox);
  fs.writeFileSync(`${OUT_DIR}/${n}.json`, json);
}
fs.writeFileSync(`${OUT_DIR}/map_sizes.json`, JSON.stringify(summary, null, 2));
console.log(JSON.stringify(summary, null, 2));
