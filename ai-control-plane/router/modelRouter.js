const fs=require("fs")
const path=require("path")

// 获取配置（热更新后直接使用缓存）
function getConfig(){
 const {getConfig:get}=require("../utils/config")
 return get()
}

// 动态加载 provider
function loadProvider(providerName){
 try{
 return require("../providers/"+providerName)
 }catch(e){
 throw new Error("provider not found: "+providerName)
 }
}

// 智能路由 - 带模型级 Fallback
async function route(prompt){
 const cfg=getConfig()
 const primary=cfg.primary_model
 const model=cfg.models[primary]
 
 if(!model){
 throw new Error("model not found: "+primary)
 }
 
 const provider=loadProvider(model.provider)
 
 if(!provider.chat){
 throw new Error("provider missing chat(): "+model.provider)
 }
 
 try{
 return await provider.chat(prompt,model)
 }catch(e){
 // 模型级别的 fallback
 if(model.fallback){
 console.log("primary model failed, trying fallback: "+model.fallback)
 const backup=cfg.models[model.fallback]
 if(backup){
 const backupProvider=loadProvider(backup.provider)
 return await backupProvider.chat(prompt,backup)
 }
 }
 throw e
 }
}

module.exports={route}
