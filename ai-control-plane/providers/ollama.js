const axios=require("axios")

async function chat(prompt,model){
 const res=await axios.post(
 model.url+"/api/generate",
 {
 model:model.model,
 prompt:prompt,
 stream:false
 }
 )
 return res.data.response
}

module.exports={chat}
