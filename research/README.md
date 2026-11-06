# Industry Academy 研究知識庫

來源蒐集批次：2026-11-06。保留 v2.0 的 00–49 課號及網站九個群組；原文「十個模組」與實際九組不同，不重編。

本庫是可追溯的來源索引與研究卡，並非 50 堂正式講義。所有原文下載只在被 Git 忽略的 `private_sources/`；公開成果為原創筆記、來源連結及核對狀態。即使可公開瀏覽，亦不推定可重新散布全文。不得使用 Railway、修改 M&A Academy、覆寫 docs 或變更 Pages。

`registries/`：七份主索引；`notes/theory_cards/`：逐篇研究卡；`notes/lessons/`：逐課來源狀態；`audit/`：下載、覆蓋與限制；`schemas/`：欄位約定；`scripts/`：蒐集及驗證程序。

執行：Python 3，安裝 requests pandas beautifulsoup4 openpyxl pypdf。依序執行 `python research/scripts/acquire.py 1` 至 `4`，最後 `python research/scripts/validate.py`。網路結果會隨時間變動；本批日期固定保留，不宣稱即時同步。重跑沿用本機快取，下載紀錄記為 cached_download。

狀態：metadata=僅書目或入口；sourced=已有特定資料/文件且核對內容；reviewed=已閱讀原文與核對主張；teaching-ready=另需正式教材審查，本批不使用。HTTP 200 只代表入口可讀，不能證明資料已下載、全文可讀或單位一致。

授權：未取得可用的已登入校園 session；不讀取憑證。使用者允許使用台大管理學院可用內容，取得困難時可略過。受限文件保留 DOI 與存取佇列。

最終批次須接續 `python research/scripts/refine.py`、`python research/scripts/enrich.py`、`python research/scripts/supplement_official.py`、`python research/scripts/finalize.py`，最後 `python research/scripts/validate.py`。refine隔離同名書評及重印錯配，finalize保存人工版本核對；只重跑acquire不會重現最終人工查核狀態。

## 八課深度驗證（2026-11-06）

最新可用證據見[evidence/deep-2026-11-06](evidence/deep-2026-11-06/README.md)：8篇正式期刊PDF核心段落核讀、1篇正式HTML（PDF精確頁碼待補）、1份作者稿、6家企業、8堂Evidence Pack。候選來源並未全部轉為知識庫，8課仍各有缺口。

本批人工核讀結果由`build_deep_evidence.py`產生；依序執行`validate_deep_evidence.py`與`validate.py`。使用`deep_acquire.py --evidence-manifest`可重取sources.csv所列文件並比對既有SHA；網站或授權可能變動，版本改變會標記。不要以較早finalize流程覆寫本批核讀狀態。原始全文及OCR僅在本機private_sources。

## 50課全來源蒐集 v2

使用者已授權將來源蒐集擴大至00–49全部課程；本輪不撰寫教材。先前八課深度核讀保留。新入口：[逐課涵蓋](audit/coverage_report.md)、[九類缺口](audit/full-acquisition-v2/lesson_gaps.csv)、[續跑指令](audit/next_actions.md)、[來源catalog](sources/catalog.csv)。來源總編輯指令與Master原文保存在project_instructions/；編輯規範仍依repository根目錄。

`full_acquisition.py`提供init/fetch/report/inventory，按lesson或task篩選、resume/skip-verified/retry-failures、rate-limit、output-dir、每輪檔數與bytes、單檔bytes上限、dry-run。output-dir必須位於被忽略的private_sources。首次盤點存baseline_inventory.csv，每輪更新current_inventory.csv；不同SHA版本保留，不把相同URL或工作稿/期刊版盲目合併。不要重跑舊acquire的Phase1或finalize覆寫已核讀成果。

成功下載只代表檔案及格式可取得，全文段落與主張核對另列。主表保留舊欄位並追加v2欄位；schema與migration見schemas/full_acquisition_v2.json與audit/full-acquisition-v2/schema_migration.csv。全部50課目前均未達出版級充分性。
