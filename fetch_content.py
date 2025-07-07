import pandas as pd
import requests
from bs4 import BeautifulSoup
import chardet

input_file = "/Applications/SMU/Great Eastern/Personal Project/RFM Project/Dataset/search_results_20250706_192342.xlsx"
output_file = "/Applications/SMU/Great Eastern/Personal Project/RFM Project/Dataset/search_results_with_content.xlsx"

df = pd.read_excel(input_file, sheet_name="简化数据")

def fetch_article_content(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        detected = chardet.detect(response.content)
        response.encoding = detected['encoding'] or 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all('p')
        content = '\n'.join(p.get_text(strip=True) for p in paragraphs)
        return content if len(content) > 100 else None
    except:
        return None

print("⏳ 正在抓取正文内容...")
df["content"] = df["url"].apply(fetch_article_content)
df.to_excel(output_file, index=False)
print(f"✅ 爬取完成，已保存到：{output_file}")
