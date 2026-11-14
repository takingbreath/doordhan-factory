// transparent stickers laid over Pandey's own shots by the edit (build3.py): "18 months" and a question mark, on yellow tape in marker handwriting
import React from "react";
import { AbsoluteFill } from "remotion";
import { Defs, Fonts, SceneClock } from "../lib/core";
import { TapeLabel } from "../lib/marks";

export const Over18: React.FC = () => <SceneClock v0={0}><AbsoluteFill><Defs /><Fonts /><TapeLabel x={270} y={90} w={500} h={128} rot={-4} t0={-1} text="18 months" size={76} seed={41} /></AbsoluteFill></SceneClock>;
export const OverQ: React.FC = () => <SceneClock v0={0}><AbsoluteFill><Defs /><Fonts /><TapeLabel x={100} y={100} w={150} h={150} rot={5} t0={-1} text="?" size={120} seed={42} /></AbsoluteFill></SceneClock>;
