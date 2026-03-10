let queue=[]
let working=false

function push(task){
 return new Promise((resolve,reject)=>{
 queue.push({task,resolve,reject})
 process()
 })
}

async function process(){
 if(working) return
 const item=queue.shift()
 if(!item) return
 working=true
 try{
 const result=await item.task()
 item.resolve(result)
 }catch(e){
 item.reject(e)
 }
 working=false
 process()
}

module.exports={push}
