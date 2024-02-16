{
  "width": 512,
  "height": 512,
  "prompt": "",
  "steps": 16,
  "run": [{
    "method": "input",
    "params": {
      "title": "Enter prompt",
      "type": "notify",
      "form": [{
        "type": "text",
        "key": "prompt",
        "placeholder": "Enter parameters for generatenpc.py (for example --npcrace human --npcgender female --npcclass cleric --imagesperscenario 1 --scenarios 1"
      }]
    }
  }, {
    "method": "shell.run",
    "params": {
      "env": { "PYTORCH_MPS_HIGH_WATERMARK_RATIO": "0.0" },
      "venv": "venv",
      "path": "app",
      "message": "python generatenpc.py \"{{input.prompt}}\" --steps {{self.steps}} --width {{self.width}} --height {{self.height}} --continuous"
    }
  }]
}
