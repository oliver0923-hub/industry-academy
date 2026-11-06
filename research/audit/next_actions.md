# 下一批續跑

本輪未執行背景自動任務。先查看 full-acquisition-v2/coverage.csv、lesson_gaps.csv、restricted_and_failures.csv。

從repository目錄執行：

```powershell
python research/scripts/full_acquisition.py fetch --lessons all --resume --skip-verified --rate-limit 2 --max-files-per-run 25 --max-bytes-per-run 80000000
python research/scripts/full_acquisition.py discover --lessons all --max-files-per-run 20
python research/scripts/full_acquisition.py fetch --lessons 06,07,08,09,27,42,44 --resume --skip-verified --retry-failures --max-files-per-run 15 --max-bytes-per-run 60000000
python research/scripts/full_acquisition.py report
python research/scripts/validate_full_acquisition.py
python research/scripts/validate_deep_evidence.py
python research/scripts/validate.py
```

`--dry-run`僅列待辦、不發送請求。預設不自動重試受限或失敗來源；開啟retry-failures才重新嘗試，每次最多一次暫時性502/503/504退避。遇robots/login/CAPTCHA不繞過。download log保留latest view，每次嘗試另存acquisition_attempts_v2.csv。

優先下一步：逐課補兩項真正全球資料與兩項台灣統計，對已下載文件核對定義與值；擴充產業專屬期刊OA查核及公司時間線；取得TW12正式細目與TW11官方對照，不猜配對；歷史／圖像權利／跨產業主張須獨立核讀。現有候選不足的課應先以官方搜尋補源，不能把共用宏觀入口當產業專屬證據。
