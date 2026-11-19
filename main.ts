// news-image-20261119 entrypoint: copy the pre-rendered front page to the
// grader's output dir. COPY pattern only — no subprocess, no network, no
// drawing at run time, so both runs write byte-identical output.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const out = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
if (!existsSync(src)) throw new Error("entry.png missing");
mkdirSync(out, { recursive: true });
copyFileSync(src, join(out, "entry.png"));
