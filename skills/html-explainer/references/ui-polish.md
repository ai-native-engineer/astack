# 마감 디테일 - 표면·모션·아이콘

두 시작 템플릿에 CSS 토큰으로 기본 배선돼 있다. 새 표면(카드·패널)·버튼·이미지·아이콘을 추가할 때 같은 규칙으로 맞춘다.

무엇을 애니메이션할지(정보를 나르는가)는 `SKILL.md` 철칙이 정하고, 이 문서는 어떻게 구현할지를 정한다.

## 깊이는 그림자, 구조는 보더

깊이를 내려고 두른 1px 보더는 배경이 바뀌어도 같이 안 바뀌어 이질적으로 뜬다. 투명도를 쓰는 그림자는 어떤 배경 위에서도 성립한다.

- 그림자로: 카드, 다이어그램·차트 컨테이너, 코드/트리 블록, 표, 보더형 버튼.
- 보더로 남길 것: 표 셀 구분선, 섹션 구분선(`border-top`), 강조 박스의 색 좌측 보더, 상태를 나타내는 보더.
- 토큰 값(양 템플릿의 `--shadow-border`):
    - 라이트는 3겹 - `0 0 0 1px oklch(0 0 0 / .06), 0 1px 2px -1px oklch(0 0 0 / .06), 0 2px 4px 0 oklch(0 0 0 / .04)`
    - 다크는 흰 링 1겹 - `0 0 0 1px oklch(1 0 0 / .08)`. 어두운 배경에서는 층진 그림자가 안 보인다.
- hover로 들어올릴 때는 `--shadow-border-hover`로 바꾸고 `transition-property: box-shadow`를 명시한다.

## 중첩 표면의 radius는 동심으로

바깥 radius = 안쪽 radius + 그 사이 padding. 두 값이 같으면 안쪽 모서리가 눌린 것처럼 보인다.

```css
.card       { border-radius: 20px; padding: 8px; }  /* 12 + 8 */
.card > .in { border-radius: 12px; }
```

사이 padding이 24px를 넘으면 두 면은 독립 표면으로 읽히니 동심 계산을 강제하지 말고 각자 값을 고른다.

## 이미지 아웃라인

스크린샷·도해에는 1px 아웃라인을 둬 배경과 경계를 만든다. 색은 순수 흑/백만 쓴다. 팔레트의 near-black(slate·zinc 계열)은 아래 표면 색을 받아 이미지 가장자리에 때가 낀 것처럼 보인다.

- 라이트 `oklch(0 0 0 / .1)`, 다크 `oklch(1 0 0 / .1)`. 두 템플릿의 `--img-outline` 토큰.
- `border`가 아니라 `outline` + `outline-offset: -1px`. 레이아웃 크기를 안 바꾸고 모서리 radius를 따라 안쪽에 붙는다.

## transition은 바뀌는 속성만 적는다

`transition: all`을 쓰면 의도하지 않은 속성까지 따라 움직이고 브라우저 최적화가 막힌다.

```css
.btn { transition-property: scale, box-shadow, color; transition-duration: 150ms; transition-timing-function: ease-out; }
```

`will-change`는 첫 프레임 끊김을 실제로 봤을 때만, `transform`·`opacity`·`filter`에만 붙인다. 레이어마다 메모리를 쓴다.

## 누름 피드백은 scale(0.96)

버튼에 `:active { scale: .96 }`를 준다. 0.95보다 작으면 과장돼 보인다. keyframes가 아니라 transition으로 걸어야 누르다 손을 떼도 중간에서 부드럽게 돌아온다.

## 모션 절제

- 자주 반복되는 조작(스텝 이동, 행 hover, 탭 전환)은 150~200ms 이내 최소 전환만. 주의 비용이 매 클릭마다 청구된다.
- 상호작용 상태 변화는 CSS transition(중간에 인터럽트되고 되돌아온다), 한 번만 도는 등장 시퀀스는 keyframes.
- 애니메이션이 유일한 피드백 채널이 되면 안 된다. 색·아이콘·라벨 같은 정적 신호를 같이 준다.
- 애니메이션을 추가하면 감속 대응도 같이 넣는다.

```css
@media (prefers-reduced-motion: reduce) {
  .step-anim { animation: none; }
  .btn { transition-duration: 1ms; }
}
```

## 아이콘

- 인접 텍스트와 광학 무게를 맞춘다. 크기는 고정 px 대신 `1em`~`1.25em`로 두면 텍스트와 같이 스케일된다.
- Iconify lucide는 스트로크 2px 고정이라 semibold 이상 라벨과 어울린다. 본문(400) 옆에 놓을 때는 `1.15em` 이하로 낮춰 무게를 맞춘다.
- 색과 상태는 `currentColor` 상속과 CSS 색으로만 표현한다. 상태별로 다른 아이콘 에셋을 두지 않는다.
- 외곽선 변형이 기본이고, 채운 변형은 활성 상태 표시에만 쓴다.
