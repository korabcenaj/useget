"""
post_processor.py
------------------
Handles post-processing actions on downloaded files (e.g., permissions, moving files).
"""

import os
import shutil

class PostProcessor:
	"""
	Performs post-processing on downloaded files (e.g., fix permissions, move files).
	"""
	def __init__(self, config):
		# config: dict with post-processing settings (e.g., fix_permissions, target_uid, target_gid)
		self.config = config

	def process(self, file_path):
		"""
		Process a file after download. Example: fix permissions if enabled in config.
		"""
		if self.config.get('fix_permissions'):
			try:
				# Change file ownership to target_uid/gid
				os.chown(file_path, self.config['target_uid'], self.config['target_gid'])
			except Exception as e:
				print(f"Failed to chown {file_path}: {e}")
		# Add more post-processing as needed
