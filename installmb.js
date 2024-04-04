const config = require("./config.js")
const pre = require("./pre.js")
module.exports = async (kernel) => {
  let script = {
    run: [{
      method: "shell.run",
      params: {
        venv: "moonbeam/venv",
        message: [
          "pip install -r moonbeam/requirements.txt"
        ],
      }
    }, {
      method: "fs.share",
      params: {
        venv: "venv"
      }
    },{
    "method": "shell.run",
    "params": { 
		"path": "app",
      "message": "git clone https://github.com/miroku0000/npclibrary.git"}
  },

 {
      method: "notify",
      params: {
        html: "Click the 'start' tab to get started!"
      }
    }]
  }
  let pre_command = pre(config, kernel)
  if (pre_command) {
    script.run[0].params.message = [pre_command].concat(script.run[0].params.message)
  }
  return script
}
