#!/usr/bin/env python3
"""Bake a uniform scale + translate into SVG path data.

Needed to express a logo (its own viewBox) inside a folder's 16x16 coordinate
space so it can be subtracted with fill-rule="evenodd" (resvg honors evenodd
but not <mask>). Uniform scale only (no rotation/skew), so arc flags and the
x-axis-rotation are preserved; rx/ry just scale.

Includes a proper scanner: arc flag args (large-arc, sweep) are single 0/1
chars that may be glued to neighbors (e.g. "011.248" = flag 0, flag 1, 1.248).
"""
import re

_NUM = re.compile(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")
_WS = re.compile(r"[\s,]*")
ARITY = {"m": 2, "l": 2, "t": 2, "h": 1, "v": 1,
         "c": 6, "s": 4, "q": 4, "a": 7, "z": 0}


def _fmt(n):
    s = f"{n:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class _Scanner:
    def __init__(self, d):
        self.d = d
        self.i = 0

    def _skip(self):
        m = _WS.match(self.d, self.i)
        self.i = m.end()

    def eof(self):
        self._skip()
        return self.i >= len(self.d)

    def peek_cmd(self):
        self._skip()
        if self.i < len(self.d) and self.d[self.i].isalpha():
            return self.d[self.i]
        return None

    def read_cmd(self):
        c = self.d[self.i]
        self.i += 1
        return c

    def read_num(self):
        self._skip()
        m = _NUM.match(self.d, self.i)
        self.i = m.end()
        return float(m.group())

    def read_flag(self):
        self._skip()
        c = self.d[self.i]
        self.i += 1
        return int(c)


def transform_path(d, s, tx, ty):
    sc = _Scanner(d)
    out = []
    cur = None
    first_move = True
    while not sc.eof():
        c = sc.peek_cmd()
        if c is not None:
            cur = sc.read_cmd()
            if cur in "Zz":
                out.append(cur)
                continue
        low = cur.lower()
        absolute = cur.isupper()
        treat_abs = absolute or (first_move and low == "m")

        if low in ("m", "l", "t"):
            x, y = sc.read_num(), sc.read_num()
            x, y = (x * s + tx, y * s + ty) if treat_abs else (x * s, y * s)
            out.append(f"{cur}{_fmt(x)} {_fmt(y)}")
        elif low == "h":
            x = sc.read_num()
            x = x * s + tx if absolute else x * s
            out.append(f"{cur}{_fmt(x)}")
        elif low == "v":
            y = sc.read_num()
            y = y * s + ty if absolute else y * s
            out.append(f"{cur}{_fmt(y)}")
        elif low in ("c", "s", "q"):
            coords = []
            for _ in range(ARITY[low] // 2):
                x, y = sc.read_num(), sc.read_num()
                x, y = (x * s + tx, y * s + ty) if absolute else (x * s, y * s)
                coords += [x, y]
            out.append(cur + " ".join(_fmt(v) for v in coords))
        elif low == "a":
            rx, ry, rot = sc.read_num(), sc.read_num(), sc.read_num()
            laf, sf = sc.read_flag(), sc.read_flag()
            x, y = sc.read_num(), sc.read_num()
            rx, ry = rx * s, ry * s
            x, y = (x * s + tx, y * s + ty) if absolute else (x * s, y * s)
            out.append(f"{cur}{_fmt(rx)} {_fmt(ry)} {_fmt(rot)} "
                       f"{laf} {sf} {_fmt(x)} {_fmt(y)}")

        if low == "m":
            cur = "L" if cur == "M" else "l"
            first_move = False

    return " ".join(out)
