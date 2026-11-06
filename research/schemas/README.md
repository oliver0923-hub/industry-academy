# Schema 與使用限制

所有 CSV 為 UTF-8，空字串代表未知，不以 0 代替。代碼、lesson_id 一律字串讀入（保留前導零）。主鍵：source_id、paper_id、filing_id；分類為 system/version/code；矩陣為 lesson_id/reference_id/source_role。外鍵必須存在。license=unknown 不代表開放授權。

source_registry：source_id,agency,dataset,measure,definition,unit,nominal_real,geography,frequency,coverage,update_frequency,url,license,access_status,lesson_ids,downloaded_on,verification_status。入口核對與資料取回分開。
literature_master：paper_id,authors,year,title,journal_or_publisher,publication_type,peer_reviewed,doi,landing_url,oa_url,access_status,license,theory,mechanism,industry_scope,lesson_ids,bibliographic_verified,fulltext_verified,notes；額外 volume/issue/pages/metadata_url 等為追溯欄位。Crossref 的 journal-article 類型不能單獨證明同行評審。
industry_lesson_matrix：lesson_id,reference_id,reference_type,source_role,confidence,verified_at,status。confidence 僅文字依據（official publisher / curated candidate），不是統計機率。
company_filings：filing_id,issuer,identifier,ticker,fiscal_year,reporting_currency,audited,source_url,filing_date,geography,lesson_ids,status。IR 主頁只能為 candidate，不可標示 filing_verified。
classification_master：system/version/code/label/definition/url/accessed_at/level/parent_code/verification_status。空定義代表尚未取得，標籤不可冒充完整活動定義。
classification_crosswalk：from_system/from_version/from_code/to_system/to_version/to_code/verified/confidence/notes/url。官方表未完成列解析時只記 artifact 索引，不猜配對。
indicator_dictionary：指標分開定義，不能加總營收、GDP、出口、市值、產能、市場規模。
audit/download_log：實際 HTTP 狀態、下載格式、bytes、SHA-256、失敗原因與本機相對路徑；不提交 cookies、token 或原始下載內容。

## v2增補schema與狀態

原主鍵/舊欄位保留，僅追加欄位。實際七CSV欄位由[full_acquisition_v2.json](full_acquisition_v2.json)列出；新增欄位與遷移處置見../audit/full-acquisition-v2/schema_migration.csv。catalog是source/paper/filing及深度document的聯合view，不將不同用途的記錄當作不同實體文件；原文可用數依SHA去重。未知日期、幣別、授權與期間留空或unknown，不能以抓取日期填充出版日期。

來源狀態：identified（候選）、metadata_verified（書目/詮釋核對）、abstract_reviewed（只讀摘要）、fulltext_downloaded（文件可取得）、fulltext_verified（實際原文版本核讀）、claim_verified（只對具定位的指定主張）、restricted、broken、superseded。實際傳輸狀態另有reused_existing、failed、budget_deferred；不與研究成熟度混為一欄。parsed_text_encoding_issue_needs_OCR表示PDF可開啟但文字不可信，不能讀作財務數字。

九類缺口的target_sources是研究目標，verified_evidence_count是已核對觀察/研究數，verified_source_count才是支持它們的來源數；不能拿前者直接填滿來源數目標。分類第12次為2026-01-01起有效，20大類；第11次878列保留歷史註記。新細碼crosswalk未核對前不得從標籤相似猜配。
