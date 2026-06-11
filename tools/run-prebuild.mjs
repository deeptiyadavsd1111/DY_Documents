import { spawnSync } from "node:child_process";

if (process.platform === "win32") {
  console.log("Skipping bash prebuild checks on Windows.");
  process.exit(0);
}

const result = spawnSync("bash", ["./tools/prebuild.sh"], {
  stdio: "inherit",
  shell: false,
});

if (result.error) {
  console.error(`Failed to run prebuild checks: ${result.error.message}`);
  process.exit(1);
}

process.exit(result.status ?? 1);
