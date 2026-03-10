#!/usr/bin/env node

/**
 * 🤖 AI 公司操作系统
 * 统一入口
 */

const express=require("express")
const cors=require("cors")
const bodyParser=require("body-parser")
const fs=require("fs")
const path=require("path")
const {exec}=require("child_process")

const app=express()
const PORT=process.env.PORT||3001

// 中间件
app.use(cors())
app.use(bodyParser.json())

// 配置
const CONFIG_PATH=path.join(__dirname,"ai-control-plane","config.json")
const STATS_PATH=path.join(__dirname,"ai-control-plane","stats.json")
const LOG_FILE=path.join(__dirname,"ai-control-plane","logs","system.log")

function log(msg){
 const line=new Date().toISOString()+" "+msg+"\n"
 fs.appendFileSync(LOG_FILE,line)
 console.log(msg)
}

function getConfig(){
 try{return JSON.parse(fs.readFileSync(CONFIG_PATH))}catch{return{}}
}

function getStats(){
 try{return JSON.parse(fs.readFileSync(STATS_PATH))}catch{return{requests:0,errors:0}}
}

// 路由 - 模型调用
app.post("/v1/chat",async(req,res)=>{
 const {prompt}=req.body
 if(!prompt) return res.status(400).json({error:"prompt required"})
 
 const cfg=getConfig()
 const model=cfg.models?.[cfg.primary_model]
 if(!model) return res.status(500).json({error:"no model configured"})
 
 try{
 // 动态加载 provider
 const provider=require(path.join(__dirname,"ai-control-plane","providers",model.provider))
 const reply=await provider.chat(prompt,model)
 
 // 更新统计
 const stats=getStats()
 stats.requests++
 fs.writeFileSync(STATS_PATH,JSON.stringify(stats,null,2))
 
 res.json({reply})
 }catch(e){
 log("chat error: "+e.message)
 const stats=getStats()
 stats.errors++
 fs.writeFileSync(STATS_PATH,JSON.stringify(stats,null,2))
 res.status(500).json({error:e.message})
 }
})

// 状态接口
app.get("/api/status",(req,res)=>{
 const cfg=getConfig()
 const stats=getStats()
 res.json({
 primary:cfg.primary_model||"none",
 models:Object.keys(cfg.models||{}).length,
 stats:stats
 })
})

// 切换模型
app.post("/api/switch",(req,res)=>{
 const {model}=req.body
 const cfg=getConfig()
 if(!cfg.models?.[model]){
 return res.status(400).json({error:"model not found"})
 }
 cfg.primary_model=model
 fs.writeFileSync(CONFIG_PATH,JSON.stringify(cfg,null,2))
 log("model switched to: "+model)
 res.json({success:true,model})
})

// 启动
app.listen(PORT,()=>{
 log("🤖 AI 公司操作系统启动")
 log(`📡 API: http://localhost:${PORT}/v1/chat`)
 log(`📊 状态: http://localhost:${PORT}/api/status`)
})
