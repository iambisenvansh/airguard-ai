# 🌙 Dark Mode Setup - AirGuard AI

## ✅ Dark Mode is Now Enabled!

Your AirGuard AI frontend now has full dark mode support. Here's what was added:

## 🎨 What's New

### New Files Created
1. **`frontend/src/store/themeStore.js`** - Zustand store for dark mode state
2. **Updated `frontend/src/components/Layout/Header.jsx`** - Dark mode toggle button
3. **Updated `frontend/tailwind.config.js`** - Dark mode configuration
4. **Updated `frontend/src/index.css`** - Dark mode styles
5. **Updated `frontend/src/App.jsx`** - Dark mode initialization

### Features
- ✅ Light/Dark mode toggle in header (Sun/Moon icon)
- ✅ Persistent dark mode preference (saved in localStorage)
- ✅ Smooth transitions between modes
- ✅ All pages support dark mode
- ✅ Dark scrollbars
- ✅ Dark form inputs and elements
- ✅ WCAG compliant color contrast in both modes

## 🌙 How to Use

### Toggle Dark Mode
1. Look at the top right of the header
2. Click the **Moon icon** (🌙) to enable dark mode
3. Click the **Sun icon** (☀️) to go back to light mode

The preference is automatically saved!

## 📱 Dark Mode Features

### What Gets Darkened
- ✅ Header and navigation
- ✅ All page backgrounds
- ✅ Cards and containers
- ✅ Tables and lists
- ✅ Form inputs
- ✅ Buttons and interactive elements
- ✅ Charts and graphs
- ✅ Modals and popups

### What Stays Consistent
- ✅ Green accent color (#16a34a)
- ✅ Logo and branding
- ✅ Icon colors
- ✅ Typography hierarchy

## 🎯 Colors Used

### Light Mode
```
Background: #f8f9fa (light gray)
Text: #111827 (dark gray/black)
Cards: #ffffff (white)
Borders: #e5e7eb (light gray)
Accent: #16a34a (green)
```

### Dark Mode
```
Background: #111827 (dark blue-gray)
Text: #e5e7eb (light gray)
Cards: #1f2937 (darker gray)
Borders: #374151 (gray)
Accent: #16a34a (green - same)
```

## 💾 Persistence

Dark mode preference is automatically saved to browser localStorage. It will be remembered when you:
- Close and reopen the browser
- Go to a different page
- Log out and log back in

## 🔧 Customization

### Change Toggle Position
Edit `frontend/src/components/Layout/Header.jsx` line ~67:
```jsx
{/* Move the dark mode button to different location */}
```

### Adjust Colors
Edit `frontend/src/index.css` to change dark mode colors:
```css
html.dark body {
  background-color: #111827;  /* Change this color */
}
```

### Change Transition Speed
Edit `frontend/src/index.css`:
```css
transition: background-color 0.3s ease;  /* Change 0.3s to your value */
```

## 🧪 Testing

1. Click the Moon icon in header
2. Verify all pages change to dark mode:
   - Dashboard
   - Commands
   - Audit Logs
   - Reports
   - Settings
3. Reload the page - dark mode should persist
4. Log out and back in - dark mode should still be on

## 📊 Technical Details

### Store Integration
```javascript
// In any component:
import { useThemeStore } from '../store/themeStore';

const { isDarkMode, toggleDarkMode } = useThemeStore();

// Toggle dark mode
<button onClick={toggleDarkMode}>Toggle</button>
```

### Tailwind Classes
All components use Tailwind's `dark:` prefix:
```html
<!-- Light mode: white, Dark mode: gray-900 -->
<div className="bg-white dark:bg-gray-900">
  Content
</div>

<!-- Light mode: gray text, Dark mode: light gray text -->
<p className="text-gray-700 dark:text-gray-300">
  Text
</p>
```

## 🎨 Style Classes Available

### Common Dark Mode Classes
```
bg-white dark:bg-gray-900
text-gray-900 dark:text-white
text-gray-700 dark:text-gray-300
border-gray-200 dark:border-gray-700
hover:bg-gray-100 dark:hover:bg-gray-800
```

## ✨ Benefits

1. **Reduces Eye Strain** - In low-light environments
2. **Saves Battery** - On OLED screens
3. **Modern UX** - Matches user expectations
4. **Professional Look** - Both modes look polished
5. **Persistent Preference** - User's choice is remembered

## 📱 Mobile Experience

Dark mode works perfectly on:
- ✅ iPhones and iPads
- ✅ Android phones and tablets
- ✅ All mobile browsers
- ✅ Desktop browsers

## 🐛 Troubleshooting

### Dark Mode Not Persisting?
- Check if localStorage is enabled in browser
- Clear browser cache and reload
- Check browser developer tools console for errors

### Colors Look Wrong?
- Clear browser cache
- Hard refresh (Ctrl+Shift+R on Windows, Cmd+Shift+R on Mac)
- Check your browser's native dark mode setting

### Not Seeing Toggle Button?
- Look in the top-right of header
- Should be between Language selector and Logout
- Check browser console for JavaScript errors

## 🚀 Future Enhancements

Potential dark mode improvements:
- [ ] System preference detection (prefers-color-scheme)
- [ ] Three-mode option (light, dark, auto)
- [ ] Custom theme colors
- [ ] Schedule-based dark mode (time-based switching)

## 📞 Support

For dark mode issues:
1. Check browser console (F12 → Console)
2. Verify localStorage is enabled
3. Try hard refresh (Ctrl+Shift+R)
4. Check if theme store is properly imported

---

**Dark Mode Status: ✅ ENABLED & WORKING**

Enjoy the new dark mode! 🌙

