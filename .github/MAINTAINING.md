# Maintaining

## Release

1. **Source APK** — the original YouTube Music APK (arm64, full APK) is attached to the draft release `source`. Replace it when a new version is supported. Do not delete or publish this draft.
2. **Actions → Release YT Music Morphe → Run workflow**
   - `rlx`: `release` (latest RLX Patches release), a release tag such as `v2.4.6`, or a branch of RLX Patches (test builds only)
   - `publish`: unchecked builds a test APK (Original_BBK only) into the run's *Artifacts*
   - `update_preview` (test builds): the APK offers the latest release, to see the update dialog

Every published build becomes the latest release. The workflow builds [RLX Patches](https://github.com/Ramik4/rlx-patches) from source with the changes in `addons/morphe/` (sheet menus in the menu color) and the additions in `extras/` (update checker, menu color, experimental notice), patches the source APK with the patches RLX Patches enables by default, verifies package name and signature, uploads the two APKs to R2, publishes the release (links to the APKs on R2) and updates `updates/*.json` for the in-app update check. Settings, theme colors and icons come from RLX Patches.

| Variant | File | Package | Theme color |
|---|---|---|---|
| `morphe` | `YT_Music_Morphe-v<YT Music>_RLX-v<RLX>_Amoled.apk` | `app.morphe.android.apps.youtube.music` | Pure black by default (Theme option `inAppDefaultColors`: `pure_black`) |
| `apple` | `YT_Music_Morphe-v<YT Music>_RLX-v<RLX>_Original_BBK.apk` | `com.apple.android.music` (Clone app) | RLX #0F0F0F by default (`rlx`) |

Test builds add the build number: `..._RLX-v<RLX>-b<build>_Original_BBK.apk`. Release tags are `v<YT Music>-rlx<RLX>-p<Morphe>-b<build>` (earlier releases: `v<YT Music>-p<Morphe>-b<build>`).

The changelog is generated from the Morphe changelog included in RLX Patches (YouTube Music only, for the Morphe version RLX Patches is based on), in the same way as in `youtube-morphe`. Bug fixes are not listed one by one: the notes end with the heading `🔧 Bug fixes and other improvements`, followed in the release notes by the reminder to install the downloaded APK from the Downloads folder (`notes/mod-fixes.md` is kept as a record only); important features of skipped versions under `## <patches version>` in `notes/extra-features.md`; the features of the mod are in `notes/mod-features.md`.

The first dev build after a stable version that was not released here (such as 2.3.0-dev.1 after 2.2.0) also lists the full changelog of that stable version, after the changes of the dev version.

**Actions → Update release notes → Run workflow** (`tag`: empty for the latest release) generates the changelog of a published release again from the current `notes/` and `scripts/changelog.py`, without a new build: the release notes keep their files table, and the in-app changelog (`DL_BASE_URL/music/updates/*.json` and `updates/*.json`) is replaced while it is still the one of that release.

## 4PDA post

`notes/4pda-post.txt` is the post for the 4PDA topic, updated for each release (YT Music and patches versions, What's new, links), in the same layout as the post of `youtube-morphe`.

- An empty line after each `[spoiler=...]` title
- No "test version" note next to dev patches versions, users could misread it
- What's new is a plain list, without a line for the YT Music and patches versions. A stable version lists its full changelog, the best YT Music features first; a dev version lists the new features of all dev versions since the last release
- Link titles in `[color="#808080"]`, followed by the file size
- Order: header, What's new, Mod features (spoiler), Download (one line per variant), Mod information, Help (MicroG and playback problems). Name color `#ff0040`
- The recommended settings file is not linked in the post, it is on the release page

## Configuration

| File | Purpose |
|---|---|
| `extras/` | Additional patches: update check, menu color (menus and sheets in the theme color, #0F0F0F with pure black), experimental notice. Strings of `extras/strings/<locale>/` are appended to the YouTube Music ones (the build fails if RLX Patches already has one of them). The update checker also turns off the patches update check of the RLX about page |
| `addons/morphe/` | Changes of the mod to RLX Patches files (`git apply` patches, applied in name order; skipped once RLX Patches includes them, the build fails if one no longer applies): `sheet-menus-color.patch` (the sheets of RLX Patches in the menu color) |

Variant options (package, theme colors) are set in `build_variant` calls of `.github/workflows/release.yml`. Settings, icons and theme defaults come from RLX Patches (`rlx/defaults.json` there).

## Downloads (Cloudflare R2)

Published builds are uploaded to the R2 bucket `R2_BUCKET`, below `music/` (the variable `DL_BASE_URL` is required to publish; the APKs are not attached to the GitHub release): the APKs to `music/apk/`, the update info to `music/updates/<variant>.json`. The apps check `DL_BASE_URL/music/updates/<variant>.json` and download the APK from `DL_BASE_URL/music/apk/`, so they no longer depend on GitHub. The APKs of the last 3 builds are kept. The bucket and its Worker are shared with YT Morphe (`cloudflare/worker.js` in RAMiK4/yt-morphe), which uses the root of the bucket. `updates/*.json` in this repository stays up to date for builds that still check GitHub.

`r2_test` (test builds, with `update_preview`): the APK and its update info are uploaded as test files (`music/apk/test_*`, `music/updates/*-test.json`) and the APK checks those; the next published build removes them.

The update address is built into each APK: `DL_BASE_URL` must not change, or the builds that use it stop getting updates.

## Secrets (Settings → Secrets and variables → Actions)

| Name | Type | Value |
|---|---|---|
| `KEYSTORE_B64` | secret | Keystore, base64 |
| `KEYSTORE_PASSWORD` | secret | Keystore password (empty: Morphe default) |
| `KEY_ALIAS` | secret | Key alias (empty: `Morphe`) |
| `KEY_PASSWORD` | secret | Key password (empty: `Morphe`) |
| `CERT_SHA256` | variable | SHA-256 fingerprint of the signing certificate |
| `R2_ACCOUNT_ID` | secret | Cloudflare account ID |
| `R2_ACCESS_KEY_ID` | secret | R2 API token: access key ID (Object Read & Write, bucket only) |
| `R2_SECRET_ACCESS_KEY` | secret | R2 API token: secret access key |
| `R2_BUCKET` | variable | R2 bucket name |
| `DL_BASE_URL` | variable | Address of the Worker, without a trailing slash |
