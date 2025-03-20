import pandas as pd
from typing import Dict
from datetime import datetime
import calendar

def export_to_excel(parsed_json: Dict, output_file: str):
    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet("Resume")
        
        worksheet.set_column('A:A', 8)       
        worksheet.set_column('B:B', 20)      
        worksheet.set_column('C:C', 20)      
        worksheet.set_column('D:D', 12)      
        worksheet.set_column('E:E', 12)      
        worksheet.set_column('F:F', 30)      
        worksheet.set_column('G:G', 30)      
        worksheet.set_column('H:H', 20)      
        worksheet.set_column('I:I', 15)      
        worksheet.set_column('J:J', 20)      
        worksheet.set_column('K:K', 10)      
        worksheet.set_column('L:L', 10)      
        worksheet.set_column('M:M', 20)      
        
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 18,
            'align': 'center',
            'valign': 'vcenter',
            'border': 0
        })
        
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#B8CCE4',   
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True
        })
        
        section_header_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'bg_color': '#B8CCE4',   
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        
        subheader_format = workbook.add_format({
            'bg_color': '#B8CCE4',  
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
        })
        
        field_header_format = workbook.add_format({
            'bg_color': '#B8CCE4',   
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'text_wrap': True
        })
        
        data_format = workbook.add_format({
            'border': 1,
            'align': 'left',
            'valign': 'vcenter',
            'text_wrap': True
        })
        
        data_center_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True
        })
        
        number_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'num_format': '0'
        })
        
        row = 0   
        
        # --- Title Section ---
        worksheet.merge_range('A1:L1', '職務経歴書', title_format)
        if parsed_json.get('個人的') and parsed_json['個人的'].get('作成日'):
            worksheet.write(0, 13, '作成日：', field_header_format)
            worksheet.write(0, 14, parsed_json['個人的'].get('作成日', ''), data_format)
        row += 1
        
        # --- Personal Info Section ---
        if parsed_json.get('個人的'):
            personal_info = parsed_json['個人的']
            
            worksheet.write(row, 0, '氏名', field_header_format)
            worksheet.merge_range(row, 1, row, 3, personal_info.get('氏名', ''), data_format)
            worksheet.write(row, 4, '年齢', field_header_format)
            worksheet.write(row, 5, personal_info.get('年齢', ''), data_format)
            worksheet.write(row, 6, '歳', data_format)
            worksheet.write(row, 7, '性別', field_header_format)
            worksheet.write(row, 8, personal_info.get('性別', ''), data_format)
            row += 1
            
            worksheet.write(row, 0, '国籍', field_header_format)
            worksheet.merge_range(row, 1, row, 3, personal_info.get('国籍', ''), data_format)
            worksheet.write(row, 4, '最寄駅', field_header_format)
            worksheet.merge_range(row, 5, row, 6, personal_info.get('最寄駅', ''), data_format)
            worksheet.write(row, 7, '駅', data_format)
            worksheet.write(row, 8, '最終学歴', field_header_format)
            worksheet.merge_range(row, 9, row, 14, personal_info.get('最終学歴', ''), data_format)
            row += 2   
        
        # --- Desired Conditions Section ---
        if parsed_json.get('望ましい'):
            worksheet.merge_range(row, 0, row, 1, '参画可能時期', subheader_format)
            worksheet.write(row, 2, '年', subheader_format)
            worksheet.write(row, 3, '月', subheader_format)
            worksheet.write(row, 4, '日', subheader_format)
            worksheet.write(row, 5, '希望地域', subheader_format)
            worksheet.write(row, 6, '-', data_center_format)
            worksheet.write(row, 7, '休日作業可否', subheader_format)
            worksheet.write(row, 8, '-', data_center_format)
            worksheet.write(row, 9, '稼働範囲', subheader_format)
            worksheet.write(row, 10, '-', data_center_format)
            worksheet.write(row, 11, '出張可否', subheader_format)  
            worksheet.write(row, 12, '-', data_center_format)
            row += 1
        
            desired = parsed_json['望ましい']
            if desired.get('参画可能時期'):
                dates = desired['参画可能時期'].split('-')
                if len(dates) >= 3:
                    worksheet.write(row-1, 2, dates[0], data_center_format)  
                    worksheet.write(row-1, 3, dates[1], data_center_format)  
                    worksheet.write(row-1, 4, dates[2], data_center_format)  
            if desired.get('希望地域'):
                worksheet.write(row-1, 6, desired['希望地域'], data_center_format)
            if desired.get('休日作業可否'):
                worksheet.write(row-1, 8, desired['休日作業可否'], data_center_format)
            if desired.get('稼働範囲'):
                worksheet.write(row-1, 10, desired['稼動範囲'], data_center_format)
            if desired.get('出張可否'):
                worksheet.write(row-1, 12, desired['出張可否'], data_center_format)
            
            row += 1  # Add space
        
        # --- Qualifications Section ---
        if parsed_json.get('資格_'):
            # Qualifications header (as in Image 2)
            worksheet.write(row, 0, '資格', subheader_format)
            worksheet.merge_range(row, 1, row, 3, '', subheader_format)
            worksheet.write(row, 4, '年', subheader_format)
            worksheet.write(row, 5, '月', subheader_format)
            worksheet.merge_range(row, 6, row, 7, '', subheader_format)
            worksheet.write(row, 8, '年', subheader_format)
            worksheet.write(row, 9, '月', subheader_format)
            worksheet.merge_range(row, 10, row, 11, '', subheader_format)
            worksheet.write(row, 12, '年', subheader_format)
            worksheet.write(row, 13, '月', subheader_format)
            row += 1
            
            qualifications = parsed_json['資格_']
            qual_row = row
            for i, qual in enumerate(qualifications):
                if i % 3 == 0 and i > 0:
                    qual_row += 1
                col = (i % 3) * 4
                worksheet.merge_range(qual_row, col, qual_row, col+3, qual.get('資格名', ''), data_format)
                if i % 3 == 0:
                    worksheet.write(qual_row, 4, qual.get('年', ''), number_format)
                    worksheet.write(qual_row, 5, qual.get('月', ''), number_format)
                elif i % 3 == 1:
                    worksheet.write(qual_row, 8, qual.get('年', ''), number_format)
                    worksheet.write(qual_row, 9, qual.get('月', ''), number_format)
                elif i % 3 == 2:
                    worksheet.write(qual_row, 12, qual.get('年', ''), number_format)
                    worksheet.write(qual_row, 13, qual.get('月', ''), number_format)
            
            row = qual_row + 2  
        
        # --- Skills Summary Section ---
        if parsed_json.get('スキルサマリー'):
            worksheet.merge_range(row, 0, row, 1, 'スキル要約\n(自己PR)', subheader_format)
            skills_summary = parsed_json['スキルサマリー']
            worksheet.merge_range(row, 2, row, 14, skills_summary.get('自己PR', ''), data_format)
            row += 2  
        
        # --- Work History Section ---
        if parsed_json.get('職歴'):
            worksheet.write(row, 0, 'S.No', header_format)
            worksheet.merge_range(row, 1, row, 2, '期間', header_format)
            worksheet.merge_range(row, 3, row, 5, 'プロジェクト名\n業務内容', header_format)
            worksheet.merge_range(row, 6, row, 7, '使用言語\nライブラリ', header_format)
            worksheet.merge_range(row, 8, row, 9, 'サーバ/OS\nDB/サーバ', header_format)
            worksheet.merge_range(row, 10, row, 11, 'FW・MW\nツールなど', header_format)
            worksheet.write(row, 12, '役割\n規模', header_format)
            
            worksheet.merge_range(row, 13, row, 19, '担当工程', header_format)
            row += 1
            
            process_phases = ['要\n件\n定\n義', '基\n本\n設\n計', '詳\n細\n設\n計', '製\n造', 'テ\nス\nト', '保\n守\n運\n用']
            for i, phase in enumerate(process_phases):
                worksheet.write(row-1, 13+i, phase, header_format)
            
            work_history = parsed_json['職歴']
            
            for i, entry in enumerate(work_history):
                entry_num = i + 1
                
                company_row = row
                worksheet.write(company_row, 0, entry_num, data_center_format)  # S.No
                worksheet.write(company_row, 1, f"株式会社{entry.get('会社名', '')}", data_format)
                row += 1
                
                period_row = row
                start_period = entry.get('期間開始', '')
                end_period = entry.get('期間終了', '') if entry.get('期間終了') else '現在'
                period_text = f"{start_period}\n~\n{end_period}"
                worksheet.merge_range(period_row, 1, period_row+1, 2, period_text, data_center_format)
                
                worksheet.merge_range(period_row, 3, period_row+1, 5, entry.get('プロジェクト名', '') + "\n" + entry.get('業務内容', ''), data_format)
                
                languages = entry.get('使用言語', [])
                if isinstance(languages, list):
                    languages = ', '.join(languages)
                
                server_os = entry.get('サーバOS', [])
                if isinstance(server_os, list):
                    server_os = ', '.join(server_os)
                
                tools = entry.get('ツールなど', [])
                if isinstance(tools, list):
                    tools = ', '.join(tools)
                
                worksheet.merge_range(period_row, 6, period_row+1, 7, languages, data_format)
                worksheet.merge_range(period_row, 8, period_row+1, 9, server_os, data_format)
                worksheet.merge_range(period_row, 10, period_row+1, 11, tools, data_format)
                
                worksheet.write(period_row, 12, '役割', subheader_format)
                worksheet.write(period_row+1, 12, entry.get('役割', ''), data_center_format)
                
                if isinstance(entry.get('担当工程'), list):
                    phases = entry.get('担当工程', [])
                    all_phases = ['要件定義', '基本設計', '詳細設計', '製造', 'テスト', '保守運用']
                    for j, phase in enumerate(all_phases):
                        if phase in phases:
                            worksheet.write(period_row, 13+j, '○', data_center_format)
                        else:
                            worksheet.write(period_row, 13+j, '-', data_center_format)
                
                def parse_date(date_str):
                    try:
                        if len(date_str.split('/')) == 2:
                            year, month = date_str.split('/')
                            return datetime(int(year), int(month), 1)
                        else:
                            return datetime.strptime(date_str, "%Y-%m-%d")
                    except (ValueError, AttributeError):
                        return None

                if end_period == '現在':
                    end_date = datetime.now()
                else:
                    end_date = parse_date(end_period)

                start_date = parse_date(start_period)

                if start_date and end_date:
                    years = end_date.year - start_date.year
                    months = end_date.month - start_date.month
                    
                    if months < 0:
                        years -= 1
                        months += 12
                    
                    period_text = f"{years}年{months}ヶ月"
                else:
                    period_text = '期間不明'

                worksheet.write(period_row + 2, 1, period_text, data_center_format)
                
                worksheet.write(period_row + 2, 12, '規模', subheader_format)
                worksheet.write(period_row + 3, 12, entry.get('規模', ''), data_center_format)
                
                row += 3  
                
            row += 1  
            
        # --- Skills Evaluation Section ---
        if parsed_json.get('スキル評価'):
            worksheet.merge_range(row, 0, row, 10, '■スキル(評価レベル)', data_format)
            row += 1
            
            skills_evaluation = parsed_json['スキル評価']
            max_category_height = 0
            for category, skills in skills_evaluation.items():
                if skills:
                    max_category_height = max(max_category_height, len(skills))
            
            col_starts = {}
            current_col = 0
            
            worksheet.merge_range(row, current_col, row+max_category_height, current_col, '職種', field_header_format)
            current_col += 1
            
            for category, skills in skills_evaluation.items():
                if skills:  
                    col_starts[category] = current_col
                    worksheet.merge_range(row, current_col, row, current_col + 1, category, header_format)
                    current_col += 2
            
            row += 1
            
            max_rows_used = 0
            category_row_map = {}  
            
            for category, skills in skills_evaluation.items():
                if category in col_starts and skills:
                    start_col = col_starts[category]
                    category_row_map[category] = 0
                    
                    for i, (skill_name, details) in enumerate(skills.items()):
                        current_row = row + i
                        
                        if category == '業務領域':
                            worksheet.write(current_row, 0, skill_name, data_format)
                        
                        worksheet.write(current_row, start_col, skill_name, data_format)
                        worksheet.write(current_row, start_col + 1, details.get('評価', '-'), data_center_format)
                        
                        category_row_map[category] = i + 1
                        max_rows_used = max(max_rows_used, i + 1)
            
            row += max_rows_used + 2  
        
    return output_file