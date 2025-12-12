import {
  CatppuccinMochaHighlightStyle,
  Colors,
} from "@hhenrichsen/canvas-commons";
import {
  Circle,
  Code,
  Layout,
  LezerHighlighter,
  Line,
  lines,
  makeScene2D,
  Rect,
  Txt,
} from "@motion-canvas/2d";
import {
  createRef,
  createRefArray,
  createSignal,
  delay,
  range,
  spawn,
  Vector2,
  waitFor,
  waitUntil,
} from "@motion-canvas/core";
import { parser as python } from "@lezer/python";
import fullText from "../../../res/day01.txt?raw";

const highlighter = new LezerHighlighter(python, CatppuccinMochaHighlightStyle);

export default makeScene2D(function* (view) {
  // Create your animations here
  const lockRef = createRef<Layout>();
  const circleRef = createRef<Circle>();
  view.fill(Colors.Catppuccin.Mocha.Base);
  view.add(<Layout ref={lockRef} position={[0, 0]}></Layout>);
  const inputText = `L68
L30
R48
L5
R60
L55
L1
L99
R14
L82`;

  yield* waitUntil("lock-in");
  lockRef().add(
    <>
      <Circle clip size={() => circleRef().size()}>
        <Line
          points={[
            [0, 0],
            [-200, 700],
            [700, 700],
            [700, -200],
          ]}
          closed
          fill={Colors.Catppuccin.Mocha.Mantle}
        ></Line>
      </Circle>
      <Circle
        ref={(node: Circle) => {
          spawn(() => node.size(700, 1));
          circleRef(node);
        }}
        size={0}
        stroke={Colors.Catppuccin.Mocha.Text}
        lineWidth={5}
      ></Circle>
    </>
  );

  const rotation = createSignal(180);

  yield* waitFor(1);

  range(0, 20).forEach((i) => {
    const v = Vector2.fromDegrees((i * 360) / 20 + 90);
    const c = circleRef();
    lockRef().add(
      <>
        <Line
          points={() => [
            c.position().add(v.scale(c.size().x / 2)),
            c.position().add(v.scale(c.size().x / 2 + 50)),
          ]}
          stroke={Colors.Catppuccin.Mocha.Text}
          end={0}
          ref={(node: Line) => spawn(() => delay(i * 0.05, node.end(1, 1)))}
          lineWidth={5}
        ></Line>
        <Txt
          text={`${i * 5}`}
          fontFamily={"Inter"}
          position={c.position().add(v.scale(c.size().x / 2 + 80))}
          fontSize={0}
          ref={(node: Txt) =>
            spawn(() => delay(i * 0.05, node.fontSize(30, 1)))
          }
          fill={Colors.Catppuccin.Mocha.Text}
        ></Txt>
      </>
    );
  });

  yield* waitFor(1);

  const innerCircleRef = createRef<Circle>();
  const spinnerRef = createRef<Layout>();

  lockRef().add(
    <Layout
      position={circleRef().position()}
      ref={spinnerRef}
      scale={0}
      rotation={() => rotation() - 180}
    >
      <Circle
        size={circleRef().size().sub(circleRef().lineWidth())}
        clip
        lineWidth={5}
      >
        <Rect
          size={[50, 204]}
          fill={Colors.Catppuccin.Mocha.Green}
          bottom={[0, -148]}
        ></Rect>
        <Circle
          ref={innerCircleRef}
          size={300}
          fill={Colors.Catppuccin.Mocha.Text}
          lineWidth={5}
        >
          {range(20).map((i) => {
            // Small lines from the circle to give it texture
            return (
              <Line
                points={() => {
                  const v = Vector2.fromDegrees((i * 360) / 20);
                  const p = v.scale(innerCircleRef().size().x / 2);
                  return [p.sub(v.scale(5)), p.add(v.scale(5))];
                }}
                stroke={Colors.Catppuccin.Mocha.Text}
                lineWidth={20}
              ></Line>
            );
          })}
        </Circle>
      </Circle>
    </Layout>
  );

  yield* spinnerRef().scale(1, 1);

  yield* waitUntil("text-in");
  yield lockRef().scale(0.8, 1);
  yield lockRef().position.y(-500, 1);
  yield* lockRef().position.x(-150, 1);

  const inputStreamRef = createRef<Layout>();
  view.add(
    <Layout ref={inputStreamRef} position={[400, -500]} scale={0}></Layout>
  );
  const inputTexts = createRefArray<Txt>();
  inputStreamRef().add(
    <Rect
      fill={Colors.Catppuccin.Mocha.Mantle}
      stroke={Colors.Catppuccin.Mocha.Crust}
      size={[181, 752]}
      radius={10}
      lineWidth={5}
      padding={40}
      layout
      justifyContent={"start"}
      alignItems={"start"}
      direction={"column"}
    >
      {inputText.split("\n").map((line, i) => (
        <Txt
          fontFamily={"JetBrains Mono"}
          fontSize={56}
          text={""}
          fill={Colors.Catppuccin.Mocha.Text}
          ref={inputTexts}
        ></Txt>
      ))}
    </Rect>
  );
  yield* inputStreamRef().scale(1, 1);
  for (const [i, step] of inputText.split("\n").entries()) {
    yield delay(i * 0.1, inputTexts[i].text(step, 1));
  }
  yield* waitFor(inputText.split("\n").length * 0.1 + 1);

  const durationPerRotation = 0.5;
  for (const [i, step] of inputText.split("\n").entries()) {
    const firstPart = step[0];
    const rest = parseInt(step.slice(1));
    yield inputTexts[i].fill(
      Colors.Catppuccin.Mocha.Green,
      durationPerRotation
    );
    if (firstPart === "L") {
      yield* rotation(rotation() - rest * 3.6, durationPerRotation);
    } else {
      yield* rotation(rotation() + rest * 3.6, durationPerRotation);
    }
    const modRotation = Math.round((rotation() % 360) + 360) % 360;
    if (modRotation === 0) {
      yield inputTexts[i].fill(
        Colors.Catppuccin.Mocha.Peach,
        durationPerRotation
      );
    } else {
      yield inputTexts[i].fill(
        Colors.Catppuccin.Mocha.Text,
        durationPerRotation
      );
    }
    yield* waitFor(0.2);
  }
  yield* waitUntil("text-part-1-out");
  for (const [i, step] of inputText.split("\n").entries()) {
    yield inputTexts[i].fill(Colors.Catppuccin.Mocha.Text, 1);
  }

  const codeRef = createRef<Code>();
  view.add(
    <Rect
      size={[980, 1000]}
      fill={Colors.Catppuccin.Mocha.Mantle}
      stroke={Colors.Catppuccin.Mocha.Crust}
      ref={(node: Rect) => spawn(() => node.scale(1, 1))}
      scale={0}
      lineWidth={5}
      radius={10}
      position={[0, 400]}
      layout
      justifyContent={"start"}
      alignItems={"start"}
      direction={"column"}
      padding={40}
    >
      <Code
        highlighter={highlighter}
        ref={codeRef}
        fontFamily={"JetBrains Mono"}
      ></Code>
    </Rect>
  );

  yield* waitFor(1);

  yield* codeRef().code(
    `\
with open('input.txt') as f:
  lines = f.readlines()
`,
    1
  );

  yield* waitUntil("part-1-variables");
  yield* codeRef().code.append(1)`
  sum = 0
  pointer = 50`;
  yield* waitUntil("part-1-loop");
  yield* codeRef().code.append(1)`
  for line in lines:`;
  yield* waitUntil("part-1-loop-variables");
  yield* codeRef().code.append(1)`
    prefix = line[0]
    offset = int(line[1:])`;
  yield* waitUntil("part-1-if");
  yield* codeRef().code.append(1)`
    if prefix == 'L':
    `;
  yield* codeRef().code.append(1)`
    else:
    `;
  yield* waitUntil("part-1-if-pointer");
  const ifRange = codeRef().findFirstRange("if prefix == 'L':\n");
  yield* codeRef().code.replace(
    [
      [ifRange[0][0], ifRange[0][1] + "if prefix == 'L':".length],
      [ifRange[1][0], 4],
    ],
    1
  )`
      pointer -= offset`;
  const elseRange = codeRef().findFirstRange("else:\n");
  yield* codeRef().code.replace(
    [
      [elseRange[0][0], elseRange[0][1] + "else:".length],
      [elseRange[1][0], 4],
    ],
    1
  )`
      pointer += offset`;
  yield* waitFor(1);

  yield* waitUntil("part-1-if-pointer-end");
  yield* codeRef().code.append(1)`
    if pointer % 100 == 0:
      sum += 1
    `;

  yield* waitFor(1);

  yield* waitUntil("part-1-print");
  yield* codeRef().code.append(1)`
  print(sum)`;

  yield* waitUntil("part-2");
  yield codeRef().fontSize(34, 1);
  yield* codeRef().opacity(0.5, 1);
  yield* rotation(180, 1);

  let rot = 50;
  for (const [i, step] of inputText.split("\n").entries()) {
    let match = false;
    const firstPart = step[0];
    const rest = parseInt(step.slice(1));
    yield inputTexts[i].fill(
      Colors.Catppuccin.Mocha.Green,
      durationPerRotation
    );
    if (firstPart === "L") {
      yield* rotation(rotation() - rest * 3.6, durationPerRotation);
      for (let j = 0; j < rest; j++) {
        rot -= 1;
        if (Math.round(((rot % 100) + 100) % 100) === 0) {
          match = true;
        }
      }
    } else {
      yield* rotation(rotation() + rest * 3.6, durationPerRotation);
      for (let j = 0; j < rest; j++) {
        rot += 1;
        if (Math.round(((rot % 100) + 100) % 100) === 0) {
          match = true;
        }
      }
    }
    if (!match) {
      yield inputTexts[i].fill(
        Colors.Catppuccin.Mocha.Text,
        durationPerRotation
      );
    } else {
      yield inputTexts[i].fill(
        Colors.Catppuccin.Mocha.Peach,
        durationPerRotation
      );
    }
    yield* waitFor(0.5);
  }
  yield* waitUntil("text-part-2-out");
  for (const [i, step] of inputText.split("\n").entries()) {
    yield inputTexts[i].fill(Colors.Catppuccin.Mocha.Text, 1);
  }

  yield* codeRef().opacity(1, 1);
  yield* waitUntil("part-2-code-1");
  yield codeRef().code.replace(
    codeRef().findFirstRange("      pointer -= offset"),
    1
  )`\
      for i in range(offset):
        pointer -= 1
        if pointer % 100 == 0:
          sum += 1`;
  yield* codeRef().code.replace(
    codeRef().findFirstRange("      pointer \\+= offset"),
    1
  )`\
      for i in range(offset):
        pointer += 1
        if pointer % 100 == 0:
          sum += 1`;

  yield* waitUntil("part-2-code-2");
  yield* codeRef().selection([lines(14, 17), lines(9, 12)], 1);

  yield* waitUntil("full-output");
  yield inputStreamRef().opacity(0, 1);
  yield* codeRef().parent().opacity(0, 1);
  yield lockRef().scale(1, 1);
  yield lockRef().position.y(-200, 1);
  yield* lockRef().position.x(0, 1);
  const commandRef = createRef<Txt>();
  const partOneCheck = createRef<Txt>();
  const partTwoCheck = createRef<Txt>();
  const partOneSum = createRef<Txt>();
  const partTwoSum = createRef<Txt>();
  view.add(
    <Layout
      layout
      y={400}
      justifyContent={"center"}
      alignItems={"center"}
      gap={20}
    >
      <Txt ref={partOneSum} fill={Colors.Catppuccin.Mocha.Text} fontSize={48}>
        0
      </Txt>
      <Txt
        ref={partOneCheck}
        fill={Colors.Catppuccin.Mocha.Green}
        fontSize={48}
        opacity={0.5}
      >
        ✓
      </Txt>
      <Rect
        size={[200, 100]}
        radius={10}
        fill={Colors.Catppuccin.Mocha.Mantle}
        stroke={Colors.Catppuccin.Mocha.Crust}
        lineWidth={5}
        layout
        justifyContent={"center"}
        alignItems={"center"}
      >
        <Txt
          fontFamily={"JetBrains Mono"}
          fontSize={34}
          ref={commandRef}
          fill={Colors.Catppuccin.Mocha.Text}
        ></Txt>
      </Rect>
      <Txt
        ref={partTwoCheck}
        fill={Colors.Catppuccin.Mocha.Green}
        fontSize={48}
        opacity={0.5}
      >
        ✓
      </Txt>
      <Txt ref={partTwoSum} fill={Colors.Catppuccin.Mocha.Text} fontSize={48}>
        0
      </Txt>
    </Layout>
  );
  const fullIters = 50;
  let rot1 = 50;
  let rot2 = 50;
  yield* rotation(180, 1);
  for (const [i, step] of fullText.split("\n").slice(0, fullIters).entries()) {
    commandRef().text(step);
    partOneCheck().opacity(0.5);
    partTwoCheck().opacity(0.5);
    const firstPart = step[0];
    const rest = parseInt(step.slice(1));
    if (firstPart === "L") {
      yield* rotation(rotation() - rest * 3.6, 0.2);
      rot1 -= rest;
      if (Math.round(((rot1 % 100) + 100) % 100) === 0) {
        partOneCheck().opacity(1);
        partOneSum().text(`${parseInt(partOneSum().text()) + 1}`);
      }
      for (let j = 0; j < rest; j++) {
        rot2 -= 1;
        if (Math.round(((rot2 % 100) + 100) % 100) === 0) {
          partTwoCheck().opacity(1);
          partTwoSum().text(`${parseInt(partTwoSum().text()) + 1}`);
        }
      }
    } else {
      yield* rotation(rotation() + rest * 3.6, 0.2);
      rot1 += rest;
      if (Math.round(((rot1 % 100) + 100) % 100) === 0) {
        partOneCheck().opacity(1);
        partOneSum().text(`${parseInt(partOneSum().text()) + 1}`);
      }
      for (let j = 0; j < rest; j++) {
        rot2 += 1;
        if (Math.round(((rot2 % 100) + 100) % 100) === 0) {
          partTwoCheck().opacity(1);
          partTwoSum().text(`${parseInt(partTwoSum().text()) + 1}`);
        }
      }
    }
    yield* waitFor(0.2);
    if (i == fullIters - 10) {
      yield commandRef().parent().parent().opacity(0, 2);
      yield lockRef().opacity(0, 2);
    }
  }
});
