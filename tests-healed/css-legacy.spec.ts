import { expect, type Page, test } from "@playwright/test";

// Strategy: id/class CSS selectors, the way legacy suites are written.
// Written against app v1 and never updated — like most real suites.

async function login(page: Page) {
	await page.goto("/");
	await page.locator("#fld_9a2b").fill("demo");
	await page.locator("#fld_4c1d").fill("demo123");
	await page.locator(".Login_submit__w6f4").click();
}

test("shows an error for invalid credentials", async ({ page }) => {
	await page.goto("/");
	await page.locator("#fld_9a2b").fill("demo");
	await page.locator("#fld_4c1d").fill("wrong");
	await page.locator(".Login_submit__w6f4").click();
	await expect(page.locator(".Alert_danger__f81m")).toBeVisible();
});

test("logs in and shows the dashboard", async ({ page }) => {
	await login(page);
	await expect(page.locator(".Board_title__u4m3")).toHaveText("My Tasks");
});

test("adds a task to the list", async ({ page }) => {
	await login(page);
	await page.locator(".Composer_input__n5q4").fill("Book flights");
	await page.locator(".Composer_submit__g3y8").click();
	await expect(page.locator(".TaskList_root__v2c9 li.TaskList_row__p3c7")).toHaveCount(4);
	await expect(page.locator(".TaskList_root__v2c9 li.TaskList_row__p3c7").last()).toContainText(
		"Book flights",
	);
});

test("completes a task", async ({ page }) => {
	await login(page);
	await page
		.locator("li.TaskList_row__p3c7", { hasText: "Write report" })
		.locator(".Icon_button__z7h3")
		.click();
	await expect(page.locator(".TaskList_root__v2c9 li.TaskList_done__k1w4")).toHaveCount(2);
	await expect(page.locator(".Board_badge__x1p6")).toHaveText("1 active");
});

test("filters to active tasks", async ({ page }) => {
	await login(page);
	await page.locator(".Filters_bar__d8e1 .Pill_button__a4n1").nth(1).click();
	await expect(page.locator(".TaskList_root__v2c9 li.TaskList_row__p3c7")).toHaveCount(2);
	await expect(page.locator(".TaskList_root__v2c9")).not.toContainText("Ship release");
});

test("filters to completed tasks", async ({ page }) => {
	await login(page);
	await page.locator(".Filters_bar__d8e1 .Pill_button__a4n1").nth(2).click();
	await expect(page.locator(".TaskList_root__v2c9 li.TaskList_row__p3c7")).toHaveCount(1);
	await expect(page.locator(".TaskList_root__v2c9")).toContainText("Ship release");
});

test("shows the active task count", async ({ page }) => {
	await login(page);
	await expect(page.locator(".Board_badge__x1p6")).toHaveText("2 active");
});
