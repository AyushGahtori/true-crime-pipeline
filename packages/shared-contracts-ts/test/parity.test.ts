import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { fileURLToPath } from "node:url";

import { gridCellToPixelAndZoom } from "../src/grid.ts";
import { YamlCraftRubricLoader, YamlProviderRegistryLoader } from "../src/loaders.ts";
import { MOTIF_REGISTRY_V1, parseContract } from "../src/models.ts";

const vectorsPath = fileURLToPath(new URL("../../shared_contracts/fixtures/vectors.json", import.meta.url));
const providersPath = fileURLToPath(new URL("../../shared_contracts/tests/fixtures/providers.yaml", import.meta.url));
const rubricPath = fileURLToPath(new URL("../../shared_contracts/tests/fixtures/craft_rubric.yaml", import.meta.url));
const document = JSON.parse(readFileSync(vectorsPath, "utf8")) as {
  valid: Array<{ id: string; model: string; payload: unknown; canonical: unknown }>;
  adversarial: Array<{ id: string; model: string; payload: unknown }>;
  grid: Array<{ args: Parameters<typeof gridCellToPixelAndZoom>[0]; expect: unknown }>;
};

test("zod matches 60 valid python canonical payloads", () => {
  assert.equal(document.valid.length, 60);
  for (const vector of document.valid) {
    assert.deepEqual(parseContract(vector.model, vector.payload), vector.canonical, vector.id);
  }
});

test("zod rejects 60 adversarial payloads", () => {
  assert.equal(document.adversarial.length, 60);
  for (const vector of document.adversarial) {
    assert.throws(() => parseContract(vector.model, vector.payload), undefined, vector.id);
  }
});

test("grid helper matches python expectations", () => {
  assert.equal(document.grid.length, 8);
  for (const row of document.grid) {
    assert.deepEqual(gridCellToPixelAndZoom(row.args), row.expect);
  }
});

test("mvp registry is the four remotion motifs", () => {
  assert.deepEqual(
    MOTIF_REGISTRY_V1.map((entry) => entry.motif_component),
    ["StickmanStage", "AudioEvidenceCard", "RedactedDocReveal", "FoiaFootageFrame"],
  );
  assert.equal(MOTIF_REGISTRY_V1.some((entry) => entry.motif_component === "Illustrative2KPanZoom"), false);
});

test("loaders read a path or a mapping and cap rubric length", () => {
  const providers = new YamlProviderRegistryLoader();
  const fromPath = providers.load(providersPath);
  const fromObject = providers.load(structuredClone(fromPath) as unknown as Record<string, unknown>);
  assert.equal(fromPath.providers.fixture_video.model_id, fromObject.providers.fixture_video.model_id);
  assert.equal(typeof fromPath.providers.fixture_video.pricing.usd_per_second, "number");
  const rubric = new YamlCraftRubricLoader().load(rubricPath);
  assert.equal(rubric.principles.length, 4);
  const dir = mkdtempSync(join(tmpdir(), "tc-rubric-"));
  const tooLong = join(dir, "craft_rubric.yaml");
  writeFileSync(tooLong, `${readFileSync(rubricPath, "utf8")}${"# pad\n".repeat(200)}`, "utf8");
  assert.throws(() => new YamlCraftRubricLoader().load(tooLong));
  assert.throws(() => providers.load(join(dir, "missing.yaml")));
});
