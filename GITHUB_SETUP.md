# 快速开始：在 GitHub 上设置项目

按以下步骤将本地项目推送到 GitHub 并启用自动构建。

## 1. 在 GitHub 创建新仓库

1. 登录 [github.com](https://github.com)
2. 点击右上角 **+** 图标，选择 **New repository**
3. 仓库名：`ExcelColumnNormalizer`（或你喜欢的名称）
4. 选择 **Public**（如果想分享）或 **Private**（私有）
5. **不要**勾选"Initialize this repository with a README"、".gitignore" 或 "License"（保持空仓库）
6. 点击 **Create repository**

## 2. 初始化本地 Git 并推送

在你的项目目录（/Users/bingfoon/Code/demo）运行以下命令：

```bash
# 初始化 git 仓库（如果还未初始化）
git init

# 添加所有文件
git add .

# 创建首次提交
git commit -m "Initial commit: Add Excel column normalizer app with GitHub Actions CI/CD"

# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/ExcelColumnNormalizer.git

# 将代码推送到 main 分支
git branch -M main
git push -u origin main
```

## 3. 验证 GitHub Actions

1. 在 GitHub 仓库页面，点击 **Actions** 标签
2. 应该看到正在运行的工作流：`Build and Release`
3. 等待构建完成（通常 10-15 分钟）
4. 构建成功后，点击工作流名称查看详情
5. 向下滚动到 **Artifacts** 部分，下载构建的 `.zip` 文件

## 4. 发布版本（可选）

准备好发布时，运行：

```bash
# 创建版本标签
git tag v1.0.0

# 推送标签到 GitHub
git push origin v1.0.0
```

GitHub Actions 将自动构建两个平台的版本，并上传到 **Releases** 页面。

## 故障排除

**如果 Actions 失败：**
- 点击失败的工作流查看日志
- 常见原因：
  - 缺少 `requirements.txt` 或依赖安装失败
  - macOS 脚本权限问题（已在工作流中添加 `chmod +x`）
  - Windows PowerShell 执行策略问题

**如果看不到 Actions：**
- 确保已推送到 `main` 或 `develop` 分支
- 检查 `.github/workflows/build.yml` 是否已提交
- 刷新页面或等待 1-2 分钟

## 下一步

- 将仓库 URL 分享给他人：`https://github.com/YOUR_USERNAME/ExcelColumnNormalizer`
- 用户可以从 **Releases** 页下载构建好的应用
- 每次推送 tag（如 `v1.1.0`）都会自动发布新版本
