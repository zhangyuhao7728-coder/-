const fs=require("fs")
const path=require("path")

const LOG_PATH=path.join(__dirname,"..","logs","system.log")

function log(msg){
 const line=new Date().toISOString()+" "+msg+"\n"
 fs.appendFileSync(LOG_PATH,line)
}

module.exports={log}
