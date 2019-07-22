# twdvbt_xmltv
自動下載台灣數位無線電視 EPG 資料，並輸出為 XMLTV 格式，可將該 XMLTV 直接匯入到 Plex 的 LiveTV & DVR

# 用法
```sh
mkdir output
python twdvbt_xmltv.py
```

# 用法 (Docker)
```sh
docker build -t twdvbt_xmltv .
docker run -v ~/twdvbt_xmltv/output:/usr/src/app/output -it --rm --name my-twdvbt_xmltv twdvbt_xmltv
```

# 使用 QNAP Container Station 運行
* 建立 Container, 使用 wenchenx/twdvbt_xmltv 這個 Image
* 共用資料夾設置 /Multimedia 掛載到 /usr/src/app/output
* 建立容器之後, 會運作第一次, 執行完畢會直接停止. 之後選擇該容器按下「執行」即可, 名稱須記起來, 例如我拿到 twdvbt_xmltv-1
* 設定定時更新需要 SSH 到 NAS 內, 執行 crontab -e 插入 (需注意名稱)
```sh
0 1 * * * /share/CACHEDEV1_DATA/.qpkg/container-station/bin/docker start twdvbt_xmltv-1
```

# 匯入到 Plex (以 QNAP 為例)
* 將輸出的 hdhomerun.xml 複製到 /Multimedia
* 在 Plex 新增 HDHomeRun, 選擇自訂 XMLTV
* 在路徑輸入 /share/CACHEDEV1_DATA/Multimedia/hdhomerun.xml
* 之後只要更新 hdhomerun.xml 就可以了
  - 預設 Plex 會在凌晨 2:00 再次讀取 hdhomerun.xml

# 其他
此程式改寫自 https://forum.libreelec.tv/thread/12228-tvheadend-epg-guide-from-hdhomerun/
