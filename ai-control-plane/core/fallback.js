const {getConfig}=require("../utils/config")
const log=require("../utils/logger")

// 动态加载 provider
function loadProvider(providerName){
 try{
 return require("../providers/"+ providerName)
 }catch(e){
 throw new Error("provider not found: "+providerName)
 }
}

// 简单路由 - 轮询
async function route(prompt){
 const cfg=getConfig()
 const models=Object.keys(cfg.models)
 
 if(!models||models.length===0){
 throw new Error("no models configured")
 }
 
 const name=models[0] // 使用第一个模型
 const model=cfg.models[name]
 
 const provider=loadProvider(model.provider)
 
 if(!provider.chat){
 throw new Error("provider missing chat(): "+model.provider)
 }
 
 try{
 return await provider.chat(prompt,model)
 }catch(e){
 // Fallback
 if(model.fallback){
 log.warn("model failed, trying fallback: "+model.fallback)
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
