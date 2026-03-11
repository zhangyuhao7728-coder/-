const {getConfig}=require("../utils/config")
const fs=require("fs")
const path=require("path")

let index=0

// 加载智能路由配置
function getSmartRouterConfig(){
  const configPath=path.join(__dirname,"../config.smart-router.json")
  if(fs.existsSync(configPath)){
    return JSON.parse(fs.readFileSync(configPath,"utf8"))
  }
  return {enabled:false,rules:[],fallback:{target:"cloud",model:"minimax_m25"}}
}

// 智能路由匹配
function matchRule(prompt,config){
  if(!config.enabled) return null
  
  // 强制模式
  if(config.force_cloud) return config.fallback
  if(config.force_local) return {target:"local",model:"qwen3.5:9b"}
  
  // 按优先级匹配规则
  const sortedRules=config.rules.sort((a,b)=>b.priority-a.priority)
  
  for(const rule of sortedRules){
    for(const keyword of rule.keywords){
      if(prompt.includes(keyword)){
        return {target:rule.target,model:rule.model,name:rule.name}
      }
    }
  }
  
  return config.fallback
}

// 获取模型配置
function getModelConfig(modelName){
  const cfg=getConfig()
  
  // 先检查本地模型
  if(cfg.models && cfg.models[modelName]){
    return cfg.models[modelName]
  }
  
  // 检查云端模型
  if(cfg.cloud_models && cfg.cloud_models[modelName]){
    return cfg.cloud_models[modelName]
  }
  
  return null
}

async function route(prompt){
 const cfg=getConfig()
 const smartCfg=getSmartRouterConfig()
 
 // 智能路由
 let selectedModel
 if(smartCfg.enabled){
   const match=matchRule(prompt,smartCfg)
   console.log(`[智能路由] 匹配结果:`,match)
   selectedModel=getModelConfig(match.model)
 }else{
   // 默认路由
   const name=cfg.primary_model || Object.keys(cfg.models)[0]
   selectedModel=cfg.models[name]
 }
 
 if(!selectedModel) {
   return "No model configured"
 }
 
 // 根据 provider 类型选择
 let provider
 if(selectedModel.provider === "ollama") {
   provider = require("../providers/ollama")
 } else if(selectedModel.provider === "openai") {
   provider = require("../providers/openai")
 } else if(selectedModel.provider === "anthropic") {
   provider = require("../providers/anthropic") 
 } else if(selectedModel.provider === "generic") {
   provider = require("../providers/generic")
 } else if(selectedModel.provider === "minimax") {
   // MiniMax 使用 generic provider
   provider = require("../providers/generic")
 } else {
   provider = require("../providers/mock")
 }
 
 return await provider.chat(prompt,selectedModel)
}

module.exports={route,matchRule,getSmartRouterConfig}
