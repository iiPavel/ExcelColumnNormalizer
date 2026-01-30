# GitHub Actions 自动构建与发布

本项目已配置 GitHub Actions 工作流，支持在 macOS ARM64 和 Windows 平台上自动构建应用。

## 工作流触发方式

1. **推送到 main 或 develop 分支**：触发构建，生成 artifacts 供下载
2. **创建 git tag `v*`**（如 `v1.0.0`）：触发构建并自动发布到 GitHub Releases
3. **手动触发**：在 GitHub Actions 标签页点击 "Run workflow"

## 构建工件

- **macOS ARM64**：`ExcelColumnNormalizer-macOS-arm64.zip`（包含 `.app` 应用包）
- **Windows x64**：`ExcelColumnNormalizer-Windows-x64.zip`（包含可执行目录）

### 使用构建的应用

#### macOS
```bash
unzip ExcelColumnNormalizer-macOS-arm64.zip
open ExcelColumnNormalizer.app
```

#### Windows
```powershell
# 解压后运行
Expand-Archive -Path "ExcelColumnNormalizer-Windows-x64.zip" -DestinationPath .
.\ExcelColumnNormalizer\ExcelColumnNormalizer.exe
```

## 发布新版本

1. 创建 git tag：
```bash
git tag v1.0.0
git push origin v1.0.0
```

2. GitHub Actions 将自动构建两个平台的版本并上传到 Releases。

3. 编辑 Release 描述并发布（可选）。

## 工作流配置位置

- 工作流文件：[`.github/workflows/build.yml`](../../.github/workflows/build.yml)
- macOS spec：[`app.spec`](app.spec)
- Windows spec：[`app_windows.spec`](app_windows.spec)
- 打包脚本：[`scripts/package_app.sh`](scripts/package_app.sh)
- 签名脚本（可选）：[`scripts/sign_and_notarize.sh`](scripts/sign_and_notarize.sh)

## 注意事项

- macOS 应用未签名/未公证。如果需要面向广泛用户发布，请：
  1. 在本地运行 `scripts/sign_and_notarize.sh`（需要 Apple Developer ID）
  2. 或在 Actions 中集成代码签名秘密（需要安全配置）
  
- Windows 应用直接构建，用户首次运行时可能看到 SmartScreen 警告（正常现象）。

- 为了加快构建速度，Actions 使用了 pip 缓存和 Python 依赖缓存。
