# LUCALIVE — Multi-Platform Live Streaming Website

**Language / 语言 / 언어:** [English](#english-default) · [中文](#中文) · [한국어](#한국어)

**Same content in each language** — every section (features, stack, run guide, API, folders, env vars, license) is fully written out in English, 中文, and 한국어; pick any one language to read the whole story.

---

<a id="english-default"></a>

## English (default)

**LUCALIVE** is a minimalist, ad-free website for watching live streams from many platforms in one place. A Python backend turns room links into playable URLs; a dark-themed Vue 3 + Element Plus frontend plays them in the browser—no separate app per platform.

### Built on [DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)

LUCALIVE **uses [DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)** as its stream-parsing engine. That project is an open-source, MIT-licensed tool for monitoring and recording live streams across **40+ platforms** (Douyin, Douyu, Bilibili, Huya, Kuaishou, Twitch, YouTube, TikTok, and many others). It exposes modular async fetchers in `src/spider.py` and related helpers; LUCALIVE vendors it as a **git submodule** under `backend/DouyinLiveRecorder/` and calls those functions directly—no separate CLI process.

- **Upstream repository:** [https://github.com/ihmily/DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)  
- **Author:** Hmily  
- **License:** MIT (same family as LUCALIVE’s dependency use)

If you clone LUCALIVE, initialize the submodule:

```bash
git submodule update --init --recursive
```

---

### Features

- **Link-to-Stream** — Paste a live room URL; play in the built-in player  
- **40+ Platforms** — Same coverage as DouyinLiveRecorder’s parsers (Douyin, Douyu, Bilibili, etc.)  
- **Favorite Library** — Star streamers; see live/offline status  
- **Live Notifications** — Browser notifications when a favorite goes live (via WebSocket)  
- **Racing Mode** — Highlights WRC/Hyundai-related titles with a blue breathing glow  
- **Dark Mode** — Dark theme UI  

### Tech Stack

| Layer    | Technology |
| -------- | ---------- |
| Backend  | Python 3.10+, FastAPI, aiosqlite, WebSocket |
| Parsers  | [DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder) (git submodule) |
| Frontend | Vue 3, Vite, TypeScript, Element Plus, Pinia |
| Player   | ArtPlayer.js, hls.js, mpegts.js |
| Database | SQLite (file-based) |

### Prerequisites

- Python 3.10+  
- Node.js 18+  
- Git (for submodules)  
- FFmpeg (optional; recording/transcoding only)  

### How to run the project (tutorial)

You run **two processes**: the **backend** (FastAPI on port `8000`) and the **frontend** (Vite dev server on port `5173`). Use **two terminal windows** (or tabs). Start the **backend first**, then the **frontend**.

#### 0. One-time: get the code and submodule

```bash
git clone --recurse-submodules https://github.com/your-username/LUCALIVE.git
cd LUCALIVE
```

If `backend/DouyinLiveRecorder` is empty, initialize the submodule:

```bash
git submodule update --init --recursive
```

#### 1. Start the backend (Terminal A)

1. Open a terminal and go to the backend folder:

   ```bash
   cd LUCALIVE/backend
   ```

2. Create a virtual environment (only needed the first time):

   ```bash
   python -m venv .venv
   ```

3. **Activate** the virtual environment (do this every time you open a new terminal):

   - **Windows (PowerShell or CMD):**

     ```bat
     .venv\Scripts\activate
     ```

   - **macOS / Linux:**

     ```bash
     source .venv/bin/activate
     ```

   Your prompt should show `(.venv)` when it is active.

4. Install Python dependencies (first time, or after `requirements.txt` changes):

   ```bash
   pip install -r requirements.txt
   ```

5. Start the API server:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Check that it works:** open a browser to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). You should see the Swagger UI. Leave this terminal running.

If port `8000` is already in use, stop the other program or use another port, for example `--port 8001`, and set `LUCALIVE_CORS_ORIGINS` if the frontend URL changes.

#### 2. Start the frontend (Terminal B)

1. Open a **second** terminal and go to the frontend folder:

   ```bash
   cd LUCALIVE/frontend
   ```

2. Install npm packages (first time, or after `package.json` changes):

   ```bash
   npm install
   ```

3. Start the dev server:

   ```bash
   npm run dev
   ```

4. The terminal prints a local URL (usually [http://localhost:5173](http://localhost:5173)). Open it in your browser. Vite is configured to **proxy** `/api` and `/ws` to `http://127.0.0.1:8000`, so the UI talks to the backend automatically **as long as the backend is running**.

**Summary**

| Step | Where | Command |
| ---- | ----- | ------- |
| Backend | `backend/` | `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` |
| Frontend | `frontend/` | `npm run dev` |

Production builds: `cd frontend && npm run build` outputs static files under `frontend/dist`; you still need the backend (or another server) to serve the API.

### API Reference

| Endpoint | Method | Description |
| -------- | ------ | ----------- |
| `/api/parse` | POST | Parse URL → stream info |
| `/api/favorites` | GET | List favorites + live status |
| `/api/favorite/add` | POST | Add favorite |
| `/api/favorite/remove` | POST | Remove favorite |
| `/ws/status` | WebSocket | Push events when favorites go live/offline |

### Project Structure

```
LUCALIVE/
├── backend/
│   ├── app/                  # FastAPI app
│   └── DouyinLiveRecorder/   # DouyinLiveRecorder (submodule)
├── frontend/
└── README.md
```

### Configuration

Environment variables (or put them in `backend/.env`, loaded automatically; copy from `backend/.env.example`).

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `LUCALIVE_DB_PATH` | `backend/lucalive.db` | SQLite path |
| `LUCALIVE_POLL_INTERVAL` | `60` | Watcher interval (seconds) |
| `LUCALIVE_CORS_ORIGINS` | `http://localhost:5173` | CORS origins |
| `LUCALIVE_DOUYU_COOKIES` | *(empty)* | Full Cookie string after logging in to [douyu.com](https://www.douyu.com) (same as DouyinLiveRecorder 「斗鱼cookie」). Required for reliable Douyu play URLs; keep **one line**. Also install **Node.js** for Douyu’s JS signature. **Never commit** real cookies—use `.env` only (gitignored). |

### Screenshots

*(Add screenshots here when available.)*

### License

MIT. Third-party licenses apply to dependencies. **[DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)** is MIT-licensed by Hmily.

---

<a id="中文"></a>

## 中文

**LUCALIVE** 是一款极简、无广告的网站，用于在同一处观看多个平台的直播。Python 后端将直播间链接转换为可播放 URL；采用深色主题的 Vue 3 + Element Plus 前端在浏览器中播放，无需为各平台单独安装客户端。

### 基于 [DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)

LUCALIVE **使用 [DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)** 作为流解析引擎。该项目为开源、MIT 许可的工具，用于值守与录制 **40+ 平台**（抖音、斗鱼、B 站、虎牙、快手、Twitch、YouTube、TikTok 等）的直播。其在 `src/spider.py` 及相关模块中提供模块化异步抓取；LUCALIVE 以 **git 子模块** 形式置于 `backend/DouyinLiveRecorder/`，直接调用上述函数，不单独启动其命令行进程。

- **上游仓库：** [https://github.com/ihmily/DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)  
- **作者：** Hmily  
- **许可证：** MIT（与 LUCALIVE 作为依赖使用时的许可族一致）

克隆本仓库后请初始化子模块：

```bash
git submodule update --init --recursive
```

---

### 功能

- **链接即播** — 粘贴直播间 URL，在内置播放器中观看  
- **40+ 平台** — 与 DouyinLiveRecorder 解析器覆盖范围一致（抖音、斗鱼、B 站等）  
- **收藏库** — 收藏主播并查看看播/下播状态  
- **开播提醒** — 收藏的主播开播时通过浏览器通知（WebSocket）  
- **Racing 模式** — 对 WRC/现代相关标题显示蓝色呼吸高亮  
- **深色模式** — 深色主题界面  

### 技术栈

| 层级 | 技术 |
| -------- | ---------- |
| 后端  | Python 3.10+、FastAPI、aiosqlite、WebSocket |
| 解析  | [DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)（git 子模块） |
| 前端 | Vue 3、Vite、TypeScript、Element Plus、Pinia |
| 播放器 | ArtPlayer.js、hls.js、mpegts.js |
| 数据库 | SQLite（文件） |

### 环境要求

- Python 3.10+  
- Node.js 18+  
- Git（用于子模块）  
- FFmpeg（可选；仅录制/转码需要）  

### 如何运行项目（教程）

需同时运行 **两个进程**：**后端**（FastAPI，端口 `8000`）与 **前端**（Vite 开发服务器，端口 `5173`）。请使用 **两个终端窗口**（或标签页）。**先启动后端，再启动前端。**

#### 0. 一次性：获取代码与子模块

```bash
git clone --recurse-submodules https://github.com/your-username/LUCALIVE.git
cd LUCALIVE
```

若 `backend/DouyinLiveRecorder` 为空，请初始化子模块：

```bash
git submodule update --init --recursive
```

#### 1. 启动后端（终端 A）

1. 打开终端并进入后端目录：

   ```bash
   cd LUCALIVE/backend
   ```

2. 创建虚拟环境（仅需首次）：

   ```bash
   python -m venv .venv
   ```

3. **激活**虚拟环境（每次新开终端都要执行）：

   - **Windows（PowerShell 或 CMD）：**

     ```bat
     .venv\Scripts\activate
     ```

   - **macOS / Linux：**

     ```bash
     source .venv/bin/activate
     ```

   激活成功后提示符前会出现 `(.venv)`。

4. 安装 Python 依赖（首次，或 `requirements.txt` 变更后）：

   ```bash
   pip install -r requirements.txt
   ```

5. 启动 API 服务：

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **验证：** 在浏览器打开 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)，应看到 Swagger 界面。请保持该终端运行。

若端口 `8000` 已被占用，请关闭占用程序或改用例如 `--port 8001`，若前端地址变化请相应设置 `LUCALIVE_CORS_ORIGINS`。

#### 2. 启动前端（终端 B）

1. 打开 **第二个** 终端并进入前端目录：

   ```bash
   cd LUCALIVE/frontend
   ```

2. 安装 npm 包（首次，或 `package.json` 变更后）：

   ```bash
   npm install
   ```

3. 启动开发服务器：

   ```bash
   npm run dev
   ```

4. 终端会打印本地地址（一般为 [http://localhost:5173](http://localhost:5173)）。在浏览器中打开。Vite 会将 `/api` 与 `/ws` **代理**到 `http://127.0.0.1:8000`，只要 **后端在运行**，前端即可自动访问后端。

**步骤小结**

| 步骤 | 目录 | 命令 |
| ---- | ----- | ------- |
| 后端 | `backend/` | `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` |
| 前端 | `frontend/` | `npm run dev` |

生产构建：`cd frontend && npm run build` 会在 `frontend/dist` 生成静态文件；仍需要后端（或其它服务）提供 API。

### API 说明

| 路径 | 方法 | 说明 |
| -------- | ------ | ----------- |
| `/api/parse` | POST | 解析 URL → 流信息 |
| `/api/favorites` | GET | 列出收藏及在/离线状态 |
| `/api/favorite/add` | POST | 添加收藏 |
| `/api/favorite/remove` | POST | 移除收藏 |
| `/ws/status` | WebSocket | 收藏开播/下播时推送事件 |

### 项目结构

```
LUCALIVE/
├── backend/
│   ├── app/                  # FastAPI 应用
│   └── DouyinLiveRecorder/   # DouyinLiveRecorder（子模块）
├── frontend/
└── README.md
```

### 配置

可将环境变量写入 `backend/.env`（会自动加载），可从 `backend/.env.example` 复制模板。

| 变量 | 默认值 | 说明 |
| -------- | ------- | ----------- |
| `LUCALIVE_DB_PATH` | `backend/lucalive.db` | SQLite 路径 |
| `LUCALIVE_POLL_INTERVAL` | `60` | 轮询间隔（秒） |
| `LUCALIVE_CORS_ORIGINS` | `http://localhost:5173` | CORS 来源 |
| `LUCALIVE_DOUYU_COOKIES` | *（空）* | 登录 [douyu.com](https://www.douyu.com) 后浏览器中的完整 Cookie 字符串（与 DouyinLiveRecorder「斗鱼 cookie」相同）。获得稳定斗鱼播放链接建议配置；**单行**书写。斗鱼 JS 签名需安装 **Node.js**。**切勿**将真实 Cookie 提交到 git——仅使用 `.env`（已 gitignore）。 |

### 截图

*（有素材后可在此补充截图。）*

### 许可证

MIT。依赖项沿用各自许可证。**[DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)** 由 Hmily 以 MIT 发布。

---

<a id="한국어"></a>

## 한국어

**LUCALIVE**는 광고 없는 미니멀 웹사이트로, 여러 플랫폼의 라이브를 한곳에서 시청합니다. Python 백엔드가 방송 URL을 재생 가능한 주소로 바꾸고, 다크 테마의 Vue 3 + Element Plus 프론트엔드가 브라우저에서 재생합니다. 플랫폼마다 별도 앱을 둘 필요가 없습니다.

### [DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder) 기반

LUCALIVE는 스트림 파싱에 **[DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)** 를 사용합니다. 이 프로젝트는 MIT 라이선스 오픈소스로, **40개 이상** 플랫폼(더우인, 두위, Bilibili, 후야, 콰이쇼우, Twitch, YouTube, TikTok 등) 라이브 모니터링·녹화를 지원합니다. `src/spider.py` 등에 모듈형 비동기 페처가 있습니다. LUCALIVE는 `backend/DouyinLiveRecorder/` 에 **git 서브모듈**로 포함하며, 별도 CLI 프로세스 없이 해당 함수를 직접 호출합니다.

- **업스트림 저장소:** [https://github.com/ihmily/DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)  
- **작성자:** Hmily  
- **라이선스:** MIT (LUCALIVE의 의존성 사용과 동일 계열)

저장소를 클론한 뒤 서브모듈을 초기화하세요:

```bash
git submodule update --init --recursive
```

---

### 기능

- **URL → 재생** — 라이브 방 URL을 붙여 넣고 내장 플레이어로 시청  
- **40+ 플랫폼** — DouyinLiveRecorder 파서와 동일한 범위(더우인, 두위, Bilibili 등)  
- **즐겨찾기** — 스트리머 즐겨찾기 및 라이브/오프라인 상태  
- **라이브 알림** — 즐겨찾기가 방송을 켤 때 브라우저 알림(WebSocket)  
- **Racing 모드** — WRC/현대 관련 제목에 파란 호흡 하이라이트  
- **다크 모드** — 다크 테마 UI  

### 기술 스택

| 계층    | 기술 |
| -------- | ---------- |
| 백엔드  | Python 3.10+, FastAPI, aiosqlite, WebSocket |
| 파서  | [DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder) (git 서브모듈) |
| 프론트엔드 | Vue 3, Vite, TypeScript, Element Plus, Pinia |
| 플레이어   | ArtPlayer.js, hls.js, mpegts.js |
| 데이터베이스 | SQLite (파일) |

### 사전 요구 사항

- Python 3.10+  
- Node.js 18+  
- Git (서브모듈용)  
- FFmpeg (선택; 녹음/트랜스코딩만 해당)  

### 실행 방법 (튜토리얼)

**백엔드**(FastAPI, 포트 `8000`)와 **프론트엔드**(Vite 개발 서버, 포트 `5173`) **두 프로세스**를 실행합니다. **터미널 두 개**(또는 탭)를 사용하고, **백엔드를 먼저** 띄운 뒤 프론트엔드를 시작하세요.

#### 0. 최초 1회: 코드 및 서브모듈

```bash
git clone --recurse-submodules https://github.com/your-username/LUCALIVE.git
cd LUCALIVE
```

`backend/DouyinLiveRecorder` 가 비어 있으면 서브모듈을 초기화합니다:

```bash
git submodule update --init --recursive
```

#### 1. 백엔드 시작 (터미널 A)

1. 터미널을 열고 백엔드 폴더로 이동:

   ```bash
   cd LUCALIVE/backend
   ```

2. 가상 환경 생성 (최초 1회):

   ```bash
   python -m venv .venv
   ```

3. 가상 환경 **활성화** (새 터미널마다 실행):

   - **Windows (PowerShell 또는 CMD):**

     ```bat
     .venv\Scripts\activate
     ```

   - **macOS / Linux:**

     ```bash
     source .venv/bin/activate
     ```

   프롬프트에 `(.venv)` 가 보이면 활성화된 것입니다.

4. Python 패키지 설치 (최초 또는 `requirements.txt` 변경 시):

   ```bash
   pip install -r requirements.txt
   ```

5. API 서버 실행:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **확인:** 브라우저에서 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 를 열어 Swagger UI가 보이면 정상입니다. 이 터미널은 계속 실행합니다.

포트 `8000` 이 사용 중이면 다른 프로그램을 종료하거나 `--port 8001` 등으로 바꾸고, 프론트 URL이 바뀌면 `LUCALIVE_CORS_ORIGINS` 를 맞춥니다.

#### 2. 프론트엔드 시작 (터미널 B)

1. **두 번째** 터미널을 열고 프론트 폴더로 이동:

   ```bash
   cd LUCALIVE/frontend
   ```

2. npm 패키지 설치 (최초 또는 `package.json` 변경 시):

   ```bash
   npm install
   ```

3. 개발 서버 실행:

   ```bash
   npm run dev
   ```

4. 터미널에 표시되는 로컬 URL(보통 [http://localhost:5173](http://localhost:5173))을 브라우저에서 엽니다. Vite는 `/api` 와 `/ws` 를 `http://127.0.0.1:8000` 으로 **프록시**하므로, **백엔드가 실행 중**이어야 UI가 API에 접속합니다.

**요약**

| 단계 | 위치 | 명령 |
| ---- | ----- | ------- |
| 백엔드 | `backend/` | `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` |
| 프론트엔드 | `frontend/` | `npm run dev` |

프로덕션 빌드: `cd frontend && npm run build` 는 `frontend/dist` 에 정적 파일을 만듭니다. API는 여전히 백엔드(또는 다른 서버)가 필요합니다.

### API 참고

| 엔드포인트 | 메서드 | 설명 |
| -------- | ------ | ----------- |
| `/api/parse` | POST | URL 파싱 → 스트림 정보 |
| `/api/favorites` | GET | 즐겨찾기 목록 + 라이브/오프라인 상태 |
| `/api/favorite/add` | POST | 즐겨찾기 추가 |
| `/api/favorite/remove` | POST | 즐겨찾기 제거 |
| `/ws/status` | WebSocket | 즐겨찾기 라이브/오프라인 이벤트 푸시 |

### 프로젝트 구조

```
LUCALIVE/
├── backend/
│   ├── app/                  # FastAPI 앱
│   └── DouyinLiveRecorder/   # DouyinLiveRecorder (서브모듈)
├── frontend/
└── README.md
```

### 설정

환경 변수는 `backend/.env` 에 두면 자동 로드됩니다. `backend/.env.example` 을 복사해 사용할 수 있습니다.

| 변수 | 기본값 | 설명 |
| -------- | ------- | ----------- |
| `LUCALIVE_DB_PATH` | `backend/lucalive.db` | SQLite 경로 |
| `LUCALIVE_POLL_INTERVAL` | `60` | 워처 폴링 간격(초) |
| `LUCALIVE_CORS_ORIGINS` | `http://localhost:5173` | CORS 출처 |
| `LUCALIVE_DOUYU_COOKIES` | *(비어 있음)* | [douyu.com](https://www.douyu.com) 로그인 후 브라우저의 전체 Cookie 문자열(DouyinLiveRecorder 의 「斗鱼cookie」와 동일). 두위 재생 URL 안정화에 권장; **한 줄**로 작성. 두위 JS 서명에는 **Node.js** 설치 필요. 실제 Cookie는 **절대** git에 커밋하지 말고 `.env` 만 사용(gitignore). |

### 스크린샷

*(추가 시 이곳에 스크린샷을 넣을 수 있습니다.)*

### 라이선스

MIT. 의존성은 각자의 라이선스를 따릅니다. **[DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)** 는 Hmily 가 MIT로 배포합니다.
