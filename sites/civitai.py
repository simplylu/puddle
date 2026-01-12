from fake_useragent import UserAgent
from glob import glob
import requests
import json
import os
from datetime import datetime


class CivitAI:
    def __init__(self):
        self.base_url = "https://civitai.com"
        self.session = requests.Session()
        self.session.get(self.base_url)
        self.headers = {
            "User-Agent": UserAgent().random,
        }

    def search(self, query: str, save: bool = False, update: bool = False) -> dict:
        """Search for models on CivitAI by keyword.

        Args:
            query (str): The search keyword.
            save (bool, optional): Whether to save the results to a file. Defaults to False.
            update (bool, optional): Whether to update the saved results. Defaults to False.

        Returns:
            dict: The search results.
        """
        fname = f"data/civitai_{query}.json"
        if os.path.exists(fname) and not update:
            with open(fname, "r") as f:
                return json.load(f)
        
        url = self.base_url + "/api/trpc/model.getAll"
        
        payload = {
            "json": {
                "period": "AllTime",
                "periodMode": "published",
                "sort": "Highest Rated",
                "tagname": query,
                "followed": False,
                "hidden": False,
                "pending": False,
                "browsingLevel": 1,
                "excludedTagIds": [415792, 426772, 5351, 5161, 5162, 5188, 5249, 306619, 5351, 154326, 161829, 163032, 130818, 130820, 133182],
                "disablePoi": True,
                "disableMinor": True,
                "cursor": None},
            "meta": {
                "values": {
                    "cursor": ["undefined"]
                }
            }
        }
        
        params = {"input": json.dumps(payload)}
        
        res = self.session.get(url, headers=self.headers, params=params)
        res.raise_for_status()
        
        if res.status_code == 200:
            data = res.json()
            if save:
                with open(fname, "w") as f:
                    json.dump(data, f, indent=4)
            return data
        else:
            return dict()

    def parse(self, save: bool = False) -> list:
        records = []
        files = glob("data/civitai_*.json")
        for file in files:
            with open(file, "r") as f:
                data = json.load(f)
                items = items = (
                    data
                    .get("result", {})
                    .get("data", {})
                    .get("json", {})
                    .get("items", [])
                )
                for item in items:
                    record = {
                        "source_file": file,
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "createdAt": datetime.fromisoformat(item.get("createdAt").replace('Z', '+00:00')) if item.get("createdAt") else None,
                    }
                    rank = item.get("rank") or {}
                    record.update({
                        "downloadCount": rank.get("downloadCount"),
                        "thumbsUpCount": rank.get("thumbsUpCount"),
                        "thumbsDownCount": rank.get("thumbsDownCount"),
                        "commentCount": rank.get("commentCount"),
                        "collectedCount": rank.get("collectedCount"),
                        "tippedAmountCount": rank.get("tippedAmountCount"),
                    })
                    records.append(record)
        if save:
            with open("data/civitai.json", "w") as f:
                json.dump(records, f, indent=4, default=str, ensure_ascii=False)
        return records
