from typing import Optional, List, Dict, Literal
from pydantic import BaseModel, Field
    
class 個人情報(BaseModel):
    """
    * 年齢は生年月日から算出可能な場合のみ出力。  
    """

    氏名: Optional[str] = Field(
        None,
        description="候補者のフルネーム。姓と名の間に半角スペースを含める。",
        example="宮本 雅人"
    )
    作成日: Optional[str] = Field(
        None,
        description="履歴書の更新日。YY/MM/DD 形式で表記。",
        example="23/09/15"
    )
    年齢: Optional[int] = Field(
        None,
        description="候補者の満年齢。生年月日が履歴書に記載されている場合のみ算出可能。",
        example=28
    )

    性別: Optional[Literal["男性", "女性", "その他", "回答しない"]] = Field(
        None,
        description="候補者の性別（提供されている場合のみ）。",
        example="男性"
    )
    国籍: Optional[str] = Field(
        None,
        description="候補者の国籍。履歴書に記載がある場合のみ出力。",
        example="日本"
    )
    最寄駅: Optional[str] = Field(
        None,
        description="最寄り駅の路線名と駅名。半角スペースで区切る",
        example="山手線 新宿駅"
    )

    最終学歴: Optional[str] = Field(
        None,
        description="候補者の最終学歴。履歴書に記載がある場合のみ出力。",
        example="修士"
    )

class 希望条件(BaseModel):
    """
    候補者の希望する勤務条件を記載するセクション。  
    * 履歴書に記載されている場合のみ出力。   
    """

    希望地域: Optional[Literal["関東", "関西", "東海", "中部", "九州", "中国", "東北", "北信越"]] = Field(
        None,
        description="希望する勤務地",
        example="関東"
    )

    休日作業可否: Optional[Literal["相談可", "不可"]] = Field(
        None,
        description="休日勤務の可否",
        example="相談可"
    )

    稼働範囲: Optional[Literal["相談可", "不可", "180h以内", "200h以内"]] = Field(
        None,
        description="月間の総労働時間の希望",
        example="相談可"
    )

    出張可否: Optional[Literal["相談可", "不可"]] = Field(
        None,
        description="出張が可能かどうか",
        example="不可"
    )

class 資格(BaseModel):
    """
    候補者が取得した資格・認定情報を記載するセクション。  
    * 複数資格がある場合はリスト形式で提供。  
    """

    資格名: Optional[str] = Field(
        None,
        description="資格の正式名称",
        example="AWS Certified Solutions Architect"
    )
    年: Optional[int] = Field(
        None,
        description="資格を取得した年",
        example=2022
    )
    月: Optional[Literal[1,2,3,4,5,6,7,8,9,10,11,12]] = Field(
        None,
        description="資格を取得した月（1〜12）",
        example=12
    )

class スキル要約(BaseModel):

    自己PR: Optional[str] = Field(
        None,
        description="SelfPR セクションのすべてを表示する",
        example=(
            "■ プログラミングスキル\n"
            "C, Scala, Python, JavaScript などの経験があり、コードの可読性を重視。\n\n"
            "■ リーダーシップスキル\n"
            "アジャイル開発チームのリーダー経験があり、開発プロセスの改善を推進。"
        )
    )

class 職務経歴詳細(BaseModel):
    """
    候補者の職務経歴の詳細を記載するセクション。  
    * 履歴書に記載された情報のみ含める。
    """

    会社名: Optional[str] = Field(
        None, 
        description="勤務していた会社名", 
        example="株式会社V"
    )
    事業内容: Optional[str] = Field(
        None, 
        description="会社名の直後の「事業内容:」フィールドの正確な値",
        example="事業開発"      
    )
    期間開始: Optional[str] = Field(
        None,
        description="勤務開始日 (YYYY/MM/DD形式)",
        example="2020/01/01"
    )
    期間終了: Optional[str] = Field(
        None,
        description="勤務終了日 (YYYY/MM/DD形式) または '現在'",
        example="2021/06/30"
    )
    プロジェクト名: Optional[str] = Field(
        None,
        description="プロジェクトの名前またはタイトル （履歴書に記載されている場合のみ出力）",
        example="弊社Webサイトの刷新"
    )
    業務内容: Optional[str] = Field(
        None,
        description="ビジネスコンテンツセクションからの簡潔な技術的な説明のみ、チーム そして 役割の参照を除く",
        example=(
            "インフラエンジニアSRE：Terraformを使用したIaC変革環境に参加。"
            "AWS EC2およびECSの運用を担当し、インフラストラクチャの設定を改善しました。\n"
            "GitHub Actionsを使用してE2Eテストの自動化を実装しました。\n"
            "Vitestを使用してJavaScriptベースのユニットテストを実施しました。\n"
            "バグを最小限に抑えるための効率化された開発環境。"
        )
    )
    使用言語: Optional[List[str]] = Field(
        None,
        description="プロジェクトで使用されるプログラミング言語とライブラリのリスト。技術的な文脈で明示的に言及されています。",
        example=["Java", "JavaScript", "Ruby on Rails"]
    )
    サーバOS: Optional[List[str]] = Field(
        None,
        description="サーバーテクノロジー、オペレーティングシステム、または使用されるデータベースのリスト",
        example=["Ubuntu", "Windows", "MySQL"]
    )
    ツールなど: Optional[List[str]] = Field(
        None,
        description="プロジェクトで使用したツール・ミドルウェア（履歴書の記載通り）",
        example=["Git", "Docker", "Eclipse"]
    )

    役割: Optional[Literal["メンバー", "リーダー", "マネージャー", "PM", "PMO", "PdM", "PO", "テックリード"]] = Field(
        None,
        description="候補者のプロジェクトにおける主な役割。 彼の役割に基づいて選択してください",
        example="リーダー"
    )

    規模: Optional[Literal["1～5名", "6～10名", "11～50名", "51名～99名", "100名以上"]] = Field(
        None,
        description="履歴書の「チーム: X」から抽出したチームの人数",
        example="6～10名"
    )

    担当工程: Optional[List[Literal[
        "要件定義", "基本設計", "詳細設計", "製造・実装", "テスト", "保守・運用"
    ]]] = Field(
        None,
        description="プロジェクト中に候補者が担当したプロセスの一覧 （履歴書の表から取得）。",
        example=["要件定義", "基本設計", "詳細設計",]
    )

class SkillDetail(BaseModel):
    評価: Literal["A", "B", "C", "D", "E"]
    年: Optional[str] = None  # e.g., "5 years"

class 技術スキル評価(BaseModel):
    業務範囲: Optional[Dict[str, SkillDetail]] = Field(
        None,
        description="事前定義された業務範囲の評価と経験年数。",
        example={
            "システム企画提案": {"評価": "A", "年": "5 years"},
            "基本設計": {"評価": "B", "年": "3 years"}
        }
    )
    OS: Optional[Dict[str, SkillDetail]] = Field(
        None,
        description="使用経験のあるオペレーティングシステムの評価と経験年数。",
        example={
            "Windows": {"評価": "B", "年": "2 years"},
            "Linux": {"評価": "A", "年": "7 years"}
        }
    )
    言語: Optional[Dict[str, SkillDetail]] = Field(
        None,
        description="プログラミング言語の評価と経験年数。",
        example={
            "Python": {"評価": "A", "年": "5 years"},
            "JavaScript": {"評価": "B", "年": "3 years"}
        }
    )
    データベース: Optional[Dict[str, SkillDetail]] = Field(
        None,
        description="データベースの評価と経験年数。",
        example={
            "MySQL": {"評価": "A", "年": "8 years"},
            "PostgreSQL": {"評価": "B", "年": "4 years"}
        }
    )
    フレームワーク評価: Optional[Dict[str, SkillDetail]] = Field(
        None,
        description="フレームワークやライブラリの評価と経験年数。",
        example={
            "React": {"評価": "A", "年": "4 years"},
            "Django": {"評価": "B", "年": "2 years"}
        }
    )
    クラウドサービス: Optional[Dict[str, SkillDetail]] = Field(
        None,
        description="クラウドサービスの評価と経験年数。",
        example={
            "AWS": {"評価": "A", "年": "6 years"},
            "Azure": {"評価": "C", "年": "1 year"}
        }
    )
    crm: Optional[Dict[str, SkillDetail]] = Field(
        None,
        description="CRMプラットフォームの評価と経験年数。",
        example={
            "Salesforce": {"評価": "B", "年": "5 years"},
            "Kintone": {"評価": "A", "年": "3 years"}
        }
    )





class ResumeSchema(BaseModel):
    """
    日本の履歴書の標準スキーマ。  
    * 履歴書に記載された情報のみを含め、欠落している情報は出力されません。  
    """

    個人的: Optional[個人情報] = Field(
        None,
        description="候補者の基本個人情報を含むセクション。氏名、作成日, 生年月日、性別、最寄駅、学歴などが含まれます。"
    )
    望ましい: Optional[希望条件] = Field(
        None,
        description="候補者の希望する勤務条件を記載。勤務地、リモート可否、希望労働時間、休日勤務可否、出張可否を含む。"
                    "履歴書に記載がある場合のみ出力されます。"
    )
    資格_: Optional[List[資格]] = Field(
        None,
        description="候補者が取得した資格・認定情報のリスト。資格名と取得年月を含む。"
                    "資格が履歴書に記載されていない場合は出力されません。"
    )
    スキルサマリー: Optional[スキル要約] = Field(
        None,
        description="候補者のスキルセットと自己PRを要約するセクション。プログラミングスキル、リーダーシップ、教育スキルなどを含む。"
    )
    職歴: Optional[List[職務経歴詳細]] = Field(
        None,
        description="候補者の職務経歴の詳細リスト。会社名、業務内容、期間、プロジェクト、担当フェーズ、技術スタック、チーム規模、職位を含む。"
    )
    スキル評価: Optional[技術スキル評価] = Field(
        None,
        description="候補者の技術スキルを評価するセクション。使用経験のあるOS、プログラミング言語、データベース、フレームワーク、クラウドサービス、CI/CDツールなどが含まれます。"
    )
