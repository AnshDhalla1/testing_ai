RESUME_EXTRACTION_PROMPT = r"""
# 指令書：履歴書解析・構造化タスク

## **基本原則**
1. 日本語履歴書の内容を正確に解析し、**定義済みスキーマ** に厳密に従って構造化データを出力すること。  
2. **原文の日本語表現は変更せず**、情報の抽出と正規化のみを実施する。  
3. 曖昧な情報は推測せず、**明示的に記載がない場合は、フィールドを省略する**（`None` や `"なし"` は返さない）。  
4. **スキーマに沿ったカテゴリ分類を厳守し、データの混在を防ぐ**（例: プログラミング言語とフレームワークを区別）。  

---

## **1. 個人情報 (Personal Information)**
- **履歴書の冒頭または最初のセクション** から以下の情報を抽出：
  - **氏名:** フルネーム（姓と名の間に半角スペースを含める）。  
  - **作成日:** 履歴書の更新日（フォーマット: `YY/MM/DD`）。  
  - **年齢:** 生年月日 (`YYYY/MM/DD`) がある場合のみ計算（満年齢）。  
  - **性別:** `"男性"`, `"女性"`, `"その他"`, `"回答なし"` のみ許容。  
  - **最寄駅:** `「路線名 駅名」` の形式（例: `"山手線 新宿駅"`）。  
  - **最終学歴:** `"高等学校"`, `"学士"`, `"修士"`, `"博士"`, `"その他"` に分類。  

**⚠️ 注意:**  
❌ **推測しない。履歴書にない情報は省略する。**  
❌ **「性別不明」や「記載なし」の場合、`None` を返す（デフォルト値を入れない）。**  

---

## **2. 希望条件 (Desired Preferences)**
- **「希望条件」または「希望勤務地」セクション** から以下を抽出：
  - **希望勤務地:** `"関東"`, `"関西"`, `"東海"`, `"中部"`, `"九州"`, `"中国"`, `"東北"`, `"北信越"` のみ。  
  - **休日勤務:** `"相談可"` または `"不可"` のみ。  
  - **月間総労働時間:** `"相談可"`, `"不可"`, `"180h以内"`, `"200h以内"` のみ。  
  - **出張可否:** `"相談可"` または `"不可"` のみ。  

**⚠️ 注意:**  
❌ **表記が異なっても、スキーマの選択肢に正規化する（例: `"週末勤務OK"` → `"相談可"`）。**  
❌ **曖昧な表現（"場合による", "応相談" など）は `"相談可"` に統一する。**  

---

## **3. 資格 (Certification)**
- **資格が記載されている場合のみ** 以下を抽出：
  - **資格名:** 公式名称（例: `"AWS Certified Solutions Architect - Associate"`）。  
  - **取得年:** `YYYY` 形式で記録。  
  - **取得月:** `1-12` の整数（バージョンやレベル情報を含めない）。  

**⚠️ 注意:**  
❌ **資格がない場合、`[]` (空リスト) を返す（`None` や `"なし"` は使用しない）。**  

---

## **4. スキル要約 (Summary of Skills)**
- **「自己PR」,「スキル要約」,「職務要約」 セクション** からスキルや強みを抽出：
  - **記述されている場合のみ出力**。  
  - **プログラミングスキル, リーダーシップ, DevOpsスキル, 管理経験 などを含む。**  

❌ **職務経歴の詳細や技術スキル評価と重複しないようにする。**  

---

## **5. 職務経歴詳細 (Work Experience Detail)**
- **履歴書の「職務経歴」または「経験」セクション** から以下を抽出：
  - **会社名, 事業内容, 期間開始 (`YYYY/MM/DD`), 期間終了 (`YYYY/MM/DD` or `"現在"`), プロジェクト名**  
  - **業務内容:** ビジネスコンテンツセクションの技術的な記述のみ。**チーム情報や役割は含めない**。  
  - **使用技術:** 言語 (`Java, Python`), OS (`Windows, Linux`), ツール (`Git, Docker`) に分類。  
  - **役割:** `"メンバー"`, `"リーダー"`, `"PM"` など事前定義リストに従う。  
  - **チーム規模:** `"1～5名"`, `"6～10名"` などのリストから選択。  
  - **担当工程:** `"要件定義"`, `"基本設計"`, `"詳細設計"`, `"製造・実装"`, `"テスト"`, `"保守・運用"` のみ。  

**⚠️ 注意:**  
❌ **業務内容に「プロジェクトの目的」や「成果」は含めない（技術内容のみ）。**  
❌ **使用技術はカテゴリ別に分け、リスト形式で提供（例: `"言語": ["Java", "Python"]`）。**  

---

## **6. 技術スキル評価 (Technical Skill Evaluation)** ###(MUST BE INCLUDED IF PRESENT)###
- **履歴書の「スキル」「技術経験」セクション** から以下を抽出し、A～Eで評価：
  - **業務範囲 (企画提案, 要件定義 など)**
  - **OS (Windows, Linux, Mac)**
  - **言語 (Java, Python, JavaScript)**
  - **データベース (MySQL, PostgreSQL)**
  - **フレームワーク (React, Django)**
  - **クラウドサービス (AWS, Azure)**
  - **CI/CDツール (GitHub Actions, CircleCI)**
  - **監視ツール (Datadog, NewRelic)**
  - **CRM (Salesforce, Kintone)**

技術スキルの抽出と分類 (Extract and Categorize Technical Skills)
提供された履歴書から以下の構造に従い、技術スキルを抽出し分類してください。
(Extract and categorize technical skills from the provided resume based on the following structure.)

{
    "スキル評価 (Skill Evaluation)": {
        "OS": { "<OS Name>": "<習熟度 (Proficiency Level)>" },
        "言語 (Languages)": { "<Programming Language>": "<習熟度 (Proficiency Level)>" },
        "データベース (Databases)": { "<Database>": "<習熟度 (Proficiency Level)>" },
        "フレームワーク評価 (Frameworks)": { "<Framework>": "<習熟度 (Proficiency Level)>" },
        "クラウドサービス (Cloud Services)": { "<Cloud Service>": "<習熟度 (Proficiency Level)>" },
        "CRM": { "<CRM Tool>": "<習熟度 (Proficiency Level)>" }
    }
}
分類基準 (Classification Criteria)
オペレーティングシステム (OS)
履歴書内の Windows, Linux, Mac などのオペレーティングシステムを特定し、適切な習熟度を割り当てる。
(Identify and classify operating systems such as Windows, Linux, Mac, and assign an appropriate proficiency level.)

プログラミング言語 (Languages)
Java, Python, PHP, JavaScript などのプログラミング言語を抽出し、バージョン情報も考慮する。
(Extract programming languages like Java, Python, PHP, JavaScript, and consider version details.)

データベース (Databases)
SQL Server, MySQL, PostgreSQL, Oracle などのデータベース技術を分類し、バージョン情報がある場合は保持する。
(Identify SQL Server, MySQL, PostgreSQL, Oracle, and keep version details if available.)

フレームワーク (Frameworks)
Spring Boot, Laravel, Ruby on Rails, Vue.js などのフレームワークを分類する。
(Identify frameworks such as Spring Boot, Laravel, Ruby on Rails, Vue.js.)

クラウドサービス (Cloud Services)
AWS, GCP, Datadog などのクラウドプラットフォームや監視ツールを分類する。
(Identify cloud platforms and monitoring tools like AWS, GCP, Datadog.)

CRMツール (CRM Tools)
Salesforce, Kintone などのCRMツールを分類する。
(Classify CRM tools like Salesforce, Kintone.)

習熟度の定義 (Proficiency Levels Definition)
習熟度は以下の基準に基づいて割り当てる：
(Assign proficiency levels based on the following criteria:)

A（上級 / Advanced）: 幅広い経験を持ち、プロジェクトリーダーまたは技術リードとして関与できる。
(Extensive experience, capable of leading projects as a technical lead.)
B（中級 / Intermediate）: 実務経験があり、設計・実装に関する十分な知識を持っている。
(Hands-on experience, proficient in design and implementation.)
C（初級 / Beginner）: 基礎知識があり、プロジェクトでの使用経験がある。
(Basic knowledge with some project involvement.)
E（専門家 / Expert）: 深い専門知識を持ち、システム設計や最適化に関与できる。
(Deep specialization, capable of system design and optimization.)


**🔹 追加ルール**:
✅ **バージョン情報を削除（例: `"Python3.11"` → `"Python"`）**  
✅ **スラッシュ・カンマで結合された技術を個別に分割**  
✅ **評価がない場合、そのフィールドを省略（`NA` は返さない）**  

---

## **🔹 最終確認**
✔ スキーマ通りの構造で情報を分類すること  
✔ **曖昧な情報は推測しない**  
✔ 利用可能な開始日と履歴書の作成日を混同しないでください

------------
以下は解析対象の履歴書です
"""
