# SiteCore — Changelog

## v1.08 — 2026-10-02
- **Phone tab bar:** the tabs share the screen width equally and the labels scale with the screen (9–12 px, up to two lines) — fits small and large phones in English, Lao and Thai.
- **Punch list detail pages:** new *Detail page orientation* (Portrait / Landscape) and *Tags per detail page* 1, 2, 3 or 4 — in Report settings and in the report preview.
  Layouts: portrait 1 / 2 stacked / 3 stacked / 2×2; landscape 1 / 2 side by side / 3 columns / 2×2.
- The tag block adapts to its size: compact info table, key plan beside the details or in the photo strip, description and photos share the remaining space; photo cells keep a consistent size.

## v1.07 — 2026-10-02
- **Fix: top header under the status bar / notch on Android 15–16.** On phones with an up-to-date Android System WebView the app was drawn edge-to-edge and the header could sit under the notification bar. The Android app now always lets the system place it below the status bar and camera cutout (and above the gesture bar), on every WebView version.

## v1.06 — 2026-10-02
- Version update for release: version name 1.06 / Android version code 7 (installs over all earlier versions, data kept).
- Same features as v1.05 (including dark mode); web app cache renewed so installed web apps pick up the new version.

## v1.05 — 2026-10-02
- **Dark mode:** Theme setting Auto (follows the phone / computer), Light or Dark — in Project Settings › User, in the More menu on phones, and a quick switch in the top bar on tablet / computer. Stored per device.
- Full dark palette for every screen, dialog, bottom sheet, table, card, drawing register and tag editor; system controls (lists, date pickers, scrollbars) follow the theme. Drawings and PDF reports stay white (print documents).
- Android: gesture-bar icons follow the theme; the theme is applied before the first frame (no white flash).

## v1.04 — 2026-10-02
- Version update for release: version name 1.04 / Android version code 5 (installs over all earlier versions, data kept).
- Same features as v1.03; web app cache renewed so installed web apps pick up the new version.

## v1.03 — 2026-10-01 (Google Play release candidate)
- Professional UX/UI pass: first-run welcome screen, phone tab bar with More sheet, bottom-sheet dialogs, compact plan toolbar, punch list cards on phones, ⋮ menus in the drawing register for touch screens.
- New About & Legal screen (privacy policy, open-source licences) and full backup / restore of all projects.
- Accessibility: accessible button names, dialog roles, keyboard focus, 16 px inputs on touch screens.
- Android: Play Store bundle (.aab), optional camera feature, minimal permissions, themed (monochrome) icon, improved back button.
- Public website (landing page + privacy policy + web app) and Google Play store listing assets.

## v1.02 — 2026-10-01
- **Notch / camera cutout / Dynamic Island safe areas:** top bar, bottom menu, side edges, dialogs, report preview and messages stay clear of the notch, status bar and gesture bar (Android edge-to-edge, iPhone, installed web app).
- Android: navy status bar with light icons; gesture-bar icons adapt to the background.
- **Auto scale per device:** small phone 85%, phone 90%, tablet 85–90% (fits the full side-menu layout), computer 90%. Settings shows what Auto chose on this device; re-applied on rotation.
- Uses the dynamic viewport height so mobile browser toolbars no longer hide the bottom of the app.

## v1.01 — 2026-10-01
- **Display size / auto resolution:** the app adapts to each screen and shows at 90% by default (phones, tablets, Android app and PC). Per-device setting in Project Settings → User → Display size (80–120%).
- Plan viewer touch / mouse positions corrected for the display scale (tags are placed exactly where tapped).
- Android: page-scale support in the app WebView; phone layout refinements; loading indicator; SiteCore splash screen.
- Version shown in the side menu and Project Settings; app version recorded in share packages.

## v1.0 — 2026-10-01
- First Android build (APK) and offline / installable web package (PWA) for cloud hosting.
- Drawings register (Discipline → Floor → Sub-system), tagging, punch list, task board, inspections, site diary.
- PDF reports with preview, three header logos (Owner / Consultant / Contractor), English / Lao / Thai.
- Photo markup, Before / After photos, closed dates, bulk update, responsible filter, footer credit.
