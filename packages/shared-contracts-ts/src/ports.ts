/** Ports shared by Part 1 and Part 2. No provider network calls. */

import type { z } from "zod";

import {
  CraftRubric as CraftRubricSchema,
  ProviderRegistry as ProviderRegistrySchema,
  RenderReceipt as RenderReceiptSchema,
  TimelineSpec as TimelineSpecSchema,
} from "./models.ts";

export type TimelineSpec = z.infer<typeof TimelineSpecSchema>;
export type RenderReceipt = z.infer<typeof RenderReceiptSchema>;
export type ProviderRegistry = z.infer<typeof ProviderRegistrySchema>;
export type CraftRubric = z.infer<typeof CraftRubricSchema>;

export interface RenderBackendPort {
  render(spec: TimelineSpec): RenderReceipt;
}

export interface ProviderRegistryLoader {
  load(source: string | Record<string, unknown>): ProviderRegistry;
}

export interface CraftRubricLoader {
  load(source: string | Record<string, unknown>): CraftRubric;
}
