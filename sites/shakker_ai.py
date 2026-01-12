from fake_useragent import UserAgent
from datetime import datetime
from time import time
from glob import glob
import requests
import uuid
import json
import os


class ShakkerAI:
    def __init__(self):
        self.base_url = "https://shakker.ai"
        self.session = requests.Session()
        self.session.get(self.base_url)
        self.webid = self.session.cookies.get("webid")
        self.headers = {
            "User-Agent": UserAgent().random,
            "Content-Type": "application/json",
            "webid": self.webid,
            "Origin": self.base_url,
        }

    def search(self, query: str, save: bool = False, update: bool = False) -> dict:
        """Search for models on ShakkerAI by keyword.

        Args:
            query (str): The search keyword.
            save (bool, optional): Whether to save the results to a file. Defaults to False.
            update (bool, optional): Whether to update the saved results. Defaults to False.

        Returns:
            dict: The search results.
        """
        fname = f"data/shakker_{query}.json"
        if os.path.exists(fname) and not update:
            with open(fname, "r") as f:
                return json.load(f)
        
        url = self.base_url + "/api/www/model/search"
        
        params = {
            "time": time()
        }
        
        self.headers["Referer"] = self.base_url + "/search?keyword=" + query
        
        payload = {
            "time": "",
            "keyword": query,
            "followed": 0,
            "periodTime": [
                "all"
            ],
            "models": [],
            "types": [],
            "vipType": [],
            "modelUsage": [],
            "modelLicense": [],
            "tagIds": [],
            "page": 1,
            "pageSize": 1000,
            "cid": self.webid,
            "requestId": str(uuid.uuid4())
        }
        
        res = self.session.post(url, headers=self.headers, data=json.dumps(payload), params=params)
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
        files = glob("data/shakker_*.json")
        for file in files:
            with open(file, "r") as f:
                data = json.load(f)
                for record in data.get("data", {}).get("data", []):
                    records.append({
                        "source_file": str(file),
                        "id": "",
                        "name": record.get("name"),
                        "createdAt": datetime.fromisoformat(record.get("createTime")),
                        "downloadCount": record.get("downloadCount"),
                        "thumbsUpCount": -1,
                        "thumbsDownCount": -1,
                        "commentCount": record.get("commentCount"),
                        "collectedCount": record.get("subscribeCount"),
                        "tippedAmountCount": -1,
                        "runCount": record.get("runCount") or 0,
                    })
        if save:
            with open("data/shakker.json", "w") as f:
                json.dump(records, f, indent=4, default=str, ensure_ascii=False)
        return records
