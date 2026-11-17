<div align="center">
<img src="https://raw.githubusercontent.com/Crosstalk-Solutions/project-nomad/refs/heads/main/admin/public/project_nomad_logo.png" width="200" height="200"/>

# Project N.O.M.A.D.
### 离线媒体、档案和数据的节点

**永不离线的知识**

[![Website](https://img.shields.io/badge/Website-projectnomad.us-blue)](https://www.projectnomad.us)
[![Discord](https://img.shields.io/badge/Discord-Join%20Community-5865F2)](https://discord.com/invite/crosstalksolutions)
[![Benchmark](https://img.shields.io/badge/Benchmark-Leaderboard-green)](https://benchmark.projectnomad.us)

</div>

---

Project N.O.M.A.D. 是一个自包含的、优先离线的知识和教育服务器，集成了关键工具、知识和人工智能，让您随时随地保持信息灵通和赋能。

## 安装与快速开始
Project N.O.M.A.D. 可以安装在任何基于 Debian 的操作系统上（我们推荐 Ubuntu）。安装完全基于终端，所有工具和资源都设计为通过浏览器访问，因此如果您更愿意将 N.O.M.A.D. 设置为"服务器"并通过其他客户端访问，则不需要桌面环境。

*注意：运行安装脚本需要 sudo/root 权限*

### 快速安装（仅限基于 Debian 的操作系统）
```bash
sudo apt-get update && sudo apt-get install -y curl && curl -fsSL https://raw.githubusercontent.com/Crosstalk-Solutions/project-nomad/refs/heads/main/install/install_nomad.sh -o install_nomad.sh && sudo bash install_nomad.sh
```

Project N.O.M.A.D. 现已安装在您的设备上！打开浏览器并导航到 `http://localhost:8080`（或 `http://设备IP:8080`）开始探索！

有关完整的逐步指南（包括 Ubuntu 安装），请参阅[安装指南](https://www.projectnomad.us/install)。

### 高级安装
为了更精细地控制安装过程，请将 [Docker Compose 模板](https://raw.githubusercontent.com/Crosstalk-Solutions/project-nomad/refs/heads/main/install/management_compose.yaml)复制并粘贴到 `docker-compose.yml` 文件中，并根据您的喜好进行自定义（确保用实际值替换任何占位符）。然后，运行 `docker compose up -d` 来启动命令中心及其依赖项。注意：此方法仅推荐给高级用户，因为它需要熟悉 Docker 并在启动前进行手动配置。

## 工作原理
N.O.M.A.D. 是一个管理界面（"命令中心"）和 API，通过 [Docker](https://www.docker.com/) 协调一系列容器化工具和资源。它处理所有内容的安装、配置和更新——这样您就不必操心了。

**内置功能包括：**
- **带知识库的 AI 聊天** — 由 [Ollama](https://ollama.com/) 提供支持的本地 AI 聊天，支持文档上传和语义搜索（通过 [Qdrant](https://qdrant.tech/) 实现 RAG）
- **信息库** — 离线维基百科、医学参考资料、电子书等（通过 [Kiwix](https://kiwix.org/)）
- **教育平台** — 可汗学院课程，带进度跟踪（通过 [Kolibri](https://learningequality.org/kolibri/)）
- **离线地图** — 可下载的区域地图（通过 [ProtoMaps](https://protomaps.com)）
- **数据工具** — 加密、编码和分析（通过 [CyberChef](https://gchq.github.io/CyberChef/)）
- **笔记** — 本地笔记记录（通过 [FlatNotes](https://github.com/dullage/flatnotes)）
- **系统基准测试** — 硬件评分，带[社区排行榜](https://benchmark.projectnomad.us)
- **简易设置向导** — 引导式首次配置，带精选内容集合

N.O.M.A.D. 还包括内置工具，如维基百科内容选择器、ZIM 库管理器和内容浏览器。

## 包含内容

| 功能 | 技术支持 | 您将获得 |
|-----------|-----------|-------------|
| 信息库 | Kiwix | 离线维基百科、医学参考资料、生存指南、电子书 |
| AI 助手 | Ollama + Qdrant | 内置聊天功能，支持文档上传和语义搜索 |
| 教育平台 | Kolibri | 可汗学院课程、进度跟踪、多用户支持 |
| 离线地图 | ProtoMaps | 可下载的区域地图，带搜索和导航功能 |
| 数据工具 | CyberChef | 加密、编码、哈希和数据分析 |
| 笔记 | FlatNotes | 本地笔记记录，支持 Markdown |
| 系统基准测试 | 内置 | 硬件评分、构建者标签和社区排行榜 |

## 设备要求
虽然许多类似的离线生存计算机设计为在最低配置的轻量级硬件上运行，但 Project N.O.M.A.D. 恰恰相反。为了安装和运行可用的 AI 工具，我们强烈建议使用功能强大、支持 GPU 的设备，以充分利用您的安装。

然而，N.O.M.A.D. 的核心仍然非常轻量级。对于管理应用程序本身的精简安装，需要以下最低规格：

*注意：Project N.O.M.A.D. 不受任何硬件制造商赞助，旨在尽可能与硬件无关。下面列出的硬件仅用于示例/比较用途*

#### 最低规格
- 处理器：2 GHz 双核处理器或更好
- 内存：4GB 系统内存
- 存储：至少 5 GB 可用磁盘空间
- 操作系统：基于 Debian（推荐 Ubuntu）
- 稳定的互联网连接（仅在安装期间需要）

要运行 LLM 和其他包含的 AI 工具：

#### 推荐规格
- 处理器：AMD Ryzen 7 或 Intel Core i7 或更好
- 内存：32 GB 系统内存
- 显卡：NVIDIA RTX 3060 或 AMD 同等或更好（更多显存 = 运行更大的模型）
- 存储：至少 250 GB 可用磁盘空间（最好在 SSD 上）
- 操作系统：基于 Debian（推荐 Ubuntu）
- 稳定的互联网连接（仅在安装期间需要）

**有关三个价格点（150-1000+ 美元）的详细构建建议，请参阅[硬件指南](https://www.projectnomad.us/hardware)。**

再次强调，Project N.O.M.A.D. 本身相当轻量级——是您选择与 N.O.M.A.D. 一起安装的工具和资源将决定您独特部署所需的规格。

## 常见问题解答 (FAQ)
有关 Project N.O.M.A.D. 常见问题的答案，请参阅我们的 [FAQ](FAQ.md) 页面。

## 关于互联网使用和隐私
Project N.O.M.A.D. 设计用于离线使用。互联网连接仅在初始安装期间（下载依赖项）以及如果您（用户）决定稍后下载其他工具和资源时才需要。否则，N.O.M.A.D. 不需要互联网连接，并且内置零遥测功能。

为了测试互联网连接，N.O.M.A.D. 尝试向 Cloudflare 的实用程序端点 `https://1.1.1.1/cdn-cgi/trace` 发出请求，并检查是否收到成功响应。

## 关于安全性
根据设计，Project N.O.M.A.D. 旨在无需障碍即可开放和可用——它不包含身份验证。如果您在安装后决定将设备连接到本地网络（例如，允许其他设备访问其资源），您可以阻止/开放端口来控制哪些服务被暴露。

**将来会添加身份验证吗？** 可能。目前这不是优先事项，但如果有足够的需求，我们可能会考虑在未来的版本中构建一个可选的身份验证层，以支持多个用户需要访问同一实例但具有不同权限级别的用例（例如，带家长控制的家庭使用、带教师/管理员账户的课堂使用等）。我们在公共路线图上对此有一个建议，所以如果您希望看到这个功能，请在这里投票：https://roadmap.projectnomad.us/posts/1/user-authentication-please-build-in-user-auth-with-admin-user-roles

目前，如果您计划将 N.O.M.A.D. 实例暴露给本地网络上的其他设备，我们建议使用网络级控制来管理访问。N.O.M.A.D. 不设计为直接暴露给互联网，我们强烈建议不要这样做，除非您真正知道自己在做什么，已经采取了适当的安全措施，并了解所涉及的风险。

## 贡献
欢迎并感谢贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何为项目做出贡献的指南。

## 社区与资源

- **网站：** [www.projectnomad.us](https://www.projectnomad.us) - 了解更多关于项目的信息
- **Discord：** [加入社区](https://discord.com/invite/crosstalksolutions) - 获取帮助、分享您的构建并与其他 NOMAD 用户联系
- **基准测试排行榜：** [benchmark.projectnomad.us](https://benchmark.projectnomad.us) - 查看您的硬件与其他 NOMAD 构建的对比情况
- **故障排除指南：** [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 查找常见问题的解决方案
- **常见问题解答：** [FAQ.md](FAQ.md) - 查找常见问题的答案

## 许可证

Project N.O.M.A.D. 根据 [Apache License 2.0](LICENSE) 许可。

## 辅助脚本
安装后，Project N.O.M.A.D. 有一些辅助脚本，如果您需要排除故障或执行无法通过命令中心完成的维护。所有这些脚本都位于 Project N.O.M.A.D. 的安装目录 `/opt/project-nomad` 中。

###

###### 启动脚本 - 启动所有已安装的项目容器
```bash
sudo bash /opt/project-nomad/start_nomad.sh
```
###

###### 停止脚本 - 停止所有已安装的项目容器
```bash
sudo bash /opt/project-nomad/stop_nomad.sh
```
###

###### 更新脚本 - 尝试拉取命令中心及其依赖项（即 mysql）的最新镜像并重新创建容器。注意：这*仅*更新命令中心容器。它不更新可安装的应用程序容器——这应该通过命令中心 UI 完成
```bash
sudo bash /opt/project-nomad/update_nomad.sh
```

###### 卸载脚本 - 需要重新开始？使用卸载脚本让您的生活更轻松。注意：这无法撤销！
```bash
curl -fsSL https://raw.githubusercontent.com/Crosstalk-Solutions/project-nomad/refs/heads/main/install/uninstall_nomad.sh -o uninstall_nomad.sh && sudo bash uninstall_nomad.sh
```