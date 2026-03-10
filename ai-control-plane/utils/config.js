const fs=require("fs")
const path=require("path")

const CONFIG_PATH=path.join(__dirname,"..","config.json")
let config=JSON.parse(fs.readFileSync(CONFIG_PATH))

fs.watch(CONFIG_PATH,()=>{
 console.log("config updated")
 config=JSON.parse(fs.readFileSync(CONFIG_PATH))
})

function getConfig(){
 return config
}

module.exports={getConfig}
