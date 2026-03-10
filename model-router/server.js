const express = require("express")
const axios = require("axios")
const cors = require("cors")
const bodyParser = require("body-parser")
const fs = require("fs")
const { exec } = require("child_process")

const app = express()
const PORT = 3000

app.use(cors())
app.use(bodyParser.json())
app.use(express.static("public"))

const CONFIG_PATH = "./config.json"
const LOG_FILE = "./logs/server.log"

function log(msg) {
 const line = new Date().toISOString() + " " + msg + "\n"
 fs.appendFileSync(LOG_FILE, line)
}

function loadConfig() {
 return JSON.parse(fs.readFileSync(CONFIG_PATH))
}

function saveConfig(cfg) {
 fs.writeFileSync(CONFIG_PATH, JSON.stringify(cfg, null, 2))
}

function auth(req, res, next) {
 const cfg = loadConfig()
 const token = req.headers["x-api-key"]

 if (token !== cfg.api_token) {
 return res.status(403).json({ error: "unauthorized" })
 }

 next()
}

function getLocalModels() {
 return new Promise((resolve, reject) => {
 exec("ollama list", (err, stdout) => {
 if (err) return reject(err)

 const models = stdout
 .split("\n")
 .slice(1)
 .map(x => x.split(" ")[0])
 .filter(Boolean)

 resolve(models)
 })
 })
}

app.get("/api/models", async (req, res) => {
 try {
 const cfg = loadConfig()
 const local = await getLocalModels()

 res.json({
 primary: cfg.primary_model,
 local_models: local
 })
 } catch (e) {
 log(e.message)
 res.status(500).json({ error: e.message })
 }
})

app.get("/api/current", (req, res) => {
 const cfg = loadConfig()
 res.json({ model: cfg.primary_model })
})

app.post("/api/set", auth, async (req, res) => {
 try {
 const { model } = req.body
 if (!model) return res.status(400).json({ error: "model required" })

 const models = await getLocalModels()

 if (!models.includes(model)) {
 return res.status(400).json({ error: "model not found" })
 }

 const cfg = loadConfig()
 cfg.primary_model = model
 saveConfig(cfg)

 log("model switched to " + model)

 res.json({
 message: "model switched",
 model
 })
 } catch (e) {
 log(e.message)
 res.status(500).json({ error: e.message })
 }
})

app.get("/api/status", async (req, res) => {
 const cfg = loadConfig()

 try {
 await axios.get(cfg.ollama_url + "/api/tags")

 res.json({
 ollama: "running",
 primary_model: cfg.primary_model
 })
 } catch {
 res.json({
 ollama: "offline"
 })
 }
})

app.post("/api/restart", auth, (req, res) => {
 exec("openclaw restart", (err) => {
 if (err) {
 log(err.message)
 return res.status(500).json({ error: err.message })
 }

 log("gateway restarted")

 res.json({
 message: "gateway restarting"
 })
 })
})

app.listen(PORT, () => {
 console.log("Model Router running")
 console.log("http://localhost:" + PORT)
})
