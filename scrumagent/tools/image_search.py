from PIL import Image
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from transformers import BlipProcessor, BlipForConditionalGeneration


# Define the input schema for the tool
class FileInput(BaseModel):
    image_path: str = Field(description="should be a filepath")


# Define the tool
@tool("image-search-tool", args_schema=FileInput, return_direct=True)
def image_search(image_path: str) -> str:
    """Recognize images """
    # Load the BLIP processor and model
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    # Open the image
    image = Image.open(image_path).convert("RGB")

    # Generate the image description
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)

    print("Image description:", description)
    return description


# Example usage
if __name__ == '__main__':
    image_path = "/home/deniz/Masaüstü/AutoBotCentral/autobotcentral/discord_multi_agent/agents/tools/pythogoras.jpg"  # Replace with the actual image path
    result = image_search(image_path)
    print("Tool Result:", result)
