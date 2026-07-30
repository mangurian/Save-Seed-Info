import os
import folder_paths
from datetime import datetime

class SaveSeedNode:
    def __init__(self):
        # Tells the node to look at your default ComfyUI Output folder
        self.output_dir = folder_paths.get_output_directory()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # Naming it exactly "seed" tells the ComfyUI interface to automatically 
                # add the "randomize / fixed / increment" control switch to it.
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "filename_prefix": ("STRING", {"default": "seed_record"}),
                "save_mode": (["Individual Files", "Append to Master Log"], {"default": "Individual Files"}),
            }
        }

    # Outputs the seed so you can plug it into a KSampler. Seeds saved to Output folder
    # Harry Mangurian 25 Jun 2026
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("seed",)
    FUNCTION = "save_seed"
    OUTPUT_NODE = True # Forces the node to run even if it isn't connected to a Save Image node
    CATEGORY = "Utils"

    def save_seed(self, seed, filename_prefix, save_mode):
        # Get the current time in a readable format
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format the data into 2 columns using f-string padding
        # Seed (20 chars) | Time
        header_row = f"{'SEED':<20} | CURRENT TIME\n"
        divider = "-" * 40 + "\n"
        data_row = f"{str(seed):<20} | {current_time}\n"
        
        if save_mode == "Append to Master Log":
            # Appends the seed to a single running text document
            file_path = os.path.join(self.output_dir, f"{filename_prefix}_log.txt")
            
            # Check if file exists so we only write the header once
            needs_header = not os.path.exists(file_path)
            
            with open(file_path, "a", encoding="utf-8") as f:
                if needs_header:
                    f.write(header_row)
                    f.write(divider)
                f.write(data_row)
        else:
            # Creates an individual text file (e.g., seed_record_00001.txt)
            counter = 1
            while True:
                file_path = os.path.join(self.output_dir, f"{filename_prefix}_{counter:05d}.txt")
                if not os.path.exists(file_path):
                    break
                counter += 1
                
            with open(file_path, "w", encoding="utf-8") as f:
                # Include the header for individual files as well for consistency
                f.write(header_row)
                f.write(divider)
                f.write(data_row)
                
        return {"ui": {"text": [f"Saved Seed: {seed}\nTime: {current_time}"]}, "result": (seed,)}

# This registers the node so ComfyUI can find it
NODE_CLASS_MAPPINGS = {
    "SaveSeedNode": SaveSeedNode
}

# This sets the friendly name you will search for in the menu
NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveSeedNode": "Save Seed to Text"
}