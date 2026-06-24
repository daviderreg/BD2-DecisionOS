const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './',
  fullyParallel: false,
  reporter: 'html',
  use: {
    baseURL: 'http://127.0.0.1:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});