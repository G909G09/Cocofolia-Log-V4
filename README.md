# Cocofolia-Log-V4

코코포리아(CCFOLIA)에서 뽑은 로그를 **A5 국배판 인쇄용 로그북**으로 조판하기 위한 한/글(HWP) 템플릿과 매크로,
그리고 로그 HTML을 마커 텍스트로 바꿔주는 변환기 원본을 관리하는 레포지토리입니다.

[Cocofolia-Setter](https://github.com/G909G09/Cocofolia-Setter)의 "로그북용 로그 백업" 탭과 함께 쓰도록 설계되어 있으며,
전체 파이프라인은 **"로그 HTML → 마커 텍스트(`@@스타일@@본문`) → 한/글에 붙여넣기 → 매크로 실행 → 조판 완성"** 순서로 진행됩니다.

## 전체 흐름

```
코코포리아 "로그 출력" .html
        │
        ▼  (Cocofolia_Log_V4.html 또는 Cocofolia-Setter 5번 탭)
@@스타일@@본문 형태의 마커 텍스트
        │
        ▼  Cocofolia_Log_V4.hwp 사본 맨 아래에 붙여넣기
        ▼  매크로 실행 (Cocofolia_Log_V4.msr)
A5 국배판으로 조판된 로그북 (완성)
```

## 파일별 설명

### `Cocofolia_Log_V4.html` — 마커 변환기 (독립 실행 웹앱)
코코포리아 "로그 출력"으로 받은 `.html` 파일을 브라우저에 끌어다 놓으면, 문단을 파싱해서 자동으로 스타일을 배정하고
`@@스타일@@본문` 형태의 마커 텍스트를 만들어줍니다. 순수 HTML/JS 파일이라 더블클릭해서 바로 열 수 있습니다.

- 로그를 GM 서술(`Story`), GM 주사위 판정(`Storydice`/`GMdice`), 플레이어 주사위(`dice`), 시스템 메시지(`system`),
  그리고 발화 빈도 상위 5명까지의 대사(`대사`/`대사2`/`대사3`, 여러 줄 연속 발화는 `_2` 접미사)로 자동 분류합니다.
- 정규식으로 주사위 판정 표기(`(1d100<=50)` 등)와 산정치 표기(`3/5` 등)를 인식해 알맞은 스타일을 붙입니다.
- 어떤 캐릭터를 어떤 스타일(대사/대사2/대사3)에 배정할지는 화면에서 직접 조정할 수 있습니다.
- 같은 로직이 [Cocofolia-Setter](https://github.com/G909G09/Cocofolia-Setter)의 5번 탭("로그북용 로그 백업")에도 이식되어 있습니다.
  이 파일은 그 로직의 원본이자 Setter 없이도 단독으로 쓸 수 있는 버전입니다.

### `Cocofolia_Log_V4.hwp` — A5 국배판 한/글 템플릿
실제 조판을 담당하는 한/글 문서입니다.

- 첫 페이지에 스타일별 **견본 문단**이 들어있습니다(`Cocofolia_Story`, `Ccfolia_대사2` 등 문단마다 고유한 텍스트로 구분됩니다).
  매크로가 이 문단들의 모양(글꼴/여백/테두리/배경 등)을 읽어서 마커 텍스트에 그대로 복사해 적용합니다.
- **첫 페이지는 지우지 말고 그대로 둔 채** 마커 텍스트를 문서 맨 아래(또는 다음 페이지)에 붙여넣고 매크로를 돌려야 합니다.
  매크로 실행이 끝난 뒤에만 첫 페이지를 삭제합니다.

### `Cocofolia_Log_V4.msr` — 문단 스타일 자동 적용 매크로
한/글 스크립트 매크로(HWPW Script Macro Definition) 파일입니다.

- 마커 텍스트(`@@스타일@@본문`)를 순회하면서, 각 마커에 해당하는 **견본 문단을 고유 텍스트로 검색**해 찾은 뒤
  그 문단 모양을 현재 문단 전체에 적용합니다. (v3에서는 "현재 스타일 읽기" 방식이었는데, Style 액션이 테두리/배경
  같은 문단 모양을 제대로 가져오지 못하는 문제가 있어 v4에서 텍스트 검색 + 모양 재적용 방식으로 바꿨습니다.)
- 실행 단축키는 `Alt+Shift+L` → 빈 공간 클릭 → 팝업 하단 파일 아이콘으로 이 `.msr` 파일을 불러오면 됩니다.

### `사용법.txt`
위 세 파일을 실제로 쓰는 6단계 순서를 요약한 텍스트입니다(매크로 실행 순서, 첫 페이지 처리 방법 등).
`Cocofolia_Log_V4.msr` 파일 맨 앞의 주석과 동일한 내용입니다.

## Cocofolia-Setter와의 자동 동기화

이 레포는 [Cocofolia-Setter](https://github.com/G909G09/Cocofolia-Setter)의 서브 레포입니다.
여기서 파일을 수정해 `main` 브랜치에 push하면, `.github/workflows/sync-to-setter.yml` 워크플로우가 자동으로:

1. `scripts/sync_to_setter.py`로 `.hwp` / `.msr` / `사용법.txt`를 base64로 다시 인코딩해서
   Cocofolia-Setter의 `Cocofolia_Setter.html` 안에 내장된 `<script id="macro-*-b64">` 블록을 갱신합니다.
   (이 블록은 Setter 5번 탭의 "한/글 템플릿 + 매크로 다운로드(.zip)" 버튼이 사용합니다.)
2. Cocofolia-Setter의 `Cocofolia_Log_V4/` 미러 폴더도 최신 파일로 갱신합니다.
3. 변경 사항이 있으면 Cocofolia-Setter의 `master` 브랜치에 자동 커밋 · push합니다.

Cocofolia-Setter 쪽에서 따로 수동 작업을 할 필요가 없습니다 — 템플릿/매크로 수정은 항상 이 레포에서만 하면 됩니다.

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
