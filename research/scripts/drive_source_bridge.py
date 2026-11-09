#!/usr/bin/env python3
"""Read-only Google Drive source bridge for Industry Academy.

All raw source files and the complete manifest remain under gitignored private_sources/.
Requires owner-configured, read-only Google service-account credentials.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import sys
from pathlib import Path

try:
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
except ImportError as e:
    raise SystemExit("Missing dependencies: pip install google-api-python-client google-auth") from e

ROOT = Path(__file__).resolve().parents[2]
PRIVATE = (ROOT / "private_sources").resolve()
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
FOLDER_MIME = "application/vnd.google-apps.folder"

def service():
    cred = os.environ.get("GDRIVE_SERVICE_ACCOUNT_JSON", "").strip()
    if not cred:
        raise SystemExit("GDRIVE_SERVICE_ACCOUNT_JSON not set; no login attempted.")
    try:
        info = json.loads(cred)
    except json.JSONDecodeError as e:
        raise SystemExit("GDRIVE_SERVICE_ACCOUNT_JSON must be a JSON service-account key") from e
    auth = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return build("drive", "v3", credentials=auth, cache_discovery=False)

def safe_name(s: str):
    s = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", s).strip(" .")
    return (s[:130] or "unnamed")

def walk(drive, folder_id, path="", seen=None):
    seen = seen or set()
    if folder_id in seen:
        return
    seen.add(folder_id)
    token = None
    while True:
        q = f"'{folder_id}' in parents and trashed = false"
        result = drive.files().list(
            q=q, fields="nextPageToken,files(id,name,mimeType,size,md5Checksum,modifiedTime,webViewLink)",
            pageSize=1000, pageToken=token, supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        for f in result.get("files", []):
            nested = (path + "/" + safe_name(f["name"])).lstrip("/")
            if f.get("mimeType") == FOLDER_MIME:
                yield from walk(drive, f["id"], nested, seen)
            else:
                yield f, nested
        token = result.get("nextPageToken")
        if not token:
            break

def download_file(drive, f, target, limit_bytes):
    length = int(f.get("size") or 0)
    if length > limit_bytes:
        return "skipped_size_limit"
    if f.get("mimeType", "").startswith("application/vnd.google-apps."):
        return "metadata_only_native_google_file"
    request = drive.files().get_media(fileId=f["id"], supportsAllDrives=True)
    target.parent.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    dl = MediaIoBaseDownload(buf, request, chunksize=1 << 20)
    done = False
    while not done:
        status, done = dl.next_chunk()
        if buf.tell() > limit_bytes:
            return "skipped_size_limit"
    data = buf.getvalue()
    if len(data) > limit_bytes:
        return "skipped_size_limit"
    if target.exists() and hashlib.sha256(target.read_bytes()).digest() == hashlib.sha256(data).digest():
        return "already_downloaded"
    target.write_bytes(data)
    return "downloaded"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--download", action="store_true", help="Download eligible files privately")
    p.add_argument("--max-files", type=int, default=2000)
    p.add_argument("--max-file-bytes", type=int, default=30_000_000)
    args = p.parse_args()
    folder = os.environ.get("GDRIVE_ROOT_FOLDER_ID", "").strip()
    if not folder:
        raise SystemExit("GDRIVE_ROOT_FOLDER_ID not set.")
    target_root = (PRIVATE / "drive_source_bridge").resolve()
    if not target_root.is_relative_to(PRIVATE):
        raise SystemExit("Unsafe output location")
    target_root.mkdir(parents=True, exist_ok=True)
    drive = service()
    rows = []
    for f, rel in walk(drive, folder):
        if len(rows) >= args.max_files:
            break
        row = dict(source_name=rel, mime_type=f.get("mimeType"),
                   bytes=f.get("size"), modified_time=f.get("modifiedTime"),
                   provider_md5=f.get("md5Checksum"), drive_file_id=f.get("id"),
                   source_url=f.get("webViewLink"), status="indexed_only")
        if args.download:
            filename = safe_name(f["id"]) + "_" + safe_name(f["name"])
            row["status"] = download_file(drive, f, target_root / "raw" / filename, args.max_file_bytes)
        rows.append(row)
    destination = target_root / "manifest_private.json"
    destination.write_text(json.dumps({"total": len(rows), "files": rows}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Listed {len(rows)} source objects. Private manifest saved under private_sources/ only.")
    print("No original files, Drive IDs or share URLs were committed to public GitHub.")

if __name__ == "__main__":
    main()
