const axios=require("axios")

async function chat(prompt,model){
 const res=await axios.post(model.url,{prompt})
 return res.data.reply || JSON.stringify(res.data)
}

module.exports={chat}
