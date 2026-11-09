# Industry Academy｜Google Drive 原始來源讀取橋接

**狀態（2026-11-09）：** Google Drive 連接器在 ChatGPT 對話中已可授權讀取「產業課程」與 `batch-37-41` 子目錄。GitHub 研究庫與 Drive 的**自動授權同步尚未啟用**，不能宣稱「GitHub 已自動讀取」。此文件與 `research/scripts/drive_source_bridge.py` 是可執行的**讀取端**，本次不變更任何 Google Drive 分享權限，不把連結／檔案 ID／原始檔案提交公開 GitHub。

## 使用方式與邊界

- **ChatGPT 教材研究**：直接透過已連接的 Google Drive API 讀取目錄、文件與原始 PDF；讀取後以來源標題、發布日、資料期間、原文定位、統計單位、來源身份記錄逐項證據。不能因資料在 Drive 就宣稱內容已核實。
- **Codex／研究機器**：需要單獨的 Google Drive API **read-only** 授權；ChatGPT 的 Drive 連線權限不會自動轉授 GitHub Actions 或 Codex。必須由檔案擁有者在 Google Cloud 建立服務帳號，開啟 Google Drive API，將指定資料夾給該帳號讀取權，再在受信任的執行環境提供 `GDRIVE_SERVICE_ACCOUNT_JSON` 與 `GDRIVE_ROOT_FOLDER_ID`。採最小權限，不使用使用者個人 OAuth token/密碼公開儲存。
- 在 GitHub Actions 建立 repository secrets 可協助之後啟用；**沒有 secrets 就不會自動觸發同步**。不建議對 public repo 的未知 fork/PR 開啟擁有秘密值的 workflow。
- **資料安全**：目前資料夾的連結分享曾回報任何持連結者有 writer 權限。請先由擁有者改為「限制存取」，或至少取消任何人可編輯，再使用 GitHub 長期索引。此 repo 只保存程式、可公開的研究筆記、去識別後的摘要，**不能發布 Drive 的原始論文、PDF、檔案 ID、公開分享連結或 service account key**。

## 在已合法授權的本機環境執行

```bash
python -m pip install google-api-python-client google-auth
# 環境變數必須在本機私有設定／已授權 GitHub Secrets 中安全注入：
# GDRIVE_SERVICE_ACCOUNT_JSON=<完整服務帳號 JSON，勿加入任何 commit>
# GDRIVE_ROOT_FOLDER_ID=<指定資料夾 ID，勿加入任何 commit>
python research/scripts/drive_source_bridge.py --max-files 2000
# 需要取得原件時（仍只儲存在 private_sources，不能 commit）：
python research/scripts/drive_source_bridge.py --download --max-files 2000 --max-file-bytes 30000000
```

預設僅產生 `private_sources/drive_source_bridge/manifest_private.json`，不下載內容；`--download` 才會保存符合大小限制且非 Google 原生文件的原始件。大型 ZIP 會依上限跳過，避免失控同步。Google 原生 Docs/Sheets/Slides 如需內文需後續依類型另行匯出，不當作 PDF 下載。原始來源的引用與授權仍須逐件核對。

## 課程 37 研究入口與寫作順序

第 37–41 課共享的 Google Drive evidence pool 目前提供共用來源表、`claims_evidence.csv`、`indicator_series.csv`、`literature_reviews`、企業年報、原始 PDF/HTML 與 gaps；其中 **37 課尚缺文策院 2024 四冊完整原文、2025 消費調查交叉表、台灣新聞／出版原始時間序列**。第 37 課的撰寫母稿獨立放於 `editorial/lessons/lesson-37/draft.md`；研究充足且四關審查後才將它改編成 `docs/lesson-37-reading.html` 並更新網站入口。不在此步驟更動現行 `main` 網站。
