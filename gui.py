import sys
import os
import yaml
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QListWidget, QRadioButton, QButtonGroup, QMessageBox, QDialog, QFormLayout
)
from clients.nzbgeek_client import NZBGeekClient
from clients.sabnzbd_client import SABnzbdClient

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        layout = QFormLayout()
        self.nzbgeek_api = QLineEdit()
        self.sab_url = QLineEdit()
        self.sab_api = QLineEdit()
        self.jellyfin_url = QLineEdit()
        self.jellyfin_api = QLineEdit()
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

class UsegetGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('useget GUI')
        self.resize(700, 500)
        self.config = load_config()
        self.nzbgeek = NZBGeekClient(self.config['nzbgeek'])
        self.sab = SABnzbdClient(self.config['sabnzbd'])
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
    def on_search(self):
        self.status_label.setText('Searching...')
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, 'Input Error', 'Please enter a title to search.')
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
        self.sab.add_nzb(nzb)
        self.status_label.setText(f'Sent to SABnzbd: {nzb["title"]}')
    def open_settings(self):
        dlg = SettingsDialog(self)
        dlg.exec_()
        # TODO: Save settings
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = UsegetGUI()
    gui.show()
    sys.exit(app.exec_())
