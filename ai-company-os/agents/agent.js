// AI 代理基类
const axios=require("axios")

class Agent{
 constructor(name,apiUrl){
 this.name=name
 this.apiUrl=apiUrl
 }
 
 async chat(prompt){
 try{
 const res=await axios.post(this.apiUrl+"/v1/chat",{
 prompt:prompt
 })
 return res.data.reply
 }catch(e){
 return "error: "+e.message
 }
 }
 
 async run(task){
 console.log(`[${this.name}] executing: ${task}`)
 const result=await this.chat(task)
 console.log(`[${this.name}] result: ${result}`)
 return result
 }
}

// 规划师
class Planner extends Agent{
 constructor(apiUrl){
 super("Planner",apiUrl)
 }
 
 async plan(goal){
 return await this.chat(`你是一个规划师。请为以下目标制定详细计划: ${goal}`)
 }
}

// 工程师
class Engineer extends Agent{
 constructor(apiUrl){
 super("Engineer",apiUrl)
 }
 
 async implement(task){
 return await this.chat(`你是一个工程师。请实现以下任务: ${task}`)
 }
}

// 研究员
class Researcher extends Agent{
 constructor(apiUrl){
 super("Researcher",apiUrl)
 }
 
 async research(topic){
 return await this.chat(`你是一个研究员。请研究以下主题: ${topic}`)
 }
}

// 审核员
class Reviewer extends Agent{
 constructor(apiUrl){
 super("Reviewer",apiUrl)
 }
 
 async review(code){
 return await this.chat(`你是一个审核员。请审核以下代码: ${code}`)
 }
}

module.exports={Agent,Planner,Engineer,Researcher,Reviewer}
