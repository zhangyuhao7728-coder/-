const express = require("express")
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args))

const app = express()
app.use(express.json())

// ========== 配置 ==========
const OLLAMA_URL = "http://127.0.0.1:11434"
const DEFAULT_MODEL = "qwen2.5:7b"

// 预算配置
const BUDGET_CONFIG = {
  "ceo": 100.0,
  "planner": 50.0,
  "engineer": 50.0,
  "researcher": 30.0,
  "analyst": 30.0,
  "reviewer": 20.0,
}

// 风险状态
const riskState = {
  costs: {},
  overrides: {}
}

// 风险评估
function evaluateRisk(agent, cost, overrideCount) {
  const budget = BUDGET_CONFIG[agent] || 50.0
  const ratio = cost / budget
  
  if (ratio >= 2.0) return { level: "CRITICAL", reason: `Cost exceeds 200%` }
  if (ratio >= 1.5) return { level: "HIGH", reason: `Cost exceeds 150%` }
  if (overrideCount >= 8) return { level: "CRITICAL", reason: `Excessive overrides` }
  if (overrideCount >= 5) return { level: "HIGH", reason: `High overrides` }
  if (overrideCount >= 3) return { level: "MEDIUM", reason: `Multiple overrides` }
  if (overrideCount === 1) return { level: "LOW", reason: `Single override` }
  return null
}

function recordCost(agent, cost) {
  const today = new Date().toISOString().split('T')[0]
  const key = `${agent}:${today}`
  if (!riskState.costs[key]) riskState.costs[key] = 0
  riskState.costs[key] += cost
  const risk = evaluateRisk(agent, riskState.costs[key], riskState.overrides[key] || 0)
  if (risk) console.log(`🚨 Risk [${risk.level}] - ${agent}: ${risk.reason}`)
}

function recordOverride(agent) {
  const today = new Date().toISOString().split('T')[0]
  const key = `${agent}:${today}`
  if (!riskState.overrides[key]) riskState.overrides[key] = 0
  riskState.overrides[key]++
  const risk = evaluateRisk(agent, riskState.costs[key] || 0, riskState.overrides[key])
  if (risk) console.log(`🚨 Risk [${risk.level}] - ${agent}: ${risk.reason}`)
}

function isLocked(agent) {
  const today = new Date().toISOString().split('T')[0]
  const key = `${agent}:${today}`
  const risk = evaluateRisk(agent, riskState.costs[key] || 0, riskState.overrides[key] || 0)
  return risk && risk.level === "CRITICAL"
}

function selectProvider(content, agent = "engineer") {
  if (isLocked(agent)) {
    throw new Error(`[SECURITY] ${agent} blocked due to CRITICAL risk`)
  }
  return content.length < 500 
    ? { provider: "local", model: DEFAULT_MODEL }
    : { provider: "cloud", model: "minimax" }
}

// ========== API ==========

app.post("/chat", async (req, res) => {
  const { message, agent = "engineer", forceProvider } = req.body

  try {
    const selection = forceProvider 
      ? { provider: forceProvider, model: DEFAULT_MODEL }
      : selectProvider(message, agent)
    
    console.log(`[Router] ${selection.provider} - ${message.substring(0, 20)}...`)
    recordCost(agent, 0.01)
    
    if (selection.provider === "local") {
      const ollamaRes = await fetch(`${OLLAMA_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: DEFAULT_MODEL,
          stream: false,
          messages: [{ role: "user", content: message }]
        })
      })
      const data = await ollamaRes.json()
      res.json({ response: data.message?.content, provider: selection.provider, model: selection.model })
    } else {
      res.json({ response: "[Cloud] Not configured", provider: selection.provider, model: selection.model })
    }
  } catch (e) {
    res.status(500).json({ error: e.message })
  }
})

app.post("/chat/stream", async (req, res) => {
  const { message, agent = "engineer" } = req.body

  try {
    const selection = selectProvider(message, agent)
    
    res.setHeader("Content-Type", "text/event-stream")
    res.setHeader("Cache-Control", "no-cache")

    const response = await fetch(`${OLLAMA_URL}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: DEFAULT_MODEL,
        stream: true,
        messages: [{ role: "user", content: message }]
      })
    })

    for await (const chunk of response.body) {
      const lines = chunk.toString().split("\n").filter(Boolean)
      for (const line of lines) {
        try {
          const json = JSON.parse(line)
          if (json.message?.content) res.write(`data: ${json.message.content}\n\n`)
        } catch (e) {}
      }
    }
    res.end()
  } catch (e) {
    res.status(500).json({ error: e.message })
  }
})

app.post("/override", (req, res) => {
  const { agent = "engineer" } = req.body
  recordOverride(agent)
  res.json({ status: "ok" })
})

app.post("/cost", (req, res) => {
  const { agent = "engineer", cost = 10.0 } = req.body
  recordCost(agent, cost)
  res.json({ status: "ok" })
})

app.get("/risk", (req, res) => res.json({ budgets: BUDGET_CONFIG, costs: riskState.costs, overrides: riskState.overrides }))

app.get("/models", async (req, res) => {
  try {
    const response = await fetch(`${OLLAMA_URL}/api/tags`)
    res.json(await response.json())
  } catch (e) {
    res.status(500).json({ error: e.message })
  }
})

app.get("/status", (req, res) => res.json({
  router: { local: { threshold: 500 }, cloud: { model: "minimax" } },
  budgets: BUDGET_CONFIG
}))

app.use(express.static("public"))

app.listen(3001, () => {
  console.log("🚀 LLM Debug Panel with Risk Manager v2.0")
  console.log("📍 http://localhost:3001")
  console.log("📡 /chat - Smart Router")
  console.log("📡 /risk - Risk Status")
  console.log("📡 /override - Record Override")
  console.log("📡 /cost - Record Cost")
})
