"use client";
import Image from "next/image";
import { Button } from "@/components/ui/button";
import { useEffect, useMemo, useRef, useState } from "react";

function deserializeFrame(frameStr: string): number[][] {
  // Convert string to 2D array. "o" is 0, "l" is 255. Each line is separated by '\n'
  return frameStr
    .split("\n")
    .map((row) => Array.from(row).map((char) => (char === "o" ? 0 : 255)));
}

function decompressFrame(compressedFrame: string): string {
  // Each char can be "o" or "l". Compress consecutive same char to a number followed by the char.
  let decompressed = [];
  let count = "";

  for (let char of compressedFrame) {
    if (!isNaN(parseInt(char))) {
      count += char;
    } else {
      if (count) {
        decompressed.push(char.repeat(parseInt(count)));
        count = "";
      } else {
        decompressed.push(char);
      }
    }
  }

  return decompressed.join("");
}

function Cell({ value }: { value: number }) {
  return (
    <div className={`w-2 h-2 ${value === 0 ? "bg-white dark:bg-inherit" : "bg-black dark:bg-white"}`}></div>
  );
}

function Row({ cells }: { cells: number[] }) {
  return (
    <div className="flex">
      {cells.map((cell, i) => (
        <Cell key={i} value={cell} />
      ))}
    </div>
  );
}

async function getData() {
  const res = await fetch("/api/data");
  // The return value is *not* serialized
  // You can return Date, Map, Set, etc.

  if (!res.ok) {
    // This will activate the closest `error.js` Error Boundary
    throw new Error("Failed to fetch data");
  }

  return res.json();
}

export default function Home() {
  const requestRef = useRef<number>();
  const previousTimeRef = useRef();
  const interval = useRef<NodeJS.Timeout>();
  const [fps, setFps] = useState(15);
  const [rawFrames, setRawFrames] = useState<string[]>([]);
  const frames = useMemo(
    () =>
      rawFrames.map((frame: string) =>
        deserializeFrame(decompressFrame(frame))
      ),
    [rawFrames]
  );
  const [frameIdx, setFrameIdx] = useState(0);
  const nframes = useMemo(() => frames.length, [frames]);
  const height = useMemo(
    () => (frames.length ? frames[0].length : 0),
    [frames]
  );
  const width = useMemo(
    () => (frames.length ? frames[0][0].length : 0),
    [frames]
  );
  const frame = useMemo(
    () => (frames.length ? frames[frameIdx] : []),
    [frames, frameIdx]
  );

  useEffect(() => {
    getData().then((data) => {
      setRawFrames(data);
    });
  }, []);

  useEffect(() => {
    if (frames.length) {
      // increment frame index every 1/30s
      interval.current = setInterval(() => {
        setFrameIdx((prevIdx) => (prevIdx + 1) % nframes);
      }, 1000 / fps);
    }
    return () => {
      clearInterval(interval.current);
      setFrameIdx(0);
    };
  }, [frames, nframes, fps]);

  return (
    <main className="flex justify-center items-center h-full">
      <div>
        {frame?.map((row, i) => (
          <Row key={i} cells={row} />
        ))}
      </div>
    </main>
  );
}
