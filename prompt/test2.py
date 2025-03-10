RESUME_EXTRACTION_PROMPT = r"""

説明書 ： 
- 抽出された履歴書と構造化された出力スキーマを提供します。
- 明確に定義された階層セクションがあります。抽出したテキストをスキーマにマッピングする必要があります。そしてJSON出力を与えます。
- 職務経験は全て出力すること。履歴書内の異なるフォーマット（表形式・リスト形式）を全て解析し、欠損情報は null として出力すること。
- 注意すべき点は、職務経験はすべての経験を記入することです。
- そして、すべてのスキルはスキル評価で分類する必要があり、それらは常に履歴書に記載されます。
- 自己や職歴の業務内容を説明するため。最初の行だけではなく、常にコンテンツ全体を抽出してください。
- 履歴書にないことは想定しません。 

---
さて、以下の履歴書です。 100% 正確なマッピングが必要です。
"""
