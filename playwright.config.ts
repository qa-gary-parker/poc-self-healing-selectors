import { defineConfig } from "@playwright/test";

// APP_VERSION selects which drift stage of the demo app to serve (v1 | v2 | v3).
// SUITE_DIR selects the suite copy under test (tests | tests-healed).
const version = process.env.APP_VERSION || "v1";

export default defineConfig({
	testDir: process.env.SUITE_DIR || "./tests",
	fullyParallel: true,
	reporter: [["list"]],
	use: {
		baseURL: "http://localhost:4173",
	},
	webServer: {
		command: `npx http-server app/${version} -p 4173 -s -c-1`,
		url: "http://localhost:4173",
		reuseExistingServer: false,
	},
});
