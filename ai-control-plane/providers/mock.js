async function chat(prompt, model){
 // Mock response for testing
 return "[" + model.model + "] " + prompt + " - 这是测试响应"
}

module.exports = { chat }
