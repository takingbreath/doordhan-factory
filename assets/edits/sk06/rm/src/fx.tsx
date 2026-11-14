// sk06 edit helpers: reel clock, easing, whip / zoom-through transitions with directional motion blur, punch-ins,
// logo cards, kinetic words, captions, the chart scene with marks drawn on their words, the bug and the disclaimer.
import React from "react";
import { AbsoluteFill, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export const FPS = 30;
export const F = (s: number) => Math.round(s * FPS);
export const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const easeIn3 = (x: number) => Math.pow(clamp(x), 3);
export const easeOut3 = (x: number) => 1 - Math.pow(1 - clamp(x), 3);
export const smooth = (x: number) => { x = clamp(x); return x * x * (3 - 2 * x); };
export const back = (x: number, s = 1.7) => { x = clamp(x); return 1 + (s + 1) * Math.pow(x - 1, 3) + s * Math.pow(x - 1, 2); };
/** reel time (s) inside a <Sequence from={F(t0)}> */
export const useT = (t0: number) => t0 + useCurrentFrame() / useVideoConfig().fps;

export const FONTS: React.FC = () => (
  <style>{`
  @font-face{font-family:Anton;src:url(${staticFile("fonts/Anton-Regular.ttf")})}
  @font-face{font-family:Caveat;src:url(${staticFile("fonts/Caveat.ttf")})}
  @font-face{font-family:Playfair;font-weight:700;src:url(${staticFile("fonts/PlayfairDisplay-Bold.ttf")})}
  @font-face{font-family:Playfair;font-weight:900;src:url(${staticFile("fonts/PlayfairDisplay-Black.ttf")})}
  `}</style>
);

// ---------------------------------------------------------------- transitions
export const HW = 0.2;            // seconds on each side of a whip cut
export const WD = 700;            // whip travel in px
export type Dir = "left" | "right" | "up" | "down" | "zoom" | "none";

/** offset (px) and blur (px) of a layer at time t for a whip OUT ending at `cut` or a whip IN starting at `cut` */
export function whip(t: number, cut: number, dir: Dir, phase: "out" | "in") {
  if (dir === "none") return { dx: 0, dy: 0, blur: 0, z: 1, o: 1 };
  let u: number, d: number, v: number;
  if (phase === "out") { u = clamp((t - (cut - HW)) / HW); d = easeIn3(u); v = 3 * u * u; }
  else { u = clamp((t - cut) / HW); d = easeOut3(u) - 1; v = 3 * (1 - u) * (1 - u); }
  if (dir === "zoom") {
    // zoom-through: the old shot rushes toward the lens, the new one settles from 1.6x
    const z = phase === "out" ? 1 + 1.6 * d : 1 - 0.6 * d;
    return { dx: 0, dy: 0, blur: v * 9, z, o: 1 };
  }
  const s = dir === "left" || dir === "up" ? -1 : 1;
  const amt = phase === "out" ? d * WD * s : d * WD * s;   // in: d runs -1..0, so the new shot comes from the opposite side
  const horiz = dir === "left" || dir === "right";
  return { dx: horiz ? amt : 0, dy: horiz ? 0 : amt, blur: v * 26, z: 1, o: 1 };
}

let FID = 0;
/** a layer moved by a whip: three mirrored copies so no edge shows, blurred along the move */
export const Moving: React.FC<{ dx: number; dy: number; blur: number; z?: number; children: (mirror: string) => React.ReactNode }> = ({ dx, dy, blur, z = 1, children }) => {
  const still = dx === 0 && dy === 0 && blur < 0.05 && z === 1;
  if (still) return <AbsoluteFill>{children("")}</AbsoluteFill>;
  const id = "mb" + (FID++ % 100000);
  const horiz = Math.abs(dx) > 0 || (dy === 0 && z === 1);
  const sd = z !== 1 ? `${blur} ${blur}` : horiz ? `${blur} 0` : `0 ${blur}`;
  const copies = z !== 1 ? [[0, 0, ""]] : horiz ? [[-720, 0, "scaleX(-1)"], [0, 0, ""], [720, 0, "scaleX(-1)"]] : [[0, -1280, "scaleY(-1)"], [0, 0, ""], [0, 1280, "scaleY(-1)"]];
  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      <svg width="0" height="0" style={{ position: "absolute" }}><defs><filter id={id} x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation={sd} /></filter></defs></svg>
      <AbsoluteFill style={{ transform: `translate(${dx}px, ${dy}px) scale(${z})`, filter: blur > 0.05 ? `url(#${id})` : undefined }}>
        {copies.map(([x, y, m], i) => (
          <AbsoluteFill key={i} style={{ transform: `translate(${x}px, ${y}px)` }}>
            <AbsoluteFill style={{ transform: m as string }}>{children(m as string)}</AbsoluteFill>
          </AbsoluteFill>
        ))}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- pictures
export type Punch = { t: number; s: number; cx?: number; cy?: number };
/** scale at time t from a list of punch-ins (instant, with a 3-frame settle from 4 % over) */
export function punchAt(t: number, punches: Punch[] = []) {
  let s = 1, cx = 0.5, cy = 0.475;
  for (const p of punches) if (t >= p.t) { const k = clamp((t - p.t) / 0.1); s = p.s * (1 + 0.04 * (1 - easeOut3(k))); cx = p.cx ?? 0.5; cy = p.cy ?? 0.475; }
  return { s, cx, cy };
}

export const Clip: React.FC<{ src: string; c0: number; rate?: number; s?: number; cx?: number; cy?: number; filter?: string; opacity?: number; mask?: string }> = ({ src, c0, rate = 1, s = 1, cx = 0.5, cy = 0.475, filter, opacity, mask }) => (
  <AbsoluteFill style={{ transform: `scale(${s})`, transformOrigin: `${cx * 100}% ${cy * 100}%`, filter, opacity, WebkitMaskImage: mask, maskImage: mask }}>
    <OffthreadVideo src={staticFile("v/" + src)} trimBefore={Math.max(0, Math.round(c0 * FPS))} playbackRate={rate} muted
      style={{ width: 720, height: 1280, objectFit: "cover" }} />
  </AbsoluteFill>
);

/** a still photo, slow push (Ken Burns), with a film-ish grade so it sits with the bus footage */
export const Photo: React.FC<{ src: string; t: number; t0: number; t1: number; z0?: number; z1?: number; fx?: number; fy?: number; fit?: "cover" | "contain"; bg?: string }> = ({ src, t, t0, t1, z0 = 1.04, z1 = 1.14, fx = 0.5, fy = 0.45, fit = "cover", bg = "#111" }) => {
  const u = smooth((t - t0) / Math.max(0.1, t1 - t0)); const z = z0 + (z1 - z0) * u;
  return (
    <AbsoluteFill style={{ background: bg, overflow: "hidden" }}>
      {fit === "contain" && <Img src={staticFile(src)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", filter: "blur(28px) brightness(0.55) saturate(0.9)", transform: "scale(1.2)" }} />}
      <Img src={staticFile(src)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: fit, transform: `scale(${z})`, transformOrigin: `${fx * 100}% ${fy * 100}%`, filter: "contrast(1.04) saturate(0.88) sepia(0.10)" }} />
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0) 55%, rgba(0,0,0,0.68) 100%)" }} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- type
export const YEL = "#F5D90A";
/** v4 (2026-11-14): the cover's design language for all type: Doordhan lime box, ink text, ink outline, hard ink
 *  shadow, a slight tilt (docs/covers.md). LIME/INK are the cover's colours. */
export const LIME = "#C1FE06";
export const INK = "#0C1E14";

/** the official logo on a white card with an ink frame and a hard ink shadow, slammed in on its word (never over a face) */
export const LogoCard: React.FC<{ src: string; t: number; t0: number; t1?: number; x?: number; y?: number; w?: number; h?: number }> = ({ src, t, t0, t1, x = 360, y = 300, w = 470, h = 170 }) => {
  if (t < t0 || (t1 !== undefined && t > t1 + 0.15)) return null;
  const k = back(clamp((t - t0) / 0.2)); const o = t1 !== undefined && t > t1 ? 1 - (t - t1) / 0.15 : 1;
  const blur = (1 - clamp((t - t0) / 0.1)) * 6;
  return (
    <div style={{ position: "absolute", left: x - w / 2, top: y - h / 2, width: w, height: h, background: "#fff", borderRadius: 8,
      border: `6px solid ${INK}`, boxShadow: `12px 12px 0 ${INK}, 0 16px 36px rgba(0,0,0,0.35)`, boxSizing: "border-box",
      transform: `scale(${0.55 + 0.45 * k}) rotate(${-2 + (1 - k) * -4}deg)`, opacity: clamp(o) * clamp((t - t0) / 0.06),
      filter: `blur(${blur}px)`, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <Img src={staticFile(src)} style={{ maxWidth: w - 64, maxHeight: h - 52, objectFit: "contain" }} />
    </div>
  );
};

/** the kicker: white Anton caps with a thick ink outline (the cover's "SPACE & CHIPS") */
const kickerStyle = (size: number): React.CSSProperties => ({ fontFamily: "Anton", fontSize: size, lineHeight: 1.05, color: "#fff",
  letterSpacing: 1, WebkitTextStroke: `${Math.max(6, size * 0.16)}px ${INK}`, paintOrder: "stroke fill", textShadow: "0 5px 14px rgba(0,0,0,0.5)" });

/** a word slammed in the lime box (the cover's "AGLA BOOM?"), with an optional kicker word above it */
export const BigWord: React.FC<{ text: string; small?: string; t: number; t0: number; t1: number; y: number; size: number; color?: string; tilt?: number }> = ({ text, small, t, t0, t1, y, size, tilt = -3 }) => {
  if (t < t0 || t > t1 + 0.12) return null;
  const k = easeOut3(clamp((t - t0) / 0.12)); const o = t > t1 ? 1 - (t - t1) / 0.12 : 1;
  const bw = Math.max(5, Math.round(size * 0.045)), sh = Math.round(size * 0.09);
  return (
    <div style={{ position: "absolute", left: 0, width: 720, top: y - size * 0.62 - (small ? size * 0.5 : 0), display: "flex", flexDirection: "column",
      alignItems: "center", gap: size * 0.08, opacity: clamp(o) }}>
      {small && <div style={{ ...kickerStyle(size * 0.42), textTransform: "uppercase", opacity: clamp((t - t0 - 0.04) / 0.12) }}>{small}</div>}
      <div style={{ fontFamily: "Anton", fontSize: size, lineHeight: 1.04, color: INK, background: LIME, letterSpacing: 1,
        padding: `${size * 0.05}px ${size * 0.17}px ${size * 0.02}px`, border: `${bw}px solid ${INK}`,
        boxShadow: `${sh}px ${sh}px 0 ${INK}, 0 18px 40px rgba(0,0,0,0.4)`,
        transform: `rotate(${tilt}deg) scale(${1.25 - 0.25 * k}) translateY(${(1 - k) * 20}px)`, filter: `blur(${(1 - k) * 8}px)` }}>{text}</div>
    </div>
  );
};

/** captions: white Anton caps with a thick ink outline; the key word ("hi") in a lime box; "pill" = an ink box behind
 *  the line for busy or white backgrounds (charts, logo cards) */
export type Cap = { t0: number; t1: number; text: string; y?: number; pill?: boolean; hi?: string };
export const Captions: React.FC<{ t: number; caps: Cap[] }> = ({ t, caps }) => {
  const c = caps.find((c) => t >= c.t0 && t < c.t1);
  if (!c) return null;
  const k = easeOut3(clamp((t - c.t0) / 0.1));
  const text = c.text.toUpperCase(), hi = c.hi?.toUpperCase();
  let parts: [string, boolean][] = [[text, false]];
  if (hi && text.includes(hi)) { const i = text.indexOf(hi); parts = [[text.slice(0, i), false], [hi, true], [text.slice(i + hi.length), false]]; }
  const hk = easeOut3(clamp((t - c.t0 - 0.05) / 0.14));
  return (
    <div style={{ position: "absolute", left: 50, width: 620, top: (c.y ?? 960) - 44, textAlign: "center", opacity: k, transform: `translateY(${(1 - k) * 8}px)` }}>
      <span style={{ fontFamily: "Anton", fontSize: 42, lineHeight: 1.42, letterSpacing: 0.6, color: "#fff",
        ...(c.pill ? { background: "rgba(12,30,20,0.92)", padding: "4px 14px", borderRadius: 4 } : { WebkitTextStroke: `9px ${INK}`, paintOrder: "stroke fill", textShadow: "0 4px 12px rgba(0,0,0,0.55)" }),
        boxDecorationBreak: "clone", WebkitBoxDecorationBreak: "clone" }}>
        {parts.map(([s, h], i) => h
          ? <span key={i} style={{ display: "inline-block", background: LIME, color: INK, WebkitTextStroke: "0px transparent", textShadow: "none",
              padding: "0 9px", margin: "0 3px", border: `3px solid ${INK}`, boxShadow: `5px 5px 0 ${INK}`, lineHeight: 1.12,
              transform: `rotate(-2deg) scale(${1.15 - 0.15 * hk})` }}>{s}</span>
          : <React.Fragment key={i}>{s}</React.Fragment>)}
      </span>
    </div>
  );
};

export const Bug: React.FC = () => (
  <div style={{ position: "absolute", right: 20, top: 30, fontFamily: "Anton", fontSize: 26, letterSpacing: 2, color: "#fff", textShadow: "0 2px 6px rgba(0,0,0,0.7)", opacity: 0.92 }}>DOORDHAN</div>
);

export const Disclaimer: React.FC<{ t: number; t0: number; t1: number }> = ({ t, t0, t1 }) => {
  if (t < t0) return null;
  const o = clamp((t - t0) / 0.35) * (1 - clamp((t - (t1 - 0.3)) / 0.3));
  return (
    <div style={{ position: "absolute", left: 50, width: 620, top: 905, opacity: o, textAlign: "center" }}>
      <div style={{ display: "inline-block", background: "rgba(10,10,14,0.78)", borderRadius: 14, padding: "16px 22px",
        fontFamily: "Helvetica Neue, Helvetica, Arial, sans-serif", fontWeight: 600, fontSize: 25, lineHeight: 1.35, color: "#fff" }}>
        Investments in securities market are subject to market risks. Read all the related documents carefully before investing.
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- charts
export type ChartDef = { img: string; w: number; h: number; marks?: any };
/** a TradingView screen fitted to the frame height on a white page; children are SVG marks in screenshot pixels */
export const ChartView: React.FC<{ def: ChartDef; z?: number; cx?: number; cy?: number; children?: React.ReactNode }> = ({ def, z = 1, cx, cy, children }) => {
  // v3: the TradingView screen fills the WIDTH on a white page (the silver01 look); the camera zooms about (cx, cy)
  const k = 720 / def.w; const w = 720, h = def.h * k, oy = (1280 - h) / 2;
  const px = cx ?? def.w / 2, py = cy ?? def.h / 2;
  const sx = px * k, sy = oy + py * k; const tx = 360 - sx * z, ty = 640 - sy * z;
  const fx = z === 1 && cx === undefined ? 0 : tx, fy = z === 1 && cy === undefined ? 0 : ty;
  return (
    <AbsoluteFill style={{ background: "#fff", overflow: "hidden" }}>
      <AbsoluteFill style={{ transform: `translate(${fx}px, ${fy}px) scale(${z})`, transformOrigin: "0 0" }}>
        <div style={{ position: "absolute", left: 0, top: oy, width: w, height: h }}>
          <Img src={staticFile(def.img)} style={{ width: w, height: h }} />
          <svg viewBox={`0 0 ${def.w} ${def.h}`} style={{ position: "absolute", left: 0, top: 0, width: w, height: h, overflow: "visible" }}>{children}</svg>
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

/** camera keys {t, z, cx, cy} (screenshot px) eased between */
export function cam(t: number, keys: { t: number; z: number; cx: number; cy: number }[]) {
  let { z, cx, cy } = keys[0];
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i], b = keys[i + 1];
    if (t >= a.t && t <= b.t) { const e = smooth((t - a.t) / (b.t - a.t)); z = a.z + (b.z - a.z) * e; cx = a.cx + (b.cx - a.cx) * e; cy = a.cy + (b.cy - a.cy) * e; }
    else if (t > b.t) ({ z, cx, cy } = b);
  }
  return { z, cx, cy };
}

/** a dashed line drawn left to right from t0 over dur */
export const DrawLine: React.FC<{ t: number; t0: number; x1: number; x2: number; y1: number; y2?: number; color: string; w?: number; dash?: string; dur?: number }> = ({ t, t0, x1, x2, y1, y2, color, w = 5, dash = "14 9", dur = 0.35 }) => {
  if (t < t0) return null;
  const u = easeOut3((t - t0) / dur); const yy2 = y2 ?? y1;
  const ex = x1 + (x2 - x1) * u, ey = y1 + (yy2 - y1) * u;
  return (
    <g>
      <line x1={x1} y1={y1} x2={ex} y2={ey} stroke="#111" strokeWidth={w + 4} strokeDasharray={dash} strokeLinecap="butt" />
      <line x1={x1} y1={y1} x2={ex} y2={ey} stroke={color} strokeWidth={w} strokeDasharray={dash} strokeLinecap="butt" />
    </g>
  );
};

/** a chart label (v5, Akhilesh 2026-11-14: "on charts keep the text simple so that it is readable"): small, plain bold
 *  sans in the line's colour with a thin white halo, no box; it pops in on its word and can fade out (t1) */
export const Label: React.FC<{ t: number; t0: number; t1?: number; x: number; y: number; text: string; size?: number; anchor?: "start" | "middle" | "end"; color?: string }> = ({ t, t0, t1, x, y, text, size = 21, anchor = "start", color = INK }) => {
  if (t < t0 || (t1 !== undefined && t > t1 + 0.2)) return null;
  const k = easeOut3(clamp((t - t0) / 0.18)); const fade = t1 !== undefined ? 1 - clamp((t - t1) / 0.2) : 1;
  return (
    <g transform={`translate(${x} ${y - (1 - k) * 6})`} opacity={k * fade}>
      <text x={0} y={0} textAnchor={anchor} fontFamily="Helvetica Neue, Helvetica, Arial, sans-serif" fontWeight={700} fontSize={size}
        fill={color} stroke="#fff" strokeWidth={4} paintOrder="stroke" strokeLinejoin="round">{text}</text>
    </g>
  );
};

/** a company logo on a small white badge with an ink frame (the four-chart recap: which chart is which) */
export const LogoBadge: React.FC<{ src: string; x: number; y: number; w: number; h: number; t?: number; t0?: number }> = ({ src, x, y, w, h, t, t0 }) => {
  const k = t !== undefined && t0 !== undefined ? back(clamp((t - t0) / 0.18)) : 1;
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, height: h, background: "#fff", borderRadius: 8, border: `3px solid ${INK}`,
      boxShadow: `5px 5px 0 ${INK}`, boxSizing: "border-box", display: "flex", alignItems: "center", justifyContent: "center",
      transform: `scale(${0.7 + 0.3 * k})`, transformOrigin: "left top", opacity: clamp(k * 3) }}>
      <Img src={staticFile(src)} style={{ maxWidth: w - 26, maxHeight: h - 18, objectFit: "contain" }} />
    </div>
  );
};

/** a thick arrow drawn from (x1, y1) to (x2, y2) */
export const DrawArrow: React.FC<{ t: number; t0: number; x1: number; y1: number; x2: number; y2: number; color?: string; dur?: number; w?: number }> = ({ t, t0, x1, y1, x2, y2, color = LIME, dur = 0.45, w = 9 }) => {
  if (t < t0) return null;
  const u = easeOut3((t - t0) / dur); const ex = x1 + (x2 - x1) * u, ey = y1 + (y2 - y1) * u;
  const a = Math.atan2(ey - y1, ex - x1), L = 26;
  const head = `${ex},${ey} ${ex - L * Math.cos(a - 0.45)},${ey - L * Math.sin(a - 0.45)} ${ex - L * Math.cos(a + 0.45)},${ey - L * Math.sin(a + 0.45)}`;
  return (
    <g>
      <line x1={x1} y1={y1} x2={ex} y2={ey} stroke={INK} strokeWidth={w + 6} strokeLinecap="round" />
      <line x1={x1} y1={y1} x2={ex} y2={ey} stroke={color} strokeWidth={w} strokeLinecap="round" />
      {u > 0.6 && <polygon points={head} fill={color} stroke="#111" strokeWidth={3} strokeLinejoin="round" />}
    </g>
  );
};

/** a box that grows from its left edge */
export const DrawBox: React.FC<{ t: number; t0: number; x1: number; x2: number; y1: number; y2: number; dur?: number }> = ({ t, t0, x1, x2, y1, y2, dur = 0.45 }) => {
  if (t < t0) return null;
  const u = easeOut3((t - t0) / dur); const w = (x2 - x1) * u;
  return (
    <g>
      <rect x={x1} y={y1} width={w} height={y2 - y1} fill="rgba(193,254,6,0.20)" />
      <rect x={x1} y={y1} width={w} height={y2 - y1} fill="none" stroke="#111" strokeWidth={4} strokeDasharray="12 8" />
    </g>
  );
};

// ---------------------------------------------------------------- fast cuts (sk06 v2: "cut like a pro editor")
/** one B-roll item: a still or a video clip. kind "v": src under public/, c0 = clip seconds to start from, rate = speed */
export type Item = { t: number; src: string; kind?: "i" | "v"; c0?: number; rate?: number; fx?: number; fy?: number; dim?: number };
/** a montage that cuts on words: every cut lands with an impact zoom (1.12 -> 1 in 0.16 s), a 2-frame flash and a tiny
 *  alternating tilt, and each shot keeps creeping in so nothing sits still */
export const Montage: React.FC<{ t: number; a: number; items: Item[]; b: number; flash?: boolean }> = ({ t, a, items, b, flash = true }) => {
  let i = 0; for (let k = 0; k < items.length; k++) if (t >= items[k].t) i = k;
  const it = items[i]; const t1 = i + 1 < items.length ? items[i + 1].t : b; const age = t - it.t;
  const hit = easeOut3(clamp(age / 0.16)); const z = (1.12 - 0.12 * hit) * (1 + 0.05 * smooth(age / Math.max(0.3, t1 - it.t)));
  const tilt = (i % 2 ? 1 : -1) * 0.7 * (1 - hit);
  const fl = flash && i > 0 ? Math.max(0, 0.55 - age / 0.07 * 0.55) : 0;
  const fx = it.fx ?? 0.5, fy = it.fy ?? 0.5;
  return (
    <AbsoluteFill style={{ background: "#0b0b0d", overflow: "hidden" }}>
      <AbsoluteFill style={{ transform: `scale(${z}) rotate(${tilt}deg)`, transformOrigin: `${fx * 100}% ${fy * 100}%` }}>
        {it.kind === "v"
          ? <Sequence key={i} from={Math.round((it.t - a) * FPS)} layout="none">
              <OffthreadVideo src={staticFile(it.src)} trimBefore={Math.round((it.c0 ?? 0) * FPS)} playbackRate={it.rate ?? 1} muted
                style={{ width: 720, height: 1280, objectFit: "cover", objectPosition: `${fx * 100}% ${fy * 100}%`, filter: "contrast(1.05) saturate(0.9) sepia(0.08)" }} />
            </Sequence>
          : <Img src={staticFile(it.src)} style={{ width: 720, height: 1280, objectFit: "cover", objectPosition: `${fx * 100}% ${fy * 100}%`, filter: "contrast(1.05) saturate(0.88) sepia(0.10)" }} />}
      </AbsoluteFill>
      {it.dim ? <AbsoluteFill style={{ background: `rgba(0,0,0,${it.dim})` }} /> : null}
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0) 55%, rgba(0,0,0,0.68) 100%)" }} />
      {fl > 0 && <AbsoluteFill style={{ background: `rgba(255,250,235,${fl})` }} />}
    </AbsoluteFill>
  );
};

/** a camera shake that decays (for slams and the brakes) */
export function shake(t: number, t0: number, dur = 0.35, amp = 12) {
  if (t < t0 || t > t0 + dur) return { x: 0, y: 0, r: 0 };
  const u = (t - t0) / dur, a = Math.pow(1 - u, 2) * amp;
  return { x: Math.sin(t * 91) * a, y: Math.cos(t * 73) * a * 0.8, r: Math.sin(t * 57) * 0.06 * a };
}

/** v4 disclaimer (Akhilesh, 2026-11-14: the whole line on one screen, a smaller font that fills the screen, in the
 *  cover's style): eight lines, each fitted to 640 px wide (sizes measured with PIL on Anton), 891 px tall in all,
 *  white with a thick ink outline; MARKET RISKS in the lime box. The lines slam in one after another, hold, and the
 *  block flies out past the camera at the end, so the last frame is clean for the loop. */
// sizes fit 590 px (x 50..640: clear of Instagram's action buttons on the right)
const DISC: [string, number, boolean][] = [
  ["INVESTMENTS IN", 100, false], ["SECURITIES MARKET", 81, false], ["ARE SUBJECT TO", 100, false], ["MARKET RISKS.", 90, true],
  ["READ ALL THE", 120, false], ["RELATED DOCUMENTS", 77, false], ["CAREFULLY BEFORE", 87, false], ["INVESTING.", 151, false],
];
export const KineticDisclaimer: React.FC<{ t: number; t0: number; t1: number }> = ({ t, t0, t1 }) => {
  if (t < t0 || t > t1) return null;
  const out = clamp((t - (t1 - 0.32)) / 0.32);
  const totalH = DISC.reduce((s, [, sz, hi]) => s + sz * 1.0 + (hi ? 26 : 0), 0); let y = 640 - totalH / 2 - 20;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <AbsoluteFill style={{ background: `rgba(12,30,20,${0.5 * (1 - out) * clamp((t - t0) / 0.2)})` }} />
      <AbsoluteFill style={{ transform: `scale(${1 + 0.9 * easeIn3(out)})`, transformOrigin: "50% 45%", opacity: 1 - out, filter: `blur(${6 * out}px)` }}>
        {DISC.map(([txt, sz, hi], i) => {
          const ti = t0 + 0.08 + i * 0.075; const k = easeOut3(clamp((t - ti) / 0.13));
          const top = y + (hi ? 13 : 0); y += sz * 1.0 + (hi ? 26 : 0);
          if (t < ti) return null;
          const common: React.CSSProperties = { fontFamily: "Anton", fontSize: sz, lineHeight: 1, letterSpacing: 0.5 };
          return <div key={i} style={{ position: "absolute", left: 0, width: 690, top, display: "flex", justifyContent: "center",
            transform: `scale(${1.3 - 0.3 * k})`, opacity: k, filter: `blur(${(1 - k) * 8}px)` }}>
            {hi
              ? <span style={{ ...common, color: INK, background: LIME, padding: "6px 22px 0", border: `5px solid ${INK}`, boxShadow: `10px 10px 0 ${INK}`, transform: "rotate(-2deg)" }}>{txt}</span>
              : <span style={{ ...common, color: "#fff", WebkitTextStroke: `${Math.round(sz * 0.12)}px ${INK}`, paintOrder: "stroke fill", textShadow: "0 6px 18px rgba(0,0,0,0.5)" }}>{txt}</span>}
          </div>;
        })}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
