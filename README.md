# Cocofolia-Log-V4

코코포리아 "로그북용 로그 백업" 탭(5번 탭)과 연동되는 **한/글(HWP) 템플릿 + 매크로**의 원본을 관리하는 레포지토리입니다.

이 레포는 [Cocofolia-Setter](https://github.com/G909G09/Cocofolia-Setter)의 서브 레포로,
여기서 파일을 수정해 `main` 브랜치에 push하면 GitHub Actions가 자동으로 Cocofolia-Setter 레포까지 반영합니다.
Cocofolia-Setter 쪽에서 따로 수동 작업을 할 필요가 없습니다.

## 포함 파일

| 파일 | 설명 |
|---|---|
| `Cocofolia_Log_V4.hwp` | A5 국배판 로그북 한/글 템플릿 |
| `Cocofolia_Log_V4.msr` | 문단 스타일 자동 적용 매크로 |
| `Cocofolia_Log_V4.html` | 마커 변환 로직의 원본 (Cocofolia-Setter 5번 탭에 이식되어 있음) |
| `사용법.txt` | 템플릿 + 매크로 사용 순서 |

## 자동 동기화 방식

`.github/workflows/sync-to-setter.yml` 워크플로우가 `main` 브랜치에 push될 때마다 실행되어:

1. `scripts/sync_to_setter.py`로 `.hwp` / `.msr` / `사용법.txt`를 base64로 다시 인코딩해서
   Cocofolia-Setter의 `Cocofolia_Setter.html` 안에 내장된 `<script id="macro-*-b64">` 블록을 갱신합니다.
   (이 블록은 5번 탭의 "한/글 템플릿 + 매크로 다운로드(.zip)" 버튼이 사용합니다.)
2. Cocofolia-Setter의 `Cocofolia_Log_V4/` 폴더와 `Cocofolia_Log_V4.zip`도 최신 파일로 갱신합니다.
3. 변경 사항이 있으면 Cocofolia-Setter의 `master` 브랜치에 자동 커밋 · push합니다.

### 최초 설정 (한 번만)

이 워크플로우가 Cocofolia-Setter 레포에 push하려면, Cocofolia-Setter에 대한 쓰기 권한을 가진
**Fine-grained Personal Access Token**이 필요합니다.

1. https://github.com/settings/tokens?type=beta 에서 토큰 발급
   - Repository access: `Cocofolia-Setter`만 선택
   - Permissions: **Contents: Read and write**
2. 이 레포(Cocofolia-Log-V4)의 **Settings → Secrets and variables → Actions → New repository secret**
   - Name: `SETTER_REPO_TOKEN`
   - Value: 위에서 발급한 토큰

등록이 끝나면 이후 `main` 브랜치에 push할 때마다 자동으로 동기화됩니다.
수동으로 한 번 돌려보고 싶다면 Actions 탭 → "Sync macro to Cocofolia-Setter" → "Run workflow"로 실행할 수 있습니다.
