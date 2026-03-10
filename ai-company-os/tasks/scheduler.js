// 任务调度器
const fs=require("fs")
const path=require("path")

const TASKS_FILE=path.join(__dirname,"tasks.json")
const LOG_FILE=path.join(__dirname,"logs","task.log")

let tasks=[]

function loadTasks(){
 try{
 tasks=JSON.parse(fs.readFileSync(TASKS_FILE))
 }catch{
 tasks=[]
 }
}

function saveTasks(){
 fs.writeFileSync(TASKS_FILE,JSON.stringify(tasks,null,2))
}

function log(msg){
 const line=new Date().toISOString()+" "+msg+"\n"
 fs.appendFileSync(LOG_FILE,line)
}

// 添加任务
function addTask(name,schedule,callback){
 tasks.push({name,schedule,callback,lastRun:null,enabled:true})
 saveTasks()
}

// 运行任务
async function runTasks(){
 for(const task of tasks){
 if(!task.enabled) continue
 try{
 log("running task: "+task.name)
 await task.callback()
 task.lastRun=new Date().toISOString()
 saveTasks()
 log("task completed: "+task.name)
 }catch(e){
 log("task error: "+task.name+" - "+e.message)
 }
 }
}

// 定时器
function start(){
 loadTasks()
 setInterval(runTasks,60000) // 每分钟检查
 log("task scheduler started")
}

module.exports={addTask,runTasks,start}
