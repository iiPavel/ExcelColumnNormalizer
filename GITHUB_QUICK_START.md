# 建立 GitHub 仓库快速指南

## 第 1 步：在 GitHub 创建空仓库

1. 访问 https://github.com/new
2. **Repository name**：`ExcelColumnNormalizer`
3. **Description**：`Excel Column Standardization Tool`（可选）
4. 选择 **Public** 或 **Private**
5. **不勾选** "Add a README file"、"Add .gitignore"、"Add a license"（保持空仓库）
6. 点击 **Create repository**

## 第 2 步：在本地初始化 Git 并推送

复制你的仓库 URL（形如 `https://github.com/YOU/ExcelColumnNormalizer.git`），然后运行：

```bash
cd /Users/bingfoon/Code/demo
git init
git add .
git commit -m "Initial commit: Excel Column Normalizer with GitHub Actions CI/CD"
git branch -M main
git remote add origin https://github.com/YOU/ExcelColumnNormalizer.git
git push -u origin main
```

（将 `https://github.com/YOU/ExcelColumnNormalizer.git` 替换为你的仓库 URL）

## 第 3 步：验证 GitHub Actions 自动构建

1. 推送后，访问你的仓库页面
2. 点击 **Actions** 标签
3. 应该看到 "Build and Release" 工作流正在运行
4. 等待 10-15 分钟，直到两个平台（macOS ARM64 + Windows）构建完成
5. 构建完成后，点击工作流，向下滚动到 **Artifacts** 下载 `.zip` 文件

## 第 4 步：发布版本（发布给用户）

当你想发布新版本时：

```bash
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions 会自动构建并发布到 **Releases** 页面。用户可以从 `https://github.com/YOU/ExcelColumnNormalizer/releases` 下载应用。

---

## 快速命令汇总

```bash
# 初始化本地仓库
git init
git add .
git commit -m "Initial commit"

# 连接到 GitHub（替换 YOUR_USERNAME 为你的用户名）
git remote add origin https://github.com/YOUR_USERNAME/ExcelColumnNormalizer.git
git branch -M main
git push -u origin main

# 发布版本（可选）
git tag v1.0.0
git push origin v1.0.0
```

祝你上传顺利！有任何问题可以随时问我。
