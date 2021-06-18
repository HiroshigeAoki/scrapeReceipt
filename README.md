# scrapeReceipt
DMM英会話のレシートを自動で取得します。email, passwd等は、config/config.yamlで変更できます。<br><br>
事前にchromediriverをインストールする必要があります。<br><br>
[Ubuntuの場合]
```
$ sudo apt install chromium-browser unzip
$ wget https://chromedriver.storage.googleapis.com/$(wget -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
$ unzip chromedriver_linux64.zip
$ sudo mv chromedriver /usr/local/bin/
```
