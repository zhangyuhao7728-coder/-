const axios=require("axios")

async function chat(prompt,model){
 const res=await axios.post(
 model.url,
 {
 model:model.model,
 messages:[
 {role:"user",content:prompt}
 ]
 },
 {
 headers:{
 Authorization:"Bearer "+model.key
 }
 }
 )
 return res.data.choices[0].message.content
}

module.exports={chat}
