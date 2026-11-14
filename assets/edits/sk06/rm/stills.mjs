// render a list of frames of SK06 to ../check/st_<frame>.png with one bundle: node stills.mjs 198 400 ...
import { bundle } from "@remotion/bundler";
import { renderStill, selectComposition } from "@remotion/renderer";
import path from "node:path";
const serveUrl = await bundle({ entryPoint: path.resolve("src/index.ts") });
const comp = await selectComposition({ serveUrl, id: "SK06", browserExecutable: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" });
for (const a of process.argv.slice(2)) {
  const frame = Math.round(parseFloat(a) * 30);
  await renderStill({ serveUrl, composition: comp, frame, output: path.resolve(`../check/st_${a}.png`), browserExecutable: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" });
  console.log("still", a);
}
