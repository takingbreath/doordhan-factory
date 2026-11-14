// Core helpers for the sk05 Vox-style scenes: voice-time clock, word anchors, easing, camera, texture overlay, SVG filters.
import React, { createContext, useContext } from "react";
import { AbsoluteFill, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import wordsJson from "../../public/data/words_scribe.json";

export const WORDS = wordsJson as unknown as [number, number, string][];

/** voice time (s) at which a spoken word starts: the occurrence nearest `near`, or the nth one */
export function wt(text: string, near?: number, nth = 0): number {
  const hits = WORDS.filter((w) => w[2].replace(/[,.?!।]/g, "").toLowerCase() === text.toLowerCase()).map((w) => w[0]);
  if (!hits.length) throw new Error("word not found: " + text);
  if (near !== undefined) return hits.reduce((a, b) => (Math.abs(b - near) < Math.abs(a - near) ? b : a));
  return hits[nth];
}

export const C = {
  paper: "#e9e9e4", ink: "#1e1e23", purple: "#6a5acd", yellow: "#ece23c", tape: "#e9df3b", red: "#c8202a", green: "#2fa872", cream: "#f1ebdc", kraft: "#c9a877",
};
export const FONT = { marker: "SK5Marker", serif: "SK5Playfair", bungee: "SK5Bungee", baloo: "SK5Baloo", ui: "Helvetica Neue, Helvetica, Arial, sans-serif" };

export const Fonts: React.FC = () => (
  <style>{`
  @font-face{font-family:${FONT.marker};src:url(${staticFile("fonts/PermanentMarker-Regular.ttf")})}
  @font-face{font-family:${FONT.serif};font-weight:900;src:url(${staticFile("fonts/PlayfairDisplay-Black.ttf")})}
  @font-face{font-family:${FONT.serif};font-weight:700;src:url(${staticFile("fonts/PlayfairDisplay-Bold.ttf")})}
  @font-face{font-family:${FONT.bungee};src:url(${staticFile("fonts/Bungee.ttf")})}
  @font-face{font-family:${FONT.baloo};font-weight:800;src:url(${staticFile("fonts/Baloo2-Latin-ExtraBold.ttf")})}
  `}</style>
);

// ---- easing and progress
export const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const prog = (v: number, t0: number, dur: number) => clamp((v - t0) / dur);
export const easeOut = (x: number) => 1 - Math.pow(1 - clamp(x), 3);
export const easeInOut = (x: number) => { x = clamp(x); return x * x * (3 - 2 * x); };
export const easeBack = (x: number, s = 1.6) => { x = clamp(x); return 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2); };
export function rng(seed: number) { let s = (seed * 9301 + 49297) % 233280 || 1; return () => { s = (s * 16807) % 2147483647; return s / 2147483647; }; }

// ---- the scene clock: v = voice time = v0 + frame / fps
const Clock = createContext<number>(0);
export const useV = () => { const f = useCurrentFrame(); const { fps } = useVideoConfig(); return useContext(Clock) + f / fps; };
export const SceneClock: React.FC<{ v0: number; children: React.ReactNode }> = ({ v0, children }) => <Clock.Provider value={v0}>{children}</Clock.Provider>;

// ---- camera: keyframes in voice time, zoom z about the scene point (cx, cy)
export type CamKey = { t: number; z: number; cx: number; cy: number };
export const Camera: React.FC<{ keys: CamKey[]; children: React.ReactNode; anchor?: [number, number] }> = ({ keys, children, anchor }) => {
  const v = useV(); const { width: W, height: H } = useVideoConfig();
  let k = keys[0];
  let z = k.z, cx = k.cx, cy = k.cy;
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i], b = keys[i + 1];
    if (v >= a.t && v <= b.t) { const e = easeInOut((v - a.t) / (b.t - a.t)); z = a.z + (b.z - a.z) * e; cx = a.cx + (b.cx - a.cx) * e; cy = a.cy + (b.cy - a.cy) * e; }
    else if (v > b.t) { z = b.z; cx = b.cx; cy = b.cy; }
  }
  return <AbsoluteFill style={{ transform: `translate(${(anchor?.[0] ?? W / 2) - cx * z}px, ${(anchor?.[1] ?? H / 2) - cy * z}px) scale(${z})`, transformOrigin: "0 0" }}>{children}</AbsoluteFill>;
};

// ---- SVG filters: a rough hand-drawn stroke, chalky speckle, scissor-cut edge, soft misregistration
export const Defs: React.FC = () => (
  <svg width="0" height="0" style={{ position: "absolute" }}>
    <defs>
      <filter id="rough" x="-10%" y="-10%" width="120%" height="120%">
        <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="3" result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale="5" />
      </filter>
      <filter id="chalk" x="-10%" y="-10%" width="120%" height="120%">
        <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="3" seed="7" result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale="6" result="d" />
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="2" result="g" />
        <feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.5 1.62" result="holes" />
        <feComposite in="d" in2="holes" operator="in" />
      </filter>
      <filter id="scissor" x="-5%" y="-5%" width="110%" height="110%">
        <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="11" result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale="7" />
      </filter>
      <filter id="fringe" x="0" y="0" width="100%" height="100%">
        <feColorMatrix in="SourceGraphic" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="r" />
        <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 1 0" result="cb" />
        <feOffset in="r" dx="1.2" dy="0" result="ro" />
        <feOffset in="cb" dx="-1.2" dy="0" result="cbo" />
        <feBlend in="ro" in2="cbo" mode="screen" />
      </filter>
    </defs>
  </svg>
);

// ---- global texture: paper fibres + grain flicker (multiply), a fine halftone, a vignette
const NOISE = `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='320' height='320'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.42  0 0 0 0 0.38  0 0 0 0 0.33  0 0 0 0.55 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")`;
const FIBRE = `url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='600' height='600'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='0.012 0.5' numOctaves='3' seed='4'/><feColorMatrix values='0 0 0 0 0.5  0 0 0 0 0.45  0 0 0 0 0.4  0 0 0 0.35 0'/></filter><rect width='100%' height='100%' filter='url(%23f)'/></svg>")`;
export const Overlay: React.FC<{ halftone?: number; grain?: number; vignette?: number }> = ({ halftone = 0.16, grain = 0.5, vignette = 0.5 }) => {
  const f = useCurrentFrame();
  return (
    <>
      <AbsoluteFill style={{ backgroundImage: FIBRE, mixBlendMode: "multiply", opacity: 0.55, pointerEvents: "none" }} />
      <AbsoluteFill style={{ backgroundImage: NOISE, backgroundPosition: `${(f * 47) % 320}px ${(f * 91) % 320}px`, mixBlendMode: "multiply", opacity: grain, pointerEvents: "none" }} />
      <AbsoluteFill style={{ backgroundImage: "radial-gradient(circle at 50% 50%, rgba(20,20,20,0.9) 0.8px, transparent 1.25px)", backgroundSize: "4.2px 4.2px", mixBlendMode: "multiply", opacity: halftone, pointerEvents: "none" }} />
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 48%, rgba(0,0,0,0) 55%, rgba(30,24,16,${vignette}) 130%)`, pointerEvents: "none" }} />
    </>
  );
};

/** shows its children only between voice times a and b (b optional), with a short fade at both ends */
export const Gate: React.FC<{ a: number; b?: number; children: React.ReactNode }> = ({ a, b, children }) => {
  const v = useV(); if (v < a || (b !== undefined && v > b + 0.3)) return null;
  const o = b === undefined ? 1 : 1 - clamp((v - b) / 0.3);
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};
