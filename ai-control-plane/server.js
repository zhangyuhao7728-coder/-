/**
 * 🤖 AI Control Plane - 智能路由版 v2.1
 * 本地/云端模型分离 + 智能任务路由
 */

const express = require("express")
const cors = require("cors")
const bodyParser = require("body-parser")
const fs = require("fs")
const path = require("path")
const axios = require("axios")

const CONFIG_PATH = path.join(__dirname, "config.json")
const STATS_PATH = path.join(__dirname, "stats.json")
const PUBLIC_PATH = path.join(__dirname, "public")
const LOG_PATH = path.join(__dirname, "logs", "system.log")
const OPENCLAW_CONFIG = "/Users/zhangyuhao/.openclaw/openclaw.json"

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}\n`
  try { fs.appendFileSync(LOG_PATH, line) } catch {}
  console.log(msg)
}

function loadConfig() {
  try { return JSON.parse(fs.readFileSync(CONFIG_PATH)) } 
  catch { return { local_model: "qwen3.5:9b", cloud_model: "", models: {}, cloud_models: {} } }
}

function saveConfig(cfg) {
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(cfg, null, 2))
}

function loadStats() {
  try { return JSON.parse(fs.readFileSync(STATS_PATH)) }
  catch { return { requests: 0, errors: 0, tokens: 0, local: 0, cloud: 0 } }
}

function saveStats(stats) {
  fs.writeFileSync(STATS_PATH, JSON.stringify(stats, null, 2))
}

// 智能路由 - 根据任务类型选择模型
function route(prompt, options = {}) {
  const cfg = loadConfig()
  const { force_type, use_case } = options
  
  // 强制指定类型
  if (force_type === 'cloud') {
    return { modelName: cfg.cloud_model, models: cfg.cloud_models, type: 'cloud' }
  }
  if (force_type === 'local') {
    return { modelName: cfg.local_model, models: cfg.models, type: 'local' }
  }
  
  // 智能判断任务复杂度
  const isComplex = isComplexTask(prompt, use_case)
  
  if (isComplex) {
    return { modelName: cfg.cloud_model, models: cfg.cloud_models, type: 'cloud' }
  }
  
  // 默认使用本地模型
  return { modelName: cfg.local_model, models: cfg.models, type: 'local' }
}

// 判断是否为复杂任务
function isComplexTask(prompt, use_case) {
  // 如果指定了use_case
  if (use_case) {
    const complexCases = ['complex', 'code_generation', 'architecture', 'reasoning', 'reviewer', 'high_quality']
    return complexCases.includes(use_case)
  }
  
  // 复杂任务关键词
  const complexKeywords = [
    '生成', '创建', '设计', '架构', '分析', '审查', 'review',
    'implement', 'build', 'create', 'design', 'analyze', 'architect',
    '代码生成', '复杂', '深度', '详细解释'
  ]
  
  // 简单任务关键词
  const simpleKeywords = [
    '总结', '摘要', '简单', '翻译', '列表', '是什么',
    'summarize', 'what is', 'list', 'translate', 'simple'
  ]
  
  const lowerPrompt = prompt.toLowerCase()
  
  for (const kw of complexKeywords) {
    if (lowerPrompt.includes(kw)) return true
  }
  
  for (const kw of simpleKeywords) {
    if (lowerPrompt.includes(kw)) return false
  }
  
  // 默认根据长度判断
  return prompt.length > 200
}

function getProvider(providerName) {
  try {
    return require(path.join(__dirname, "providers", providerName))
  } catch {
    return require(path.join(__dirname, "providers", "mock"))
  }
}

const queue = { queue: [], working: false }
function enqueue(task) {
  return new Promise((resolve, reject) => {
    queue.queue.push({ task, resolve, reject })
    processQueue()
  })
}
async function processQueue() {
  if (queue.working || queue.queue.length === 0) return
  queue.working = true
  const item = queue.queue.shift()
  try {
    const result = await item.task()
    item.resolve(result)
  } catch (e) { item.reject(e) }
  queue.working = false
  processQueue()
}

const app = express()
app.use(cors())
app.use(bodyParser.json())
app.use(express.static(PUBLIC_PATH))

app.get("/", (req, res) => res.sendFile(path.join(PUBLIC_PATH, "index.html")))

// ========== API ==========

app.get("/api/models", (req, res) => {
  const cfg = loadConfig()
  const localModels = Object.entries(cfg.models || {}).map(([name, config]) => ({
    name, provider: config.provider, type: "local", size: config.size || "", enabled: config.enabled !== false, use_cases: config.use_cases || []
  }))
  const cloudModels = Object.entries(cfg.cloud_models || {}).map(([name, config]) => ({
    name, provider: config.provider, type: "cloud", url: config.url || "", enabled: config.enabled !== false, use_cases: config.use_cases || []
  }))
  res.json({ local_model: cfg.local_model, cloud_model: cfg.cloud_model, localModels, cloudModels })
})

// 切换本地模型
app.post("/api/local/switch", (req, res) => {
  const { model } = req.body
  const cfg = loadConfig()
  if (!cfg.models?.[model]) return res.status(400).json({ error: "模型不存在" })
  cfg.local_model = model
  saveConfig(cfg)
  res.json({ success: true, model })
})

// 切换云端模型
app.post("/api/cloud/switch", (req, res) => {
  const { model } = req.body
  const cfg = loadConfig()
  if (!cfg.cloud_models?.[model]) return res.status(400).json({ error: "模型不存在" })
  cfg.cloud_model = model
  saveConfig(cfg)
  res.json({ success: true, model })
})

// 添加模型
app.post("/api/local/add", (req, res) => {
  const { name, provider, url, model, size, use_cases } = req.body
  const cfg = loadConfig()
  cfg.models = cfg.models || {}
  cfg.models[name] = { provider, url: url || "", model: model || name, type: "local", size: size || "", enabled: true, use_cases: use_cases || [] }
  saveConfig(cfg)
  res.json({ success: true, model: name })
})

app.post("/api/cloud/add", (req, res) => {
  const { name, provider, url, model, use_cases } = req.body
  const cfg = loadConfig()
  cfg.cloud_models = cfg.cloud_models || {}
  cfg.cloud_models[name] = { provider, url: url || "", model: model || name, type: "cloud", enabled: true, use_cases: use_cases || [] }
  saveConfig(cfg)
  res.json({ success: true, model: name })
})

// 删除模型
app.post("/api/local/remove", (req, res) => {
  const { name } = req.body
  const cfg = loadConfig()
  if (Object.keys(cfg.models || {}).length <= 1) return res.status(400).json({ error: "至少保留一个" })
  delete cfg.models[name]
  if (cfg.local_model === name) cfg.local_model = Object.keys(cfg.models)[0]
  saveConfig(cfg)
  res.json({ success: true })
})

app.post("/api/cloud/remove", (req, res) => {
  const { name } = req.body
  const cfg = loadConfig()
  delete cfg.cloud_models[name]
  if (cfg.cloud_model === name) cfg.cloud_model = ""
  saveConfig(cfg)
  res.json({ success: true })
})

// 对话接口 - 支持智能路由
app.post("/api/chat", async (req, res) => {
  const { prompt, force_type, use_case } = req.body
  if (!prompt) return res.status(400).json({ error: "请输入内容" })
  
  try {
    const routeInfo = route(prompt, { force_type, use_case })
    const model = routeInfo.models[routeInfo.modelName]
    
    if (!model) {
      throw new Error(routeInfo.type === 'cloud' ? "云端模型未配置" : "本地模型未配置")
    }
    
    const provider = getProvider(model.provider)
    const reply = await provider.chat(prompt, model)
    
    const stats = loadStats()
    stats.requests++
    stats[routeInfo.type]++
    saveStats(stats)
    
    res.json({ 
      reply,
      _model: routeInfo.modelName,
      _type: routeInfo.type,
      _route: routeInfo.type === 'cloud' ? '☁️ 云端模型 (复杂任务)' : '💻 本地模型 (简单任务)'
    })
  } catch (e) {
    const stats = loadStats()
    stats.errors++
    saveStats(stats)
    res.status(500).json({ error: e.message })
  }
})

// 手动选择模型对话
app.post("/api/chat/local", async (req, res) => {
  const { prompt, model } = req.body
  const cfg = loadConfig()
  const modelCfg = cfg.models[model || cfg.local_model]
  if (!modelCfg) return res.status(400).json({ error: "模型不存在" })
  
  try {
    const provider = getProvider(modelCfg.provider)
    const reply = await provider.chat(prompt, modelCfg)
    res.json({ reply, _model: model || cfg.local_model, _type: 'local' })
  } catch (e) {
    res.status(500).json({ error: e.message })
  }
})

app.post("/api/chat/cloud", async (req, res) => {
  const { prompt, model } = req.body
  const cfg = loadConfig()
  const modelCfg = cfg.cloud_models[model || cfg.cloud_model]
  if (!modelCfg) return res.status(400).json({ error: "云端模型不存在" })
  
  try {
    const provider = getProvider(modelCfg.provider)
    const reply = await provider.chat(prompt, modelCfg)
    res.json({ reply, _model: model || cfg.cloud_model, _type: 'cloud' })
  } catch (e) {
    res.status(500).json({ error: e.message })
  }
})

// 获取统计
app.get("/api/stats", (req, res) => res.json(loadStats()))

// 可用模型
app.get("/api/cloud/available", (req, res) => {
  try {
    const openclaw = JSON.parse(fs.readFileSync(OPENCLAW_CONFIG))
    const models = []
    for (const [p, cfg] of Object.entries(openclaw.models?.providers || {})) {
      if (cfg.models) {
        for (const m of cfg.models) {
          models.push({ name: `${p}/${m.id}`, provider: p, model: m.id, url: cfg.baseUrl || "" })
        }
      }
    }
    res.json({ success: true, models })
  } catch (e) { res.json({ success: false, models: [] }) }
})

app.get("/api/local/ollama", (req, res) => {
  axios.get("http://localhost:11434/api/tags").then(r => {
    res.json({ success: true, models: r.data.models?.map(m => ({ name: m.name, size: (m.size / 1024 / 1024 / 1024).toFixed(1) + "GB" })) || [] })
  }).catch(e => res.json({ success: false }))
})

const PORT = process.env.PORT || 3001
app.listen(PORT, () => {
  log(`🤖 AI Control Plane v2.1 启动`)
  log(`📡 http://localhost:${PORT}`)
})

module.exports = app
