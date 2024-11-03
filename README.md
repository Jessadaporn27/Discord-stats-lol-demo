# Discord Bot for League of Legends

## 📚 เกี่ยวกับโปรเจกต์
โปรเจกต์นี้เป็น Discord Bot ที่สร้างขึ้นเพื่อการศึกษา โดยมุ่งเน้นการดึงข้อมูลจากเว็บไซต์ที่เกี่ยวข้องกับเกม League of Legends เพื่อให้ผู้ใช้สามารถเข้าถึงข้อมูลที่สำคัญ เช่น สถิติของผู้เล่น, แชมเปี้ยนที่มีอัตราชนะสูง, และข้อมูลเกี่ยวกับการจับคู่ (Counters) ของแชมเปี้ยนต่างๆ
ใช้ 2 website ในการทำ web scraping  1.op.gg 2.u.gg

## ⚙️ เทคโนโลยีที่ใช้
โปรเจกต์นี้ใช้ไลบรารีและเฟรมเวิร์กดังต่อไปนี้:
- **aiohttp**: สำหรับการจัดการคำขอ HTTP แบบไม่บล็อก
- **discord.py**: สำหรับการสร้างบอท Discord
- **requests**: สำหรับการจัดการคำขอ HTTP
- **BeautifulSoup**: สำหรับการทำ Web Scraping เพื่อดึงข้อมูลจาก HTML

## 🚀 วิธีการใช้งาน
1. ติดตั้งไลบรารีที่จำเป็น: bash pip install aiohttp discord requests beautifulsoup4
2. แก้ไขค่า TOKEN ในโค้ดด้วยโทเค็นของบอท Discord
3. รันบอท : python yourfilename.py
