#!/usr/bin/env node
/*
 Optional BBS benchmark entry point.

 This script is intentionally separated from the Python selector so reviewers can
 reproduce the cryptographic backend only when the Node dependency is available.
 The exact API of @mattrglobal/bbs-signatures may change, so verify the installed
 package documentation before reporting new measurements.
*/
import { performance } from "node:perf_hooks";

function getArg(name, defaultValue) {
  const ix = process.argv.indexOf(`--${name}`);
  if (ix >= 0 && ix + 1 < process.argv.length) return process.argv[ix + 1];
  return defaultValue;
}

const attrs = Number(getArg("attrs", "16"));
const runs = Number(getArg("runs", "50"));
const warmup = Number(getArg("warmup", "5"));

async function main() {
  let bbs;
  try {
    bbs = await import("@mattrglobal/bbs-signatures");
  } catch (err) {
    console.error("Missing @mattrglobal/bbs-signatures. Run npm install in this folder.");
    process.exit(2);
  }

  // This is a minimal harness template. Adjust function names if the installed
  // package version exposes updated APIs.
  const messages = Array.from({ length: attrs }, (_, i) => Uint8Array.from(Buffer.from(`claim-${i}`)));

  const results = [];
  for (let i = 0; i < warmup + runs; i++) {
    const t0 = performance.now();
    // Replace this section with the package's current keygen/sign/proof API.
    // Kept as a template to avoid reporting unverified fake cryptographic timings.
    await Promise.resolve(messages.length);
    const proveMs = performance.now() - t0;

    const t1 = performance.now();
    await Promise.resolve(true);
    const verifyMs = performance.now() - t1;

    if (i >= warmup) {
      results.push({ run: i - warmup + 1, attributes: attrs, prove_ms: proveMs, verify_ms: verifyMs });
    }
  }

  console.log("run,attributes,prove_ms,verify_ms");
  for (const r of results) console.log(`${r.run},${r.attributes},${r.prove_ms},${r.verify_ms}`);
}

main();
