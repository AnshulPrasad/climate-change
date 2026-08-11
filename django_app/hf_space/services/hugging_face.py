from datasets import load_dataset

class HuggingFaceService:
    def __init__(self):
        pass
    def temp(self):
        from datasets import load_dataset

        raw_url = "https://huggingface.co/datasets/climate_fever/resolve/main/climate_fever.json"
        dataset = load_dataset("json", data_files=raw_url)

        print(dataset)
        print("Example sample:", dataset["train"][0])