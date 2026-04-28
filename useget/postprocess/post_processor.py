"""
post_processor.py
------------------
Handles post-processing actions on downloaded files (e.g., permissions, moving files).
"""

import os
import logging

from typing import Any

import importlib
import glob
import shutil

class PostProcessor:
	"""
	Performs post-processing on downloaded files (e.g., fix permissions, move files, plugins).
	"""
	def __init__(self, config: dict) -> None:
		"""
		Initialize PostProcessor with configuration.
		Args:
			config: Dictionary with post-processing settings (e.g., fix_permissions, target_uid, target_gid, move_to, chmod, plugins).
		"""
		self.config = config
		self.plugins = self._load_plugins()

	def _load_plugins(self):
		"""
		Discover and load post-processing plugins from the postprocess/plugins directory.
		Returns a list of plugin callables.
		"""
		plugins = []
		plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins')
		if not os.path.isdir(plugins_dir):
			return plugins
		for file in glob.glob(os.path.join(plugins_dir, '*.py')):
			mod_name = os.path.splitext(os.path.basename(file))[0]
			if mod_name.startswith('_'):
				continue
			try:
				mod = importlib.import_module(f'useget.postprocess.plugins.{mod_name}')
				if hasattr(mod, 'process'):
					plugins.append(mod.process)
			except Exception as e:
				logging.error(f"Failed to load plugin {mod_name}: {e}")
		return plugins

	def process(self, file_path: str) -> None:
		"""
		Process a file after download. Supports fix_permissions, move, chmod, and plugins.
		Args:
			file_path: Path to the file to process.
		"""
		# Fix permissions
		if self.config.get('fix_permissions'):
			try:
				os.chown(file_path, self.config['target_uid'], self.config['target_gid'])
			except OSError as e:
				logging.error(f"Failed to chown {file_path}: {e}")

		# Move file
		move_to = self.config.get('move_to')
		if move_to:
			try:
				dest = os.path.join(move_to, os.path.basename(file_path))
				shutil.move(file_path, dest)
				file_path = dest
				logging.info(f"Moved file to {dest}")
			except Exception as e:
				logging.error(f"Failed to move {file_path} to {move_to}: {e}")

		# Chmod
		chmod_mode = self.config.get('chmod')
		if chmod_mode:
			try:
				os.chmod(file_path, int(chmod_mode, 8))
				logging.info(f"Set permissions {chmod_mode} on {file_path}")
			except Exception as e:
				logging.error(f"Failed to chmod {file_path}: {e}")

		# Run plugins
		for plugin in self.plugins:
			try:
				plugin(file_path, self.config)
				logging.info(f"Ran plugin {plugin.__module__}")
			except Exception as e:
				logging.error(f"Plugin {plugin.__module__} failed: {e}")
