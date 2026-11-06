# 深度證據品質檢查

{"passed": 49, "checks": 49, "failed": [], "open_lesson_gaps": 8, "full_lessons_ready": 0}

- PASS sources_keys: 28 distinct records required
- PASS observations_keys: 55 distinct records required
- PASS paper_reviews_keys: 10 distinct records required
- PASS company_cases_keys: 6 distinct records required
- PASS sufficiency_keys: 8 distinct records required
- PASS claims_keys: 42 distinct records required
- PASS gaps_keys: 8 distinct records required
- PASS source_url_unique: No exact duplicate evidence URL
- PASS all_source_bytes_match: []
- PASS observations_source_fk: set()
- PASS paper_reviews_source_fk: set()
- PASS company_cases_source_fk: set()
- PASS audit_opinions_source_fk: set()
- PASS observations_metadata: All numeric observations have units/period/scope/locator/caution; values may be rounded/lower bounds
- PASS TYSON_income_original_page: PDF45; missing numeric tokens=[]
- PASS DACHAN_income_original_page: PDF8; missing numeric tokens=[]
- PASS INTEL_income_original_page: PDF65; missing numeric tokens=[]
- PASS TSMC_income_original_page: PDF64; missing numeric tokens=[]
- PASS JPMBANK_income_original_page: PDF5; missing numeric tokens=[]
- PASS MEGA_income_original_page: PDF13; missing numeric tokens=[]
- PASS jpm_assets_original: Bank subsidiary consolidated balance, not holding group
- PASS mega_assets_original: Bank consolidated balance
- PASS tsmc_duplicate_financial_table: Both annual variants financial page64 match after whitespace normalization; original files/SHA retained
- PASS tsmc_iasb_profit_conflict_retained: Different reporting basis retained; no artificial reconciliation
- PASS taiwan_bank_snapshot_keys: ROC113 December,38 unique reporting entries
- PASS regulatory_mega_original: Regulatory row retained; no replacement by annual consolidated value
- PASS conceptual_papers_no_invented_sample: Theoretical model time/publication years not sample periods
- PASS gvc_versions_distinct: Both versions read; original2005 Table1 has its own printed p87
- PASS mof_primary_value: Original MOF preliminary2024 total, USD million; not rounded CBC figure
- PASS dynamic_capability_version: 1997 processes/positions/paths; later framework not backdated
- PASS pnas_locator_not_fabricated: HTML fulltext read; exact print-page locator not invented
- PASS pnas_design_not_panel: Income location FE vs individual labor household FE separated
- PASS barney_vrin: Original1991 attributes not later framework
- PASS hendersongeneration_measure: Table2 not annual market share
- PASS only_eight_sufficiency_records: No added industries
- PASS no_false_complete_status: All eight retain full-lesson gaps; structural pass does not promote status
- PASS six_company_cases: One global and one Taiwan firm for each demonstration industry
- PASS operating_indicator_each_case: Each case links a specific segment, operating or loan indicator
- PASS six_audit_opinion_locators: Opinion scope/year separate from financial figure scope
- PASS evidence_relative_links: []
- PASS lesson_00_pack: Evidence/pending/limitations separated
- PASS lesson_01_pack: Evidence/pending/limitations separated
- PASS lesson_02_pack: Evidence/pending/limitations separated
- PASS lesson_03_pack: Evidence/pending/limitations separated
- PASS lesson_04_pack: Evidence/pending/limitations separated
- PASS lesson_05_pack: Evidence/pending/limitations separated
- PASS lesson_18_pack: Evidence/pending/limitations separated
- PASS lesson_31_pack: Evidence/pending/limitations separated
- PASS unselected_lessons_unchanged: ['research/notes/lessons/lesson-00/acquisition-v2.md', 'research/notes/lessons/lesson-00/index.md', 'research/notes/lessons/lesson-01/acquisition-v2.md', 'research/notes/lessons/lesson-01/index.md', 'research/notes/lessons/lesson-02/acquisition-v2.md', 'research/notes/lessons/lesson-02/index.md', 'research/notes/lessons/lesson-03/acquisition-v2.md', 'research/notes/lessons/lesson-03/index.md', 'research/notes/lessons/lesson-04/acquisition-v2.md', 'research/notes/lessons/lesson-04/index.md', 'research/notes/lessons/lesson-05/acquisition-v2.md', 'research/notes/lessons/lesson-05/index.md', 'research/notes/lessons/lesson-06/acquisition-v2.md', 'research/notes/lessons/lesson-07/acquisition-v2.md', 'research/notes/lessons/lesson-08/acquisition-v2.md', 'research/notes/lessons/lesson-09/acquisition-v2.md', 'research/notes/lessons/lesson-10/acquisition-v2.md', 'research/notes/lessons/lesson-11/acquisition-v2.md', 'research/notes/lessons/lesson-12/acquisition-v2.md', 'research/notes/lessons/lesson-13/acquisition-v2.md', 'research/notes/lessons/lesson-14/acquisition-v2.md', 'research/notes/lessons/lesson-15/acquisition-v2.md', 'research/notes/lessons/lesson-16/acquisition-v2.md', 'research/notes/lessons/lesson-17/acquisition-v2.md', 'research/notes/lessons/lesson-18/acquisition-v2.md', 'research/notes/lessons/lesson-18/index.md', 'research/notes/lessons/lesson-19/acquisition-v2.md', 'research/notes/lessons/lesson-20/acquisition-v2.md', 'research/notes/lessons/lesson-21/acquisition-v2.md', 'research/notes/lessons/lesson-22/acquisition-v2.md', 'research/notes/lessons/lesson-23/acquisition-v2.md', 'research/notes/lessons/lesson-24/acquisition-v2.md', 'research/notes/lessons/lesson-25/acquisition-v2.md', 'research/notes/lessons/lesson-26/acquisition-v2.md', 'research/notes/lessons/lesson-27/acquisition-v2.md', 'research/notes/lessons/lesson-28/acquisition-v2.md', 'research/notes/lessons/lesson-29/acquisition-v2.md', 'research/notes/lessons/lesson-30/acquisition-v2.md', 'research/notes/lessons/lesson-31/acquisition-v2.md', 'research/notes/lessons/lesson-31/index.md', 'research/notes/lessons/lesson-32/acquisition-v2.md', 'research/notes/lessons/lesson-33/acquisition-v2.md', 'research/notes/lessons/lesson-34/acquisition-v2.md', 'research/notes/lessons/lesson-35/acquisition-v2.md', 'research/notes/lessons/lesson-36/acquisition-v2.md', 'research/notes/lessons/lesson-37/acquisition-v2.md', 'research/notes/lessons/lesson-38/acquisition-v2.md', 'research/notes/lessons/lesson-39/acquisition-v2.md', 'research/notes/lessons/lesson-40/acquisition-v2.md', 'research/notes/lessons/lesson-41/acquisition-v2.md', 'research/notes/lessons/lesson-42/acquisition-v2.md', 'research/notes/lessons/lesson-43/acquisition-v2.md', 'research/notes/lessons/lesson-44/acquisition-v2.md', 'research/notes/lessons/lesson-45/acquisition-v2.md', 'research/notes/lessons/lesson-46/acquisition-v2.md', 'research/notes/lessons/lesson-47/acquisition-v2.md', 'research/notes/lessons/lesson-48/acquisition-v2.md', 'research/notes/lessons/lesson-49/acquisition-v2.md']; only legacy index.md constrained, new v2 acquisition notes for all50 explicitly authorized

上述為證據鏈與內容約束檢查。全課充分性是另一道門檻，8課均有開放缺口，0課宣稱完整就緒。
