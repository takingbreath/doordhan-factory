// Scene widgets: the desk stage, a stock quote card (price, arrow and percent together), a clipped-in browser/screen print.
import React from "react";
import { AbsoluteFill, Img, staticFile, useVideoConfig } from "remotion";
import { C, FONT, easeBack, easeOut, prog, useV } from "./core";

/** the stage: a Gemini desk photo, slightly oversized so the camera can move over it */
export const Desk: React.FC<{ src: string; scale?: number; dx?: number; dy?: number }> = ({ src, scale = 1.14, dx = 0, dy = 0 }) => {
  const { width: W, height: H } = useVideoConfig();
  const w = W * scale; const h = (w * 2752) / 1536;
  return <AbsoluteFill><Img src={staticFile(src)} style={{ position: "absolute", left: (W - w) / 2 + dx, top: (H - h) / 2 + dy, width: w, height: h }} /></AbsoluteFill>;
};

const money = (n: number) => n.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

/** the quote card: price falls from 540.00 to 432.00 (starts tA), then to 345.60 (starts tB); the red change chip counts to 36.0% from tPct; the arrow bounces at tGir */
export const TickerCard: React.FC<{ x: number; y: number; w?: number; tIn: number; tA: number; tB: number; tPct: number; tGir: number; rot?: number; k?: number }> = ({ x, y, w = 620, tIn, tA, tB, tPct, tGir, rot = -1, k = 1 }) => {
  const v = useV(); if (v < tIn) return null; const p = easeBack(prog(v, tIn, 0.25), 1.3);
  let price = 540;
  if (v >= tA && v < tB) price = 540 - 108 * easeOut((v - tA) / 0.26);
  else if (v >= tB) price = 432 - 86.4 * easeOut((v - tB - 0.02) / 0.45);
  const pct = v >= tPct ? 36 * easeOut((v - tPct) / 0.55) : null;
  const bounce = v >= tGir && v < tGir + 0.3 ? Math.sin((Math.PI * (v - tGir)) / 0.3) : 0;
  const h = w * 0.5;
  return (
    <div style={{ position: "absolute", left: x - w / 2, top: y - h / 2, width: w, height: h, transform: `rotate(${rot}deg) scale(${(0.9 + 0.1 * p) * k}) translateY(${(1 - p) * -50}px)`, opacity: Math.min(1, p * 1.5), filter: "drop-shadow(7px 12px 10px rgba(30,20,8,0.45))" }}>
      <div style={{ position: "absolute", inset: 0, background: "#17181c", borderRadius: 16, filter: "url(#scissor)" }} />
      <div style={{ position: "absolute", left: 34, top: 20, color: "#f1ebdc", fontFamily: FONT.ui, fontWeight: 800, fontSize: 42, letterSpacing: 1 }}>EMUDHRA</div>
      <div style={{ position: "absolute", right: 34, top: 28, color: "#8b8d96", fontFamily: FONT.ui, fontWeight: 500, fontSize: 32 }}>NSE</div>
      <div style={{ position: "absolute", left: 30, top: 66, color: "#fff", fontFamily: FONT.ui, fontWeight: 800, fontSize: 128, letterSpacing: -2 }}>₹{money(price)}</div>
      {pct !== null && (
        <div style={{ position: "absolute", left: 34, bottom: 22, height: 82, padding: "0 28px 0 22px", background: C.red, borderRadius: 16, display: "flex", alignItems: "center", gap: 14 }}>
          <svg width="44" height="38" viewBox="0 0 44 38" style={{ transform: `translateY(${bounce * 8}px)` }}><polygon points="0,0 44,0 22,38" fill="#fff" /></svg>
          <span style={{ color: "#fff", fontFamily: FONT.ui, fontWeight: 800, fontSize: 60 }}>{pct.toFixed(1)}%</span>
        </div>
      )}
    </div>
  );
};

/** a sign-in window (crisp HTML): lock icon, user field, password field with typed digits and a caret, strength bar, button, pointer.
 *  tType = [t1, t2, t3] when each digit is typed; tClick = when the pointer clicks; it then turns green and the lock opens. */
export const SignIn: React.FC<{ x: number; y: number; w?: number; tIn: number; tType: number[]; tClick: number; tOut?: number }> = ({ x, y, w = 560, tIn, tType, tClick, tOut }) => {
  const v = useV(); if (v < tIn) return null;
  const p = easeBack(prog(v, tIn, 0.3), 1.1); const gone = tOut !== undefined ? easeOut(prog(v, tOut, 0.3)) : 0; if (gone >= 1) return null;
  const s = w / 1100; const h = 1250 * s; const n = tType.filter((t) => v >= t).length; const typed = "123".slice(0, n);
  const ok = v >= tClick + 0.1; const press = v >= tClick && !ok; const open = Math.min(1, Math.max(0, (v - tClick - 0.1) / 0.25));
  const blink = Math.floor(v * 3) % 2 === 0 || (n > 0 && v - tType[n - 1] < 0.3);
  const mp = Math.min(1, Math.max(0, (v - (tClick - 0.28)) / 0.24)); const mx = 960 + (610 - 960) * easeOut(mp), my = 1190 + (1020 - 1190) * easeOut(mp);
  const S = (n: number) => n * s;
  return (
    <div style={{ position: "absolute", left: x - w / 2 + gone * -900, top: y - h / 2, width: w, height: h, transform: `rotate(${-1.2}deg) scale(${0.9 + 0.1 * p})`, opacity: Math.min(1, p * 1.4), filter: "drop-shadow(8px 14px 14px rgba(30,20,8,0.45))" }}>
      <div style={{ position: "absolute", inset: 0, background: "#faf9f5", borderRadius: S(40), overflow: "hidden", filter: "url(#scissor)" }}>
        <div style={{ height: S(92), background: "#e4e1d8", display: "flex", alignItems: "center", paddingLeft: S(40), gap: S(22) }}>
          {["#ec6056", "#f2be46", "#60c46c"].map((c) => <div key={c} style={{ width: S(34), height: S(34), borderRadius: "50%", background: c }} />)}
        </div>
        <svg width={S(1100)} height={S(330)} viewBox="0 0 1100 330" style={{ position: "absolute", left: 0, top: S(112) }}>
          <g transform={`translate(0 ${-open * 34}) rotate(${-26 * open} 462 150)`}>
            <path d={`M470 170 V120 a46 46 0 0 1 92 0 V${170 - 26 * (1 - open)}`} fill="none" stroke="#34343a" strokeWidth="22" strokeLinecap="round" />
          </g>
          <rect x="472" y="150" width="156" height="118" rx="20" fill={ok ? "#2fa872" : "#fcc428"} /><circle cx="550" cy="196" r="15" fill="#161619" /><polygon points="542,204 558,204 563,238 537,238" fill="#161619" />
        </svg>
        <div style={{ position: "absolute", left: 0, right: 0, top: S(402), textAlign: "center", fontFamily: FONT.ui, fontWeight: 800, fontSize: S(64), color: "#28282e" }}>Sign in</div>
        <div style={{ position: "absolute", left: S(110), top: S(496), fontFamily: FONT.ui, fontSize: S(34), color: "#78766e" }}>Username</div>
        <div style={{ position: "absolute", left: S(110), right: S(110), top: S(538), height: S(96), border: `${S(4)}px solid #c4c0b4`, borderRadius: S(18), background: "#fff", fontFamily: FONT.ui, fontSize: S(50), color: "#6e6c64", paddingLeft: S(26), lineHeight: `${S(88)}px` }}>admin</div>
        <div style={{ position: "absolute", left: S(110), top: S(668), fontFamily: FONT.ui, fontSize: S(34), color: "#78766e" }}>Password</div>
        <div style={{ position: "absolute", left: S(110), right: S(110), top: S(712), height: S(140), border: `${S(6)}px solid #28387a`, borderRadius: S(20), background: "#fff", fontFamily: FONT.ui, fontWeight: 800, fontSize: S(104), color: "#18181c", paddingLeft: S(34), lineHeight: `${S(128)}px`, letterSpacing: S(6) }}>
          {typed}<span style={{ display: "inline-block", width: S(6), height: S(88), background: "#18181c", marginLeft: S(8), verticalAlign: "middle", opacity: blink && !ok ? 1 : 0 }} />
        </div>
        {n > 0 && <div style={{ position: "absolute", left: S(110), right: S(110), top: S(880), display: "flex", gap: S(12) }}>{[0, 1, 2, 3].map((i) => <div key={i} style={{ flex: 1, height: S(16), borderRadius: S(8), background: i < 1 ? C.red : "#dedacd" }} />)}</div>}
        <div style={{ position: "absolute", left: S(110), right: S(110), top: S(946 + (press ? 5 : 0)), height: S(124), borderRadius: S(24), background: ok ? "#2fa872" : press ? "#121c3e" : "#1c2856", color: "#fff", fontFamily: FONT.ui, fontWeight: 800, fontSize: S(54), textAlign: "center", lineHeight: `${S(124)}px` }}>{ok ? "Welcome" : "Sign in"}</div>
        {v >= tClick - 0.28 && (
          <svg width={S(70)} height={S(96)} viewBox="0 0 62 90" style={{ position: "absolute", left: S(mx), top: S(my), filter: "drop-shadow(3px 4px 3px rgba(0,0,0,0.4))" }}><polygon points="0,0 0,74 19,56 33,90 49,83 35,50 62,50" fill="#fff" stroke="#0a0a0c" strokeWidth="3" /></svg>
        )}
      </div>
    </div>
  );
};

/** a form on paper: the title in big type is what the narration says; a clear box for the seal */
export const Form: React.FC<{ lines: string[]; x: number; y: number; w?: number; rot?: number; t0: number }> = ({ lines, x, y, w = 300, rot = -4, t0 }) => {
  const v = useV(); if (v < t0) return null; const p = easeBack(prog(v, t0, 0.3), 1.2); const h = w * 1.3; const fs = lines.length === 1 ? w * 0.26 : w * 0.18;
  return (
    <div style={{ position: "absolute", left: x - w / 2, top: y - h / 2, width: w, height: h, transform: `rotate(${rot}deg) scale(${0.9 + 0.1 * p}) translateY(${(1 - p) * -90}px)`, opacity: Math.min(1, p * 1.5), filter: "drop-shadow(6px 11px 9px rgba(30,20,8,0.42))" }}>
      <div style={{ position: "absolute", inset: 0, background: "#f2ecdc", filter: "url(#scissor)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: h * 0.07, textAlign: "center", fontFamily: FONT.bungee, fontSize: fs, lineHeight: 1.05, color: "#1e1e23" }}>{lines.map((l, i) => <div key={i}>{l}</div>)}</div>
      {[0, 1, 2].map((i) => <div key={i} style={{ position: "absolute", left: w * 0.1, width: w * (0.8 - (i % 2) * 0.2), top: h * (0.5 + i * 0.05), height: 6, background: "#bbb5a2", borderRadius: 3 }} />)}
    </div>
  );
};

import { Camera, CamKey, Defs, Fonts, Overlay, SceneClock, easeInOut } from "./core";

/** the standard scene shell: clock, filters, fonts, desk plate under a camera, texture overlay on top */
export const Stage: React.FC<{ v0: number; cam?: CamKey[]; desk?: string; dx?: number; dy?: number; deskScale?: number; children: React.ReactNode; bg?: string; hud?: React.ReactNode }> = ({ v0, cam, desk = "img/desk1.png", dx = 0, dy = 0, deskScale = 1.14, children, bg = "#c9b79a", hud }) => {
  const { width: W, height: H } = useVideoConfig();
  const anchor: [number, number] = H > 1000 ? [340, 512] : [W / 2, H / 2];            // zoom lands on the centre of the safe box (x 40..640, y 170..855), and z = 1 at the anchor means no shift
  return (
    <SceneClock v0={v0}>
      <AbsoluteFill style={{ background: bg }}>
        <Defs /><Fonts />
        <Camera anchor={anchor} keys={cam ?? [{ t: v0, z: 1, cx: anchor[0], cy: anchor[1] }]}>
          {desk && <Desk src={desk} dx={dx} dy={dy} scale={deskScale} />}
          {children}
        </Camera>
        {hud}
        <Overlay />
      </AbsoluteFill>
    </SceneClock>
  );
};

export type TrackKey = { t: number; x: number; y: number; rot?: number; s?: number; a?: number };
/** moves its children along keyframes in voice time (smooth between them): children are positioned at (0,0) */
export const Track: React.FC<{ keys: TrackKey[]; children: React.ReactNode }> = ({ keys, children }) => {
  const v = useV(); let k = keys[0]; let x = k.x, y = k.y, r = k.rot ?? 0, s = k.s ?? 1, a = k.a ?? 1;
  for (let i = 0; i < keys.length - 1; i++) {
    const A = keys[i], B = keys[i + 1];
    if (v >= A.t && v <= B.t) { const e = easeInOut((v - A.t) / (B.t - A.t)); x = A.x + (B.x - A.x) * e; y = A.y + (B.y - A.y) * e; r = (A.rot ?? 0) + ((B.rot ?? 0) - (A.rot ?? 0)) * e; s = (A.s ?? 1) + ((B.s ?? 1) - (A.s ?? 1)) * e; a = (A.a ?? 1) + ((B.a ?? 1) - (A.a ?? 1)) * e; }
    else if (v > B.t) { x = B.x; y = B.y; r = B.rot ?? 0; s = B.s ?? 1; a = B.a ?? 1; }
  }
  if (v < keys[0].t) return null;
  return <div style={{ position: "absolute", left: 0, top: 0, transform: `translate(${x}px, ${y}px) rotate(${r}deg) scale(${s})`, opacity: a }}>{children}</div>;
};
