# Publishing SiteCore on Google Play

Everything that can be prepared in advance is ready in this folder. The steps marked **YOU** need your
Google account, payment or a public web address, so only you can do them.

## 1. Files to upload

| What | File | Play Console location |
|---|---|---|
| App bundle (v1.08, code 9) | `SiteCore-v1.08.aab` (= `SiteCore.aab`) | Release › Production (or Internal testing) › Create release |
| App icon 512×512 | `store/icon-512.png` | Grow › Store presence › Main store listing |
| Feature graphic 1024×500 | `store/feature-graphic.png` | Main store listing |
| Phone screenshots (6) | `store/phone/*.png` (1080×1920) | Main store listing › Phone |
| 7" and 10" tablet screenshots (3) | `store/tablet/*.png` (1600×2560) | Main store listing › Tablets |
| Privacy policy | `website/privacy.html` → must be online, e.g. `https://YOUR-SITE/privacy.html` | Policy › App content › Privacy policy |

## 2. Steps

1. **YOU** — Create a Google Play developer account: <https://play.google.com/console> (one-time USD 25 fee, identity verification).
   New *personal* accounts must run a **closed test with at least 12 testers for 14 days** before production access — plan for this.
2. **YOU** — Put the `website/` folder online (Netlify Drop, GitHub Pages, Cloudflare Pages or your company server) so the privacy policy has a public URL.
   Before uploading, set your support e-mail in `website-src/privacy.html` (`CONTACT_EMAIL`) and rebuild (`python tools/build_site.py`).
3. Play Console › **Create app**: name `SiteCore`, default language English (United States), App, Free.
4. Fill **App content** with the answers in section 4.
5. Fill the **Main store listing** with section 3 and upload the graphics from section 1.
6. Release › Testing › **Internal testing** (or Closed testing) › Create release › upload `SiteCore.aab`.
   Accept **Play App Signing** (Google keeps the app-signing key; `android-app/sitecore-release.jks` becomes your *upload key*).
7. Add testers, test, then **promote to Production** and submit for review (usually 1–7 days).
8. After approval, put the Play Store link in `website-src/index.html` (`PLAY_URL`) and rebuild the website.

## 3. Store listing text

**App name (30):** `SiteCore: Punch List & QC`

**Short description (80):**
`Tag defects on drawings, manage punch lists & inspections, send PDF reports.`

**Full description:**

```
SiteCore is a field quality app for construction and MEP teams. Import your drawings, tag issues exactly where they are, follow them up with your subcontractors and send professional PDF reports — even without internet.

DRAWINGS & TAGS
• Import PDF, JPG or PNG layout plans
• Organise drawings as Discipline › Floor › Sub-system › Layout (1. EE WORK › 1ST FLOOR › 1.1 LIGHTING…)
• Tap the plan to place a tag; tag numbers are generated automatically and can be edited

PUNCH LISTS
• Status: Open, In Progress, Defect, Not Pass, Pass, Closed
• Priority, responsible company, assignee, due date, location and comments
• Photos from the camera or gallery, with markup (pen, arrow, box, ellipse, text)
• Before / After photo labels and automatic closed dates
• Filters, bulk updates and export to Excel (CSV)

INSPECTIONS & SITE DIARY
• Pass / Fail / N/A checklists from templates
• Failed items become tags on the plan in one tap
• Daily site diary with weather, manpower, work done and photos
• Task board to track responsibilities between teams

PROFESSIONAL PDF REPORTS
• Owner, consultant and contractor logos in the header, with editable captions
• Layout overview with every tag, register table and detail pages with photos and key plan
• Detail pages in portrait or landscape, 1 to 4 tags per page
• Report a single layout, a sub-system, a floor or a whole discipline
• Filter by responsible company for subcontractor reports
• Preview before you share; English, Lao or Thai

MADE FOR THE FIELD
• Works fully offline — no account, no server
• Your data stays on your device; share a project with one file
• Back up and restore all projects
• Phone and tablet layouts, display size adjustable
• Dark mode (follows the system, or choose Light / Dark)
• English, ລາວ (Lao) and ไทย (Thai)

SiteCore does not collect any personal data and contains no ads.
```

**Category:** Business   ·   **Tags:** Productivity, Construction, Business
**Contact e-mail:** **YOU** — required, shown publicly on the listing.
**Website:** the URL where you host `website/`.

Optional translated short descriptions:
- Lao: `ໝາຍບັນຫາເທິງແບບແປນ, ຈັດການລາຍການແກ້ໄຂ ແລະ ການກວດກາ, ສົ່ງລາຍງານ PDF.`
- Thai: `ปักหมุดปัญหาบนแบบ จัดการรายการแก้ไขและการตรวจสอบ ส่งรายงาน PDF`

## 4. App content answers

| Section | Answer |
|---|---|
| Privacy policy | URL of `privacy.html` on your website |
| Ads | **No**, the app does not contain ads |
| App access | **All functionality is available without special access** (no login) |
| Content rating (IARC) | Category: *Utility, Productivity, Communication or Other*. Answer **No** to violence, sexuality, language, controlled substances, gambling, user-generated content shared with others, location sharing, purchases → rating *Everyone / 3+* |
| Target audience | **18 and over** (professional tool). Not designed for children |
| News app | No |
| COVID-19 / Health | No |
| Government app | No |
| Financial features | None |
| Data safety — *Does your app collect or share any of the required user data types?* | **No.** All data is processed and stored only on the device; nothing is transmitted to the developer or third parties |
| Data safety — encryption in transit | Not applicable (no data transmitted) |
| Data safety — account deletion | Not applicable (no accounts) |
| Permissions | CAMERA — used only when the user takes a photo (declared optional, `required=false`) |

## 5. Before each update

1. Edit `tools/source/src.html` → `python build.py` (in `tools/source`).
2. Increase `APP_VERSION` and the `application-version` meta (src.html), `versionCode` +1 and `versionName` in `android-app/android/app/build.gradle`, `VERSION` in `tools/build_www.py`.
3. `bash tools/build_apk.sh` → upload the new `SiteCore-vX.YY.aab`.
4. Keep `android-app/sitecore-release.jks` + `keystore.properties` backed up — without the upload key you cannot publish updates (Google can reset an upload key on request, but it takes time).
