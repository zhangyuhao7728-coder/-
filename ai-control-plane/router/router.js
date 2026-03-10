const {getConfig}=require("../utils/config")

let index=0

async function route(prompt){
 const cfg=getConfig()
 const name=cfg.primary_model || Object.keys(cfg.models)[0]
 const model=cfg.models[name]
 
 if(!model) {
   return "No model configured"
 }
 
 // 根据 provider 类型选择
 let provider
 if(model.provider === "ollama") {
   provider = require("../providers/ollama")
 } else if(model.provider === "openai") {
   provider = require("../providers/openai")
 } else if(model.provider === "anthropic") {
   provider = require("../providers/anthropic") 
 } else if(model.provider === "generic") {
   provider = require("../providers/generic")
 } else {
   provider = require("../providers/mock")
 }
 
 return await provider.chat(prompt,model)
}

module.exports={route}
