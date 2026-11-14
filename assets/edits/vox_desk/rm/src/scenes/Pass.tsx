// sk05 scene 5 (v0 23.60 - 30.05): "...security itni kamzor nikli ki jaise aapka password ek, do, teen ho!"
import React from "react";
import { AbsoluteFill } from "remotion";
import { Camera, Defs, Fonts, Overlay, SceneClock, wt } from "../lib/core";
import { Crack, Cutout, Scribble } from "../lib/marks";
import { Desk, SignIn } from "../lib/widgets";

export const V0 = 23.60;

export const Pass: React.FC = () => {
  const tLock = wt("security", 24.22), tWeak = wt("कमजोर"), tPw = wt("password", 28.0), tEk = wt("एक", 28.72), tDo = wt("दो", 28.9), tTeen = wt("तीन", 29.18), tClick = wt("हो", 29.44);
  return (
    <SceneClock v0={V0}>
      <AbsoluteFill style={{ background: "#c9b79a" }}>
        <Defs /><Fonts />
        <Camera anchor={[340, 512]} keys={[{ t: 23.6, z: 1.0, cx: 340, cy: 512 }, { t: tPw, z: 1.0, cx: 340, cy: 512 }, { t: tPw + 0.65, z: 1.5, cx: 340, cy: 560 }]}>
          <Desk src="img/desk1.png" dx={-14} dy={30} />
          <Scribble cx={345} cy={520} rx={195} ry={245} t0={tLock + 0.05} dur={0.6} color="#e6dc2a" width={30} seed={9} rot={2.2} loops={0.85} />
          <Cutout src="img/v/padlock.png" x={340} y={520} w={300} rot={-3} t0={tLock} tOut={tPw} />
          <Crack x={352} y={470} len={230} t0={tWeak} angle={86} seed={4} width={8} />
          <SignIn x={340} y={515} w={440} tIn={tPw} tType={[tEk, tDo, tTeen]} tClick={tClick} />
          <Scribble cx={222} cy={580} rx={72} ry={34} t0={tTeen + 0.08} dur={0.4} color="#6a5acd" width={7} seed={12} />
        </Camera>
        <Overlay />
      </AbsoluteFill>
    </SceneClock>
  );
};
