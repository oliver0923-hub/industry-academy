# 品質驗證報告

40/40 結構與保全檢查通過。

- PASS classification_crosswalk_unique: 1808 rows; keys ['from_system', 'from_version', 'from_code', 'to_system', 'to_version', 'to_code']
- PASS classification_crosswalk_utf8_no_bom: pandas read with string dtypes
- PASS classification_master_unique: 4609 rows; keys ['system', 'version', 'code']
- PASS classification_master_utf8_no_bom: pandas read with string dtypes
- PASS company_filings_unique: 79 rows; keys ['filing_id']
- PASS company_filings_utf8_no_bom: pandas read with string dtypes
- PASS indicator_dictionary_unique: 10 rows; keys ['indicator_id']
- PASS indicator_dictionary_utf8_no_bom: pandas read with string dtypes
- PASS industry_lesson_matrix_unique: 670 rows; keys ['lesson_id', 'reference_id', 'source_role']
- PASS industry_lesson_matrix_utf8_no_bom: pandas read with string dtypes
- PASS literature_master_unique: 35 rows; keys ['paper_id']
- PASS literature_master_utf8_no_bom: pandas read with string dtypes
- PASS source_registry_unique: 51 rows; keys ['source_id']
- PASS source_registry_utf8_no_bom: pandas read with string dtypes
- PASS DOI_unique: 29 nonempty DOIs
- PASS 50_lessons: IDs 00–49 preserved
- PASS source_foreign_keys: []
- PASS paper_foreign_keys: []
- PASS filing_foreign_keys: []
- PASS global_candidate_coverage: 50/50; candidate coverage is not evidence completeness
- PASS taiwan_candidate_coverage: 50/50; candidate coverage is not evidence completeness
- PASS theory_candidate_coverage: 50/50; candidate coverage is not evidence completeness
- PASS firm_candidate_coverage: 50/50; candidate coverage is not evidence completeness
- PASS no_teaching_ready: No published lessons implied
- PASS TW11_sections: 19 historical sections required
- PASS TW11_level_2: official manual required 88; range codes and ODT typo reconciled
- PASS TW11_level_3: official manual required 249; range codes and ODT typo reconciled
- PASS TW11_level_4: official manual required 522; range codes and ODT typo reconciled
- PASS NAICS2022_sectors: 20 sectors, including combined manufacturing/retail/transport codes
- PASS version_conflicts_quarantined: 658 mappings withheld from verified use
- PASS download_checksum: 176 success records matched bytes; mismatches []
- PASS unchanged_docs/index.html: same Git content vs origin/main; Windows checkout CRLF normalized
- PASS unchanged_docs/styles.css: same Git content vs origin/main; Windows checkout CRLF normalized
- PASS unchanged_docs/app.js: same Git content vs origin/main; Windows checkout CRLF normalized
- PASS private_not_tracked: No PDF/raw private data in public Git index
- PASS no_pdf_public: All PDFs local ignored only
- PASS one_card_per_paper: 35 cards expected
- PASS 50_lesson_source_packs: Per-lesson sources and gaps
- PASS industrial_data_unique: 124988 actual source rows
- PASS industrial_units: Volume index; cannot be treated as revenue/GDP

實質限制：URL HTTP成功不代表資料內容、授權、更新日或跨國可比性已核對。全文下載、身份核對、研究內容閱讀分開紀錄。期刊文章不一律為實證，也不一律經同等同行評審。分類版本衝突、受限平台及每課學術/年報缺口詳見 coverage_report.md 與 restricted_access_queue.md。
