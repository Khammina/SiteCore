# SiteCore — Field Quality & Punch List

Created by Khammina SCMV. Current version: **1.09** (see `CHANGELOG.md`).

| File / folder | What it is |
|---|---|
| `SiteCore.html` | The app as one file. Double-click to use on a PC (Chrome / Edge). |
| `www/` | Offline, installable web app (PWA). Upload this folder to any web host to run SiteCore on the cloud. |
| `SiteCore.apk` | Android app (release-signed). `SiteCore-v1.08.apk` / `SiteCore-v1.08.html` are the versioned copies. `SiteCore-debug.apk` is the debug build. |
| `SiteCore.aab` | **Google Play upload file** (Android App Bundle). See `PLAYSTORE.md`. |
| `website/` | Public website: landing page, privacy policy, web app (`/app/`), APK download. Upload this folder to publish. |
| `store/` | Google Play listing graphics (icon, feature graphic, screenshots). |
| `PLAYSTORE.md` / `AUDIT.md` | Publishing guide with listing text and form answers / release audit. |
| `android-app/` | Android (Capacitor) project used to build the APK. |
| `tools/` | Build scripts. `tools/source/` holds the app source (`src.html`), translations (`tr.json`) and PDF font builder. |

## Run on the cloud (web)
Upload the **contents of `www/`** to any static HTTPS host, for example:
- **Netlify Drop** — open https://app.netlify.com/drop and drag the `www` folder in.
- **GitHub Pages**, **Cloudflare Pages**, **Firebase Hosting**, or a company web server (IIS / Nginx / Apache).

Open the site on a phone or PC and choose **Install app** / **Add to Home screen**. After the first visit it works offline.

> Data is stored on each device (browser storage). Use **Share / Export** and **Import** to move a project between office and field devices.

## Install on Android
1. Copy `SiteCore.apk` to the phone (USB, Google Drive, WhatsApp, e-mail…).
2. Open it and allow **Install unknown apps** for the app you opened it from.
3. Launch **SiteCore**. PDF / CSV / package exports are saved to `Documents/SiteCore` and offered in the Android share sheet.

## Rebuild after changing the app
Edit `tools/source/src.html` (and `tr.json` for Lao / Thai text), then `cd tools/source && python keys.py > nul && python build.py` to regenerate `SiteCore.html`.

### Build the web package and APK
From Git Bash in this folder:

```bash
bash tools/build_apk.sh      # rebuilds www/, SiteCore.apk and SiteCore-debug.apk
python tools/build_www.py    # only rebuild the web package www/
```

Build tools live in `%LOCALAPPDATA%\SiteCoreBuild` (JDK 21 + Android SDK, portable).

**Important:** `android-app/sitecore-release.jks` and `android-app/keystore.properties` sign the app.
Back them up somewhere safe. Android only accepts updates signed with the same key.
Increase `versionCode` / `versionName` in `android-app/android/app/build.gradle` for every new release.

## Releasing a new version
1. Update `APP_VERSION` and the `application-version` meta in `tools/source/src.html`.
2. Increase `versionCode` (+1) and set `versionName` in `android-app/android/app/build.gradle`, and `VERSION` in `tools/build_www.py`.
3. Add the changes to `CHANGELOG.md`, then run `bash tools/build_apk.sh`.
