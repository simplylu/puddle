from huggingface_hub import HfApi
from huggingface_hub.errors import HfHubHTTPError
from dotenv import load_dotenv
from glob import glob
from time import sleep
import json
import os

load_dotenv()


class HuggingFace:
    def __init__(self):
        self.api = HfApi(token=os.getenv("HUGGINGFACE_TOKEN"))

    def search(self, query: str, save: bool = False, update: bool = False) -> list | dict:
        """Search for models on HuggingFace by keyword.

        Args:
            query (str): The search keyword.
            save (bool, optional): Whether to save the results to a file. Defaults to False.
            update (bool, optional): Whether to update the saved results. Defaults to False.

        Returns:
            dict: The search results.
        """
        if query in {"anal", "ass"}:
            return []
        fname = f"data/huggingface_{query.strip()}.json"
        if os.path.exists(fname) and not update:
            with open(fname, "r") as f:
                return json.load(f)

        model_list = self.api.list_models(search=query, pipeline_tag="text-to-image")
        data = []
        for model in model_list:
            sleep(0.5)  # to avoid rate limiting
            try:
                res = self.api.model_info(model.id, expand=["likes", "downloads", "createdAt", "downloadsAllTime"])
                res = vars(res)
                res["created_at"] = str(res["created_at"])
                data.append(res)
            except HfHubHTTPError:
                print("Rate limit exceeded, sleeping for 6 minutes...")
                sleep(360)  # wait for rate limit reset
        
        if save:
            with open(fname, "w") as f:
                json.dump(data, f, indent=4)
        return data

    def parse(self, save: bool = False) -> list:
        records = []
        files = glob("data/huggingface_*.json")
        for file in files:
            with open(file, "r") as f:
                data = json.load(f)
                for entry in data:
                    record = {
                        "source_file": file,
                        "author": entry.get("id").split("/")[0],
                        "id": entry.get("_id"),
                        "name": entry.get("id").split("/")[-1],
                        "createdAt": entry.get("created_at"),
                        "downloadCount": entry.get("downloads_all_time"),
                        "thumbsUpCount": -1,
                        "thumbsDownCount": -1,
                        "commentCount": -1,
                        "collectedCount": entry.get("likes"),
                        "tippedAmountCount": -1,
                        "runCount": -1
                    }
                    records.append(record)
        if save:
            with open("data/huggingface.json", "w") as f:
                json.dump(records, f, indent=4, default=str, ensure_ascii=False)
        return records
