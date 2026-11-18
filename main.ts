// Node 22 entrypoint: publish the generated front page to the output directory.
import { mkdirSync, copyFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const destination = join(outputDir, "entry.png");

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, destination);
console.log(`Copied entry.png to ${destination}`);
