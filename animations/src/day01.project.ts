import { makeProject } from "@motion-canvas/core";
import "./global.css";

import example from "./scenes/day-01?scene";
import day1audio from "../audio/day01.mp3?url";

export default makeProject({
  scenes: [example],
  audio: day1audio,
});
