// sk05 scene 2 (v0 4.30 - 7.95): "E-Mudhra do lower circuits mein 36% gir gaya". Vox desk style, every mark on its word.
import React from "react";
import { AbsoluteFill } from "remotion";
import { Camera, Defs, Fonts, Overlay, SceneClock, wt } from "../lib/core";
import { Arrow, PaperClip, Print, Scribble, TapeLabel, Highlighter } from "../lib/marks";
import { Desk, TickerCard } from "../lib/widgets";

export const V0 = 4.30;

export const Chart: React.FC = () => {
  const tEm = wt("E-Mudhra", 4.4), tDo = wt("दो", 4.98), tLower = wt("lower"), tCirc = wt("circuits"), tPct = wt("36%", 6.26), tGir = wt("गिर", 6.96);
  // the chart print: 640 x 380 centred (360, 720); the screenshot crop is 1250 x 715 shown at 608 px wide
  const px = 340, py = 625, pw = 600, ph = 355, k = 568 / 1250, ox = px - pw / 2 + 16, oy = py - ph / 2 + 16;
  const at = (cx: number, cy: number): [number, number] => [ox + cx * k, oy + cy * k];
  const c1 = at(196, 215), c2 = at(668, 560);
  return (
    <SceneClock v0={V0}>
      <AbsoluteFill style={{ background: "#c9b79a" }}>
        <Defs /><Fonts />
        <Camera anchor={[340, 512]} keys={[{ t: 4.3, z: 1.0, cx: 340, cy: 512 }, { t: tLower - 0.2, z: 1.0, cx: 340, cy: 512 }, { t: tLower + 0.3, z: 1.15, cx: 320, cy: 512 }, { t: tPct - 0.1, z: 1.15, cx: 320, cy: 512 }, { t: tPct + 0.5, z: 1.04, cx: 340, cy: 512 }]}>
          <Desk src="img/desk1.png" />
          <TickerCard x={340} y={305} k={0.8} tIn={tEm} tA={tLower} tB={tCirc} tPct={tPct} tGir={tGir} />
          <TapeLabel x={104} y={192} w={84} h={34} rot={-38} t0={tEm + 0.05} text="" />
          <Print src="img/chart5d.png" x={px} y={py} w={pw} h={ph} rot={-1.5} t0={tDo} clip fit="fill" />
          <Scribble cx={c1[0]} cy={c1[1]} rx={48} ry={76} t0={tLower} color="#6a5acd" seed={3} />
          <TapeLabel x={c1[0] + 125} y={c1[1] - 35} w={160} h={60} rot={-4} t0={tLower + 0.12} text="−20%" size={38} seed={4} />
          <Scribble cx={c2[0]} cy={c2[1]} rx={54} ry={68} t0={tCirc} color="#6a5acd" seed={5} />
          <TapeLabel x={c2[0] + 80} y={c2[1] + 88} w={160} h={60} rot={3} t0={tCirc + 0.12} text="−20%" size={38} seed={6} />
        </Camera>
        <Overlay />
      </AbsoluteFill>
    </SceneClock>
  );
};
