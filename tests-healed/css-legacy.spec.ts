import { expect, type Page, test } from "@playwright/test";

// Strategy: id/class CSS selectors, the way legacy suites are written.
// Written against app v1 and never updated — like most real suites.

async function login(page: Page) {
	await page.goto("/");
	await page.locator("#field-user").fill("demo");
	await page.locator("#field-pass").fill("demo123");
	await page.locator(".submit-action").click();
}

test("shows an error for invalid credentials", async ({ page }) => {
	await page.goto("/");
	await page.locator("#field-user").fill("demo");
	await page.locator("#field-pass").fill("wrong");
	await page.locator(".submit-action").click();
	await expect(page.locator(".notification--danger")).toBeVisible();
});

test("logs in and shows the dashboard", async ({ page }) => {
	await login(page);
	await expect(page.locator(".dashboard-panel__title")).toHaveText("My Tasks");
});

test("adds a task to the list", async ({ page }) => {
	await login(page);
	await page.locator(".task-composer__input").fill("Book flights");
	await page.locator(".task-composer__submit").click();
	await expect(page.locator(".tasks li.task-row")).toHaveCount(4);
	await expect(page.locator(".tasks li.task-row").last()).toContainText("Book flights");
});

test("completes a task", async ({ page }) => {
	await login(page);
	await page
		.locator("li.task-row", { hasText: "Write report" })
		.locator(".icon-btn")
		.click();
	await expect(page.locator(".tasks li.task-row--done")).toHaveCount(2);
	await expect(page.locator(".badge-count")).toHaveText("1 active");
});

test("filters to active tasks", async ({ page }) => {
	await login(page);
	await page.locator(".filter-bar .chip").nth(1).click();
	await expect(page.locator(".tasks li.task-row")).toHaveCount(2);
	await expect(page.locator(".tasks")).not.toContainText("Ship release");
});

test("filters to completed tasks", async ({ page }) => {
	await login(page);
	await page.locator(".filter-bar .chip").nth(2).click();
	await expect(page.locator(".tasks li.task-row")).toHaveCount(1);
	await expect(page.locator(".tasks")).toContainText("Ship release");
});

test("shows the active task count", async ({ page }) => {
	await login(page);
	await expect(page.locator(".badge-count")).toHaveText("2 active");
});
