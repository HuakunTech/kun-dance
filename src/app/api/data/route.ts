import fs from "fs";
import path from "path";
import { NextRequest, NextResponse } from "next/server";

const filePath = path.join(process.cwd(), "scripts", "frames.json");
const jsonData = fs.readFileSync(filePath, "utf-8");
const rawFrames = JSON.parse(jsonData);

export function GET(request: NextRequest) {
  return NextResponse.json(rawFrames);
}
