const sharp = require('sharp');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const sizes = [
  { size: 16, name: 'icon_16x16.png' },
  { size: 32, name: 'icon_16x16@2x.png' },
  { size: 32, name: 'icon_32x32.png' },
  { size: 64, name: 'icon_32x32@2x.png' },
  { size: 128, name: 'icon_128x128.png' },
  { size: 256, name: 'icon_128x128@2x.png' },
  { size: 256, name: 'icon_256x256.png' },
  { size: 512, name: 'icon_256x256@2x.png' },
  { size: 512, name: 'icon_512x512.png' },
  { size: 1024, name: 'icon_512x512@2x.png' }
];

const iconsetPath = path.join(__dirname, 'assets', 'icon.iconset');
const svgPath = path.join(__dirname, 'assets', 'flaco-logo.svg');
const icnsPath = path.join(__dirname, 'assets', 'icon.icns');

// Create iconset directory
if (!fs.existsSync(iconsetPath)) {
  fs.mkdirSync(iconsetPath, { recursive: true });
}

// Generate PNG files
Promise.all(
  sizes.map(({ size, name }) => {
    return sharp(svgPath)
      .resize(size, size)
      .png()
      .toFile(path.join(iconsetPath, name));
  })
)
.then(() => {
  console.log('✓ Generated all PNG sizes');

  // Convert iconset to icns using iconutil
  exec(`iconutil -c icns "${iconsetPath}" -o "${icnsPath}"`, (error, stdout, stderr) => {
    if (error) {
      console.error('Error creating icns:', error);
      return;
    }
    console.log('✓ Created icon.icns');

    // Clean up iconset directory
    fs.rmSync(iconsetPath, { recursive: true, force: true });
    console.log('✓ Cleaned up temporary files');
    console.log('\n✨ Icon generation complete!');
  });
})
.catch(err => {
  console.error('Error generating icons:', err);
});
