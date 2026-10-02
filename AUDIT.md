# SiteCore v1.08 — Release audit

Date: 1 October 2026 · Scope: Android app (AAB/APK), web app (PWA), single-file desktop app, public website.

## Google Play requirements

| Check | Result |
|---|---|
| Android App Bundle (.aab) | ✔ `SiteCore.aab`, signed with the upload key (`jarsigner -verify`: verified) |
| Target API level | ✔ targetSdk 36 (Android 16), compileSdk 36, minSdk 24 (Android 7.0) |
| Version | ✔ versionCode 9, versionName 1.08 (installs over 1.0–1.07) |
| Release build not debuggable | ✔ no `debuggable` flag; WebView remote debugging only in debug builds |
| 16 KB page-size support | ✔ no native (.so) libraries in the bundle |
| Permissions minimal | ✔ INTERNET, CAMERA, WRITE_EXTERNAL_STORAGE (maxSdk 29 only). READ_EXTERNAL_STORAGE request removed (Android adds it automatically, limited to the same old versions) |
| Camera optional | ✔ `uses-feature camera required=false` — installs on tablets without a camera |
| No restricted permissions | ✔ no photo/video, location, contacts, SMS or background permissions; images are picked through the system picker |
| Edge-to-edge (Android 15+) | ✔ the system keeps the app below the status bar, camera cutout / notch and above the gesture bar on every WebView version (v1.07) |
| Network / cleartext | ✔ no external requests; all libraries bundled; cleartext traffic not enabled |
| Privacy policy | ✔ in-app (About) and `website/privacy.html` — **must be published at a public URL** |
| Data safety | ✔ no data collected or shared (see `PLAYSTORE.md`) |
| Account deletion | ✔ not applicable (no accounts) |
| Store graphics | ✔ icon 512, feature graphic 1024×500, 6 phone (1080×1920) and 3 tablet (1600×2560) screenshots — aspect ratios within Play limits |
| Adaptive + themed icon | ✔ adaptive icon with monochrome layer (Android 13 themed icons), splash screen |
| Open-source licences | ✔ listed in About (pdf.js Apache-2.0, jsPDF MIT, AutoTable MIT, Capacitor MIT, Noto OFL-1.1, Lucide ISC) |

## UX / UI changes in 1.03

- First-run **welcome screen** (no auto-loaded sample data): create project, explore sample, import, language chips, trust notes.
- **Phone tab bar**: Dashboard · Drawings · Punch List · Reports · More (sheet with Task Board, Inspections, Site Diary, Settings, About, Share, Import, Language).
- **Bottom-sheet dialogs** on phones with a drag handle, safe-area padding and full-width primary button.
- **Plan screen on phones**: one compact toolbar row; filters, zoom, lock, info, renumber and the tag list moved to a *More* sheet → the plan uses most of the screen.
- **Punch list as cards** on phones (selection and bulk update kept); table on tablet / desktop.
- **Drawing register on touch screens**: a ⋮ menu per row (hover-only actions were unreachable on phones and tablets).
- **About & Legal** screen: version, privacy policy, open-source licences.
- **Backup & restore** of all projects in one file; last-backup date shown.
- Accessibility: accessible names for icon-only buttons, dialog roles, visible keyboard focus, 16 px inputs on touch screens (prevents iPhone zoom-on-focus), larger touch targets.
- Notifications placed above the phone tab bar; Android back button closes preview / dialog / side panels / Add-Tag mode before leaving the screen.

## Verified

- Desktop, phone (412×915) and tablet (800×1280) layouts in English, Lao and Thai — no errors, no untranslated placeholders.
- Backup → restore round trip (projects, tags, plan images).
- Release APK installs and runs on Android 14 emulator; upgrade from v1.02 keeps data (see report).
- Tag placement accuracy at the 90 % display scale (phone and desktop).

## Remaining (needs you)

1. Google Play developer account and, for new personal accounts, the 12-tester / 14-day closed test.
2. Host `website/` and enter the privacy-policy URL in Play Console.
3. Set the public support e-mail (`CONTACT_EMAIL` in `website-src/privacy.html`, and in the Play listing).
4. Keep the upload key (`android-app/sitecore-release.jks`, `keystore.properties`) backed up.

## Known limitations

- Data is stored per device (no cloud sync). Use Share / Export, Import and Backup to move data.
- Very old Android WebView versions (< 140) pad the app below the status bar instead of drawing edge-to-edge — both look correct.
- iPhone / iPad: works as an installed web app (Add to Home Screen); there is no App Store build.
