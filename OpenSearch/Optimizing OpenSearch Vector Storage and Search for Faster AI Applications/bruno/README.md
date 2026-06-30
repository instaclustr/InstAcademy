# Fast mode — Bruno REST collection

**Vector Storage & Search for AI** · [← How to run labs](../HANDS-ON-GUIDE.md)

Run the same REST calls as the lesson READMEs without typing them into Dev Tools. Use this to **catch up**, **recover after a mistake**, or **smoke-test** a cluster.

## Setup (once)

1. Install [Bruno](https://www.usebruno.com/downloads).
2. **Open Collection** → select this `bruno/` folder.
3. Open **Environments → Local** and set:

   | Variable | Example | Notes |
   |----------|---------|--------|
   | `baseUrl` | `https://123.45.67.89:9200` | Cluster URL from Instaclustr (no trailing slash) |
   | `username` | `icopensearch` | As shown in the console |
   | `password` | *(your password)* | |
   | `modelGroupId` | | Fill after **Register model group** |
   | `modelId` | | Fill after register/deploy **COMPLETED** |
   | `taskId` | | Update when polling ML tasks |

4. **Disable SSL certificate verification** in Bruno: **Settings → SSL/TLS Certificate Verification → OFF**. Trial clusters use certificates that fail strict verification.

5. Select the **Local** environment in the top-right before sending requests.

## How to run a lesson

1. Open the folder for the chapter and lesson (e.g. `Chapter 2 / Lesson 1`).
2. Run requests **top to bottom** (`seq` order).
3. After **Register model** or **Deploy model**, if the response contains `task_id`:
   - Set `taskId` in the environment (or edit the Poll request URL).
   - Run **Poll ML task** repeatedly until `"state": "COMPLETED"`.
   - Copy `model_id` into `modelId` (and into `src/.env` as `ML_MODEL_ID` if you use Python scripts).
4. Bulk requests use body files under [`../rest/bulk/`](../rest/bulk/). In Bruno, the file path is relative to the request file.

## Folder layout

```
bruno/
  environments/
    Local.bru          # Your cluster credentials
  Chapter 1/
    Lesson 1/          # Connectivity
    Lesson 2/          # Keyword index
    Lesson 4/          # Vector reindex
  Chapter 2/
    Lesson 1/ … Lesson 5/
  Chapter 3/
    Lesson 1/
  Chapter 4/
    Lesson 1/ … Lesson 3/
  Chapter 5/
    Lesson 1/ … Lesson 5/
```

Each lesson folder matches the **Learn mode** README in `src/Chapter …`.

## Learn mode vs fast mode

| | Learn mode | Fast mode (Bruno) |
|---|------------|-------------------|
| Where | Dev Tools in Dashboards | Bruno app |
| Goal | Understand each API | Same outcome, less typing |
| ML tasks | You poll manually in Dev Tools | **Poll ML task** request |
| Bulk data | Small inline examples + `rest/bulk/` files | Bruno file bodies |

Start with [Learn mode](../HANDS-ON-GUIDE.md) at least once; use Bruno when you need speed or recovery.
