// sk05 v8: cert + pass as ONE composition with a CURVE CUT (Chris Moran, "cutting the curve"): the padlock is the baton.
// It rides a single heavy ease-in-out move from the left (end of the certificate scene) to the right (start of the password scene).
// The cut (tc) sits at the PEAK of its velocity: what leaves (key, tag, seal) and what arrives is hidden under the motion blur of the baton.
// Same speed and same position on both sides of the cut: the baton is parented to one curve, not two.
import React from "react";
import { C, Gate, clamp, easeBack, easeOut, prog, useV, wt } from "../lib/core";
import { BrowserWin, Crack, Cutout, LogoTag, Scribble, Seal } from "../lib/marks";
import { Desk, SignIn, Stage, Track } from "../lib/widgets";

export const CERTPASS = [15.75, 30.05] as const;
const P0: [number, number] = [185, 545], P1: [number, number] = [470, 520];
const TC = 23.60, HALF = 0.40;                                  // the cut and half the transit (the whole move is 0.8 s)
const inOut = (u: number) => (u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2);   // a heavy cubic ease: the speed peaks at u = 0.5
const dInOut = (u: number) => (u < 0.5 ? 12 * u * u : 12 * (1 - u) * (1 - u));                  // its derivative (1 = the average speed, 3 at the peak)

const DeskJump: React.FC = () => {                                // the desk framing changes at the cut, hidden by the baton's blur
  const v = useV(); return <Desk src="img/desk1.png" dx={v < TC ? 0 : -14} dy={v < TC ? 0 : 30} />;
};

const Baton: React.FC<{ tIn: number; tOut: number }> = ({ tIn, tOut }) => {
  const v = useV(); if (v < tIn) return null;
  const u = clamp((v - (TC - HALF)) / (2 * HALF)); const e = inOut(u);
  const px = P0[0] + (P1[0] - P0[0]) * e, py = P0[1] + (P1[1] - P0[1]) * e;
  const speed = (Math.hypot(P1[0] - P0[0], P1[1] - P0[1]) * dInOut(u)) / (2 * HALF);        // px per second
  const blur = u > 0 && u < 1 ? (speed / 30) * 0.28 : 0;                                      // px of standard deviation along the move
  const ang = Math.atan2(P1[1] - P0[1], P1[0] - P0[0]); const sx = Math.abs(Math.cos(ang)) * blur + 0.01, sy = Math.abs(Math.sin(ang)) * blur + 0.01;
  const lean = 7 * Math.sin(Math.PI * e);
  return (
    <>
      {blur > 0.3 && <svg width="0" height="0" style={{ position: "absolute" }}><filter id="batonBlur" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation={`${sx.toFixed(2)} ${sy.toFixed(2)}`} /></filter></svg>}
      <div style={{ position: "absolute", left: 0, top: 0, transform: `translate(${px}px, ${py}px) rotate(${lean}deg)`, filter: blur > 0.3 ? "url(#batonBlur)" : "none" }}>
        <Cutout src="img/v/padlock.png" x={0} y={0} w={300} rot={-2 - e} t0={tIn} tOut={tOut} />
      </div>
    </>
  );
};

export const CertPass: React.FC = () => {
  const tWeb = wt("website", 16.44), tReal = wt("असली", 17.04), tCert = wt("certificate", 18.38), tDeti = wt("देती"), tAnd = wt("और", 19.84), tPad = wt("certificate", 20.0), tCtl = wt("control"), tSirf = wt("सिर्फ", 21.86), tComp = wt("company", 22.18);
  const tLock = wt("security", 24.22), tWeak = wt("कमजोर"), tPw = wt("password", 28.0), tEk = wt("एक", 28.72), tDo = wt("दो", 28.9), tTeen = wt("तीन", 29.18), tClick = wt("हो", 29.44);
  const tExit = wt("चाहिए", 23.2) - 0.1;                          // what the baton leaves behind sweeps away on "chahiye", before the baton starts to move
  return (
    <Stage v0={CERTPASS[0]} desk="" cam={[
      { t: CERTPASS[0], z: 1, cx: 340, cy: 512 }, { t: tReal, z: 1, cx: 340, cy: 512 }, { t: tReal + 0.55, z: 2.1, cx: 262, cy: 250 }, { t: tCert + 0.25, z: 2.1, cx: 262, cy: 250 }, { t: tCert + 0.7, z: 1, cx: 340, cy: 512 },
      { t: tPw, z: 1, cx: 340, cy: 512 }, { t: tPw + 0.65, z: 1.5, cx: 340, cy: 560 }]}>
      <DeskJump />
      {/* ---- the certificate half */}
      <BrowserWin x={340} y={400} w={520} rot={-1.5} t0={tWeb} okAt={tCert} lock="bad" tOut={tAnd - 0.05} />
      <Gate a={tDeti} b={tAnd - 0.05}><Seal x={440} y={470} d={140} t0={tDeti + 0.04} rot={-8} /></Gate>
      <Track keys={[
        { t: CERTPASS[0], x: 0, y: 0 }, { t: tExit, x: 0, y: 0 }, { t: tExit + 0.38, x: 330, y: -520, rot: 24, a: 1 }, { t: tExit + 0.40, x: 330, y: -520, rot: 24, a: 0 }]}>
        <Track keys={[
          { t: tCtl, x: 640, y: 200, rot: -30, s: 1.1, a: 0 }, { t: tCtl + 0.2, x: 560, y: 290, rot: -35, s: 1.1, a: 1 }, { t: tSirf, x: 330, y: 470, rot: -70, s: 1.05 }, { t: tSirf + 0.5, x: P0[0], y: P0[1] - 11, rot: -90, s: 1.0 }]}>
          <Cutout src="img/v/key.png" x={0} y={0} w={240} rot={0} t0={tCtl - 0.1} pop={false} rim={4} />
        </Track>
        <LogoTag x={480} y={330} w={210} t0={tSirf + 0.3} rot={10} />
        <Scribble cx={480} cy={330} rx={130} ry={56} t0={tComp} dur={0.4} color="#6a5acd" width={7} seed={31} />
      </Track>
      {/* ---- the baton: one curve across the cut */}
      <Baton tIn={tPad} tOut={tPw} />
      {/* ---- the password half */}
      <Scribble cx={P1[0] + 5} cy={P1[1]} rx={190} ry={240} t0={tLock + 0.05} dur={0.6} color="#e6dc2a" width={30} seed={9} rot={2.2} loops={0.85} />
      <Crack x={P1[0] + 12} y={P1[1] - 50} len={230} t0={tWeak} angle={86} seed={4} width={8} />
      <SignIn x={340} y={515} w={440} tIn={tPw} tType={[tEk, tDo, tTeen]} tClick={tClick} />
      <Scribble cx={222} cy={580} rx={72} ry={34} t0={tTeen + 0.08} dur={0.4} color="#6a5acd" width={7} seed={12} />
    </Stage>
  );
};
