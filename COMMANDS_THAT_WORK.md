# AirGuard AI - Commands That Generate Reports

## ✅ Commands That CREATE Reports (Will Show in Reports Page)

### Generate Report Commands
```
"Generate pollution report for Delhi"
"Generate pollution report for Mumbai"
"Create report for Bangalore"
"Produce a pollution report for Hyderabad"
"Make a report for Pune"
```

**Result**: ✅ Creates a report FILE → Saved to database → Shows in Reports page

---

## ⚠️ Commands That DON'T CREATE Reports (Analysis Only)

### Analyze Commands
```
"Analyze AQI for Delhi"
"Analyze AQI in Mumbai"
"Check air quality for Bangalore"
"Review pollution levels for Delhi"
```

**Result**: ❌ No file created → Shows analysis data → NO report in Reports page

### Alert Commands
```
"Send critical alert about high pollution"
"Send warning for Delhi area"
```

**Result**: ❌ No file created → No report in Reports page

---

## 🎯 Quick Test Flow

### Step 1: Go to Commands Page
Click the **Commands** tab

### Step 2: Enter This Command
```
Generate pollution report for Delhi
```

### Step 3: Submit
- Press Enter or click Submit button
- Wait for response
- You should see: "✅ Allowed" + "Report generated successfully"

### Step 4: Check Reports
- Click **Reports** tab
- You should now see the generated report in the list!
- Try Download or View buttons

---

## 📍 Supported Locations

These locations have data in the system:
- **Delhi** - Very Poor air quality (AQI ~300)
- **Mumbai** - Very Poor air quality (AQI ~275)
- **Nagpur** - Unhealthy for Sensitive Groups (AQI ~170)
- **Bangalore** - Moderate air quality (AQI ~100)
- **Hyderabad** - Unhealthy for Sensitive Groups (AQI ~130)
- **Pune** - Unhealthy for Sensitive Groups (AQI ~120)
- **Kolkata** - Unhealthy (AQI ~200)
- **Chennai** - Moderate air quality (AQI ~80)
- **Ahmedabad** - Unhealthy for Sensitive Groups (AQI ~150)
- **Jaipur** - Unhealthy (AQI ~180)
- **Lucknow** - Very Unhealthy (AQI ~220)

Try commands like:
```
Generate pollution report for Mumbai
Generate pollution report for Bangalore
Generate pollution report for Nagpur
Generate pollution report for Hyderabad
Generate pollution report for Chennai
```

---

## 🔍 How It Works

1. **You type**: "Generate pollution report for Delhi"
2. **Backend parses** → Detects action: `generate_report`
3. **Policy checks** → Allows it (green ✅)
4. **Executor runs** → Creates actual report FILE
5. **Backend saves** → Adds report metadata to database
6. **Frontend fetches** → Shows report in Reports page

---

## Troubleshooting

### "No reports found" in Reports page?

**Check this**:
1. ✅ Did you use "Generate report..." command? (not "Analyze AQI")
2. ✅ Did you see "✅ Allowed" response?
3. ✅ Did you see "Report generated successfully" in response?
4. ✅ Did you use a valid location? (Delhi, Mumbai, Bangalore, etc.)

### Report shows but no content?

**This is OK** - The Report model stores metadata but may not load file content by default. The download button will work perfectly.

### Command got blocked?

**This means** the policy denied it. Check the response for the reason (usually only `shutdown_factory` and `issue_fine` are blocked).

---

## ✨ Full Example Workflow

```bash
1. Go to http://localhost:3000
2. Login as: admin / password123
3. Click Commands tab
4. Type: "Generate pollution report for Delhi"
5. Press Enter
6. Wait for green "✅ Allowed" response
7. See "Report generated successfully"
8. Click Reports tab
9. See the report in the list with download button
```

---

## Key Difference

| Command | Type | Creates File? | In Reports? | Use For |
|---------|------|---------------|------------|---------|
| "Generate report for Delhi" | generate_report | ✅ YES | ✅ YES | Getting actual reports |
| "Analyze AQI for Delhi" | analyze_aqi | ❌ NO | ❌ NO | Quick data lookup |
| "Send alert..." | send_alert | ❌ NO | ❌ NO | Notifications |

---

**TL;DR**: Use **"Generate pollution report for [location]"** to create reports that show up in the Reports page!
