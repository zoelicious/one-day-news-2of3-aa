// Entry: one-page newspaper for Saturday 21 November 2026 (1024x1024).
// The image is rendered by generate.py in this repo; main.ts only copies it
// to the grader output dir, resolved absolutely from this file's location.
import { copyFileSync } from "node:fs";
import { join } from "node:path";

const entry = new URL("./entry.png", import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(entry, join(outDir, "entry.png"));
console.log("entry.png copied to", join(outDir, "entry.png"));
