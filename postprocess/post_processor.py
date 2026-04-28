
import os
import shutil

class PostProcessor:
    def __init__(self, config):
        self.config = config

    def process(self, file_path):
        # Example: fix permissions and move file if needed
        if self.config.get('fix_permissions'):
            try:
                os.chown(file_path, self.config['target_uid'], self.config['target_gid'])
            except Exception as e:
                print(f"Failed to chown {file_path}: {e}")
        # Add more post-processing as needed
