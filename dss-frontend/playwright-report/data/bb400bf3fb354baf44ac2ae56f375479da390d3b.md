# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: integration.test.js >> DSS DecisionOS - E2E Integration Audit >> should complete the Golden Path: Ask -> Response -> Source Detail
- Location: integration.test.js:5:3

# Error details

```
Error: page.goto: net::ERR_CONNECTION_REFUSED at http://127.0.0.1:3000/
Call log:
  - navigating to "http://127.0.0.1:3000/", waiting until "load"

```

# Test source

```ts
  1  | const { test, expect } = require('@playwright/test');
  2  | 
  3  | test.describe('DSS DecisionOS - E2E Integration Audit', () => {
  4  |   
  5  |   test('should complete the Golden Path: Ask -> Response -> Source Detail', async ({ page }) => {
  6  |     console.log('🚀 Avvio Test di Integrazione: Golden Path...');
  7  | 
  8  |     // 1. Navigazione al Frontend
> 9  |     await page.goto('/');
     |                ^ Error: page.goto: net::ERR_CONNECTION_REFUSED at http://127.0.0.1:3000/
  10 |     console.log('✅ Pagina caricata correttamente');
  11 | 
  12 |     // 2. Intercettazione della rete per monitorare l'endpoint /ask
  13 |     // Questo catturerà l'errore 405 se avviene
  14 |     const networkPromise = page.waitForResponse(response => 
  15 |       response.url().includes('/ask') && (response.status() === 200 || response.status() === 405)
  16 |     );
  17 | 
  18 |     // 3. Interazione con la Chat
  19 |     const inputSelector = 'input[placeholder*="Chiedi alla memoria"]';
  20 |     const sendButtonSelector = 'button:has-text("Send"), button:has(.lucide-send)'; // Adattato ai possibili selettori
  21 | 
  22 |     await page.fill(inputSelector, 'Perché Discord ha cambiato DB?');
  23 |     console.log('✍️ Domanda inserita: "Perché Discord ha cambiato DB?"');
  24 |     
  25 |     await page.click(sendButtonSelector);
  26 |     console.log('🖱️ Pulsante Invia cliccato. In attesa della risposta dal backend...');
  27 | 
  28 |     // 4. Analisi della Risposta HTTP
  29 |     const response = await networkPromise;
  30 |     const status = response.status();
  31 |     console.log(`🌐 Risposta dal Backend (Porta 8000): HTTP ${status}`);
  32 | 
  33 |     if (status === 405) {
  34 |       throw new Error('❌ BUG RILEVATO: Errore 405 Method Not Allowed. Il frontend sta usando il metodo HTTP errato per l\'endpoint /ask.');
  35 |     }
  36 | 
  37 |     expect(status).toBe(200);
  38 |     console.log('✅ Risposta 200 OK ricevuta dal backend.');
  39 | 
  40 |     // 5. Verifica della risposta dell'AI nell'interfaccia
  41 |     // Aspettiamo che appaia il testo della risposta o i badge delle fonti
  42 |     const sourceBadgeSelector = 'button:has-text("Source")';
  43 |     await page.waitForSelector(sourceBadgeSelector, { timeout: 10000 });
  44 |     console.log('✅ Badge delle fonti renderizzati correttamente nell\'interfaccia.');
  45 | 
  46 |     // 6. Test del Source Click -> Slide-over
  47 |     await page.click(sourceBadgeSelector);
  48 |     console.log('🖱️ Click sul Source ID effettuato.');
  49 | 
  50 |     // Verifica che il pannello di dettaglio sia visibile (cerca l'intestazione o il titolo)
  51 |     const detailPanel = page.locator('h2:has-text("Scelta Framework Frontend"), h2:has-text("Migrazione")');
  52 |     await expect(detailPanel).toBeVisible({ timeout: 5000 });
  53 |     console.log('✅ Pannello Detail Slide-over aperto correttamente.');
  54 | 
  55 |     console.log('🎯 TEST COMPLETATO CON SUCCESSO: Il Golden Path è integro.');
  56 |   });
  57 | });
```