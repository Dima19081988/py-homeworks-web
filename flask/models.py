from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import os
import json

@dataclass
class Ad:
	id: int
	title: str
	description: str
	created_at: str
	owner: str

	def to_dict(self):
		return {
			'id': self.id,
			'title': self.title,
			'description': self.description,
			'created_at': self.created_at,
			'owner': self.owner
		}

	@staticmethod
	def from_dict(data: dict) -> 'Ad':
		return Ad(
			id=data['id'],
			title=data['title'],
			description=data['description'],
			created_at=data['created_at'],
			owner=data['owner']
		)

class AdRepository:
	def __init__(self, storage_file: str = 'ads.json'):
		self.storage_file = storage_file
		self._ensure_file_exists()

	def _ensure_file_exists(self):
		if not os.path.exists(self.storage_file):
			with open(self.storage_file, 'w', encoding='utf-8') as f:
				json.dump([], f)

	def _load_data(self) -> list:
		with open(self.storage_file, 'r', encoding='utf-8') as f:
			return json.load(f)

	def _save_data(self, data: list):
		with open(self.storage_file, 'w', encoding='utf-8') as f:
			json.dump(data, f, indent=2, ensure_ascii=False)

	def get_all(self) -> list[Ad]:
		data = self._load_data()
		result = []
		for item in data:
			result.append(Ad.from_dict(item))
		return result

	def get_by_id(self, ad_id: int) -> Optional[Ad]:
		ads = self.get_all()
		for ad in ads:
			if ad.id == ad_id:
				return ad
		return None

	def create(self, title: str, description: str, owner: str) -> Ad:
		ads = self.get_all()

		new_id = max([ad.id for ad in ads], default=0) + 1
		new_ad = Ad(
			id=new_id,
			title=title,
			description=description,
			owner=owner,
			created_at=datetime.now().isoformat()
		)

		data = [ad.to_dict() for ad in ads]
		data.append(new_ad.to_dict())
		self._save_data(data)

		return new_ad

	def update(self, ad_id: int, title: str = None, description: str = None, owner: str = None) -> Optional[Ad]:
		ads = self.get_all()
		for ad in ads:
			if ad.id == ad_id:
				if title is not None:
					ad.title = title
				if description is not None:
					ad.description = description
				if owner is not None:
					ad.owner = owner
				data = [ad.to_dict() for ad in ads]
				self._save_data(data)
				return ad
		return None

	def delete(self, ad_id: int) -> bool:
		ads = self.get_all()
		initial_count = len(ads)

		ads = [ad for ad in ads if ad.id != ad_id]
		if len(ads) < initial_count:
			data = [ad.to_dict() for ad in ads]
			self._save_data(data)
			return True
		return False



