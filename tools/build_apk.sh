#!/usr/bin/env bash
# Builds the SiteCore Android app.
#   1. SiteCore.html  ->  www/ (offline web package, PWA)          [tools/build_www.py]
#   2. www/           ->  android-app/android (Capacitor sync)
#   3. Gradle         ->  SiteCore.apk (release, signed) + SiteCore-debug.apk
# Toolchain (portable, no admin): %LOCALAPPDATA%\SiteCoreBuild\{jdk,android-sdk}
# Run from Git Bash:  bash tools/build_apk.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TC="${LOCALAPPDATA//\\//}/SiteCoreBuild"
export JAVA_HOME="$(ls -d "$TC"/jdk/jdk-21* | head -1)"
export ANDROID_HOME="$TC/android-sdk" ANDROID_SDK_ROOT="$TC/android-sdk"
export PATH="$JAVA_HOME/bin:$ANDROID_HOME/platform-tools:$PATH"

python "$ROOT/tools/build_www.py"
cd "$ROOT/android-app"
npx cap sync android
python "$ROOT/tools/build_www.py" >/dev/null   # re-apply launcher icons after sync

cd android
./gradlew --no-daemon assembleDebug
cp app/build/outputs/apk/debug/app-debug.apk "$ROOT/SiteCore-debug.apk"
if [ -f "$ROOT/android-app/keystore.properties" ]; then
  ./gradlew --no-daemon assembleRelease bundleRelease
  cp app/build/outputs/apk/release/app-release.apk "$ROOT/SiteCore.apk"
  cp app/build/outputs/bundle/release/app-release.aab "$ROOT/SiteCore.aab"   # upload this file to Google Play
fi
VER="$(grep -o 'versionName "[^"]*"' app/build.gradle | cut -d'"' -f2)"
cp "$ROOT/SiteCore.html" "$ROOT/SiteCore-v$VER.html"
[ -f "$ROOT/SiteCore.apk" ] && cp "$ROOT/SiteCore.apk" "$ROOT/SiteCore-v$VER.apk"
[ -f "$ROOT/SiteCore.aab" ] && cp "$ROOT/SiteCore.aab" "$ROOT/SiteCore-v$VER.aab"
python "$ROOT/tools/build_site.py"   # website/ (landing + privacy + app + APK download)
echo "Version $VER"; ls -la "$ROOT"/SiteCore*
