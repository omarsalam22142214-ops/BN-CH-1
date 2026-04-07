import json
import cloudscraper
from bs4 import BeautifulSoup

def fetch_matches():
    url = "https://koora-lives.mov/"
    # بنستخدم cloudscraper عشان نحاول نتخطى حماية Cloudflare
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    
    try:
        response = scraper.get(url)
        if response.status_code != 200:
            print(f"فشل الاتصال بالموقع. الكود: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = []
        
        # بنجمع كل اللينكات اللي في الصفحة
        links = soup.find_all('a')
        for link in links:
            href = link.get('href', '')
            # بندور على اللينكات اللي فيها كلمة match أو live
            if '/match/' in href or '/live/' in href:
                title = link.get_text(separator=" ", strip=True)
                if len(title) < 3:
                    title = "مباراة اليوم"
                
                # تظبيط اللينك لو ناقص
                if not href.startswith('http'):
                    href = "https://koora-lives.mov" + href
                
                # منع التكرار
                if not any(m['url'] == href for m in matches):
                    matches.append({
                        "name": "🔥 " + title,
                        "url": href
                    })
        return matches
    except Exception as e:
        print(f"حصل خطأ: {e}")
        return []

if __name__ == "__main__":
    print("جاري سحب الماتشات...")
    data = fetch_matches()
    
    if data:
        # بنكتب الداتا في ملف matches.json
        with open("matches.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"عاش! تم حفظ {len(data)} ماتش.")
    else:
        print("ملقيناش ماتشات، أو Cloudflare قفل السكة.")
