#!/usr/bin/env node
import { argv } from "node:process";
import { parseArgs } from "node:util";
import { load } from "yaml-datastore";
import yaml from "js-yaml";
import path from "path"
import { fileURLToPath } from 'url'
import { dirname } from 'path';

// Get the current module's file path
const __filename = fileURLToPath(import.meta.url);

// Get the directory name
const __dirname = dirname(__filename);

const INVALID_FORMAT_ERROR = "Error: Invalid format";

const args = argv.slice(2);
const numArgs = args.length;

// Print help text for no args or --help flag
if (numArgs == 0 || args.includes("--help")) {
  console.log("Usage: transient-conduction <element-path> [OPTIONS]");
  console.log("");
  console.log(
    "  Print in-memory representation of an element from the transient conduction model"
  );
  console.log("");
  console.log("Options:");
  console.log(
    "  --depth, -d <n>                    integer from -1 to depth of element indicating how deep into element's hierachy to read into memory (-1 = read full depth. Defaults to -1), will not throw error if depth exceeds actual maximum depth of element"
  );
  console.log(
    "  --format, -f [yaml|json]           output format  [default: yaml)"
  );
  console.log("");
  console.log("Examples:");
  console.log("  $ transient-conduction model");
  console.log("  $ transient-conduction model -d 0");
  console.log("  $ transient-conduction model -f json");
  console.log("  $ transient-conduction model.lumpedCapacitance");
  console.log("  $ transient-conduction model.lumpedCapacitance.biotNumber");
  console.log("");
  process.exit(0);
}

const options = {
  elementPath: { type: "string", short: "e" },
  depth: { type: "string", short: "d" },
  format: { type: "string", short: "f" },
};

const workingDirPath = path.join(__dirname, "..")
const parser = parseArgs({ options, allowPositionals: true, args: args });

const elementPath = parser.positionals[0];

let depth = -1;
if (parser.values.depth) {
  depth = parseInt(parser.values.depth);
}

let format = "yaml";
if (parser.values.format) {
  format = parser.values.format;
}

const loadResult = load(workingDirPath, elementPath, depth);

let element = "";
if (loadResult.success) {
  element = loadResult.element;
} else {
  console.error(loadResult.message);
  process.exit(1);
}

if (format === "yaml") {
  const elementAsYaml = yaml.dump(element).trimEnd();
  console.log(elementAsYaml);
} else if (format === "json") {
  const elementAsJson = JSON.stringify(element, null, 2);
  console.log(elementAsJson);
} else {
  console.error(INVALID_FORMAT_ERROR);
  process.exit(2);
}
