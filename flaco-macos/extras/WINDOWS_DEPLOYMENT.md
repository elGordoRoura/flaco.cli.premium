# Windows Deployment Guide

This guide covers building, signing, and distributing Flaco AI for Windows.

## Prerequisites

### 1. Development Environment

**Option A: Build on Windows**
- Windows 10/11 (64-bit)
- Node.js 18+ ([nodejs.org](https://nodejs.org))
- Git for Windows ([git-scm.com](https://git-scm.com))

**Option B: Cross-compile from macOS/Linux**
- Node.js 18+
- Wine (for building Windows installers)
  ```bash
  # macOS
  brew install wine-stable

  # Linux
  sudo apt install wine64
  ```

### 2. Code Signing Certificate (Optional but Recommended)

Without code signing:
- ❌ Windows SmartScreen warnings
- ❌ "Unknown publisher" alerts
- ❌ Users must click through security warnings

With code signing:
- ✅ No security warnings
- ✅ Professional appearance
- ✅ Better user trust

**Where to get certificates:**
- [DigiCert](https://www.digicert.com/signing/code-signing-certificates) - $474/year
- [Sectigo](https://sectigo.com/ssl-certificates-tls/code-signing) - $299/year
- [SSL.com](https://www.ssl.com/certificates/code-signing/) - $239/year

**Certificate types:**
- Standard Code Signing - Basic signing
- EV Code Signing - Immediate SmartScreen reputation (recommended)

---

## Building for Windows

### From Windows

```bash
# Install dependencies
npm install

# Build for Windows
npm run build:win

# Output:
# dist/Flaco AI-0.0.2-x64-Setup.exe
# dist/Flaco AI-0.0.2-ia32-Setup.exe
# dist/Flaco AI-0.0.2-x64.zip
# dist/Flaco AI-0.0.2-ia32.zip
```

### From macOS (Cross-compile)

```bash
# Install Wine (first time only)
brew install wine-stable

# Install dependencies
npm install

# Build for Windows
npm run build:win

# This creates Windows installers on Mac!
```

### From Linux (Cross-compile)

```bash
# Install Wine (first time only)
sudo apt install wine64

# Install dependencies
npm install

# Build for Windows
npm run build:win
```

---

## Code Signing on Windows

### Step 1: Install Certificate

1. Double-click your certificate file (`.pfx` or `.p12`)
2. Choose "Local Machine" (requires admin)
3. Enter certificate password
4. Store in "Automatically select the certificate store"
5. Complete the wizard

### Step 2: Configure Signing

Create a `.env` file in project root:

```env
# Windows Code Signing
WIN_CSC_LINK=C:\path\to\certificate.pfx
WIN_CSC_KEY_PASSWORD=your-certificate-password
```

**Security Note:** Never commit `.env` to git! Add to `.gitignore`:

```gitignore
.env
*.pfx
*.p12
```

### Step 3: Build with Signing

```bash
npm run build:win
```

electron-builder will automatically:
1. Sign the executable
2. Sign the installer
3. Add timestamp (proves signing time)

### Step 4: Verify Signing

```powershell
# Check signature
Get-AuthenticodeSignature "dist\Flaco AI-0.0.2-x64-Setup.exe"

# Should show:
# Status        : Valid
# SignerCertificate : CN=Your Company Name
```

---

## CI/CD with GitHub Actions

### Setup Secrets

Add to GitHub repository secrets:
- `WIN_CSC_LINK` - Base64 encoded certificate
- `WIN_CSC_KEY_PASSWORD` - Certificate password

To encode certificate:

```bash
# macOS/Linux
base64 -i certificate.pfx -o certificate.txt

# Windows
certutil -encode certificate.pfx certificate.txt
```

Copy the content of `certificate.txt` to GitHub secret `WIN_CSC_LINK`.

### GitHub Actions Workflow

Create `.github/workflows/build-windows.yml`:

```yaml
name: Build Windows

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm install

      - name: Build for Windows
        env:
          WIN_CSC_LINK: ${{ secrets.WIN_CSC_LINK }}
          WIN_CSC_KEY_PASSWORD: ${{ secrets.WIN_CSC_KEY_PASSWORD }}
        run: npm run build:win

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: windows-installers
          path: |
            dist/*.exe
            dist/*.zip

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            dist/*.exe
            dist/*.zip
```

---

## Distribution Options

### 1. Direct Download (Recommended for Beta)

**Pros:**
- Simple, no approval process
- Full control
- Quick updates

**Cons:**
- Manual distribution
- No automatic discovery
- SmartScreen warnings (without EV cert)

**How to:**
1. Upload installers to GitHub Releases
2. Link from your website
3. Users download and install

### 2. Microsoft Store

**Pros:**
- Built-in trust (no SmartScreen)
- Automatic updates
- Discoverability

**Cons:**
- $19 registration fee
- App review process (3-7 days)
- Must follow store policies
- 15% Microsoft fee (if paid app)

**Requirements:**
- Microsoft Partner Center account
- App must pass certification
- Privacy policy URL
- Age ratings

**Not recommended for v0.0.2** - wait until app is more mature.

### 3. Chocolatey

**Pros:**
- Popular Windows package manager
- Developer-friendly
- Free

**Cons:**
- Smaller user base than Store
- Still requires code signing for trust

**How to:**
```bash
choco install flaco-ai
```

See [chocolatey.org/docs](https://docs.chocolatey.org) for publishing guide.

---

## Windows SmartScreen

### What is SmartScreen?

Windows security feature that warns users about unknown applications.

### Levels of Trust

1. **No Signature** - Red warning, very scary
2. **Standard Signature** - Yellow warning, less scary, requires "reputation"
3. **EV Signature** - No warning (immediate trust)

### Building Reputation

**For Standard Certificates:**
- Downloads must accumulate over weeks/months
- Microsoft tracks installations
- Eventually SmartScreen learns your app is safe
- Can take 3-6 months for good reputation

**For EV Certificates:**
- Immediate trust
- No warnings from day one
- Worth the extra cost (~$500/year)

### Bypassing for Testing

Users can click "More info" → "Run anyway" to bypass SmartScreen.

**Document this in your README:**

```markdown
## Windows Installation

If you see a SmartScreen warning:

1. Click "More info"
2. Click "Run anyway"

This happens because Flaco AI is new. Once we build reputation,
warnings will disappear. We're working on getting an EV certificate
for immediate trust.
```

---

## Auto-Updates on Windows

### How it Works

Flaco AI uses `electron-updater` for automatic updates:

1. App checks GitHub Releases for new versions
2. Downloads update in background
3. Prompts user to restart
4. Installs update on restart

### Update Files Needed

For Windows updates, you need:

1. **NSIS Installer** (`.exe`)
   - Full installer for new users

2. **NSIS Update** (`.exe` with different metadata)
   - Delta update for existing users
   - electron-builder creates this automatically

3. **Blockmap Files** (`.exe.blockmap`)
   - For efficient delta updates
   - electron-builder creates this automatically

4. **`latest.yml`** (auto-generated)
   - Update manifest
   - electron-builder creates this

### Release Process

```bash
# 1. Build for Windows
npm run build:win

# 2. Upload to GitHub Releases
# - Flaco AI-0.0.2-x64-Setup.exe (full installer)
# - Flaco AI-0.0.2-x64-Setup.exe.blockmap (for updates)
# - latest.yml (update manifest)

# 3. App will auto-detect and prompt users to update
```

### Testing Updates

1. Install v0.0.1
2. Release v0.0.2 to GitHub
3. Open v0.0.1
4. Wait 3 seconds (initial check delay)
5. Should see update notification

---

## Windows-Specific Features

### Installation Paths

```
Default: C:\Users\<Username>\AppData\Local\Programs\Flaco AI\
User Data: C:\Users\<Username>\AppData\Roaming\flaco-desktop\
```

### Start Menu & Desktop Shortcuts

Automatically created by NSIS installer:
- Start Menu: `Flaco AI`
- Desktop: `Flaco AI` (optional during install)

### Uninstaller

Located in:
```
C:\Users\<Username>\AppData\Local\Programs\Flaco AI\Uninstall Flaco AI.exe
```

Also in Windows Settings → Apps & features

### Registry Keys

electron-builder creates:
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Uninstall\{GUID}
```

For app registration and uninstall info.

---

## Troubleshooting

### Build fails with "Wine not found"

**Fix (macOS):**
```bash
brew install wine-stable
```

**Fix (Linux):**
```bash
sudo apt install wine64
```

### "Code signing certificate not found"

**Fix:**
1. Check certificate is installed in Windows
2. Verify environment variables:
   ```bash
   echo $WIN_CSC_LINK
   echo $WIN_CSC_KEY_PASSWORD
   ```
3. Try absolute path in environment variable

### SmartScreen blocks installer

**For developers:**
```powershell
# Disable SmartScreen temporarily (testing only!)
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" -Name "SmartScreenEnabled" -Value "Off"
```

**For users:**
- Click "More info" → "Run anyway"
- Or right-click installer → Properties → Unblock

### Auto-updater not working

**Check:**
1. `latest.yml` exists in GitHub Release
2. `package.json` has correct `publish` config:
   ```json
   "publish": {
     "provider": "github",
     "owner": "RouraIO",
     "repo": "flaco.desktop"
   }
   ```
3. Release is marked as "Latest" (not pre-release)
4. Check DevTools console for update errors

---

## Windows vs macOS Differences

| Feature | macOS | Windows |
|---------|-------|---------|
| **Installer** | DMG (drag-drop) | NSIS (setup wizard) |
| **Code Signing** | Developer ID ($99/yr) | Standard/EV cert ($300-500/yr) |
| **Trust** | Notarization required | EV cert for immediate trust |
| **App Path** | `/Applications` | `C:\Users\...\AppData\Local\Programs` |
| **User Data** | `~/Library/Application Support` | `%APPDATA%` |
| **Auto-update** | ✅ Works | ✅ Works |
| **Multiple instances** | No (singleton) | No (singleton) |

---

## Linux Support

Flaco AI also builds for Linux:

```bash
npm run build:linux
```

**Formats:**
- AppImage (portable, no install)
- .deb (Debian/Ubuntu)
- .rpm (Fedora/RedHat)

**Distribution:**
- AppImage: Direct download
- Snap Store: `snapcraft.io`
- Flathub: `flathub.org`

See `LINUX_DEPLOYMENT.md` (coming soon) for details.

---

## Best Practices

1. **Always sign production builds**
   - Users trust signed apps more
   - Reduces support requests about warnings

2. **Test on fresh Windows VM**
   - Test installer on clean Windows
   - Verify no security warnings (with signing)
   - Check all features work

3. **Include blockmaps in releases**
   - Makes updates much faster
   - electron-builder creates them automatically

4. **Document SmartScreen warnings**
   - Be transparent about warnings
   - Explain why they happen
   - Show how to bypass safely

5. **Consider EV certificate**
   - If targeting non-technical users
   - Worth the extra cost for trust
   - No reputation-building time needed

---

## Cost Summary

### Minimum (No Signing)
- **Free** - But users see scary warnings

### Standard Code Signing
- **$239-474/year** - Certificate
- **3-6 months** - Build reputation for no warnings

### EV Code Signing
- **$400-700/year** - Certificate
- **Immediate** - No warnings from day one
- **Recommended for production**

---

## Next Steps

1. ✅ Windows build configuration added
2. ⏳ Get code signing certificate
3. ⏳ Test build on Windows
4. ⏳ Set up CI/CD
5. ⏳ Create first Windows release
6. ⏳ Build SmartScreen reputation

---

**Remember:** Windows has the largest desktop market share (~75%). Supporting it well is critical for success!
