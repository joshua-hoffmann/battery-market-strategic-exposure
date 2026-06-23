$ErrorActionPreference = "Stop"

$SnapshotPath = "PROJECT_STATUS_SNAPSHOT.md"

$lines = @()
$lines += "# PROJECT STATUS SNAPSHOT"
$lines += ""
$lines += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$lines += ""
$lines += "Project Root:"
$lines += ""
$lines += '```text'
$lines += (Get-Location).Path
$lines += '```'
$lines += ""

$lines += "## 1. Top-Level Folder State"
$lines += ""
$lines += '```text'
$lines += (Get-ChildItem -Force | Select-Object Mode, LastWriteTime, Length, Name | Format-Table -AutoSize | Out-String)
$lines += '```'
$lines += ""

$lines += "## 2. Important Governance Files"
$lines += ""
$governanceFiles = @(
    "PROJECT_STATE.md",
    "PROJECT_FILE_REGISTRY.md",
    "PROJECT_CHANGELOG.md",
    "PROJECT_STATUS_SNAPSHOT.md",
    "README.md",
    "requirements.txt",
    ".gitignore"
)

$lines += '```text'
foreach ($file in $governanceFiles) {
    if (Test-Path $file) {
        $item = Get-Item $file
        $lines += ("{0,-35} EXISTS  {1}  {2} bytes" -f $file, $item.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss"), $item.Length)
    } else {
        $lines += ("{0,-35} MISSING" -f $file)
    }
}
$lines += '```'
$lines += ""

$lines += "## 3. Source Scripts"
$lines += ""
$lines += '```text'
if (Test-Path "src") {
    $lines += (Get-ChildItem "src" -File | Select-Object LastWriteTime, Length, Name | Format-Table -AutoSize | Out-String)
} else {
    $lines += "src folder missing"
}
$lines += '```'
$lines += ""

$lines += "## 4. Data Folders"
$lines += ""
$lines += '```text'
if (Test-Path "data") {
    $lines += (Get-ChildItem "data" -Recurse -File | Select-Object LastWriteTime, Length, FullName | Format-Table -AutoSize | Out-String)
} else {
    $lines += "data folder missing"
}
$lines += '```'
$lines += ""

$lines += "## 5. Output Files"
$lines += ""
$lines += '```text'
if (Test-Path "outputs") {
    $lines += (Get-ChildItem "outputs\briefs","outputs\charts" -Recurse -File -ErrorAction SilentlyContinue | Select-Object LastWriteTime, Length, FullName | Format-Table -AutoSize | Out-String)
} else {
    $lines += "outputs folder missing"
}
$lines += '```'
$lines += ""

$lines += "## 6. Documentation and Learning Files"
$lines += ""
$lines += '```text'
$docLearningFiles = @()
if (Test-Path "docs") {
    $docLearningFiles += Get-ChildItem "docs" -Recurse -File
}

if ($docLearningFiles.Count -gt 0) {
    $lines += ($docLearningFiles | Select-Object LastWriteTime, Length, FullName | Format-Table -AutoSize | Out-String)
} else {
    $lines += "No documentation files found"
}
$lines += '```'
$lines += ""

$lines += "## 7. Git Status"
$lines += ""
$lines += '```text'
try {
    $gitStatus = git status --short | Out-String
    if ([string]::IsNullOrWhiteSpace($gitStatus)) {
        $lines += "Working tree clean"
    } else {
        $lines += $gitStatus
    }
} catch {
    $lines += "Git status unavailable"
}
$lines += '```'

$lines | Set-Content -Path $SnapshotPath -Encoding UTF8

Get-Content $SnapshotPath

