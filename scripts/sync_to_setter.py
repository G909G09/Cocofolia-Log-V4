#!/usr/bin/env python3
"""
Cocofolia-Log-V4 -> Cocofolia-Setter 동기화 스크립트.

이 레포(Cocofolia-Log-V4)의 매크로 원본 파일이 바뀔 때마다
Cocofolia-Setter 레포의 Cocofolia_Setter.html 안에 내장된 base64 블록과
Cocofolia_Log_V4/ 미러 폴더를 갱신한다.
(과거에는 Cocofolia_Log_V4.zip 사본도 함께 만들었지만, Setter 앱이 같은 내용을
다운로드 버튼에서 그때그때 만들어주고 미러 폴더도 있어 중복이라 더 이상 생성하지
않는다 — 남아있다면 삭제한다.)

사용법: python3 sync_to_setter.py <log_v4_repo_dir> <setter_repo_dir>
"""
import base64
import re
import sys
from pathlib import Path

SOURCE_FILES = {
    "html": "Cocofolia_Log_V4.html",
    "hwp": "Cocofolia_Log_V4.hwp",
    "msr": "Cocofolia_Log_V4.msr",
    "usage": "사용법.txt",
}

# Cocofolia_Setter.html 안에 base64로 내장되는 파일들 (html은 내장 대상이 아님 — 로직만 이식되어 있음)
EMBED_KEYS = ["hwp", "msr", "usage"]


def replace_b64_block(html_text: str, marker_id: str, b64_content: str) -> str:
    pattern = re.compile(
        r'(<script type="text/plain" id="' + re.escape(marker_id) + r'">\s*)'
        r".*?"
        r'(\s*</script>)',
        re.S,
    )
    if not pattern.search(html_text):
        raise SystemExit(f"마커를 찾지 못했습니다: id=\"{marker_id}\" (Cocofolia_Setter.html 구조가 바뀌었을 수 있습니다)")
    return pattern.sub(lambda m: m.group(1) + b64_content + m.group(2), html_text, count=1)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    log_v4_dir = Path(sys.argv[1])
    setter_dir = Path(sys.argv[2])

    source_paths = {key: log_v4_dir / name for key, name in SOURCE_FILES.items()}
    for key, path in source_paths.items():
        if not path.is_file():
            raise SystemExit(f"소스 파일이 없습니다: {path}")

    setter_html_path = setter_dir / "Cocofolia_Setter.html"
    html_text = setter_html_path.read_text(encoding="utf-8")

    for key in EMBED_KEYS:
        raw = source_paths[key].read_bytes()
        b64 = base64.b64encode(raw).decode("ascii")
        marker_id = f"macro-{key}-b64"
        html_text = replace_b64_block(html_text, marker_id, b64)

    setter_html_path.write_text(html_text, encoding="utf-8")

    mirror_dir = setter_dir / "Cocofolia_Log_V4"
    mirror_dir.mkdir(exist_ok=True)
    for key, path in source_paths.items():
        (mirror_dir / SOURCE_FILES[key]).write_bytes(path.read_bytes())

    zip_path = setter_dir / "Cocofolia_Log_V4.zip"
    zip_removed = zip_path.exists()
    zip_path.unlink(missing_ok=True)

    print("동기화 완료:")
    print(f"  - {setter_html_path} 내 base64 블록 3개 갱신 (hwp/msr/usage)")
    print(f"  - {mirror_dir} 미러 파일 4개 갱신")
    if zip_removed:
        print(f"  - {zip_path} 삭제 (미러 폴더/앱 내 다운로드 버튼과 중복이라 더 이상 생성하지 않음)")


if __name__ == "__main__":
    main()
