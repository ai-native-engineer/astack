# 에피소드 발행

외부 변경은 사용자가 publish를 명시했을 때만 실행한다. `publish.sh`는 입력 검증, Release, RSS, commit, push를 한 경로로 처리하므로 수동으로 단계를 나누지 않는다.

## 실행

먼저 같은 인자로 side effect 없는 preflight를 실행한다.

```bash
scripts/publish.sh --repo <show-repo> --audio <episode.mp3> \
  --title "<title>" --desc "<show-notes>" --dry-run
```

통과하면 `--dry-run`만 빼고 발행한다. 회차를 생략하면 기존 최대 회차의 다음 번호를 쓰고, 같은 회차를 재발행하면 GUID를 보존하면서 오디오와 Release 제목/설명을 함께 갱신한다.

## 발행 전후 확인

- 최종 오디오가 MP3인지와 duration을 `ffprobe`로 확인한다.
- loudness는 아래 분석 결과의 integrated `input_i`로 확인한다. 목표가 -16 LUFS이면 `mean_volume`을 대신 쓰지 않는다.

```bash
ffmpeg -i <episode.mp3> -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null -
```

- 스크립트가 Release asset의 byte-range `206`과 원격 크기 일치를 확인한다.
- GitHub Pages 반영 뒤 공개 `feed.xml`을 XML로 파싱하고 최신 회차가 첫 번째인지 확인한다.
- Apple과 Spotify의 RSS 재수집은 즉시 끝나지 않을 수 있으므로 플랫폼 화면과 피드 원본을 구분해 보고한다.

push가 실패하면 로컬 commit을 보존한다. 같은 publish 명령을 다시 실행하면 Release를 멱등하게 갱신하고 남은 push를 재시도한다.
