const { test, expect } = require('@playwright/test');

test.describe('DSS DecisionOS - E2E Integration Audit', () => {
  
  test('should complete the Golden Path: Ask -> Response -> Source Detail', async ({ page }) => {
    console.log('🚀 Avvio Test di Integrazione: Golden Path...');

    // 1. Navigazione al Frontend
    await page.goto('/');
    console.log('✅ Pagina caricata correttamente');

    // 2. Intercettazione della rete per monitorare l'endpoint /ask
    // Questo catturerà l'errore 405 se avviene
    const networkPromise = page.waitForResponse(response => 
      response.url().includes('/ask') && (response.status() === 200 || response.status() === 405)
    );

    // 3. Interazione con la Chat
    const inputSelector = 'input[placeholder*="Chiedi alla memoria"]';
    const sendButtonSelector = 'button:has-text("Send"), button:has(.lucide-send)'; // Adattato ai possibili selettori

    await page.fill(inputSelector, 'Perché Discord ha cambiato DB?');
    console.log('✍️ Domanda inserita: "Perché Discord ha cambiato DB?"');
    
    await page.click(sendButtonSelector);
    console.log('🖱️ Pulsante Invia cliccato. In attesa della risposta dal backend...');

    // 4. Analisi della Risposta HTTP
    const response = await networkPromise;
    const status = response.status();
    console.log(`🌐 Risposta dal Backend (Porta 8000): HTTP ${status}`);

    if (status === 405) {
      throw new Error('❌ BUG RILEVATO: Errore 405 Method Not Allowed. Il frontend sta usando il metodo HTTP errato per l\'endpoint /ask.');
    }

    expect(status).toBe(200);
    console.log('✅ Risposta 200 OK ricevuta dal backend.');

    // 5. Verifica della risposta dell'AI nell'interfaccia
    // Aspettiamo che appaia il testo della risposta o i badge delle fonti
    const sourceBadgeSelector = 'button:has-text("Source")';
    await page.waitForSelector(sourceBadgeSelector, { timeout: 10000 });
    console.log('✅ Badge delle fonti renderizzati correttamente nell\'interfaccia.');

    // 6. Test del Source Click -> Slide-over
    await page.click(sourceBadgeSelector);
    console.log('🖱️ Click sul Source ID effettuato.');

    // Verifica che il pannello di dettaglio sia visibile (cerca l'intestazione o il titolo)
    const detailPanel = page.locator('h2:has-text("Scelta Framework Frontend"), h2:has-text("Migrazione")');
    await expect(detailPanel).toBeVisible({ timeout: 5000 });
    console.log('✅ Pannello Detail Slide-over aperto correttamente.');

    console.log('🎯 TEST COMPLETATO CON SUCCESSO: Il Golden Path è integro.');
  });
});