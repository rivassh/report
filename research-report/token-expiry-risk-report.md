# گزارش ریسک انقضای توکن — gapgpt
## Project Stakeholder Report: ACCESS_TOKEN Expiry Risk & Mitigation

**تاریخ تهیه:** ۱۴۰۵/۰۸/۰۵ (اکتبر ۲۰۲۶)
**توسط:** MiMoCode Research Agent
**دست्गاه:** gapgpt Knowledge Hub & Dashboard

---

## ۱. خلاصه اجرایی (Executive Summary)

توکن احراز هویت `ACCESS_TOKEN` مورد استفاده در همه‌ی اسکریپت‌های gapgpt در تاریخ **۱نوامبر ۲۰۲۶ (۲۰۲۶-۱۱-۰۱)** انقضا می‌یابد. تا حالا توکن معتبر است اما تا آن زمان. اگر تا آن تاریخ مکانیزم به‌روزرسانی خودکار اجرا نشود، همه‌ی عملیات سنکرین‌سازی چت، مهاجرتی دیتابیس، داشبورد و چت‌بات سازمانی با خطای ۴۰۱ (احراز هویت ناموفق) متوقف می‌شود.

**سطح ریسک:** بالا (High)
**زمان باقی‌مانده:** < ۷ روز
**تأثیر:** متوقف شدن کامل دسترسی به gapgpt.app API

---

## ۲. جزئیات فنی

### ۲.۱ توکن فعلی
| مورد | مقدار |
|------|-------|
| فایل تنظیمات | `.env.docker` (و `.env` برای fallback) |
| کلید | `ACCESS_TOKEN` |
| تاریخ انقضای JWT (`exp`) | ۱۷۹۳۵۱۵۶۸۵ → ۲۰۲۶-۱۱-۰۱ |
| وضعیت فعلی | معتبر (hasn't expired yet) |

### ۲.۲ چرا ریسک بالا است؟

1. **بدون به‌روزرسانی خودکار (no auto-refresh):** همه‌ی اسکریپت‌ها توکن را به صورت دستی در فایل `.env` نگه می‌دارند. هر توکن جدید نیاز به تدخل دستی دارد.
2. **خطاهای احراز هویت predominant:** در `scripts/dashboard.log` تقریبا ۶۰٪ خطاهای ثبت شده به نوع `Authentication failed for: /api/v1/move_to_project` مربوط است.
3. **استفاده از کوکی HAR:** توکن تنها در صورت همراه بودن با کوکی‌های صحیح `browser_fingerprint`، `did`، `device_id` از فایل HAR صادر شده از مرورگر معتبر است. هرگونه تغییر در کوکی‌ها باعث قطعی می‌شود

### ۲.۳ مکانیزم موجود در gapgpt.app API
API gapgpt.app از احراز هویت مبتنی بر کوکی استفاده می‌کند و شامل مکانیزم با‌چندlegen است:
- نقاط خطایی: در صورت ۴۰۱ متد `_request_with_referer()` در `scripts/ingest/sources/gapgpt_api.py` می‌تواند از `/api/v1/token/refresh` استفاده کند تا هر دو توکن access و refresh را به‌روز کند.
- مشکل: هیچ اسکریپتی فعلاً این جریان refresh را به صورت خودکار فراخوانی نمی‌کند. جاب cron هر ۵ دقیقه (`docker compose exec -T gapgpt-client`) هیچ检查 توکنی ندارد.

---

## ۳. تأثیر برicingaging بر روی عملیات

| عملیات | حداقل زمان در{|بسته به} | وضعیت در případě انقضا |
|---------|-----------------|----------------------|
| سنکرین چت‌ها (`sync_chats.py`) | هر ۵ دقیقه | متوقف (۴۰۱) |
| مهاجرتی mimocode.db → PostgreSQL | پیوسته | متوقف |
| داشبورد وب (:5056) | در هر لود صفحه | داشبورد خالی / خطا |
| چت‌بات سازمانی | در هر استعلام | خطای احراز هویت |
| Timline analysis | دوره‌ای | متوقف |

---

## ۴. برنامه-mailiff제로کاهش (Mitigation Plan)

### لایه ۱ — فوری (قبل از ۱نوامبر ۲۰۲۶)

1. **بررسی پیش‌از 발از توکن:** افزودن یک مرحله 초기 در همه اسکریپت‌ها که claims JWT را decode می‌کند، `exp` را gegen زمان فعلی مقایسه می‌کند و اگر کمتر از ۷ روز باشد، هشدار می‌دهد.
2. **اسکریپت به‌روزرسانی توکن:** ساخت `scripts/refresh_token.py` که از `/api/v1/token/refresh` استفاده می‌کند و توکن جدید را در `.env.docker` می‌نویسد.
3. **جاب cron هر ۶ ساعت:** اجرا خودکار بررسی و به‌روزرسانی توکن به صورت دوره‌ای.
4. **نقطه ورود داشبورد:** افزودن `/api/token-status` که `{exp, days_left, needs_refresh}` را برمی‌گرداند.
5. **Makefile target:** افزودن `make check-tokens` برای بررسی دستی وضعیت توکن.

### لایه ۲ — مدت‌مدت (تا قبل از ۱نوامبر)

1. **اجبار به refresh خودکار در gapgpt_api.py:** در `_request_with_referer()`، در صورت دریافت ۴۰۱، ابتدا refresh فراخوانی شود، کوکی‌ها به‌روزرسانی شوند و درخواست دوباره ارسال شود.
2. **روشننمایی توکن:** اضافه کردن وضعیت توکن به داشبورد پیش‌فرض برای نظارت مدام.
3. **ت destinés Koongeri-gir:** اگر gapgpt.app پشتیبانی می‌کند، به توکن‌های refresh長 عمری منتقل شود.

### لایه ۳ — استراتژیک (مدت بلند)

1. **تغییر به OAuth2 device flow** اگر gapgpt.app در آینده پشتیبانی کند (بدون نیاز به مرورگر.
2. **ایجاد توکن‌های swept** در GitOps protocol تا sessions multiagent دسترسی را از دست ندهند.

---

## ۵. اقدامات پیشنهادی به است anticipated holderها (Recommended Next Steps)

| اولویت | اقدام | مخاطب | حداکثر زمان اجرا |
|--------|-------|-------|------------------|
| حرج | اجرا `make check-tokens` و بررسی days_left | DevOps / Backend | امروز |
| حرج | ساخت `scripts/refresh_token.py` | Backend Engineer | ۳ روز |
| متوسط | افزودن cron هر ۶ ساعت برای refresh | DevOps | ۵ روز |
| متوسط | نقطه `/api/token-status` در داشبورد | Backend Engineer | ۷ روز |
| عادی | مستندسازی lifecycle توکن در KNOWLEDGE_HUB.md | Technical Writer | ۲ هفته |

---

## ۶. چگونه وضعیت توکن را حالا بررسی کنید

```bash
python3 -c "
import json, base64
from datetime import datetime, timezone
with open('.env.docker') as f:
    for line in f:
        if line.startswith('ACCESS_TOKEN='):
            token = line.split('=', 1)[1].strip()
            parts = token.split('.')
            payload = json.loads(base64.urlsafe_b64decode(parts[1] + '==='))
            exp = datetime.fromtimestamp(payload['exp'], tz=timezone.utc)
            now = datetime.now(timezone.utc)
            days_left = (exp - now).days
            print(f'Expiry: {exp.strftime(\"%Y-%m-%d %H:%M UTC\")}')
            print(f'Days left: {days_left}')
            print(f'Needs refresh: {\"YES\" if days_left < 7 else \"NO\"}')
            break
"
```

---

## ۷. میخانه (References)

- `scripts/ingest/sources/gapgpt_api.py` — مکانیزم refresh روی ۴۰۱
- `scripts/dashboard.log` — خطاهای احراز هویت ثبت‌شده
- `.env.docker` — فایل حاوی ACCESS_TOKEN
- `scripts/sync_chats.py` — اسکریپت سنکرین چت‌ها
- `KNOWLEDGE_HUB.md` — مستندات معماری gapgpt

---

**نتیجه:** از آنجایی که انقضا تا ۱نوامبر ۲۰۲۶ است و لایه ۱ را می‌توان در چند روز پیاده‌سازی کرد، استقرار اقدامات کاهش فوری را توصیه می‌کنیم تا 중단arbeits تمام خدمات gapgpt ایجاد نشود.
