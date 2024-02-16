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
        return [
          { icon: "fa-solid fa-power-off", text: "Run LCM", href: "run.json", params: { fullscreen: true, run: true } },
          { icon: "fa-solid fa-check", text: "uncensor", href: "fix.json", params: { fullscreen: true, run: true } },
          { icon: "fa-solid fa-people-group", text: "generatenpc", href: "npcgen.json", params: { fullscreen: true, run: true } }
        ]
      }
    } else {
      return [{ icon: "fa-solid fa-plug", text: "Install", href: "install.json", params: { run: true, fullscreen: true } }]
    }
  }
}
