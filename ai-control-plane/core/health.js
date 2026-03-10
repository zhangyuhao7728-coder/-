const {getConfig}=require("../utils/config")
const axios=require("axios")

let startTime=Date.now()

function getUptime(){
 return Math.floor((Date.now()-startTime)/1000)
}

function resetUptime(){
 startTime=Date.now()
}

async function checkHealth(){
 const cfg=getConfig()
 const models=Object.keys(cfg.models||{})
 
 const providerStatus={}
 for(const name of models){
 const provider=cfg.models[name].provider
 providerStatus[provider]=providerStatus[provider]||"ok"
 }
 
 let ollamaStatus="ok"
 try{
 await axios.get("http://localhost:11434/api/tags",{timeout:2000})
 }catch{
 ollamaStatus="offline"
 }
 
 return {
 status:"ok",
 uptime:getUptime(),
 providers:models.length,
 providerStatus:providerStatus,
 ollama:ollamaStatus
 }
}

module.exports={checkHealth,getUptime,resetUptime}
