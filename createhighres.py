import os
import torch
import argparse
import glob
import time
import json
from diffusers import DiffusionPipeline

class Predictor:
    
    def __init__(self,model):
        self.pipe = self._load_model(model)

    def _load_model(self,model):
        model = DiffusionPipeline.from_pretrained(
            model
            #"SimianLuo/LCM_Dreamshaper_v7"
            #"Ryzan/fantasy-diffusion-v1"
            #"Lykon/dreamshaper-xl-v2-turbo"
            #"Lykon/AAM_XL_AnimeMix_Turbo"
        )
        if torch.cuda.is_available():
            model.to("cuda")
        elif torch.backends.mps.is_available():
            model.to(torch_device="cpu", torch_dtype=torch.float32).to('mps:0')
        else:
            model.to("cpu")
        return model

    def getMetaData(self,prompt, width,height, steps, model):
        ret={"prompt":prompt, "width":width, "height":height, "steps":steps,"model":model, "seed": self.seed}
        return json.dumps(ret)    
    def write_prompt_to_text_files(self, directory, prompt):
        # Search for all .png files in the specified directory
        png_files = glob.glob(os.path.join(directory, '*.png'))
        for png_file in png_files:
            # Generate the new filename by adding "_prompt.txt" to the original file name
            base_name = os.path.basename(png_file)  # Get the base name of the file
            new_filename = os.path.splitext(base_name)[0] + ".json"  # Remove .png extension and add "_prompt.txt"
            new_filepath = os.path.join(directory, new_filename)  # Create the full path for the new file
        # Write the prompt to the new text file
        with open(new_filepath, 'w') as text_file:
            text_file.write(prompt)
        print(f"Prompt written to {new_filepath}")
        

    def predict(self, prompt: str, width: int, height: int, steps: int, seed: int = None) -> str:
        seed = seed or int.from_bytes(os.urandom(2), "big")
        print(f"Using seed: {seed}")
        torch.manual_seed(seed)
        self.seed=seed
        result = self.pipe(
            prompt=prompt, width=width, height=height,
            guidance_scale=8.0, num_inference_steps=steps,
            num_images_per_prompt=1, lcm_origin_steps=50,
            output_type="pil"
        ).images[0]

        return self._save_result(result)

    def _save_result(self, result):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        output_dir = "highres"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, f"out-{timestamp}.png")
        result.save(output_path)
        return output_path

def main():
    args = parse_args()
    predictor = Predictor(args.model)
    if args.continuous:
        try:
            while True:
                output_path = predictor.predict(args.prompt, args.width, args.height, args.steps, args.seed)
                print(f"Output image saved to: {output_path}")
                output_path = predictor.predict(args.prompt, args.width, args.height, args.steps, args.seed)
            print(f"Output image saved to: {output_path}")
            output_dir = "highres"
            predictor.write_prompt_to_text_files(output_dir, predictor.getMetaData(args.prompt, args.width,args.height, args.steps, args.model))
        except KeyboardInterrupt:
            print("\nStopped by user.")
            output_dir = "highres"
            predictor.write_prompt_to_text_files(output_dir, args.prompt)
    else:
        output_path = predictor.predict(args.prompt, args.width, args.height, args.steps, args.seed)
        print(f"Output image saved to: {output_path}")
        output_dir = "highres"
        predictor.write_prompt_to_text_files(output_dir, predictor.getMetaData(args.prompt, args.width,args.height, args.steps, args.model))
        
def parse_args():
    parser = argparse.ArgumentParser(description="Generate images based on text prompts.")
    parser.add_argument("prompt", type=str, help="A single text prompt for image generation.")
    parser.add_argument("--width", type=int, default=512, help="The width of the generated image.")
    parser.add_argument("--height", type=int, default=512, help="The height of the generated image.")
    parser.add_argument("--steps", type=int, default=8, help="The number of inference steps.")
    parser.add_argument("--seed", type=int, default=None, help="Seed for random number generation.")
    parser.add_argument("--continuous", action='store_true', help="Enable continuous generation.")
    parser.add_argument("--model", default="SimianLuo/LCM_Dreamshaper_v7", 
        choices=['SimianLuo/LCM_Dreamshaper_v7','Ryzan/fantasy-diffusion-v1','Lykon/dreamshaper-xl-v2-turbo','Lykon/AAM_XL_AnimeMix_Turbo','stabilityai/stable-cascade-prior'])    
    return parser.parse_args()

if __name__ == "__main__":
    main()
