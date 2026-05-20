const express = require('express');
const multer = require('multer');
const path = require('path');
const puppeteer = require('puppeteer');
const fs = require('fs');

const app = express();
const port = 3000;

// Setup Multer for file uploads (simulating Trust Gap #1: no strict content validation)
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadDir = path.join(__dirname, 'uploads');
        if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir);
        }
        cb(null, uploadDir);
    },
    filename: (req, file, cb) => {
        // Just keeping the extension, simple ID mapping
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        const ext = path.extname(file.originalname).toLowerCase();
        cb(null, file.fieldname + '-' + uniqueSuffix + ext);
    }
});
const upload = multer({ storage: storage });

// Serve static frontend files
app.use(express.static(path.join(__dirname, 'public')));
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));
app.use(express.json()); // For JSON body parsing

// Array to store logs for the frontend
const oobLogs = [];

// ==========================================
// OUT-OF-BAND (OOB) ENDPOINT SIMULATION
// ==========================================
// This sits on the same server for lab convenience.
// In reality this would be an attacker-controlled server (e.g. RequestBin)
app.get('/api/oob-log', (req, res) => {
    const data = req.query;
    console.log('[OOB SERVER HIT!] SSRF Successful! Data received:', data);
    oobLogs.push({ timestamp: new Date().toISOString(), message: 'SSRF requested with data', data });
    res.send('OOB Server Logged Request');
});

// Endpoint to fetch logs for the frontend UI
app.get('/api/logs', (req, res) => {
    res.json(oobLogs);
});

// ==========================================
// VULNERABLE ENDPOINTS
// ==========================================

/**
 * 1. The Entry Point: Uploading the malicious SVG
 * Trust Gap: Only relies on file extension (or maybe not even that, we just allow uploads).
 */
app.post('/api/upload', upload.single('avatar'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded' });
    }
    console.log(`[+] File uploaded successfully: ${req.file.filename}`);
    res.json({ id: req.file.filename, message: 'Upload successful. Next, trigger the processing job.' });
});

/**
 * 2. The Internal Worker / processing job
 * Trust Gap: Processes the file assuming it's a safe image, rendering it fully using a headless browser.
 */
app.post('/api/process', async (req, res) => {
    const { id } = req.query;
    if (!id) {
        return res.status(400).json({ error: 'Missing file id parameter' });
    }

    const filePath = path.join(__dirname, 'uploads', id);
    if (!fs.existsSync(filePath)) {
        return res.status(404).json({ error: 'File not found' });
    }

    console.log(`[*] Mocking background job: Internal service is processing ${id}...`);

    let browser;
    try {
        // Vulnerable Internal Indexing/Thumbnailing Service!
        // We use Puppeteer to "render" the svg to take a screenshot.
        browser = await puppeteer.launch({ 
            headless: 'new',
            args: ['--no-sandbox'] // common in docker environments
        });
        const page = await browser.newPage();
        
        // This is where SSRF / HTML injection happens!
        // Loading the locally uploaded file directly into the browser
        const fileUrl = `http://localhost:${port}/uploads/${id}`;
        console.log(`[Worker] Rendering file URL: ${fileUrl}`);

        // Wait loosely for network idle to allow SSRF to fire out.
        await page.goto(fileUrl, { waitUntil: 'networkidle2', timeout: 5000 });
        
        // Simulating the internal worker taking a screenshot
        const screenshotPath = path.join(__dirname, 'uploads', `thumb-${id}.png`);
        await page.screenshot({ path: screenshotPath });
        
        console.log(`[Worker] Finished processing ${id}.`);
        
        res.json({ message: 'Processing finished! Check internal logs for SSRF hits.' });
    } catch (err) {
        console.error('[Worker] Error during processing:', err.message);
        res.status(500).json({ error: 'Worker failed to process image' });
    } finally {
        if (browser) await browser.close();
    }
});

// ==========================================
// START SERVER
// ==========================================
app.listen(port, () => {
    console.log(`Lab running at http://localhost:${port}`);
    console.log(\`To exploit, upload a malicious SVG designed to hit http://localhost:\${port}/api/oob-log?stolen=\`);
});
