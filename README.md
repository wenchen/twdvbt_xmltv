# twdvbt_xmltv
自動下載台灣數位無線電視 EPG 資料，並輸出為 XMLTV 格式，可將該 XMLTV 直接匯入到 Plex 的 LiveTV & DVR

# 用法
python twdvbt_xmltv.py

# 匯入到 Plex (以 QNAP 為例)
* 將輸出的 hdhomerun.xml 複製到 /Multimedia
* 在 Plex 新增 HDHomeRun, 選擇自訂 XMLTV
* 在路徑輸入 /share/CACHEDEV1_DATA/Multimedia/hdhomerun.xml
* 之後只要更新 hdhomerun.xml 就可以了

# 其他
此程式改寫自 https://forum.libreelec.tv/thread/12228-tvheadend-epg-guide-from-hdhomerun/