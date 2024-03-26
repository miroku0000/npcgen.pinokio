module.exports = {
  title: "npcgen",
  icon: "icon.png",
  description: "Fast Image generator for D&D NPCS using Latent consistency models https://replicate.com/blog/run-latent-consistency-model-on-mac",
  menu: async (kernel) => {
    let installed = await kernel.exists(__dirname, "app", "venv")
    if (installed) {
      let running = await kernel.running(__dirname, "start.json")
      if (running) {
        return [
          { icon: "fa-solid fa-spin fa-circle-notch", text: "Running" },
          { icon: "fa-solid fa-terminal", text: "Terminal", href: "run.json" }
        ]
      } else {
        let npclibinstalled=await kernel.exists(__dirname, "app", "npclibrary")
        if (npclibinstalled)
        {  
        return [
          { icon: "fa-solid fa-people-group", text: "Generate NPCs", href: "npcgen.json", params: { fullscreen: true, run: true } },
          { icon: "fa-solid fa-paperclip", text: "View NPCs", href: "generatehtml.json", params: { fullscreen: true, run: true } },
          { icon: "fa-solid fa-power-off", text: "Manual Text To Image", href: "run.json", params: { fullscreen: true, run: true } }, 
          { icon: "fa-brands fa-instalod", text: "Install NPC Library(Requires 1.6GB Disk Space)", href: "installnpclib.json", params: { fullscreen: true, run: true } }        
        ]
      }
      else
        return [
          { icon: "fa-solid fa-people-group", text: "Generate NPCs", href: "npcgen.json", params: { fullscreen: true, run: true } },
          { icon: "fa-solid fa-paperclip", text: "View NPCs", href: "generatehtml.json", params: { fullscreen: true, run: true } },
          { icon: "fa-solid fa-power-off", text: "Manual Text To Image", href: "run.json", params: { fullscreen: true, run: true } }, 
          { icon: "fa-brands fa-instalod", text: "update NPC Library", href: "updatenpclib.json", params: { fullscreen: true, run: true } }        
        ]

      }
    } else {
      return [
        { icon: "fa-solid fa-glasses", text: "Install uncensored", href: "install.json", params: { run: true, fullscreen: true } },
        { icon: "fa-solid fa-plug", text: "Install censored", href: "installcensored.json", params: { run: true, fullscreen: true } },
             ]
    }
  }
}
