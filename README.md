# LUCALIVE — Multi-Platform Live Streaming Website

**Language / 语言 / 언어:** [English](#english-default) · [中文](#中文) · [한국어](#한국어)

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

**LUCALIVE** 是一款极简、无广告的 **多平台直播聚合网站**：在浏览器里用同一个页面观看抖音、斗鱼、B 站等多个平台的直播；Python 后端负责解析地址，Vue 3 + Element Plus 暗色前端负责播放与收藏。

### 基于 [DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)

本项目**使用 [DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)** 作为核心解析能力。它是开源、MIT 协议的多平台直播值守与录制工具，支持抖音、斗鱼、B 站、虎牙、快手、Twitch、YouTube、TikTok 等 **40+ 平台**。其核心逻辑在 `src/spider.py` 等模块中；LUCALIVE 以 **git 子模块** 形式放在 `backend/DouyinLiveRecorder/`，直接调用其中的异步解析函数，而不单独跑其命令行程序。

- **项目地址：** [https://github.com/ihmily/DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)  
- **作者：** Hmily  
- **协议：** MIT  

克隆本仓库后请执行：`git submodule update --init --recursive`

**斗鱼 Cookie：** 复制 `backend/.env.example` 为 `backend/.env`，在文件中设置一行 `LUCALIVE_DOUYU_COOKIES=浏览器里登录斗鱼后的整段 Cookie`（勿提交 `.env`）。也可在系统/终端里设置同名环境变量。需安装 Node.js 以执行斗鱼签名脚本。

### 如何启动后端与前端

需要 **两个终端**，先启 **后端**，再启 **前端**。

**终端 A — 后端**

```bash
cd LUCALIVE/backend
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

浏览器打开 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 能看到接口文档即表示后端正常。保持该窗口不要关。

**终端 B — 前端**

```bash
cd LUCALIVE/frontend
npm install
npm run dev
```

按终端提示打开（一般为 [http://localhost:5173](http://localhost:5173)）。前端会把 `/api`、`/ws` 代理到本机 `8000` 端口，因此 **必须先开着后端**。

更多说明见上文 **[English (default)](#english-default)** 中的 *How to run the project* 与 API、目录结构。

---

<a id="한국어"></a>

## 한국어

**LUCALIVE**는 광고 없는 미니멀 **멀티 플랫폼 라이브 웹사이트**입니다. 브라우저 한 곳에서 더우인·두위·Bilibili 등 여러 플랫폼 방송을 시청할 수 있으며, Python 백엔드가 URL을 재생 가능한 스트림으로 바꾸고, Vue 3 + Element Plus 다크 UI로 재생·즐겨찾기를 제공합니다.

### [DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder) 기반

LUCALIVE는 스트림 파싱에 **[DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)** 를 사용합니다. 이 프로젝트는 MIT 라이선스의 오픈소스로, 더우인·두위·Bilibili·후야·콰이쇼우·Twitch·YouTube·TikTok 등 **40개 이상** 플랫폼 라이브를 지원하는 녹화·모니터링 도구입니다. `src/spider.py` 등에 비동기 파서가 모여 있으며, LUCALIVE는 `backend/DouyinLiveRecorder/` **git 서브모듈**로 포함해 CLI 없이 해당 함수를 직접 호출합니다.

- **저장소:** [https://github.com/ihmily/DouyinLiveRecorder](https://github.com/ihmily/DouyinLiveRecorder)  
- **작성자:** Hmily  
- **라이선스:** MIT  

클론 후 서브모듈 초기화: `git submodule update --init --recursive`

### 백엔드·프론트엔드 실행 방법

**터미널 두 개**가 필요합니다. **백엔드 → 프론트엔드** 순서로 실행하세요.

**터미널 A (백엔드)** — `LUCALIVE/backend` 에서 가상환경 생성·활성화 후 `pip install -r requirements.txt`, 그다음:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 가 열리면 정상입니다.

**터미널 B (프론트엔드)** — `LUCALIVE/frontend` 에서 `npm install` 후 `npm run dev`. 브라우저에서 안내 URL(보통 [http://localhost:5173](http://localhost:5173))을 엽니다. Vite가 `/api`, `/ws`를 백엔드(8000)로 프록시하므로 **백엔드를 먼저 켜 두어야** 합니다.

자세한 단계는 **[English (default)](#english-default)** 의 *How to run the project* 를 참고하세요.
