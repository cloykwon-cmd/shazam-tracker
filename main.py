import requests
from datetime import datetime

def main():
    print("Shazam Korea Top 200 Real Data Collection Start...")
    
    # 샤잠 대한민국 Top 200 공식 API 엔드포인트
    url = "https://www.shazam.com/services/charts/v1.1/chart/world/KR"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9"
    }
    
    tracks = []
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        raw_tracks = data.get('tracks', [])
        
        for index, track in enumerate(raw_tracks, start=1):
            title = track.get('heading', {}).get('title', 'Unknown Title')
            artist = track.get('heading', {}).get('subtitle', 'Unknown Artist')
            
            # 샤잠 곡별 고유 상세 페이지 링크 추출
            share_url = track.get('share', {}).get('href', 'https://www.shazam.com')
            
            tracks.append({
                "rank": index,
                "artist": artist,
                "title": title,
                "shazam_url": share_url
            })
    except Exception as e:
        print(f"Error fetching chart: {e}")
        
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # README.md 마크다운 생성
    readme_content = f"""# 🚀 샤잠 대한민국 Top 200 실시간 발굴 리포트

> **마지막 업데이트:** `{today_str}` (실시간 데이터 연동 완료)  
> **총 수집 곡 수:** **{len(tracks)}곡**

---

### 📊 샤잠 대한민국 Top 200 실시간 순위 리포트

| 순위 | 아티스트 | 곡명 | 바로 듣기 |
|:---:|:---|:---|:---:|
"""

    if tracks:
        for t in tracks[:50]:  # 상위 50위 표기 (필요시 조절 가능)
            readme_content += f"| **{t['rank']}위** | {t['artist']} | {t['title']} | [🎧 샤잠에서 보기]({t['shazam_url']}) |\n"
    else:
        readme_content += "| - | - | 데이터를 불러오지 못했습니다. | - |\n"

    readme_content += "\n<br>\n\n*This report is managed by Miae Kwon.*"

    # README.md 파일로 직접 저장
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
        
    print("README.md updated with real chart data and links!")

if __name__ == "__main__":
    main()
