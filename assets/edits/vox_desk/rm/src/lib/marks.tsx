// Hand-made marks and paper pieces: scribble circle, arrow, underline, X, tick, highlighter swipe, tape label, photo print + paperclip, scissor-cut cutout.
import React from "react";
import { Img, staticFile, useVideoConfig } from "remotion";
import { C, FONT, easeBack, easeOut, prog, rng, useV } from "./core";

const SvgLayer: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { width, height } = useVideoConfig();
  return <svg width={width} height={height} style={{ position: "absolute", left: 0, top: 0, overflow: "visible", pointerEvents: "none" }}>{children}</svg>;
};
const draw = (p: number) => ({ pathLength: 1, strokeDasharray: "1 1", strokeDashoffset: 1 - p } as any);

/** a pen scribble around something: 1.15 turns, a little overshoot, wobbling radius; it draws itself on */
export const Scribble: React.FC<{ cx: number; cy: number; rx: number; ry: number; t0: number; dur?: number; color?: string; width?: number; seed?: number; rot?: number; loops?: number }> = ({ cx, cy, rx, ry, t0, dur = 0.5, color = C.purple, width = 7, seed = 1, rot = -0.3, loops = 1.18 }) => {
  const v = useV(); const p = easeOut(prog(v, t0, dur)); if (v < t0) return null;
  const r = rng(seed); const N = 90; const pts: string[] = [];
  for (let i = 0; i <= N * loops; i++) {
    const a = (2 * Math.PI * i) / N + rot; const k = i / (N * loops);
    const wob = 1 + 0.04 * Math.sin(a * 3 + seed) + 0.02 * Math.sin(a * 5 + seed * 2) + (r() - 0.5) * 0.012; const grow = 1 + 0.09 * k;
    pts.push(`${i === 0 ? "M" : "L"}${(cx + rx * wob * grow * Math.cos(a)).toFixed(1)} ${(cy + ry * wob * grow * Math.sin(a)).toFixed(1)}`);
  }
  return <SvgLayer><path d={pts.join(" ")} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" filter="url(#chalk)" {...draw(p)} /></SvgLayer>;
};

/** a curved hand-drawn arrow from a to b (bend = sideways pull of the curve) */
export const Arrow: React.FC<{ a: [number, number]; b: [number, number]; bend?: number; t0: number; dur?: number; color?: string; width?: number }> = ({ a, b, bend = 60, t0, dur = 0.45, color = C.green, width = 6 }) => {
  const v = useV(); if (v < t0) return null; const p = easeOut(prog(v, t0, dur));
  const mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2; const dx = b[0] - a[0], dy = b[1] - a[1]; const L = Math.hypot(dx, dy) || 1;
  const cx = mx - (dy / L) * bend, cy = my + (dx / L) * bend;
  const d = `M${a[0]} ${a[1]} Q${cx} ${cy} ${b[0]} ${b[1]}`;
  const tx = b[0] - cx, ty = b[1] - cy; const tl = Math.hypot(tx, ty) || 1; const ux = tx / tl, uy = ty / tl; const hl = 26;
  const h1 = `M${b[0] - ux * hl + uy * hl * 0.55} ${b[1] - uy * hl - ux * hl * 0.55} L${b[0]} ${b[1]} L${b[0] - ux * hl - uy * hl * 0.55} ${b[1] - uy * hl + ux * hl * 0.55}`;
  return <SvgLayer><path d={d} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" filter="url(#chalk)" {...draw(Math.min(1, p / 0.8))} />
    <path d={h1} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" filter="url(#chalk)" {...draw(Math.max(0, (p - 0.78) / 0.22))} /></SvgLayer>;
};

export const Underline: React.FC<{ x1: number; x2: number; y: number; t0: number; dur?: number; color?: string; width?: number; seed?: number; double?: boolean }> = ({ x1, x2, y, t0, dur = 0.3, color = C.purple, width = 7, seed = 2, double = true }) => {
  const v = useV(); if (v < t0) return null; const p = easeOut(prog(v, t0, dur)); const r = rng(seed);
  const d1 = `M${x1} ${y} Q${(x1 + x2) / 2} ${y + 6 + r() * 6} ${x2} ${y - 3}`; const d2 = `M${x1 + 30} ${y + 14} Q${(x1 + x2) / 2} ${y + 18} ${x2 - 20} ${y + 10}`;
  return <SvgLayer><path d={d1} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" filter="url(#chalk)" {...draw(p)} />{double && <path d={d2} fill="none" stroke={color} strokeWidth={width * 0.7} strokeLinecap="round" filter="url(#chalk)" {...draw(Math.max(0, (p - 0.4) / 0.6))} />}</SvgLayer>;
};

export const XMark: React.FC<{ cx: number; cy: number; s?: number; t0: number; color?: string; width?: number }> = ({ cx, cy, s = 60, t0, color = C.red, width = 10 }) => {
  const v = useV(); if (v < t0) return null; const p = prog(v, t0, 0.28);
  return <SvgLayer><path d={`M${cx - s} ${cy - s} L${cx + s} ${cy + s * 0.95}`} stroke={color} strokeWidth={width} strokeLinecap="round" filter="url(#chalk)" fill="none" {...draw(easeOut(p * 2))} />
    <path d={`M${cx + s} ${cy - s * 0.9} L${cx - s} ${cy + s}`} stroke={color} strokeWidth={width} strokeLinecap="round" filter="url(#chalk)" fill="none" {...draw(easeOut(Math.max(0, p * 2 - 1)))} /></SvgLayer>;
};

export const Tick: React.FC<{ cx: number; cy: number; s?: number; t0: number; color?: string; width?: number }> = ({ cx, cy, s = 50, t0, color = C.green, width = 11 }) => {
  const v = useV(); if (v < t0) return null; const p = easeOut(prog(v, t0, 0.3));
  return <SvgLayer><path d={`M${cx - s} ${cy} L${cx - s * 0.25} ${cy + s * 0.75} L${cx + s} ${cy - s * 0.85}`} stroke={color} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" filter="url(#chalk)" fill="none" {...draw(p)} /></SvgLayer>;
};

/** a felt-tip highlighter swipe: translucent yellow, ragged ends, grows left to right behind the ink */
export const Highlighter: React.FC<{ x: number; y: number; w: number; h: number; t0: number; dur?: number; color?: string; rot?: number; opacity?: number }> = ({ x, y, w, h, t0, dur = 0.4, color = "#f2e12e", rot = -0.6, opacity = 0.78 }) => {
  const v = useV(); if (v < t0) return null; const p = easeOut(prog(v, t0, dur));
  return <div style={{ position: "absolute", left: x, top: y, width: w * p, height: h, background: color, opacity, mixBlendMode: "multiply", transform: `rotate(${rot}deg)`, transformOrigin: "0 50%", clipPath: "polygon(0 12%, 2% 0, 98% 6%, 100% 40%, 99% 92%, 3% 100%, 0 70%)", filter: "url(#rough)" }} />;
};

/** a strip of yellow masking tape with torn ends and marker handwriting; it is slapped down (scale 1.12 to 1) on t0 */
export const TapeLabel: React.FC<{ x: number; y: number; w: number; h: number; rot?: number; t0: number; text: React.ReactNode; size?: number; color?: string; seed?: number; ink?: string }> = ({ x, y, w, h, rot = -2, t0, text, size = 44, color = C.tape, seed = 3, ink = C.ink }) => {
  const v = useV(); if (v < t0) return null; const p = easeBack(prog(v, t0, 0.22), 1.4); const q = easeOut(prog(v, t0 + 0.05, 0.3)); const r = rng(seed);
  const jag = (side: number) => Array.from({ length: 7 }, (_, i) => `${side === 0 ? r() * 2.2 : 100 - r() * 2.2}% ${(i / 6) * 100}%`);
  const poly = `polygon(${jag(0).join(",")},${jag(1).reverse().join(",")})`;
  return (
    <div style={{ position: "absolute", left: x - w / 2, top: y - h / 2, width: w, height: h, transform: `rotate(${rot}deg) scale(${0.88 + 0.12 * p})`, opacity: Math.min(1, p * 1.4), filter: "drop-shadow(2px 5px 5px rgba(40,30,10,0.38))" }}>
      <div style={{ position: "absolute", inset: 0, background: color, opacity: 0.94, clipPath: poly, backgroundImage: "linear-gradient(90deg, rgba(255,255,255,0.18), rgba(0,0,0,0.04) 40%, rgba(255,255,255,0.12))", mixBlendMode: "multiply" }} />
      <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", clipPath: `inset(0 ${100 - 100 * q}% 0 0)` }}>
        <span style={{ fontFamily: FONT.marker, fontSize: size, color: ink, letterSpacing: 1, lineHeight: 1, filter: "url(#rough)", whiteSpace: "nowrap" }}>{text}</span>
      </div>
    </div>
  );
};

/** a metal paperclip drawn in SVG, pinning a print */
export const PaperClip: React.FC<{ x: number; y: number; rot?: number; scale?: number }> = ({ x, y, rot = 8, scale = 1 }) => (
  <svg width="60" height="150" viewBox="0 0 60 150" style={{ position: "absolute", left: x - 30, top: y - 75, transform: `rotate(${rot}deg) scale(${scale})`, filter: "drop-shadow(3px 4px 3px rgba(0,0,0,0.35))" }}>
    <path d="M22 118 V30 a14 14 0 0 1 28 0 V122 a22 22 0 0 1 -44 0 V40" fill="none" stroke="#b8bcc2" strokeWidth="5" strokeLinecap="round" />
    <path d="M22 118 V30 a14 14 0 0 1 28 0 V122 a22 22 0 0 1 -44 0 V40" fill="none" stroke="#f3f5f7" strokeWidth="1.6" strokeLinecap="round" transform="translate(-1 -1)" opacity="0.8" />
  </svg>
);

/** a printed photo / screenshot: white border, slight tilt, soft shadow, optional paperclip; pops in on t0 */
export const Print: React.FC<{ src: string; x: number; y: number; w: number; h: number; rot?: number; t0: number; border?: number; clip?: boolean; children?: React.ReactNode; fit?: string; tone?: string; dark?: boolean }> = ({ src, x, y, w, h, rot = -1.5, t0, border = 16, clip = false, children, fit = "cover", tone, dark }) => {
  const v = useV(); if (v < t0) return null; const p = easeBack(prog(v, t0, 0.3), 1.2);
  return (
    <div style={{ position: "absolute", left: x - w / 2, top: y - h / 2, width: w, height: h, transform: `rotate(${rot}deg) scale(${0.9 + 0.1 * p}) translateY(${(1 - p) * -40}px)`, opacity: Math.min(1, p * 1.5) }}>
      <div style={{ position: "absolute", inset: 0, background: "#f3efe4", boxShadow: "6px 12px 16px rgba(30,20,8,0.4), 0 0 0 1px rgba(0,0,0,0.12)", filter: "url(#scissor)" }} />
      <div style={{ position: "absolute", inset: border, overflow: "hidden", background: dark ? "#16161a" : "#fff" }}>
        <Img src={staticFile(src)} style={{ width: "100%", height: "100%", objectFit: fit as any, filter: tone || "none" }} />
        {children}
      </div>
      {clip && <PaperClip x={w * 0.18} y={6} rot={-6} />}
    </div>
  );
};

/** a cut-out picture with a scissor-cut paper edge (white rim), shadow and optional yellow offset like the Porsche portrait */
export const Cutout: React.FC<{ src: string; x: number; y: number; w: number; rot?: number; t0: number; bw?: boolean; rim?: number; offsetColor?: string; h?: number; pop?: boolean; tOut?: number }> = ({ src, x, y, w, rot = 0, t0, bw = false, rim = 5, offsetColor, h, pop = true, tOut }) => {
  const v = useV(); if (v < t0) return null; const p = pop ? easeBack(prog(v, t0, 0.3), 1.3) : 1;
  const gone = tOut !== undefined ? easeOut(prog(v, tOut, 0.3)) : 0; if (gone >= 1) return null;
  const edge = `drop-shadow(${rim}px 0 0 #f4f1e6) drop-shadow(-${rim}px 0 0 #f4f1e6) drop-shadow(0 ${rim}px 0 #f4f1e6) drop-shadow(0 -${rim}px 0 #f4f1e6)`;
  const off = offsetColor ? `drop-shadow(14px 8px 0 ${offsetColor})` : "";
  return (
    <div style={{ position: "absolute", left: x - w / 2 + gone * -900, top: y - (h ?? w) / 2, width: w, height: h, transform: `rotate(${rot - gone * 12}deg) scale(${0.85 + 0.15 * p})`, opacity: Math.min(1, p * 1.6), filter: `${off} drop-shadow(7px 12px 9px rgba(30,20,8,0.42))` }}>
      <div style={{ filter: `${edge}`, width: "100%" }}><div style={{ filter: "url(#scissor)" }}>
        <Img src={staticFile(src)} style={{ width: "100%", display: "block", filter: bw ? "grayscale(1) contrast(1.15)" : "none" }} />
      </div></div>
    </div>
  );
};

/** a jagged crack drawn with a marker across something, with a few impact ticks */
export const Crack: React.FC<{ x: number; y: number; len: number; t0: number; dur?: number; color?: string; width?: number; seed?: number; angle?: number }> = ({ x, y, len, t0, dur = 0.35, color = C.red, width = 9, seed = 4, angle = -80 }) => {
  const v = useV(); if (v < t0) return null; const p = easeOut(prog(v, t0, dur)); const r = rng(seed); const a = (angle * Math.PI) / 180; const ux = Math.cos(a), uy = Math.sin(a);
  const pts: string[] = []; const N = 9;
  for (let i = 0; i <= N; i++) { const t = i / N; const j = (r() - 0.5) * len * 0.16; pts.push(`${i === 0 ? "M" : "L"}${(x + ux * len * t - uy * j).toFixed(1)} ${(y + uy * len * t + ux * j).toFixed(1)}`); }
  const ticks = [0.3, 0.55, 0.8].map((t, i) => { const bx = x + ux * len * t, by = y + uy * len * t; const s = i % 2 ? 1 : -1; return `M${bx} ${by} l${-uy * 34 * s} ${ux * 34 * s}`; });
  return <SvgLayer><path d={pts.join(" ")} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" filter="url(#chalk)" {...draw(p)} />
    {ticks.map((d, i) => <path key={i} d={d} fill="none" stroke={color} strokeWidth={width * 0.6} strokeLinecap="round" filter="url(#chalk)" {...draw(easeOut(prog(v, t0 + 0.12 + i * 0.05, 0.15)))} />)}</SvgLayer>;
};

/** a real screenshot cropped to one phrase, as a clipping: paper rim, scissor edge, slight tilt; a yellow highlighter sweeps over it */
export const Clipping: React.FC<{ src: string; x: number; y: number; w: number; h: number; rot?: number; t0: number; hl?: number; dur?: number }> = ({ src, x, y, w, h, rot = -1.2, t0, hl, dur = 0.55 }) => {
  const v = useV(); if (v < t0) return null; const p = easeBack(prog(v, t0, 0.28), 1.2);
  const hp = hl === undefined ? 0 : easeOut(prog(v, hl, dur));
  return (
    <div style={{ position: "absolute", left: x - w / 2, top: y - h / 2, width: w, height: h, transform: `rotate(${rot}deg) scale(${0.92 + 0.08 * p})`, opacity: Math.min(1, p * 1.5), filter: "drop-shadow(5px 9px 8px rgba(30,20,8,0.4))" }}>
      <div style={{ position: "absolute", inset: 0, background: "#f6f2e6", filter: "url(#scissor)" }} />
      <div style={{ position: "absolute", inset: 10, overflow: "hidden", background: "#fff" }}>
        <Img src={staticFile(src)} style={{ width: "100%", height: "100%", objectFit: "fill", filter: "grayscale(0.25) contrast(1.05)" }} />
        {hl !== undefined && <div style={{ position: "absolute", left: 0, top: "10%", height: "78%", width: `${hp * 100}%`, background: "#f2e12e", mixBlendMode: "multiply", opacity: 0.85 }} />}
      </div>
    </div>
  );
};

/** a red rubber-stamp impression (text), slammed on t0 with a small bounce; ink uneven */
export const StampText: React.FC<{ text: string; x: number; y: number; rot?: number; t0: number; color?: string; size?: number }> = ({ text, x, y, rot = -8, t0, color = "#b3141c", size = 92 }) => {
  const v = useV(); if (v < t0) return null; const q = prog(v, t0, 0.2); const s = 1.5 - 0.5 * easeOut(q);
  return (
    <div style={{ position: "absolute", left: x, top: y, transform: `translate(-50%,-50%) rotate(${rot}deg) scale(${s})`, opacity: Math.min(1, q * 3) * 0.92, mixBlendMode: "multiply" }}>
      <div style={{ border: `8px solid ${color}`, borderRadius: 10, padding: "6px 26px", fontFamily: FONT.bungee, fontSize: size, color, letterSpacing: 3, lineHeight: 1.05, filter: "url(#chalk)", whiteSpace: "nowrap" }}>{text}</div>
    </div>
  );
};

/** a blue ink seal with the eMudhra logo inside (the digital-signature stamp) */
export const Seal: React.FC<{ x: number; y: number; d?: number; rot?: number; t0: number }> = ({ x, y, d = 150, rot = -10, t0 }) => {
  const v = useV(); if (v < t0) return null; const q = prog(v, t0, 0.18); const s = 1.35 - 0.35 * easeOut(q);
  return (
    <div style={{ position: "absolute", left: x - d / 2, top: y - d / 2, width: d, height: d, transform: `rotate(${rot}deg) scale(${s})`, opacity: Math.min(1, q * 3) * 0.9, mixBlendMode: "multiply", filter: "url(#chalk)" }}>
      <div style={{ position: "absolute", inset: 0, borderRadius: "50%", border: "7px solid #2a3f8f" }} />
      <div style={{ position: "absolute", inset: 12, borderRadius: "50%", border: "2.5px solid #2a3f8f" }} />
      <Img src={staticFile("img/emudhra_logo.png")} style={{ position: "absolute", left: d * 0.14, top: d * 0.36, width: d * 0.72, opacity: 0.9, filter: "hue-rotate(185deg) saturate(1.6) brightness(0.75)" }} />
    </div>
  );
};

/** the eMudhra logo on a paper tag (the real logo); tears in two when tTear passes */
export const LogoTag: React.FC<{ x: number; y: number; w?: number; rot?: number; t0: number; tTear?: number }> = ({ x, y, w = 540, rot = -2, t0, tTear }) => {
  const v = useV(); if (v < t0) return null; const p = easeBack(prog(v, t0, 0.3), 1.2); const h = w * 0.34;
  const e = tTear === undefined ? 0 : easeOut(prog(v, tTear, 0.4));
  const zig = "0% 0%, 51% 0%, 47% 14%, 53% 28%, 48% 42%, 54% 57%, 49% 71%, 53% 86%, 50% 100%, 0% 100%";
  const zig2 = "51% 0%, 100% 0%, 100% 100%, 50% 100%, 53% 86%, 49% 71%, 54% 57%, 48% 42%, 53% 28%, 47% 14%";
  const piece = (clip: string, dx: number, drot: number) => (
    <div style={{ position: "absolute", inset: 0, transform: `translate(${dx * e}px, ${Math.abs(dx) * 0.2 * e}px) rotate(${drot * e}deg)`, filter: "drop-shadow(5px 9px 8px rgba(30,20,8,0.4))" }}>
      <div style={{ position: "absolute", inset: 0, background: "#f3eee0", clipPath: `polygon(${clip})` }}>
        <Img src={staticFile("img/emudhra_logo.png")} style={{ position: "absolute", left: w * 0.06, top: h * 0.2, width: w * 0.88 }} />
      </div>
    </div>
  );
  return <div style={{ position: "absolute", left: x - w / 2, top: y - h / 2, width: w, height: h, transform: `rotate(${rot}deg) scale(${0.9 + 0.1 * p})`, opacity: Math.min(1, p * 1.5) }}>{piece(zig, -34, -5)}{piece(zig2, 34, 6)}</div>;
};

/** a small browser window (crisp HTML): address bar with a lock; state "ok" green, "bad" red; xAt draws a red X over it */
export const BrowserWin: React.FC<{ x: number; y: number; w?: number; rot?: number; t0: number; lock?: "ok" | "bad"; okAt?: number; xAt?: number; url?: string; tOut?: number }> = ({ x, y, w = 300, rot = -2, t0, lock = "ok", okAt, xAt, url = "emudhra.com", tOut }) => {
  const v = useV(); if (v < t0) return null; const p = easeBack(prog(v, t0, 0.25), 1.2); const g = tOut !== undefined ? easeOut(prog(v, tOut, 0.3)) : 0; if (g >= 1) return null; const h = w * 0.72; const s = w / 300; if (okAt !== undefined) lock = v >= okAt ? "ok" : "bad";
  return (
    <div style={{ position: "absolute", left: x - w / 2 + g * -800, top: y - h / 2, width: w, height: h, transform: `rotate(${rot}deg) scale(${0.9 + 0.1 * p})`, opacity: Math.min(1, p * 1.4), filter: "drop-shadow(5px 9px 8px rgba(30,20,8,0.4))" }}>
      <div style={{ position: "absolute", inset: 0, background: "#faf8f2", borderRadius: 10 * s, overflow: "hidden", filter: "url(#scissor)" }}>
        <div style={{ height: 30 * s, background: "#e2dfd5", display: "flex", alignItems: "center", gap: 6 * s, paddingLeft: 10 * s }}>
          {["#ec6056", "#f2be46", "#60c46c"].map((c) => <div key={c} style={{ width: 9 * s, height: 9 * s, borderRadius: "50%", background: c }} />)}
          <div style={{ marginLeft: 8 * s, flex: 1, height: 18 * s, background: "#fff", borderRadius: 9 * s, marginRight: 10 * s, display: "flex", alignItems: "center", paddingLeft: 7 * s, gap: 6 * s, fontFamily: FONT.ui, fontSize: 11 * s, color: "#555" }}>
            <svg width={11 * s} height={13 * s} viewBox="0 0 22 26"><path d="M5 12 V8 a6 6 0 0 1 12 0 V12" fill="none" stroke="#444" strokeWidth="3" /><rect x="1" y="11" width="20" height="14" rx="3" fill={lock === "ok" ? "#2fa872" : "#c8202a"} /></svg>{url}
          </div>
        </div>
        <div style={{ height: 44 * s, background: "#1c2856" }} />
        <div style={{ margin: 14 * s, height: 10 * s, width: "62%", background: "#c9c5b8", borderRadius: 5 * s }} /><div style={{ margin: `0 ${14 * s}px`, height: 10 * s, width: "44%", background: "#c9c5b8", borderRadius: 5 * s }} />
        <div style={{ margin: 14 * s, height: 60 * s, background: "#e7e3d6", borderRadius: 6 * s }} />
      </div>
      {xAt !== undefined && <XMark cx={w / 2} cy={h / 2} s={w * 0.22} t0={xAt} width={11 * s} />}
    </div>
  );
};

/** a marker line through given points (scene coordinates), drawn on; closed = joins the end to the start */
export const PathMark: React.FC<{ pts: [number, number][]; t0: number; dur?: number; color?: string; width?: number; closed?: boolean; opacity?: number; multiply?: boolean }> = ({ pts, t0, dur = 0.7, color = "#efe22e", width = 16, closed = true, opacity = 0.9, multiply = true }) => {
  const v = useV(); if (v < t0) return null; const p = easeOut(prog(v, t0, dur));
  const all = closed ? [...pts, pts[0], pts[1]] : pts; const d = all.map((q, i) => `${i === 0 ? "M" : "L"}${q[0].toFixed(1)} ${q[1].toFixed(1)}`).join(" ");
  return <SvgLayer><path d={d} fill="none" stroke={color} strokeWidth={width} strokeLinecap="round" strokeLinejoin="round" opacity={opacity} style={multiply ? { mixBlendMode: "multiply" } : undefined} filter="url(#chalk)" {...draw(p)} /></SvgLayer>;
};

/** a torn-off calendar page with a big number, as paper on the desk */
export const CalPage: React.FC<{ x: number; y: number; w?: number; rot?: number; t0: number; top: string; big: string; sub?: string }> = ({ x, y, w = 240, rot = -3, t0, top, big, sub }) => {
  const v = useV(); if (v < t0) return null; const p = easeBack(prog(v, t0, 0.28), 1.3); const h = w * 1.05;
  return (
    <div style={{ position: "absolute", left: x - w / 2, top: y - h / 2, width: w, height: h, transform: `rotate(${rot}deg) scale(${0.88 + 0.12 * p})`, opacity: Math.min(1, p * 1.5), filter: "drop-shadow(6px 10px 8px rgba(30,20,8,0.42))" }}>
      <div style={{ position: "absolute", inset: 0, background: "#f4efe2", filter: "url(#scissor)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: h * 0.24, background: C.red, color: "#fff", fontFamily: FONT.bungee, fontSize: h * 0.14, textAlign: "center", lineHeight: `${h * 0.24}px` }}>{top}</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: h * 0.24, bottom: 0, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: FONT.serif, fontWeight: 900, fontSize: h * (big.length > 2 ? 0.34 : 0.5), color: C.ink }}>{big}</div>
      {sub && <div style={{ position: "absolute", left: 0, right: 0, bottom: h * 0.06, textAlign: "center", fontFamily: FONT.marker, fontSize: h * 0.12, color: C.ink }}>{sub}</div>}
    </div>
  );
};
