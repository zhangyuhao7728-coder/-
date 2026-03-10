const {getConfig}=require("../utils/config")
const log=require("../utils/logger")

// 负载均衡 - 简单轮询
let currentIndex=0
let history=[]

function getNextModel(models){
 const cfg=getConfig()
 const primary=cfg.primary_model
 return primary
}

function selectModel(){
 const cfg=getConfig()
 const models=Object.keys(cfg.models||{})
 if(models.length===0) return null
 currentIndex=(currentIndex+1)%models.length
 return models[currentIndex]
}

function recordRequest(model,success){
 history.push({
 model,
 success,
 time:Date.now()
 })
 // 只保留最近100条
 if(history.length>100) history.shift()
}

function getStats(){
 const total=history.length
 const success=history.filter(h=>h.success).length
 const byModel={}
 history.forEach(h=>{
 if(!byModel[h.model]) byModel[h.model]={total:0,success:0}
 byModel[h.model].total++
 if(h.success) byModel[h.model].success++
 })
 return {total,success,rate:total>0?(success/total*100).toFixed(2)+"%":0,byModel}
}

module.exports={getNextModel,selectModel,recordRequest,getStats}
