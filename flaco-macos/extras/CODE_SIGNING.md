# Code Signing & Notarization Guide

This guide explains how to properly sign and notarize Flaco AI for distribution.

## Why Code Signing Matters

Without proper code signing:
- ❌ macOS shows "unidentified developer" warnings
- ❌ Users must right-click → Open to bypass Gatekeeper
- ❌ App appears untrustworthy
- ❌ Auto-updater may not work reliably

With proper code signing:
- ✅ No security warnings
- ✅ Users can double-click to open
- ✅ Professional appearance
- ✅ Auto-updater works seamlessly

## Prerequisites

### 1. Apple Developer Account
- Cost: $99/year
- Sign up: https://developer.apple.com/programs/

### 2. Developer ID Certificate
After enrolling:
1. Go to https://developer.apple.com/account/resources/certificates
2. Click "+" to create new certificate
3. Select "Developer ID Application"
4. Follow instructions to create Certificate Signing Request (CSR)
5. Download and install certificate in Keychain

### 3. App-Specific Password
For notarization:
1. Go to https://appleid.apple.com/account/manage
2. Sign in with Apple ID
3. Generate app-specific password
4. Save it securely

## Configuration

### Step 1: Update package.json

Add to `build` section:

\`\`\`json
{
  "build": {
    "appId": "com.flaco.desktop",
    "productName": "Flaco AI",
    "mac": {
      "category": "public.app-category.developer-tools",
      "hardenedRuntime": true,
      "gatekeeperAssess": false,
      "entitlements": "build/entitlements.mac.plist",
      "entitlementsInherit": "build/entitlements.mac.plist",
      "target": [
        {
          "target": "dmg",
          "arch": ["arm64", "x64"]
        },
        {
          "target": "zip",
          "arch": ["arm64", "x64"]
        }
      ],
      "identity": "Developer ID Application: YOUR NAME (TEAM_ID)"
    },
    "dmg": {
      "sign": false,
      "contents": [
        {
          "x": 130,
          "y": 220
        },
        {
          "x": 410,
          "y": 220,
          "type": "link",
          "path": "/Applications"
        }
      ]
    },
    "afterSign": "build/notarize.js",
    "publish": {
      "provider": "github",
      "owner": "yourusername",
      "repo": "flaco-desktop"
    }
  }
}
\`\`\`

### Step 2: Create Entitlements File

Create `build/entitlements.mac.plist`:

\`\`\`xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.cs.allow-dyld-environment-variables</key>
    <true/>
    <key>com.apple.security.network.client</key>
    <true/>
    <key>com.apple.security.network.server</key>
    <true/>
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>
</dict>
</plist>
\`\`\`

### Step 3: Create Notarization Script

Create `build/notarize.js`:

\`\`\`javascript
const { notarize } = require('@electron/notarize');

exports.default = async function notarizing(context) {
  const { electronPlatformName, appOutDir } = context;

  if (electronPlatformName !== 'darwin') {
    return;
  }

  // Skip notarization in development
  if (process.env.SKIP_NOTARIZE) {
    console.log('Skipping notarization (SKIP_NOTARIZE=1)');
    return;
  }

  const appName = context.packager.appInfo.productFilename;
  const appPath = \`\${appOutDir}/\${appName}.app\`;

  console.log(\`Notarizing \${appPath}...\`);

  try {
    await notarize({
      appPath,
      appleId: process.env.APPLE_ID,
      appleIdPassword: process.env.APPLE_ID_PASSWORD,
      teamId: process.env.APPLE_TEAM_ID
    });

    console.log('Notarization complete!');
  } catch (error) {
    console.error('Notarization failed:', error);
    throw error;
  }
};
\`\`\`

### Step 4: Install Notarization Package

\`\`\`bash
npm install --save-dev @electron/notarize
\`\`\`

### Step 5: Set Environment Variables

Add to `~/.zshrc` or `~/.bash_profile`:

\`\`\`bash
export APPLE_ID="your-apple-id@email.com"
export APPLE_ID_PASSWORD="xxxx-xxxx-xxxx-xxxx"  # App-specific password
export APPLE_TEAM_ID="XXXXXXXXXX"  # Your Team ID from developer.apple.com
\`\`\`

Reload shell:
\`\`\`bash
source ~/.zshrc
\`\`\`

## Find Your Team ID

1. Go to https://developer.apple.com/account/
2. Click "Membership" in sidebar
3. Team ID is listed there (10 characters)

## Build & Sign

### Development Build (Skip Signing)
\`\`\`bash
SKIP_NOTARIZE=1 npm run build
\`\`\`

### Production Build (Full Signing)
\`\`\`bash
npm run build
\`\`\`

This will:
1. Build the app
2. Sign with Developer ID certificate
3. Create DMG and ZIP
4. Notarize with Apple
5. Staple notarization ticket

**Note:** Notarization takes 5-15 minutes. Be patient!

## Verify Signing

Check if app is properly signed:
\`\`\`bash
codesign -dv --verbose=4 "dist/mac-arm64/Flaco AI.app"
\`\`\`

Should show:
- Authority=Developer ID Application: YOUR NAME (TEAM_ID)
- Sealed Resources version=2

Check notarization:
\`\`\`bash
spctl -a -vvv -t install "dist/mac-arm64/Flaco AI.app"
\`\`\`

Should show:
- accepted
- source=Notarized Developer ID

## Troubleshooting

### "No identity found"
- Make sure Developer ID certificate is installed in Keychain
- Check certificate is valid (not expired)
- Run: \`security find-identity -v -p codesigning\`

### "Notarization failed"
- Check APPLE_ID and APPLE_ID_PASSWORD are set
- Verify app-specific password is correct
- Check notarization log:
  \`\`\`bash
  xcrun notarytool log <submission-id> --apple-id $APPLE_ID --team-id $APPLE_TEAM_ID --password $APPLE_ID_PASSWORD
  \`\`\`

### "Hardened Runtime" errors
- Ensure entitlements.mac.plist is in build/ folder
- Verify hardenedRuntime: true in package.json

### Build succeeds but no signature
- Check build logs for signing errors
- Verify identity string matches certificate exactly

## CI/CD Setup (GitHub Actions)

Add secrets to GitHub repository:
- APPLE_ID
- APPLE_ID_PASSWORD
- APPLE_TEAM_ID
- CSC_LINK (base64 encoded certificate .p12)
- CSC_KEY_PASSWORD (certificate password)

Example workflow:
\`\`\`yaml
name: Build & Release
on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm install

      - name: Build & Sign
        env:
          APPLE_ID: \${{ secrets.APPLE_ID }}
          APPLE_ID_PASSWORD: \${{ secrets.APPLE_ID_PASSWORD }}
          APPLE_TEAM_ID: \${{ secrets.APPLE_TEAM_ID }}
          CSC_LINK: \${{ secrets.CSC_LINK }}
          CSC_KEY_PASSWORD: \${{ secrets.CSC_KEY_PASSWORD }}
        run: npm run build

      - name: Upload Release
        uses: softprops/action-gh-release@v1
        with:
          files: dist/*.dmg
\`\`\`

## Best Practices

1. **Never commit certificates or passwords** to git
2. **Use environment variables** for sensitive data
3. **Test signing locally** before CI/CD
4. **Keep certificates backed up** securely
5. **Renew certificates** before expiration
6. **Monitor notarization logs** for issues

## Cost Summary

- Apple Developer Program: $99/year
- Notarization: Free (included with Developer Program)
- Code signing certificate: Free (included with Developer Program)

**Total:** $99/year

## Alternative: Self-Signing (Not Recommended)

You can create a self-signed certificate, but:
- ❌ Users still see warnings
- ❌ No notarization possible
- ❌ Not suitable for distribution

Only use for personal testing.

## Next Steps

After signing is set up:
1. Test on a fresh Mac (not your development machine)
2. Verify no Gatekeeper warnings
3. Set up auto-updater with signed builds
4. Configure CI/CD for automated releases

## Support

If you encounter issues:
- Apple Developer Forums: https://developer.apple.com/forums/
- electron-builder docs: https://www.electron.build/
- Electron notarization: https://www.electronjs.org/docs/latest/tutorial/code-signing

---

**Remember:** Code signing is required for production distribution. Don't skip this step!
