# 在 macOS 上构建可运行 App

快速说明（在 macOS 上运行）：

1. 打开终端，切换到项目根目录。
2. 运行构建脚本：

```bash
./build_mac.sh
```

脚本动作：
- 创建虚拟环境：`.venv_mac`
- 安装 `requirements.txt` 中的依赖和 `pyinstaller`
- 执行 `pyinstaller app.spec`，生成 `dist/ExcelColumnNormalizer/ExcelColumnNormalizer.app`

- 注意事项：
- 需要在 macOS 上运行构建脚本（在非 macOS 环境下生成的二进制可能不可用）。
- PySide6 依赖较多，打包过程会把 Qt 插件和库一并收集，构建目录会比较大。
- 如果需要对生成的 `.app` 做签名与 notarization，请参考 Apple 官方文档或使用 `codesign` 与 `altool`（或 `notarytool`）。

打包为 `.app`：

```bash
./scripts/package_app.sh
```

代码签名与 notarization：

1. 设置签名身份：

```bash
export CODESIGN_IDENTITY="Developer ID Application: Your Name (TEAMID)"
export BUNDLE_ID="com.yourcompany.ExcelColumnNormalizer"
```

2. 使用脚本签名并（可选）提交 notarize：

```bash
./scripts/sign_and_notarize.sh
```

说明：`sign_and_notarize.sh` 支持使用 `xcrun notarytool` 的基于 API key 的方式。要使用它，请设置环境变量 `ASC_API_KEY`（指向 `.p8` 文件）、`ASC_KEY_ID`、`ASC_ISSUER`。脚本会对 `.app` 做 `codesign --deep --options runtime` 签名并在提供 API key 时提交 notarize 请求。

常见调试方法：
- 若应用启动时报错，先以终端模式运行生成的可执行文件以查看报错：

```bash
./dist/ExcelColumnNormalizer/ExcelColumnNormalizer.app/Contents/MacOS/ExcelColumnNormalizer
```

- 若缺少资源（如 `config.json`），请确认 `app.spec` 中的 `datas` 配置包含了需要的文件或目录。
