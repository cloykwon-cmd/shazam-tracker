import os
import time
import random
import urllib.parse
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_shazam_korea_chart():
    """샤잠 대한민국 차트 Top 200 데이터 및 바로 듣기 링크 수집"""
    url = "https://www.shazam.com/services/charts/v1.1/chart/world/KR"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
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
            
            # 샤잠 상세 페이지 링크 추출 (없을 경우 검색 링크로 대체)
            shazam_url = track.get('url')
            if not shazam_url:
                query = urllib.parse.quote(f"{artist} {title}")
                shazam_url = f"https://www.shazam.com/search?q={query}"
                
            # 애플뮤직 검색 링크 생성 (바로 스트리밍 확인용)
            apple_query = urllib.parse.quote(f"{artist} {title}")
            apple_music_url = f"https://music.apple.com/kr/search?term={apple_query}"
            
            tracks.append({
                "rank": index,
                "artist": artist,
                "title": title,
                "shazam_url": shazam_url,
                "apple_music_url": apple_music_url
            })
    except Exception as e:
        print(f"샤잠 차트 수집 중 오류 발생: {e}")
        
    return tracks

def check_melon_availability(artist, title):
    """구글 검색을 통해 국내 멜론 등록 여부 확인"""
    query = f'site:melon.com "{artist}" "{title}"'
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={encoded_query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return False
            
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        
        if "다음 항목과 일치하는 검색어가 없습니다" in text_content or "did not match any documents" in text_content.lower():
            return True
        else:
            return False
            
    except Exception as e:
        print(f"검색 대조 중 오류 ({artist} - {title}): {e}")
        return False

def main():
    print("🎵 [샤잠 Top 200 차트 수집 시작]")
    chart_tracks = get_shazam_korea_chart()
    
    if not chart_tracks:
        print("❌ 차트 데이터를 가져오지 못했습니다.")
        return
        
    print(f"총 {len(chart_tracks)}곡 수집 완료. 국내 미발매
