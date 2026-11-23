/** Load a providers or craft-rubric document from a mapping or a YAML path. */

import { readFileSync } from "node:fs";
import { parse } from "yaml";

import { assertNoDeprecated, CraftRubric, ProviderRegistry } from "./models.ts";

export const CRAFT_RUBRIC_MAX_LINES = 150;

export class RegistrySourceError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "RegistrySourceError";
  }
}

/** Match Python str.splitlines(), which drops a trailing newline. */
export function splitLines(text: string): string[] {
  if (text === "") return [];
  const lines = text.split(/\r\n|\n|\r/);
  if (lines.length > 0 && lines[lines.length - 1] === "") lines.pop();
  return lines;
}

function readMapping(source: string | Record<string, unknown>, lineCap: number | null): Record<string, unknown> {
  if (typeof source !== "string") return source;
  let text: string;
  try {
    text = readFileSync(source, "utf8");
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    throw new RegistrySourceError(`registry source not found: ${source} (${message})`);
  }
  if (lineCap !== null && splitLines(text).length > lineCap) {
    throw new RegistrySourceError(`rubric exceeds ${lineCap} lines: ${source}`);
  }
  const loaded = parse(text);
  if (!loaded || typeof loaded !== "object" || Array.isArray(loaded)) {
    throw new RegistrySourceError(`registry source must be a mapping: ${source}`);
  }
  return loaded as Record<string, unknown>;
}

export class YamlProviderRegistryLoader {
  load(source: string | Record<string, unknown>) {
    const data = readMapping(source, null);
    assertNoDeprecated(data);
    return ProviderRegistry.parse(data);
  }
}

export class YamlCraftRubricLoader {
  load(source: string | Record<string, unknown>) {
    const data = readMapping(source, typeof source === "string" ? CRAFT_RUBRIC_MAX_LINES : null);
    assertNoDeprecated(data);
    return CraftRubric.parse(data);
  }
}
