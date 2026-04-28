import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QRadioButton, QButtonGroup, QMessageBox, QDialog, QFormLayout
)
from PyQt5.QtCore import QSettings

from useget.clients.nzbgeek_client import NZBGeekClient
from useget.clients.sabnzbd_client import SABnzbdClient
from useget.clients.jellyfin_client import JellyfinClient

class SettingsDialog(QDialog):
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        layout = QFormLayout()
        self.nzbgeek_api = QLineEdit()
        self.sab_url = QLineEdit()
        self.sab_api = QLineEdit()
        self.jellyfin_url = QLineEdit()
        self.jellyfin_api = QLineEdit()
        # Pre-fill with current config if available
        if config:
            self.nzbgeek_api.setText(config.get('nzbgeek', {}).get('api_key', ''))
            self.sab_url.setText(config.get('sabnzbd', {}).get('url', ''))
            self.sab_api.setText(config.get('sabnzbd', {}).get('api_key', ''))
            self.jellyfin_url.setText(config.get('jellyfin', {}).get('url', ''))
            self.jellyfin_api.setText(config.get('jellyfin', {}).get('api_key', ''))
        layout.addRow('NZBGeek API Key:', self.nzbgeek_api)
        layout.addRow('SABnzbd URL:', self.sab_url)
        layout.addRow('SABnzbd API Key:', self.sab_api)
        layout.addRow('Jellyfin URL:', self.jellyfin_url)
        layout.addRow('Jellyfin API Key:', self.jellyfin_api)
        btns = QHBoxLayout()
        save_btn = QPushButton('Save')
        save_btn.clicked.connect(self.accept)
        btns.addWidget(save_btn)
        layout.addRow(btns)
        self.setLayout(layout)
    def get_config(self):
        return {
            'nzbgeek': {
                'api_key': self.nzbgeek_api.text().strip(),
            },
            'sabnzbd': {
                'url': self.sab_url.text().strip(),
                'api_key': self.sab_api.text().strip(),
            },
            'jellyfin': {
                'url': self.jellyfin_url.text().strip(),
                'api_key': self.jellyfin_api.text().strip(),
            }
        }

    def __init__(self):
        super().__init__()
        self.setWindowTitle('useget GUI')
        self.resize(700, 500)
        # Persistent settings
        self.settings = QSettings('useget', 'useget-app')
        self.config = self.load_persistent_config()
        self.nzbgeek = None
        self.sab = None
        self.jellyfin = None
        self.last_results = []
        layout = QVBoxLayout()
        # Search controls
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Enter movie or TV show title...')
        search_layout.addWidget(self.search_input)
        self.movie_radio = QRadioButton('Movie')
        self.tv_radio = QRadioButton('TV Show')
        self.movie_radio.setChecked(True)
        self.type_group = QButtonGroup()
        self.type_group.addButton(self.movie_radio)
        self.type_group.addButton(self.tv_radio)
        search_layout.addWidget(self.movie_radio)
        search_layout.addWidget(self.tv_radio)
        self.search_btn = QPushButton('Search')
        search_layout.addWidget(self.search_btn)
        layout.addLayout(search_layout)
        # Results
        layout.addWidget(QLabel('Results:'))
        self.results_list = QListWidget()
        layout.addWidget(self.results_list)
        # Download links
        layout.addWidget(QLabel('Available Downloads:'))
        self.links_list = QListWidget()
        layout.addWidget(self.links_list)
        # Status
        self.status_label = QLabel('Ready.')
        layout.addWidget(self.status_label)
        # Settings
        self.settings_btn = QPushButton('Settings')
        layout.addWidget(self.settings_btn)
        self.setLayout(layout)
        # Connect actions
        self.search_btn.clicked.connect(self.on_search)
        self.results_list.itemClicked.connect(self.on_result_selected)
        self.links_list.itemClicked.connect(self.on_link_selected)
        self.settings_btn.clicked.connect(self.open_settings)
        # Initialize clients if config is present
        if self.config['nzbgeek']['api_key'] and self.config['sabnzbd']['url'] and self.config['sabnzbd']['api_key']:
            self.nzbgeek = NZBGeekClient(self.config['nzbgeek'])
            self.sab = SABnzbdClient(self.config['sabnzbd'])
        if self.config['jellyfin']['url'] and self.config['jellyfin']['api_key']:
            self.jellyfin = JellyfinClient(self.config['jellyfin'])

    def load_persistent_config(self):
        # Load from QSettings
        config = {
            'nzbgeek': {'api_key': self.settings.value('nzbgeek_api_key', '')},
            'sabnzbd': {
                'url': self.settings.value('sabnzbd_url', ''),
                'api_key': self.settings.value('sabnzbd_api_key', '')
            },
            'jellyfin': {
                'url': self.settings.value('jellyfin_url', ''),
                'api_key': self.settings.value('jellyfin_api_key', '')
            }
        }
        return config

    def on_search(self):
        self.status_label.setText('Searching...')
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, 'Input Error', 'Please enter a title to search.')
            return
        # Ensure clients are initialized
        if not self.nzbgeek or not self.sab:
            QMessageBox.warning(self, 'Configuration Missing', 'Please set your API keys and URLs in Settings first.')
            self.status_label.setText('Missing configuration.')
            return
        is_movie = self.movie_radio.isChecked()
        results = self.nzbgeek.search(query)
        # Filter by type: movie or tv
        import re
        filtered = []
        for item in results:
            if is_movie:
                if re.search(r'\.(19|20)\d{2}\.', item['title']):
                    filtered.append(item)
            else:
                if re.search(r'\.S\d{2}E\d{2}\.', item['title'], re.IGNORECASE):
                    filtered.append(item)
        self.last_results = filtered
        self.results_list.clear()
        self.links_list.clear()
        for item in filtered:
            self.results_list.addItem(item['title'])
        self.status_label.setText(f'Found {len(filtered)} results.')
    def on_result_selected(self, item):
        title = item.text()
        links = [r for r in self.last_results if r['title'] == title]
        self.links_list.clear()
        for link in links:
            self.links_list.addItem(f"{link['nzb_url']}")
        self.status_label.setText(f'Showing links for: {title}')
    def on_link_selected(self, item):
        url = item.text()
        # Find the result dict
        nzb = next((r for r in self.last_results if r['nzb_url'] == url), None)
        if not nzb:
            self.status_label.setText('Error: Could not find NZB info.')
            return
        if not self.sab:
            self.status_label.setText('SABnzbd not configured.')
            return
        self.sab.add_nzb(nzb)
        self.status_label.setText(f'Sent to SABnzbd: {nzb["title"]}')
    def open_settings(self):
        dlg = SettingsDialog(self, config=self.config)
        if dlg.exec_() == QDialog.Accepted:
            # Save settings in memory
            self.config = dlg.get_config()
            # Save to persistent storage
            self.settings.setValue('nzbgeek_api_key', self.config['nzbgeek']['api_key'])
            self.settings.setValue('sabnzbd_url', self.config['sabnzbd']['url'])
            self.settings.setValue('sabnzbd_api_key', self.config['sabnzbd']['api_key'])
            self.settings.setValue('jellyfin_url', self.config['jellyfin']['url'])
            self.settings.setValue('jellyfin_api_key', self.config['jellyfin']['api_key'])
            # Re-initialize clients with new config
            self.nzbgeek = NZBGeekClient(self.config['nzbgeek'])
            self.sab = SABnzbdClient(self.config['sabnzbd'])
            self.jellyfin = JellyfinClient(self.config['jellyfin'])
            self.status_label.setText('Settings updated and saved.')
        else:
            self.status_label.setText('Settings unchanged.')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = UsegetGUI()
    gui.show()
    sys.exit(app.exec_())
