/**
 * 2026 기후 콘텐츠 소비자 동향 리포트
 * PptxGenJS 빌드 스크립트
 */
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "2026 기후 콘텐츠 소비자 동향 리포트";
pres.author = "NLM Research Pipeline";

// ─── 컬러 팔레트 ────────────────────────────────────────────────
const C = {
  darkBg:    "0A2E1A",   // 타이틀/전환 배경
  forestGrn: "1B5E20",   // 섹션 헤더 강조
  sage:      "388E3C",   // 포인트 그린
  mint:      "00897B",   // 민트 포인트
  mintLight: "B2DFDB",   // 민트 라이트
  gold:      "F9A825",   // 골드 강조
  cream:     "F7FBF7",   // 슬라이드 배경 (연한 그린-화이트)
  white:     "FFFFFF",
  textDark:  "1C2D1F",
  textMid:   "37474F",
  textGray:  "607D8B",
  divider:   "C8E6C9",
  cardBg:    "FFFFFF",
  cardBorder:"CFE8CF",
};

// ─── 헬퍼 함수 ──────────────────────────────────────────────────
const makeShadow = () => ({
  type: "outer", blur: 6, offset: 2, angle: 135, color: "000000", opacity: 0.10,
});

// 다크 슬라이드 (타이틀/전환)
function addDarkSlide() {
  const s = pres.addSlide();
  s.background = { color: C.darkBg };
  return s;
}

// 라이트 슬라이드 (콘텐츠)
function addLightSlide() {
  const s = pres.addSlide();
  s.background = { color: C.cream };
  // 왼쪽 포인트 바
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.07, h: 5.625, fill: { color: C.sage }, line: { color: C.sage } });
  // 슬라이드 넘버 (하단 오른쪽 - 나중에 개별 설정)
  return s;
}

// 섹션 커버 슬라이드
function addSectionCover(num, title, subtitle) {
  const s = addDarkSlide();
  // 섹션 번호 큰 배경 숫자
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 2.2, h: 5.625, fill: { color: C.forestGrn }, line: { color: C.forestGrn } });
  s.addText(`0${num}`, {
    x: 0, y: 1.8, w: 2.2, h: 2, fontSize: 80, bold: true,
    color: C.mintLight, align: "center", margin: 0,
  });
  s.addText("SECTION", {
    x: 0, y: 1.3, w: 2.2, h: 0.5, fontSize: 11, bold: true,
    color: C.mint, align: "center", charSpacing: 4, margin: 0,
  });
  s.addText(title, {
    x: 2.5, y: 1.5, w: 7, h: 1.8, fontSize: 32, bold: true,
    color: C.white, align: "left", margin: 0,
  });
  if (subtitle) {
    s.addText(subtitle, {
      x: 2.5, y: 3.3, w: 7, h: 1, fontSize: 16,
      color: C.mintLight, align: "left", margin: 0,
    });
  }
  // 하단 민트 라인
  s.addShape(pres.shapes.RECTANGLE, { x: 2.5, y: 1.45, w: 4, h: 0.05, fill: { color: C.gold }, line: { color: C.gold } });
  return s;
}

// 슬라이드 타이틀 추가 (라이트 슬라이드용)
function addSlideTitle(s, text) {
  s.addText(text, {
    x: 0.3, y: 0.2, w: 9.2, h: 0.7, fontSize: 22, bold: true,
    color: C.textDark, align: "left", margin: 0,
  });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.9, w: 9.4, h: 0.04, fill: { color: C.divider }, line: { color: C.divider } });
}

// 불릿 텍스트 배열 만들기
function makeBullets(items, opts = {}) {
  return items.map((t, i) => ({
    text: t,
    options: {
      bullet: true,
      breakLine: i < items.length - 1,
      fontSize: opts.fontSize || 16,
      color: opts.color || C.textDark,
      paraSpaceAfter: opts.spaceAfter || 8,
    },
  }));
}

// 카드 그리기 (배경 박스)
function addCard(s, x, y, w, h, opts = {}) {
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: opts.fill || C.cardBg },
    line: { color: opts.border || C.cardBorder, width: 1 },
    shadow: opts.shadow !== false ? makeShadow() : undefined,
  });
}

// 큰 숫자 스탯 표시
function addBigStat(s, x, y, w, num, label, numColor) {
  addCard(s, x, y, w, 1.8, {});
  s.addText(num, {
    x: x + 0.1, y: y + 0.15, w: w - 0.2, h: 0.9, fontSize: 52, bold: true,
    color: numColor || C.mint, align: "center", margin: 0,
  });
  s.addText(label, {
    x: x + 0.1, y: y + 1.05, w: w - 0.2, h: 0.55, fontSize: 12,
    color: C.textGray, align: "center", margin: 0,
  });
}

// 슬라이드 번호 표시
function addSlideNum(s, n) {
  s.addText(`${n} / 50`, {
    x: 8.8, y: 5.2, w: 1.0, h: 0.3, fontSize: 9, color: C.textGray, align: "right", margin: 0,
  });
}

// 키 메시지 바
function addKeyMessage(s, text) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.3, y: 4.9, w: 9.4, h: 0.55,
    fill: { color: C.forestGrn }, line: { color: C.forestGrn },
  });
  s.addText(`💡 ${text}`, {
    x: 0.5, y: 4.92, w: 9.0, h: 0.5, fontSize: 12, bold: false,
    color: C.white, align: "left", margin: 0,
  });
}

// ═══════════════════════════════════════════════════════════════
// SLIDE 1: 타이틀
// ═══════════════════════════════════════════════════════════════
{
  const s = addDarkSlide();
  // 배경 민트 그러데이션 느낌 (우측 형태)
  s.addShape(pres.shapes.RECTANGLE, { x: 6.5, y: 0, w: 3.5, h: 5.625, fill: { color: C.forestGrn }, line: { color: C.forestGrn } });
  s.addShape(pres.shapes.RECTANGLE, { x: 6.5, y: 0, w: 0.06, h: 5.625, fill: { color: C.gold }, line: { color: C.gold } });

  s.addText("2026", {
    x: 0.5, y: 0.4, w: 5.8, h: 1.2, fontSize: 72, bold: true,
    color: C.gold, align: "left", margin: 0,
  });
  s.addText("기후 콘텐츠 소비자\n동향 리포트", {
    x: 0.5, y: 1.45, w: 5.8, h: 2.0, fontSize: 34, bold: true,
    color: C.white, align: "left", margin: 0,
  });

  s.addText([
    { text: "Z세대 62%", options: { bold: true, color: C.gold } },
    { text: " ESG 브랜드 선택  |  스트리밍 1시간 ", options: { color: C.mintLight } },
    { text: "55g CO₂", options: { bold: true, color: C.gold } },
  ], { x: 0.5, y: 3.5, w: 5.8, h: 0.5, fontSize: 14, margin: 0 });

  s.addText("팬덤이 기업 탄소 감축을 요구하고, AI가 기후 콘텐츠의 생존을 결정한다", {
    x: 0.5, y: 4.0, w: 5.8, h: 0.6, fontSize: 13, color: C.mintLight, align: "left", margin: 0,
  });

  // 우측 포인트 텍스트
  s.addText("5 SECTIONS\n50 SLIDES", {
    x: 6.8, y: 1.5, w: 2.8, h: 1.2, fontSize: 20, bold: true,
    color: C.white, align: "center", margin: 0,
  });
  s.addText("NotebookLM\nAI Research", {
    x: 6.8, y: 3.0, w: 2.8, h: 1.0, fontSize: 14,
    color: C.mintLight, align: "center", margin: 0,
  });
  addSlideNum(s, 1);
}

// ═══════════════════════════════════════════════════════════════
// SECTION 1 COVER
// ═══════════════════════════════════════════════════════════════
addSectionCover(1, "기후 소비자의 진화:\n윤리 + 실용주의의 결합", "슬라이드 2~10");

// SLIDE 2: 섹션 1 개요
{
  const s = addLightSlide();
  addSlideTitle(s, "섹션 1 개요: 기후 소비자의 세 가지 진화");

  const axes = [
    { icon: "①", title: "윤리적 컨슈머리즘", desc: "브랜드 선택의 기준이 ESG로 이동\n(Slide 3~4)", color: C.forestGrn },
    { icon: "②", title: "실용주의의 결합", desc: "피펫 소비로 친환경과 절약을 동시에\n(Slide 4~7)", color: C.mint },
    { icon: "③", title: "능동적 감시자로 진화", desc: "소비를 넘어 기업을 압박하는 주체\n(Slide 8~9)", color: C.gold },
  ];
  const startX = 0.4;
  const cardW = 2.9;
  axes.forEach((a, i) => {
    const x = startX + i * (cardW + 0.3);
    addCard(s, x, 1.1, cardW, 3.4, { border: a.color });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.1, w: cardW, h: 0.06, fill: { color: a.color }, line: { color: a.color } });
    s.addText(a.icon, { x: x + 0.1, y: 1.2, w: 0.7, h: 0.7, fontSize: 32, bold: true, color: a.color, margin: 0 });
    s.addText(a.title, { x: x + 0.15, y: 1.95, w: cardW - 0.3, h: 0.6, fontSize: 16, bold: true, color: C.textDark, margin: 0 });
    s.addText(a.desc, { x: x + 0.15, y: 2.6, w: cardW - 0.3, h: 1.7, fontSize: 13, color: C.textMid, margin: 0 });
  });
  addKeyMessage(s, "윤리와 실용주의는 더 이상 충돌하지 않는다—2026년 소비자는 이 둘을 동시에 요구하며 기업을 감시한다.");
  addSlideNum(s, 2);
}

// SLIDE 3: Z세대 62%
{
  const s = addLightSlide();
  addSlideTitle(s, "Z세대 62%: 지속 가능한 브랜드를 선택한다");

  addBigStat(s, 0.4, 1.1, 4.0, "62%", "Z세대 소비자 중 지속 가능 브랜드 선호", C.sage);
  s.addShape(pres.shapes.RECTANGLE, { x: 4.7, y: 1.1, w: 5.0, h: 1.8, fill: { color: C.forestGrn }, line: { color: C.forestGrn } });
  s.addText("ESG는 선택이\n아닌 필수 기준", { x: 4.9, y: 1.2, w: 4.6, h: 1.5, fontSize: 26, bold: true, color: C.white, margin: 0 });

  s.addText(makeBullets([
    "윤리적 생산 제품에 더 높은 가격도 기꺼이 지불",
    "ESG는 이제 브랜드 선택의 필수 기준, 선택지가 아니다",
    "기업이 '착한 척'이 아닌 실질적인 ESG 실행력을 갖춰야",
  ]), { x: 0.4, y: 3.2, w: 9.2, h: 1.5 });
  addKeyMessage(s, "Z세대 과반이 지속 가능성을 구매 결정의 1순위 기준으로 삼는 시대가 왔다.");
  addSlideNum(s, 3);
}

// SLIDE 4: 피펫 소비
{
  const s = addLightSlide();
  addSlideTitle(s, "피펫 소비: 극도의 실용주의가 친환경을 만나다");
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.1, w: 4.2, h: 3.5, fill: { color: C.mint }, line: { color: C.mint } });
  s.addText("피펫\n소비", { x: 0.4, y: 1.9, w: 4.2, h: 1.8, fontSize: 56, bold: true, color: C.white, align: "center", margin: 0 });
  s.addText("Pipette Consumption", { x: 0.4, y: 3.9, w: 4.2, h: 0.5, fontSize: 12, color: C.mintLight, align: "center", margin: 0 });

  s.addText(makeBullets([
    "필요한 만큼만 소분 구매하는 '피펫 소비' 트렌드 부상",
    "낭비 최소화 → 친환경 가치와 자연스럽게 연결",
    "대용량·과잉 소비 거부 — 소비 철학이 바뀐다",
    "브랜드는 소분 판매·리필 제도를 기회로 삼아야",
  ]), { x: 4.9, y: 1.1, w: 4.8, h: 3.5 });
  addKeyMessage(s, "피펫 소비는 친환경 마케팅의 새 공략점—실용적 가치와 환경 가치가 겹치는 교차점이다.");
  addSlideNum(s, 4);
}

// SLIDE 5: 소유의 종말
{
  const s = addLightSlide();
  addSlideTitle(s, "소유의 종말: 실물 굿즈에서 친환경 대안으로");

  const cols = [
    { label: "BEFORE", desc: "플라스틱 쓰레기를 양산하는\n실물 음반 대량 구매 문화", color: C.textGray, bg: "F5F5F5" },
    { label: "AFTER", desc: "디지털 앨범·리필 패키지 등\n폐기물 없는 친환경 소비 방식", color: C.forestGrn, bg: C.cream },
  ];
  cols.forEach((c, i) => {
    const x = 0.4 + i * 4.8;
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.1, w: 4.3, h: 3.5, fill: { color: c.bg }, line: { color: c.color } });
    s.addText(c.label, { x: x + 0.2, y: 1.25, w: 3.9, h: 0.6, fontSize: 22, bold: true, color: c.color, margin: 0 });
    s.addText(c.desc, { x: x + 0.2, y: 2.0, w: 3.9, h: 2.0, fontSize: 15, color: C.textDark, margin: 0 });
  });
  s.addText("→", { x: 4.5, y: 2.4, w: 0.7, h: 0.8, fontSize: 36, bold: true, color: C.gold, align: "center", margin: 0 });
  addKeyMessage(s, "실물 굿즈 중심 비즈니스 모델은 수명이 다했다—폐기물 없는 친환경 소비 대안으로 전환하지 않으면 도태된다.");
  addSlideNum(s, 5);
}

// SLIDE 6: 세대별 ESG 스펙트럼
{
  const s = addLightSlide();
  addSlideTitle(s, "세대별 ESG 소비 스펙트럼: Z·M·X세대의 차이");

  const gens = [
    { gen: "Z세대", keyword: "전제 조건", desc: "ESG를 브랜드 선택의 전제 조건으로 요구\n미달 시 즉각 이탈", color: C.forestGrn },
    { gen: "M세대", keyword: "균형 추구", desc: "가성비와 ESG의 균형 추구\n피펫 소비·프라이스 디코딩으로 검증", color: C.mint },
    { gen: "X세대", keyword: "경제적 인센티브", desc: "ESG 관심도 상승 중\n실질적 가격 이점이 전환의 열쇠", color: C.gold },
  ];
  gens.forEach((g, i) => {
    const y = 1.1 + i * 1.35;
    addCard(s, 0.4, y, 9.2, 1.15, { border: g.color });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y, w: 1.5, h: 1.15, fill: { color: g.color }, line: { color: g.color } });
    s.addText(g.gen, { x: 0.4, y: y + 0.2, w: 1.5, h: 0.75, fontSize: 22, bold: true, color: C.white, align: "center", margin: 0 });
    s.addText(g.keyword, { x: 2.1, y: y + 0.15, w: 2.5, h: 0.5, fontSize: 18, bold: true, color: g.color, margin: 0 });
    s.addText(g.desc, { x: 2.1, y: y + 0.6, w: 7.3, h: 0.45, fontSize: 12, color: C.textMid, margin: 0 });
  });
  addKeyMessage(s, "ESG 소비는 세대별로 다른 언어를 사용한다—세대별 접근법 차별화가 ESG 마케팅의 핵심이다.");
  addSlideNum(s, 6);
}

// SLIDE 7: 프라이스 디코딩
{
  const s = addLightSlide();
  addSlideTitle(s, "프라이스 디코딩: 친환경 프리미엄의 조건");

  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.1, w: 9.2, h: 1.0, fill: { color: C.cream }, line: { color: C.divider } });
  s.addText("소비자는 원가 · 브랜드값 · 유통비를 낱낱이 해독(디코딩)한다", {
    x: 0.6, y: 1.2, w: 8.8, h: 0.7, fontSize: 18, bold: true, color: C.textDark, margin: 0,
  });

  const items = [
    { title: "❌ 친환경 라벨만", desc: "프리미엄 정당화 불가\n소비자의 의심만 증가", ok: false },
    { title: "✅ 압도적 상품력", desc: "가성비 + 친환경 가치\n데이터 기반 투명 근거", ok: true },
  ];
  items.forEach((it, i) => {
    const x = 0.4 + i * 4.8;
    addCard(s, x, 2.3, 4.3, 2.2, { border: it.ok ? C.sage : C.textGray });
    s.addText(it.title, { x: x + 0.2, y: 2.45, w: 3.9, h: 0.6, fontSize: 18, bold: true, color: it.ok ? C.forestGrn : C.textGray, margin: 0 });
    s.addText(it.desc, { x: x + 0.2, y: 3.1, w: 3.9, h: 1.2, fontSize: 14, color: C.textMid, margin: 0 });
  });
  addKeyMessage(s, "친환경 라벨은 가격 인상의 근거가 아니다—압도적 가성비와 투명한 근거가 필수다.");
  addSlideNum(s, 7);
}

// SLIDE 8: 윤리적 소비자 → 능동적 감시자
{
  const s = addLightSlide();
  addSlideTitle(s, "윤리적 소비자에서 능동적 감시자로");
  s.addText(makeBullets([
    "소비자 역할이 '착하게 구매'에서 '기업 감시'로 확장",
    "그린워싱 적발 시 SNS를 통한 즉각적 공론화와 불매 운동",
    "앨범 탄소 배출 전 주기 평가하는 '클린 차트' 도입 요구 증가",
  ], { fontSize: 17, spaceAfter: 14 }), { x: 0.4, y: 1.1, w: 5.5, h: 3.5 });
  s.addShape(pres.shapes.RECTANGLE, { x: 6.2, y: 1.1, w: 3.5, h: 3.5, fill: { color: C.darkBg }, line: { color: C.darkBg } });
  s.addText("그린워싱은\n경영 리스크다", {
    x: 6.2, y: 2.0, w: 3.5, h: 1.5, fontSize: 24, bold: true,
    color: C.gold, align: "center", margin: 0,
  });
  addKeyMessage(s, "그린워싱은 퇴출 사유다—소비자는 이제 기업의 탄소 감시관이 되었다.");
  addSlideNum(s, 8);
}

// SLIDE 9: 섹션 1 종합
{
  const s = addLightSlide();
  addSlideTitle(s, "섹션 1 종합: 기후 소비자 진화의 3대 축");

  const rows = [
    { axis: "소비 방식", before: "대량 실물 소유", after: "소분 실용 구매 + 무형 경험" },
    { axis: "참여 방식", before: "개인 실천", after: "조직적 집단 행동 + 그린워싱 감시" },
    { axis: "선택 기준", before: "가격 · 품질", after: "ESG 실행력 + 프라이스 디코딩" },
  ];
  // 헤더
  ["구분", "Before", "After"].forEach((h, i) => {
    const xArr = [0.4, 2.8, 6.0];
    const wArr = [2.2, 3.0, 3.8];
    s.addShape(pres.shapes.RECTANGLE, { x: xArr[i], y: 1.1, w: wArr[i], h: 0.55, fill: { color: C.forestGrn }, line: { color: C.forestGrn } });
    s.addText(h, { x: xArr[i] + 0.1, y: 1.15, w: wArr[i] - 0.2, h: 0.45, fontSize: 14, bold: true, color: C.white, margin: 0 });
  });
  rows.forEach((r, i) => {
    const y = 1.7 + i * 0.95;
    const bg = i % 2 === 0 ? C.cream : C.white;
    [[0.4, 2.2, r.axis, true], [2.8, 3.0, r.before, false], [6.0, 3.8, r.after, false]].forEach(([x, w, txt, bold]) => {
      s.addShape(pres.shapes.RECTANGLE, { x, y, w, h: 0.85, fill: { color: bg }, line: { color: C.divider } });
      s.addText(txt, { x: x + 0.1, y: y + 0.1, w: w - 0.2, h: 0.65, fontSize: 13, bold: !!bold, color: bold ? C.forestGrn : C.textDark, margin: 0 });
    });
  });
  addKeyMessage(s, "기후 소비자의 진화는 일시적 유행이 아닌 소비 패러다임의 구조적 전환이다.");
  addSlideNum(s, 9);
}

// SLIDE 10: 전환 슬라이드
{
  const s = addDarkSlide();
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.12, fill: { color: C.gold }, line: { color: C.gold } });
  s.addText("소비자가 바뀌었다면, 플랫폼도 바뀌어야 한다", {
    x: 0.5, y: 0.8, w: 9, h: 1.0, fontSize: 30, bold: true, color: C.white, align: "center", margin: 0,
  });
  s.addText("그러나 디지털 소비에도 숨겨진 탄소 발자국이 존재한다 — 그 규모는?", {
    x: 0.5, y: 2.0, w: 9, h: 0.8, fontSize: 18, color: C.mintLight, align: "center", margin: 0,
  });
  s.addText("다음 섹션: RE100 경쟁과 제로 클릭 시대의 기후 콘텐츠 생존 전략", {
    x: 0.5, y: 3.2, w: 9, h: 0.6, fontSize: 14, color: C.gold, align: "center", margin: 0,
  });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.5, w: 10, h: 0.12, fill: { color: C.sage }, line: { color: C.sage } });
  addSlideNum(s, 10);
}

// ═══════════════════════════════════════════════════════════════
// SECTION 2
// ═══════════════════════════════════════════════════════════════
addSectionCover(2, "플랫폼 전쟁:\nRE100과 제로 클릭 시대의 기후 콘텐츠", "슬라이드 11~20");

// SLIDE 11: 플랫폼 개요
{
  const s = addLightSlide();
  addSlideTitle(s, "플랫폼 섹션 개요: 디지털 소비의 탄소 발자국");
  const pts = [
    { n: "01", q: "음악 스트리밍 1시간의 CO₂ 배출량은?", sub: "디지털 소비의 숨겨진 비용" },
    { n: "02", q: "글로벌 vs 국내 RE100 격차", sub: "소비자 이탈의 새 원인" },
    { n: "03", q: "AI 제로 클릭 환경에서의 생존 전략", sub: "기후 콘텐츠의 근본적 변화" },
  ];
  pts.forEach((p, i) => {
    const y = 1.15 + i * 1.3;
    addCard(s, 0.4, y, 9.2, 1.1, { border: C.mint });
    s.addText(p.n, { x: 0.5, y: y + 0.15, w: 0.8, h: 0.8, fontSize: 28, bold: true, color: C.mint, align: "center", margin: 0 });
    s.addText(p.q, { x: 1.5, y: y + 0.1, w: 5.5, h: 0.5, fontSize: 17, bold: true, color: C.textDark, margin: 0 });
    s.addText(p.sub, { x: 1.5, y: y + 0.6, w: 5.5, h: 0.4, fontSize: 12, color: C.textGray, margin: 0 });
  });
  addKeyMessage(s, "플랫폼의 탄소 배출은 더 이상 숨길 수 없다—RE100 전환 속도가 플랫폼의 생존을 결정한다.");
  addSlideNum(s, 11);
}

// SLIDE 12: 55g CO₂
{
  const s = addLightSlide();
  addSlideTitle(s, "55g CO₂: 스트리밍의 숨겨진 환경 비용");

  // 임팩트 숫자
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.1, w: 4.5, h: 3.5, fill: { color: C.darkBg }, line: { color: C.darkBg } });
  s.addText("55g", { x: 0.4, y: 1.3, w: 4.5, h: 1.8, fontSize: 90, bold: true, color: C.gold, align: "center", margin: 0 });
  s.addText("CO₂", { x: 0.4, y: 2.9, w: 4.5, h: 0.7, fontSize: 36, bold: true, color: C.mintLight, align: "center", margin: 0 });
  s.addText("음악 스트리밍 1시간", { x: 0.4, y: 3.7, w: 4.5, h: 0.5, fontSize: 13, color: C.white, align: "center", margin: 0 });

  s.addText(makeBullets([
    "= 플라스틱 빨대 41개 분량의 탄소 배출",
    "소비자들이 이 수치를 인지하면서 플랫폼 압박 증가",
    "디지털 소비가 '무탄소'라는 신화가 붕괴되고 있다",
  ], { fontSize: 16 }), { x: 5.2, y: 1.3, w: 4.5, h: 3.0 });
  addKeyMessage(s, "디지털 소비에도 탄소 발자국이 있다—55g CO₂는 플랫폼 RE100 전환을 정당화하는 핵심 수치다.");
  addSlideNum(s, 12);
}

// SLIDE 13: 글로벌 RE100
{
  const s = addLightSlide();
  addSlideTitle(s, "글로벌 플랫폼의 RE100 선점 전략");

  const platforms = [
    { name: "Apple Music", status: "RE100 달성 추진 중", level: 85, color: C.sage },
    { name: "Spotify", status: "RE100 목표 선언", level: 70, color: C.mint },
    { name: "YouTube Music", status: "RE100 달성 추진 중", level: 80, color: C.forestGrn },
    { name: "국내 플랫폼", status: "넷제로 목표 수립 단계", level: 25, color: C.gold },
  ];
  platforms.forEach((p, i) => {
    const y = 1.15 + i * 0.98;
    s.addText(p.name, { x: 0.4, y: y + 0.15, w: 2.5, h: 0.6, fontSize: 14, bold: true, color: C.textDark, margin: 0 });
    // 진행 바 배경
    s.addShape(pres.shapes.RECTANGLE, { x: 2.9, y: y + 0.2, w: 5.5, h: 0.4, fill: { color: C.divider }, line: { color: C.divider } });
    s.addShape(pres.shapes.RECTANGLE, { x: 2.9, y: y + 0.2, w: 5.5 * p.level / 100, h: 0.4, fill: { color: p.color }, line: { color: p.color } });
    s.addText(p.status, { x: 8.5, y: y + 0.15, w: 1.3, h: 0.6, fontSize: 10, color: C.textGray, align: "right", margin: 0 });
  });
  addKeyMessage(s, "RE100은 글로벌 플랫폼의 기본 스펙이 되어 가고 있다—국내 플랫폼의 추격이 시급하다.");
  addSlideNum(s, 13);
}

// SLIDE 14: 국내 플랫폼 넷제로
{
  const s = addLightSlide();
  addSlideTitle(s, "국내 플랫폼의 넷제로 로드맵: 2030~2040");
  s.addText(makeBullets([
    "멜론 · 바이브 · 플로: 2030~2040년 넷제로 달성 목표 설정",
    "RE100 가입 · 클라우드 이전 · 고효율 데이터센터 운영 등 단계적 전환",
    "소비자 요구 속도 vs 플랫폼 전환 속도의 간극이 최대 리스크",
    "목표 공표보다 중간 이정표 공개가 신뢰 회복의 열쇠",
  ], { fontSize: 17, spaceAfter: 14 }), { x: 0.4, y: 1.1, w: 9.2, h: 3.5 });
  addKeyMessage(s, "넷제로 목표 선언만으로는 부족하다—소비자가 체감할 수 있는 중간 성과 공개가 필수다.");
  addSlideNum(s, 14);
}

// SLIDE 15: RE100 격차
{
  const s = addLightSlide();
  addSlideTitle(s, "RE100 격차가 만드는 소비자 선택의 변화");
  const cols2 = [
    { title: "글로벌 플랫폼 (RE100 선점)", items: ["RE100 목표 공개 선언", "소비자 신뢰 선점", "국내 시장 점유율 상승"], good: true },
    { title: "국내 플랫폼 (RE100 지연)", items: ["RE100 미달로 환경 소비자 회피", "글로벌 플랫폼으로 이탈 가속", "구독 유지·해지 판단 기준으로 부상"], good: false },
  ];
  cols2.forEach((c, i) => {
    const x = 0.4 + i * 4.9;
    addCard(s, x, 1.1, 4.3, 3.6, { border: c.good ? C.sage : C.gold });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.1, w: 4.3, h: 0.55, fill: { color: c.good ? C.sage : C.gold }, line: { color: c.good ? C.sage : C.gold } });
    s.addText(c.title, { x: x + 0.1, y: 1.15, w: 4.1, h: 0.45, fontSize: 13, bold: true, color: C.white, margin: 0 });
    s.addText(makeBullets(c.items, { fontSize: 14 }), { x: x + 0.1, y: 1.75, w: 4.1, h: 2.8 });
  });
  addKeyMessage(s, "RE100은 환경 지표가 아니라 사용자 이탈을 결정하는 플랫폼 경쟁력 지표다.");
  addSlideNum(s, 15);
}

// SLIDE 16: 제로 클릭
{
  const s = addLightSlide();
  addSlideTitle(s, "제로 클릭 시대의 도래: AI가 콘텐츠를 선택한다");
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.1, w: 9.2, h: 1.2, fill: { color: C.forestGrn }, line: { color: C.forestGrn } });
  s.addText("ZERO CLICK", { x: 0.5, y: 1.2, w: 4.0, h: 0.9, fontSize: 42, bold: true, color: C.gold, margin: 0 });
  s.addText("AI가 클릭 없이 최적 콘텐츠를 즉시 제안", { x: 4.5, y: 1.35, w: 4.9, h: 0.75, fontSize: 16, color: C.white, margin: 0 });
  s.addText(makeBullets([
    "소비자가 능동적으로 탐색하던 시대 → AI 큐레이션 시대로 전환",
    "기후 콘텐츠가 AI 알고리즘 최상단에 오르지 못하면 소비자에게 닿지 않는다",
    "트렌드코리아 2026 핵심 키워드—미디어 생태계의 근본적 변화",
  ], { fontSize: 16 }), { x: 0.4, y: 2.5, w: 9.2, h: 2.2 });
  addKeyMessage(s, "제로 클릭 시대에는 AI 알고리즘이 선택하지 않는 기후 콘텐츠는 존재하지 않는 것과 같다.");
  addSlideNum(s, 16);
}

// SLIDE 17: AI 알고리즘 최적화
{
  const s = addLightSlide();
  addSlideTitle(s, "AI 알고리즘 최적화: 기후 콘텐츠 생존 전략");
  s.addText(makeBullets([
    "단순 브랜딩 넘어 AI가 답변으로 선택하는 데이터 구조화 필수",
    "신뢰성 높은 수치와 출처 기반 콘텐츠가 AI 큐레이션에서 우선 채택",
    "기후 콘텐츠 제작자는 'AI 피드백 루프'를 설계하는 전략가가 되어야",
  ], { fontSize: 17, spaceAfter: 16 }), { x: 0.4, y: 1.1, w: 9.2, h: 3.5 });
  addKeyMessage(s, "기후 콘텐츠의 경쟁력은 감성이 아닌 AI가 채택할 수 있는 데이터 구조화에 달려 있다.");
  addSlideNum(s, 17);
}

// SLIDE 18: 포맷 전략
{
  const s = addLightSlide();
  addSlideTitle(s, "AI 큐레이션 시대의 기후 콘텐츠 포맷 전략");
  const fmts = [
    { type: "롱폼 (30분+)", tag: "AI 신뢰 출처", desc: "AI가 신뢰 출처로 채택하는\n깊이 있는 분석 콘텐츠", color: C.forestGrn },
    { type: "숏폼 (60초~)", tag: "제로 클릭 최적화", desc: "AI가 즉각 요약·배포하는\n핵심 메시지 클립", color: C.mint },
  ];
  fmts.forEach((f, i) => {
    const x = 0.4 + i * 4.9;
    addCard(s, x, 1.1, 4.3, 3.6, { border: f.color });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.1, w: 4.3, h: 0.06, fill: { color: f.color }, line: { color: f.color } });
    s.addText(f.type, { x: x + 0.15, y: 1.25, w: 3.9, h: 0.6, fontSize: 20, bold: true, color: f.color, margin: 0 });
    s.addText(f.tag, {
      x: x + 0.15, y: 1.9, w: 3.0, h: 0.4,
      fontSize: 11, bold: true, color: C.white,
    });
    s.addShape(pres.shapes.RECTANGLE, { x: x + 0.15, y: 1.88, w: 2.5, h: 0.38, fill: { color: f.color }, line: { color: f.color } });
    s.addText(f.tag, { x: x + 0.15, y: 1.88, w: 2.5, h: 0.38, fontSize: 11, bold: true, color: C.white, align: "center", margin: 0 });
    s.addText(f.desc, { x: x + 0.15, y: 2.45, w: 3.9, h: 2.0, fontSize: 14, color: C.textDark, margin: 0 });
  });
  addKeyMessage(s, "롱폼으로 AI 신뢰 출처가 되고 숏폼으로 제로 클릭 배포를 공략하는 투트랙 전략이 필요하다.");
  addSlideNum(s, 18);
}

// SLIDE 19: 섹션 2 종합
{
  const s = addLightSlide();
  addSlideTitle(s, "섹션 2 종합: 플랫폼의 두 가지 전장");
  const battlefields = [
    { n: "전장 1", title: "RE100", status: "글로벌 선점 → 국내 2030~2040 추격 중", winner: "RE100 달성 + 투명 공개" },
    { n: "전장 2", title: "제로 클릭", status: "AI 큐레이션에서 선택받는 콘텐츠 전략 필요", winner: "데이터 구조화 + 투트랙 포맷" },
  ];
  battlefields.forEach((b, i) => {
    const y = 1.2 + i * 1.7;
    addCard(s, 0.4, y, 9.2, 1.5, { border: C.mint });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y, w: 1.6, h: 1.5, fill: { color: C.mint }, line: { color: C.mint } });
    s.addText(b.n, { x: 0.4, y: y + 0.15, w: 1.6, h: 0.5, fontSize: 14, bold: true, color: C.white, align: "center", margin: 0 });
    s.addText(b.title, { x: 0.4, y: y + 0.6, w: 1.6, h: 0.6, fontSize: 18, bold: true, color: C.white, align: "center", margin: 0 });
    s.addText(b.status, { x: 2.2, y: y + 0.2, w: 5.5, h: 0.6, fontSize: 15, bold: true, color: C.textDark, margin: 0 });
    s.addText(`✓ ${b.winner}`, { x: 2.2, y: y + 0.85, w: 7.2, h: 0.5, fontSize: 13, color: C.sage, margin: 0 });
  });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 4.6, w: 9.2, h: 0.18, fill: { color: C.divider }, line: { color: C.divider } });
  s.addText("승자: RE100 달성 + AI 최적화 콘텐츠를 동시에 갖춘 플랫폼", {
    x: 0.5, y: 4.62, w: 9.0, h: 0.16, fontSize: 13, bold: true, color: C.forestGrn, margin: 0,
  });
  addKeyMessage(s, "플랫폼의 미래는 RE100 전환 속도와 AI 최적화 역량이 함께 결정한다.");
  addSlideNum(s, 19);
}

// SLIDE 20: 전환
{
  const s = addDarkSlide();
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.12, fill: { color: C.mint }, line: { color: C.mint } });
  s.addText("팬덤이 플랫폼을 바꾼다", {
    x: 0.5, y: 1.0, w: 9, h: 1.0, fontSize: 38, bold: true, color: C.white, align: "center", margin: 0,
  });
  s.addText("케이팝포플래닛: 수만 명이 서명으로 산업 구조를 바꾼 사례", {
    x: 0.5, y: 2.3, w: 9, h: 0.7, fontSize: 18, color: C.mintLight, align: "center", margin: 0,
  });
  s.addText("다음 섹션: 집단 행동의 시대 — 팬덤이 어떻게 산업을 바꾸는가", {
    x: 0.5, y: 3.3, w: 9, h: 0.6, fontSize: 14, color: C.gold, align: "center", margin: 0,
  });
  addSlideNum(s, 20);
}

// ═══════════════════════════════════════════════════════════════
// SECTION 3
// ═══════════════════════════════════════════════════════════════
addSectionCover(3, "집단 행동의 시대:\n팬덤이 산업을 바꾼다", "슬라이드 21~30");

// SLIDE 21: 팬덤 개요
{
  const s = addLightSlide();
  addSlideTitle(s, "팬덤 섹션 개요: 왜 팬덤이 기후 행동의 주체가 되었는가");
  const reasons = [
    { icon: "🌐", title: "글로벌 네트워크", desc: "글로벌 연결망 · 강한 정체성 · 조직 동원력을 동시에 보유한 유일한 집단" },
    { icon: "💚", title: "내적 동기", desc: "사랑하는 아티스트의 환경 피해를 막으려는 강력한 내적 동기가 행동의 원동력" },
    { icon: "💰", title: "소비 권력", desc: "소비 권력을 가진 집단이 직접 기업을 압박—어떤 NGO도 갖추지 못한 구조" },
  ];
  reasons.forEach((r, i) => {
    const y = 1.15 + i * 1.3;
    addCard(s, 0.4, y, 9.2, 1.1, { border: C.sage });
    s.addText(r.icon, { x: 0.5, y: y + 0.15, w: 0.9, h: 0.8, fontSize: 32, align: "center", margin: 0 });
    s.addText(r.title, { x: 1.55, y: y + 0.1, w: 2.5, h: 0.5, fontSize: 18, bold: true, color: C.forestGrn, margin: 0 });
    s.addText(r.desc, { x: 1.55, y: y + 0.6, w: 7.9, h: 0.45, fontSize: 13, color: C.textMid, margin: 0 });
  });
  addKeyMessage(s, "팬덤이 기후 행동의 주체가 된 것은 우연이 아니다—글로벌 네트워크와 아티스트 사랑이 결합된 구조적 필연이다.");
  addSlideNum(s, 21);
}

// SLIDE 22: 케이팝포플래닛
{
  const s = addLightSlide();
  addSlideTitle(s, "케이팝포플래닛: 팬덤이 산업을 움직이다");
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.1, w: 4.2, h: 3.5, fill: { color: C.forestGrn }, line: { color: C.forestGrn } });
  s.addText("KPOP4PLANET", { x: 0.5, y: 1.4, w: 4.0, h: 0.8, fontSize: 22, bold: true, color: C.gold, align: "center", margin: 0 });
  s.addText("팬덤 기후\n행동 캠페인", { x: 0.5, y: 2.2, w: 4.0, h: 1.5, fontSize: 28, bold: true, color: C.white, align: "center", margin: 0 });
  s.addText("세계적 선례", { x: 0.5, y: 3.9, w: 4.0, h: 0.5, fontSize: 14, color: C.mintLight, align: "center", margin: 0 });
  s.addText(makeBullets([
    "전 세계 케이팝 팬들이 자발 결성한 기후 행동 캠페인 조직",
    "수만 명 이상 서명 모아 엔터사·플랫폼에 탄소 감축 공식 요구",
    "산업 구조 변화를 끌어낸 팬덤 기반 기후 행동의 세계적 선례",
  ], { fontSize: 15 }), { x: 4.9, y: 1.3, w: 4.8, h: 3.0 });
  addKeyMessage(s, "케이팝포플래닛은 소비자 집단 행동이 산업 ESG 전략을 바꿀 수 있음을 증명했다.");
  addSlideNum(s, 22);
}

// SLIDE 23: 3대 압박 전략
{
  const s = addLightSlide();
  addSlideTitle(s, "팬덤 기후 행동의 3대 압박 전략");
  const strategies = [
    { n: "전략 1", title: "글로벌 서명 캠페인", desc: "기업에 공식 RE100 약속 요구", color: C.sage },
    { n: "전략 2", title: "클린 차트 도입 촉구", desc: "앨범 전 주기 탄소 배출 투명 공개 요구", color: C.mint },
    { n: "전략 3", title: "랜덤 포토카드 비판", desc: "차트 시스템의 환경 문제 SNS 공론화", color: C.gold },
  ];
  strategies.forEach((st, i) => {
    const x = 0.4 + i * 3.15;
    addCard(s, x, 1.1, 2.85, 3.6, { border: st.color });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.1, w: 2.85, h: 0.06, fill: { color: st.color }, line: { color: st.color } });
    s.addText(st.n, { x: x + 0.1, y: 1.25, w: 2.6, h: 0.45, fontSize: 13, bold: true, color: st.color, margin: 0 });
    s.addText(st.title, { x: x + 0.1, y: 1.75, w: 2.6, h: 0.8, fontSize: 17, bold: true, color: C.textDark, margin: 0 });
    s.addText(st.desc, { x: x + 0.1, y: 2.65, w: 2.6, h: 1.7, fontSize: 13, color: C.textMid, margin: 0 });
  });
  addKeyMessage(s, "팬덤의 기후 압박은 서명에서 제도 개혁 요구까지—전방위적 전략이 기업을 움직인다.");
  addSlideNum(s, 23);
}

// SLIDE 24: 랜덤 포토카드의 역설
{
  const s = addLightSlide();
  addSlideTitle(s, "랜덤 포토카드의 역설: 팬덤이 자신의 소비를 비판한다");
  s.addText(makeBullets([
    "포토카드 완성 위한 앨범 대량 구매 → 플라스틱 폐기물 양산",
    "팬들 스스로 이 소비 구조를 비판하며 변화를 요구하기 시작",
    "사랑하는 아티스트를 위해 오히려 해로운 소비를 강요받는 구조",
  ], { fontSize: 17, spaceAfter: 16 }), { x: 0.4, y: 1.1, w: 9.2, h: 3.5 });
  addKeyMessage(s, "팬덤의 자기비판적 기후 행동은 산업 관행을 바꾸는 가장 강력한 내부 압력이다.");
  addSlideNum(s, 24);
}

// SLIDE 25: 그린워싱 감시
{
  const s = addLightSlide();
  addSlideTitle(s, "그린워싱 감시: 소비자가 진짜를 가려낸다");
  s.addText(makeBullets([
    "기업의 형식적 친환경 마케팅을 즉각 포착하고 SNS로 공론화",
    "탄소 감축 효율을 과학적으로 비교·분석해 더 효과적인 대안을 요구",
    "그린워싱 적발 브랜드는 팬덤 이탈과 불매 운동의 직격탄을 맞는다",
  ], { fontSize: 17, spaceAfter: 16 }), { x: 0.4, y: 1.1, w: 9.2, h: 3.5 });
  addKeyMessage(s, "그린워싱은 탄로나는 시대가 왔다—소비자는 친환경 캠페인의 실제 효과를 검증한다.");
  addSlideNum(s, 25);
}

// SLIDE 26: 새 숲 vs 기존 숲
{
  const s = addLightSlide();
  addSlideTitle(s, "새 숲 vs 기존 숲: 기후 행동의 고도화");
  const cmp = [
    { era: "과거", label: "새 나무 심기", desc: "아티스트 이름으로 나무 심기\n감성적·상징적 캠페인", color: C.textGray },
    { era: "현재", label: "기존 숲 보호", desc: "탄소 흡수 효율 높은 기존 숲\n입양·보호 방식으로 진화", color: C.forestGrn },
  ];
  cmp.forEach((c, i) => {
    const x = 0.4 + i * 4.9;
    addCard(s, x, 1.1, 4.3, 3.6, { border: c.color });
    s.addText(c.era, { x: x + 0.2, y: 1.25, w: 3.9, h: 0.5, fontSize: 24, bold: true, color: c.color, margin: 0 });
    s.addText(c.label, { x: x + 0.2, y: 1.85, w: 3.9, h: 0.6, fontSize: 20, bold: true, color: C.textDark, margin: 0 });
    s.addText(c.desc, { x: x + 0.2, y: 2.55, w: 3.9, h: 1.9, fontSize: 14, color: C.textMid, margin: 0 });
  });
  addKeyMessage(s, "감성적 환경 운동의 시대는 끝났다—팬덤은 이제 탄소 감축 효율을 과학적으로 따진다.");
  addSlideNum(s, 26);
}

// SLIDE 27: 글로벌 네트워크
{
  const s = addLightSlide();
  addSlideTitle(s, "팬덤의 글로벌 네트워크: 기후 행동의 무기");
  s.addText(makeBullets([
    "케이팝 팬덤의 글로벌 연결망이 기후 캠페인의 즉각적 국제화 실현",
    "수만 명 서명을 수일 내 모으는 팬덤의 조직 동원력",
    "로컬 이슈를 글로벌 압박으로 전환하는 팬덤 네트워크의 독보적 힘",
  ], { fontSize: 17, spaceAfter: 16 }), { x: 0.4, y: 1.1, w: 9.2, h: 3.5 });
  addKeyMessage(s, "케이팝 팬덤의 글로벌 네트워크는 세계 어느 환경단체도 갖추지 못한 기후 행동 동원력을 보유했다.");
  addSlideNum(s, 27);
}

// SLIDE 28: 팬덤-기업 협력
{
  const s = addLightSlide();
  addSlideTitle(s, "팬덤과 기업의 새로운 관계: 갈등에서 협력으로");
  s.addText(makeBullets([
    "기업이 먼저 투명한 ESG 로드맵 공유 시 팬덤이 적극 홍보대사로 전환",
    "팬덤 참여형 기후 캠페인 설계가 브랜드 신뢰도와 충성도를 동시에 강화",
    "팬덤을 감시자가 아닌 ESG 공동 설계자로 참여시키는 모델이 필요",
  ], { fontSize: 17, spaceAfter: 16 }), { x: 0.4, y: 1.1, w: 9.2, h: 3.5 });
  addKeyMessage(s, "팬덤을 ESG 공동 설계자로 만드는 기업이 가장 강력한 기후 브랜드가 된다.");
  addSlideNum(s, 28);
}

// SLIDE 29: 섹션 3 종합
{
  const s = addLightSlide();
  addSlideTitle(s, "섹션 3 종합: 팬덤이 실제로 바꾼 세 가지 산업 변화");
  const changes = [
    { n: "변화 1", desc: "앨범·굿즈 소비 관행 → 플랫폼 음반·경험 중심으로 재편", tag: "진행 중" },
    { n: "변화 2", desc: "기업 자율 ESG → 팬덤 압박에 의한 공식 탄소 감축 약속", tag: "성과 확인됨" },
    { n: "변화 3", desc: "일방적 팬 서비스 → 팬덤 참여형 ESG 공동 설계 모델", tag: "확산 중" },
  ];
  changes.forEach((c, i) => {
    const y = 1.15 + i * 1.2;
    addCard(s, 0.4, y, 9.2, 1.0, { border: C.sage });
    s.addText(c.n, { x: 0.5, y: y + 0.15, w: 1.0, h: 0.7, fontSize: 14, bold: true, color: C.sage, margin: 0 });
    s.addText(c.desc, { x: 1.6, y: y + 0.15, w: 6.5, h: 0.7, fontSize: 14, color: C.textDark, margin: 0 });
    s.addShape(pres.shapes.RECTANGLE, { x: 8.3, y: y + 0.2, w: 1.1, h: 0.55, fill: { color: C.sage }, line: { color: C.sage } });
    s.addText(c.tag, { x: 8.3, y: y + 0.2, w: 1.1, h: 0.55, fontSize: 10, bold: true, color: C.white, align: "center", margin: 0 });
  });
  addKeyMessage(s, "팬덤의 집단 행동은 엔터테인먼트 산업의 ESG 비즈니스 모델을 근본적으로 재편하고 있다.");
  addSlideNum(s, 29);
}

// SLIDE 30: 전환
{
  const s = addDarkSlide();
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.12, fill: { color: C.gold }, line: { color: C.gold } });
  s.addText("행동이 만드는 기회", {
    x: 0.5, y: 1.0, w: 9, h: 1.0, fontSize: 38, bold: true, color: C.white, align: "center", margin: 0,
  });
  s.addText("경험 사치 · 인간 증명 · ESG 의무화가 만드는 새로운 비즈니스 지형", {
    x: 0.5, y: 2.3, w: 9, h: 0.7, fontSize: 18, color: C.mintLight, align: "center", margin: 0,
  });
  s.addText("다음 섹션: 2026년 기회 지형 — 기업이 놓치면 안 되는 3대 기회", {
    x: 0.5, y: 3.3, w: 9, h: 0.6, fontSize: 14, color: C.gold, align: "center", margin: 0,
  });
  addSlideNum(s, 30);
}

// ═══════════════════════════════════════════════════════════════
// SECTION 4
// ═══════════════════════════════════════════════════════════════
addSectionCover(4, "2026년 기회 지형:\n경험 사치 · 인간 증명 · ESG 의무화", "슬라이드 31~40");

// SLIDE 31: 기회 개요
{
  const s = addLightSlide();
  addSlideTitle(s, "기회 지형 섹션 개요: 세 가지 황금 기회");
  const opps = [
    { n: "기회 1", title: "경험 사치", desc: "실물 굿즈의 종말과\n친환경 경험 비즈니스의 부상", color: C.forestGrn },
    { n: "기회 2", title: "인간 증명", desc: "AI 범람 시대에\n진정성 있는 오프라인 연대의 희소가치", color: C.mint },
    { n: "기회 3", title: "ESG 의무화", desc: "2030년 상장사 공시 의무화가\n만드는 선제 대응 기회", color: C.gold },
  ];
  opps.forEach((o, i) => {
    const x = 0.4 + i * 3.15;
    addCard(s, x, 1.1, 2.85, 3.6, { border: o.color });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.1, w: 2.85, h: 0.7, fill: { color: o.color }, line: { color: o.color } });
    s.addText(o.n, { x: x + 0.1, y: 1.15, w: 2.6, h: 0.55, fontSize: 13, bold: true, color: C.white, margin: 0 });
    s.addText(o.title, { x: x + 0.1, y: 1.95, w: 2.6, h: 0.65, fontSize: 22, bold: true, color: o.color, margin: 0 });
    s.addText(o.desc, { x: x + 0.1, y: 2.7, w: 2.6, h: 1.8, fontSize: 13, color: C.textMid, margin: 0 });
  });
  addKeyMessage(s, "2026년은 경험 사치·인간 증명·ESG 의무화가 동시에 열리는 기후 비즈니스의 골든타임이다.");
  addSlideNum(s, 31);
}

// SLIDE 32: 경험 사치
{
  const s = addLightSlide();
  addSlideTitle(s, "경험 사치: 소유의 종말, 경험의 부상");
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.1, w: 4.2, h: 3.5, fill: { color: C.mint }, line: { color: C.mint } });
  s.addText("경험\n사치", { x: 0.4, y: 1.9, w: 4.2, h: 1.8, fontSize: 56, bold: true, color: C.white, align: "center", margin: 0 });
  s.addText("Experiential Luxury", { x: 0.4, y: 3.9, w: 4.2, h: 0.5, fontSize: 12, color: C.mintLight, align: "center", margin: 0 });
  s.addText(makeBullets([
    "명품 소유에서 특별한 경험(여행·공연·커뮤니티)에 지출하는 시대로 전환",
    "실물 굿즈·앨범 없이도 프리미엄 가치를 제공하는 경험 비즈니스 가능",
    "탄소 발자국 없는 경험 콘텐츠가 2026년 기후 비즈니스의 핵심 영역",
  ], { fontSize: 15 }), { x: 4.9, y: 1.3, w: 4.8, h: 3.0 });
  addKeyMessage(s, "경험 사치는 기후 콘텐츠 비즈니스가 실물 폐기물 없이 프리미엄 가치를 창출할 수 있는 전략적 기회다.");
  addSlideNum(s, 32);
}

// SLIDE 33: 저탄소 콘서트
{
  const s = addLightSlide();
  addSlideTitle(s, "저탄소 콘서트: 경험 사치의 선두 주자");
  s.addText(makeBullets([
    "관객 운동 에너지를 전력으로 변환하는 친환경 플로어 기술 적용",
    "식물성 재료 기반 LED 팔찌 등 탄소 최소화 공연 소품 활용",
    "빌리 아일리시 오버히티드 콘서트 모델이 세계적 벤치마크로 부상",
  ], { fontSize: 17, spaceAfter: 16 }), { x: 0.4, y: 1.1, w: 9.2, h: 3.5 });
  addKeyMessage(s, "저탄소 콘서트는 이미 글로벌 표준이 되고 있다—국내 기업의 빠른 도입이 선점 기회다.");
  addSlideNum(s, 33);
}

// SLIDE 34: 하이엔드 친환경 투어
{
  const s = addLightSlide();
  addSlideTitle(s, "하이엔드 친환경 투어: 새로운 럭셔리 시장");
  const items2 = [
    { title: "탄소 최소화 프리미엄 여행", desc: "탄소 발자국을 최소화한 프리미엄 친환경 여행 상품 수요 증가", color: C.sage },
    { title: "생태 보호 연계 고급 투어", desc: "자연 생태 보호와 연계한 고급 투어가 경험 사치의 새 카테고리", color: C.mint },
    { title: "기후 토크 콘서트 패키지", desc: "오프라인 기후 토크 콘서트·워크샵과 결합한 투어 패키지 상품화", color: C.forestGrn },
  ];
  items2.forEach((it, i) => {
    const y = 1.15 + i * 1.2;
    addCard(s, 0.4, y, 9.2, 1.0, { border: it.color });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y, w: 0.07, h: 1.0, fill: { color: it.color }, line: { color: it.color } });
    s.addText(it.title, { x: 0.65, y: y + 0.1, w: 3.5, h: 0.5, fontSize: 16, bold: true, color: it.color, margin: 0 });
    s.addText(it.desc, { x: 0.65, y: y + 0.55, w: 8.7, h: 0.4, fontSize: 13, color: C.textMid, margin: 0 });
  });
  addKeyMessage(s, "친환경 럭셔리 투어는 경험 사치와 기후 행동이 만나는 고마진 신시장이다.");
  addSlideNum(s, 34);
}

// SLIDE 35: 인간 증명
{
  const s = addLightSlide();
  addSlideTitle(s, "인간 증명: AI 시대의 역설적 프리미엄");
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.1, w: 4.2, h: 3.5, fill: { color: C.darkBg }, line: { color: C.darkBg } });
  s.addText("인간\n증명", { x: 0.4, y: 1.8, w: 4.2, h: 1.8, fontSize: 52, bold: true, color: C.gold, align: "center", margin: 0 });
  s.addText("Human Proof", { x: 0.4, y: 3.8, w: 4.2, h: 0.5, fontSize: 12, color: C.mintLight, align: "center", margin: 0 });
  s.addText(makeBullets([
    "AI와 봇이 범람하는 시대에 '진짜 인간'의 경험이 가장 희소한 가치",
    "오프라인 아날로그 연대와 진정성 있는 관계 맺기가 최고 프리미엄",
    "AI가 대체할 수 없는 인간 중심 기후 행동 프로젝트가 차별화 요소",
  ], { fontSize: 15 }), { x: 4.9, y: 1.3, w: 4.8, h: 3.0 });
  addKeyMessage(s, "AI 시대에 가장 비싼 것은 '진짜 인간'의 경험이다—오프라인 기후 연대가 최고의 프리미엄이 된다.");
  addSlideNum(s, 35);
}

// SLIDE 36: 오프라인 기후 커뮤니티
{
  const s = addLightSlide();
  addSlideTitle(s, "오프라인 기후 커뮤니티: 인간 증명의 실전 모델");
  s.addText(makeBullets([
    "팬들이 직접 만나 연대하고 목소리 내는 기후 행동 프로젝트 설계",
    "온라인 서명을 넘어 오프라인 집회·워크샵·캠페인으로의 진화",
    "기업이 지원하는 오프라인 기후 커뮤니티가 가장 강력한 브랜드 자산",
  ], { fontSize: 17, spaceAfter: 16 }), { x: 0.4, y: 1.1, w: 9.2, h: 3.5 });
  addKeyMessage(s, "기업이 설계하고 지원하는 오프라인 기후 커뮤니티가 AI 시대 최강의 브랜드 자산이다.");
  addSlideNum(s, 36);
}

// SLIDE 37: CES 2026
{
  const s = addLightSlide();
  addSlideTitle(s, "CES 2026과 ESG: 지속가능성이 혁신 기술이 되다");
  s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y: 1.1, w: 9.2, h: 1.0, fill: { color: C.cream }, line: { color: C.divider } });
  s.addText("CES 2026에서 지속가능성 기술이 AI·자율주행과 나란히 핵심 혁신 카테고리로 선정", {
    x: 0.6, y: 1.2, w: 8.8, h: 0.7, fontSize: 15, bold: true, color: C.textDark, margin: 0,
  });
  s.addText(makeBullets([
    "글로벌 기업들이 CES에서 지속가능성을 핵심 혁신 기술로 발표",
    "태양광 나무 · 해양 폐기물 재활용 등 ESG 기술이 첨단 기술과 동급 대우",
    "ESG는 더 이상 CSR 부서 업무가 아닌 기술 혁신의 핵심 영역",
  ], { fontSize: 16 }), { x: 0.4, y: 2.3, w: 9.2, h: 2.3 });
  addKeyMessage(s, "CES가 ESG를 혁신 기술로 인정한 순간, 지속가능성은 선택이 아닌 기술 경쟁의 핵심이 되었다.");
  addSlideNum(s, 37);
}

// SLIDE 38: ESG 의무화
{
  const s = addLightSlide();
  addSlideTitle(s, "ESG 의무화: 2030년 데드라인이 만드는 선제 기회");
  addBigStat(s, 0.4, 1.1, 4.0, "2030", "국내 상장사 ESG 공시 의무화", C.gold);
  s.addText(makeBullets([
    "선제적 탄소 감축 로드맵 공개가 투자자·소비자 신뢰를 동시 확보",
    "ESG 의무화 이전 자발적 공개 기업이 시장에서 프리미엄 평가 획득",
    "CES 글로벌 흐름이 국내 규제로도 구체화되고 있음",
  ], { fontSize: 15 }), { x: 4.7, y: 1.1, w: 5.0, h: 3.5 });
  addKeyMessage(s, "2030년 ESG 의무화 데드라인은 지금 행동하는 기업에게 선점 기회를, 미루는 기업에게 위기를 준다.");
  addSlideNum(s, 38);
}

// SLIDE 39: 섹션 4 종합
{
  const s = addLightSlide();
  addSlideTitle(s, "섹션 4 종합: 세 가지 기회의 교차점");
  const intersections = [
    { label: "경험 사치 × 인간 증명", desc: "저탄소 오프라인 경험 비즈니스의 황금 교차점", colorA: C.sage, colorB: C.mint },
    { label: "인간 증명 × ESG 의무화", desc: "진정성 있는 ESG 스토리텔링의 차별화 기회", colorA: C.mint, colorB: C.gold },
    { label: "경험 사치 × ESG 의무화", desc: "친환경 럭셔리 경험이 ESG 실적이 되는 모델", colorA: C.sage, colorB: C.gold },
  ];
  intersections.forEach((it, i) => {
    const y = 1.15 + i * 1.2;
    addCard(s, 0.4, y, 9.2, 1.0, {});
    s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y, w: 0.07, h: 1.0, fill: { color: it.colorA }, line: { color: it.colorA } });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.47, y, w: 0.07, h: 1.0, fill: { color: it.colorB }, line: { color: it.colorB } });
    s.addText(it.label, { x: 0.75, y: y + 0.1, w: 4.0, h: 0.5, fontSize: 16, bold: true, color: C.textDark, margin: 0 });
    s.addText(it.desc, { x: 0.75, y: y + 0.58, w: 8.6, h: 0.4, fontSize: 13, color: C.textGray, margin: 0 });
  });
  addKeyMessage(s, "경험 사치·인간 증명·ESG 의무화 세 가지가 교차하는 지점이 2026년 가장 큰 기회의 무대다.");
  addSlideNum(s, 39);
}

// SLIDE 40: 전환
{
  const s = addDarkSlide();
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.12, fill: { color: C.sage }, line: { color: C.sage } });
  s.addText("기회를 현실로 만들려면", {
    x: 0.5, y: 1.0, w: 9, h: 1.0, fontSize: 38, bold: true, color: C.white, align: "center", margin: 0,
  });
  s.addText("분석에서 실행으로: 기업이 지금 당장 시작해야 할 3가지", {
    x: 0.5, y: 2.3, w: 9, h: 0.7, fontSize: 18, color: C.mintLight, align: "center", margin: 0,
  });
  s.addText("다음 섹션: 실행 전략 제언 — 구체적이고 실행 가능한 로드맵", {
    x: 0.5, y: 3.3, w: 9, h: 0.6, fontSize: 14, color: C.gold, align: "center", margin: 0,
  });
  addSlideNum(s, 40);
}

// ═══════════════════════════════════════════════════════════════
// SECTION 5
// ═══════════════════════════════════════════════════════════════
addSectionCover(5, "실행 전략 제언:\n기업이 지금 해야 할 3가지", "슬라이드 41~50");

// SLIDE 41: 실행 전략 개요
{
  const s = addLightSlide();
  addSlideTitle(s, "실행 전략 섹션 개요: 3가지 즉각 실행 과제");
  const strats = [
    { n: "전략 1", title: "RE100 + 탄소 투명성 확보", desc: "플랫폼과 기업의 공통 과제", color: C.forestGrn },
    { n: "전략 2", title: "경험 비즈니스 피벗", desc: "실물 굿즈에서 친환경 경험으로", color: C.mint },
    { n: "전략 3", title: "팬덤과의 ESG 협력 생태계", desc: "감시자를 파트너로", color: C.gold },
  ];
  strats.forEach((st, i) => {
    const y = 1.15 + i * 1.3;
    addCard(s, 0.4, y, 9.2, 1.1, { border: st.color });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y, w: 1.8, h: 1.1, fill: { color: st.color }, line: { color: st.color } });
    s.addText(st.n, { x: 0.4, y: y + 0.1, w: 1.8, h: 0.5, fontSize: 14, bold: true, color: C.white, align: "center", margin: 0 });
    s.addText(st.title, { x: 2.4, y: y + 0.1, w: 5.5, h: 0.5, fontSize: 20, bold: true, color: st.color, margin: 0 });
    s.addText(st.desc, { x: 2.4, y: y + 0.65, w: 6.8, h: 0.38, fontSize: 13, color: C.textGray, margin: 0 });
  });
  addKeyMessage(s, "3가지 전략의 동시 실행이 2026년 기후 콘텐츠 시장의 승자를 결정한다.");
  addSlideNum(s, 41);
}

// SLIDE 42: 전략 1
{
  const s = addLightSlide();
  addSlideTitle(s, "전략 1: RE100 + 탄소 투명성 로드맵 즉각 공개");
  s.addText(makeBullets([
    "넷제로 목표 연도만이 아닌 연간 중간 목표와 실적을 정기 공개",
    "55g CO₂ 같은 소비자가 이해할 수 있는 구체적 수치로 탄소 정보 제공",
    "RE100 달성 전이라도 현재 진행 상황의 투명한 공개가 신뢰 구축의 핵심",
  ], { fontSize: 17, spaceAfter: 16 }), { x: 0.4, y: 1.1, w: 9.2, h: 3.5 });
  addKeyMessage(s, "RE100 달성보다 RE100 여정의 투명한 공개가 소비자 신뢰를 먼저 확보한다.");
  addSlideNum(s, 42);
}

// SLIDE 43: RE100 로드맵
{
  const s = addLightSlide();
  addSlideTitle(s, "RE100 실행 로드맵: 단계별 접근법");
  const steps = [
    { phase: "1단계\n즉시", items: "현재 탄소 배출량 측정·공개\n감축 목표 수립", color: C.gold },
    { phase: "2단계\n1~2년", items: "클라우드 이전 · 고효율 데이터센터\n재생에너지 구매 시작", color: C.mint },
    { phase: "3단계\n3~5년", items: "RE100 인증 획득\n공급망 전반 탄소 감축 확대", color: C.forestGrn },
  ];
  steps.forEach((st, i) => {
    const x = 0.4 + i * 3.15;
    addCard(s, x, 1.1, 2.85, 3.6, { border: st.color });
    s.addShape(pres.shapes.RECTANGLE, { x, y: 1.1, w: 2.85, h: 1.0, fill: { color: st.color }, line: { color: st.color } });
    s.addText(st.phase, { x: x + 0.1, y: 1.15, w: 2.6, h: 0.85, fontSize: 18, bold: true, color: C.white, align: "center", margin: 0 });
    s.addText(st.items, { x: x + 0.15, y: 2.25, w: 2.55, h: 2.2, fontSize: 14, color: C.textDark, margin: 0 });
  });
  addKeyMessage(s, "RE100은 목적지가 아닌 여정이다—단계적 로드맵과 투명한 중간 성과 공개가 핵심이다.");
  addSlideNum(s, 43);
}

// SLIDE 44: 전략 2
{
  const s = addLightSlide();
  addSlideTitle(s, "전략 2: 경험 비즈니스 피벗 실행 계획");
  s.addText(makeBullets([
    "기존 굿즈·앨범 매출의 일부를 저탄소 오프라인 경험 상품으로 대체",
    "저탄소 콘서트·친환경 투어·기후 토크 등 경험 포트폴리오 다각화",
    "경험 상품의 탄소 발자국을 실시간 측정·공개하는 시스템 구축",
  ], { fontSize: 17, spaceAfter: 16 }), { x: 0.4, y: 1.1, w: 9.2, h: 3.5 });
  addKeyMessage(s, "경험 비즈니스 피벗은 탄소 감소와 매출 성장을 동시에 달성하는 기후 비즈니스의 핵심 전략이다.");
  addSlideNum(s, 44);
}

// SLIDE 45: 경험 비즈니스 수익화
{
  const s = addLightSlide();
  addSlideTitle(s, "경험 비즈니스의 수익화 모델");
  s.addText(makeBullets([
    "프리미엄 가격 책정: 경험의 희소성과 친환경 가치로 정당화",
    "구독형 멤버십: 연간 저탄소 경험 패키지로 안정적 수익 구조 확보",
    "팬덤 참여형 ESG 이벤트로 브랜드 충성도와 소셜 바이럴 동시 창출",
  ], { fontSize: 17, spaceAfter: 16 }), { x: 0.4, y: 1.1, w: 9.2, h: 3.5 });
  addKeyMessage(s, "경험 비즈니스는 낮은 탄소·높은 충성도·안정적 수익을 동시에 갖춘 최적 모델이다.");
  addSlideNum(s, 45);
}

// SLIDE 46: 전략 3
{
  const s = addLightSlide();
  addSlideTitle(s, "전략 3: 팬덤 ESG 협력 생태계 구축");
  s.addText(makeBullets([
    "팬덤을 ESG 정책 설계 단계부터 참여시키는 공동 창조 프로세스",
    "팬덤의 기후 캠페인을 기업 공식 ESG 활동으로 인정·지원·증폭",
    "팬덤 기여 ESG 성과를 데이터로 측정하고 투명하게 공유",
  ], { fontSize: 17, spaceAfter: 16 }), { x: 0.4, y: 1.1, w: 9.2, h: 3.5 });
  addKeyMessage(s, "팬덤을 ESG 공동 설계자로 만드는 기업은 홍보대사·기후 행동·그린워싱 방패를 한번에 얻는다.");
  addSlideNum(s, 46);
}

// SLIDE 47: 팬덤 협력 실행 단계
{
  const s = addLightSlide();
  addSlideTitle(s, "팬덤 협력 생태계 구축 실행 단계");
  const phases = [
    { label: "즉시", item: "팬덤 기후 행동 리더와 정기적 소통 채널 개설", color: C.gold },
    { label: "단기", item: "팬덤 제안을 반영한 ESG 캠페인 공동 기획 및 실행", color: C.mint },
    { label: "중장기", item: "팬덤 참여 ESG 성과를 연간 보고서에 포함하여 공식화", color: C.forestGrn },
  ];
  phases.forEach((p, i) => {
    const y = 1.15 + i * 1.2;
    addCard(s, 0.4, y, 9.2, 1.0, { border: p.color });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y, w: 1.4, h: 1.0, fill: { color: p.color }, line: { color: p.color } });
    s.addText(p.label, { x: 0.4, y: y + 0.2, w: 1.4, h: 0.6, fontSize: 18, bold: true, color: C.white, align: "center", margin: 0 });
    s.addText(p.item, { x: 2.0, y: y + 0.2, w: 7.4, h: 0.6, fontSize: 15, color: C.textDark, margin: 0 });
  });
  addKeyMessage(s, "팬덤 협력은 이벤트가 아닌 지속적 관계—소통 채널 개설이 첫 번째 실행 과제다.");
  addSlideNum(s, 47);
}

// SLIDE 48: 통합 로드맵
{
  const s = addLightSlide();
  addSlideTitle(s, "3가지 전략의 통합 실행 로드맵");
  const roadmap = [
    { timeline: "즉시 실행", items: "탄소 현황 공개 + 팬덤 소통 채널 개설 + 경험 상품 기획 착수", color: C.gold },
    { timeline: "6개월 내", items: "RE100 중간 목표 발표 + 첫 저탄소 오프라인 이벤트 실행", color: C.mint },
    { timeline: "1년 내", items: "RE100 1단계 달성 + 팬덤 공동 ESG 캠페인 + 경험 멤버십 론칭", color: C.forestGrn },
  ];
  roadmap.forEach((r, i) => {
    const y = 1.15 + i * 1.2;
    addCard(s, 0.4, y, 9.2, 1.0, { border: r.color });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y, w: 1.8, h: 1.0, fill: { color: r.color }, line: { color: r.color } });
    s.addText(r.timeline, { x: 0.4, y: y + 0.15, w: 1.8, h: 0.7, fontSize: 15, bold: true, color: C.white, align: "center", margin: 0 });
    s.addText(r.items, { x: 2.4, y: y + 0.2, w: 7.0, h: 0.6, fontSize: 14, color: C.textDark, margin: 0 });
  });
  addKeyMessage(s, "3가지 전략의 통합 실행이 개별 실행보다 훨씬 강력한 ESG 브랜드 가치를 만든다.");
  addSlideNum(s, 48);
}

// SLIDE 49: 전체 요약
{
  const s = addLightSlide();
  addSlideTitle(s, "전체 리포트 요약: 5가지 핵심 인사이트");
  const insights = [
    { sec: "S1", msg: "기후 소비자", detail: "윤리 + 실용주의 결합—Z세대 62%가 ESG 브랜드 선택" },
    { sec: "S2", msg: "플랫폼", detail: "55g CO₂ 해결 위해 RE100 + AI 제로 클릭 최적화 필수" },
    { sec: "S3", msg: "팬덤", detail: "수만 명 기후 행동 조직—그린워싱 감시자이자 변화의 주체" },
    { sec: "S4", msg: "기회", detail: "경험 사치·인간 증명·ESG 의무화 교차점이 2026년 핵심 시장" },
    { sec: "S5", msg: "실행", detail: "RE100 공개 + 경험 피벗 + 팬덤 협력—3가지를 통합 실행해야" },
  ];
  insights.forEach((ins, i) => {
    const y = 1.1 + i * 0.82;
    const colors = [C.forestGrn, C.mint, C.sage, C.gold, C.forestGrn];
    s.addShape(pres.shapes.RECTANGLE, { x: 0.4, y, w: 0.7, h: 0.68, fill: { color: colors[i] }, line: { color: colors[i] } });
    s.addText(ins.sec, { x: 0.4, y: y + 0.05, w: 0.7, h: 0.55, fontSize: 14, bold: true, color: C.white, align: "center", margin: 0 });
    s.addText(ins.msg, { x: 1.25, y: y + 0.05, w: 2.0, h: 0.55, fontSize: 16, bold: true, color: colors[i], margin: 0 });
    s.addText(ins.detail, { x: 3.4, y: y + 0.1, w: 6.3, h: 0.5, fontSize: 13, color: C.textMid, margin: 0 });
  });
  addKeyMessage(s, "2026년 기후 콘텐츠 시장의 승자는 진정성 있는 ESG 실행력과 오프라인 경험 커뮤니티를 동시에 갖춘 기업이다.");
  addSlideNum(s, 49);
}

// SLIDE 50: 클로징 CTA
{
  const s = addDarkSlide();
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.12, fill: { color: C.gold }, line: { color: C.gold } });
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.5, w: 10, h: 0.12, fill: { color: C.gold }, line: { color: C.gold } });

  s.addText("오늘 이 자리에서 결정하십시오", {
    x: 0.5, y: 0.5, w: 9, h: 1.0, fontSize: 34, bold: true, color: C.white, align: "center", margin: 0,
  });

  s.addShape(pres.shapes.RECTANGLE, {
    x: 1.0, y: 1.7, w: 8.0, h: 1.6,
    fill: { color: C.forestGrn }, line: { color: C.gold, width: 2 },
  });
  s.addText("지금 당장 해야 할 한 가지:\n자사의 현재 탄소 배출량을 측정하고 공개 선언을 준비하라", {
    x: 1.2, y: 1.8, w: 7.6, h: 1.3, fontSize: 18, bold: true, color: C.gold, align: "center", margin: 0,
  });

  s.addText("RE100 여정을 시작하는 기업이 소비자 신뢰와 시장 선점 기회를 먼저 가져간다", {
    x: 0.5, y: 3.55, w: 9, h: 0.6, fontSize: 15, color: C.mintLight, align: "center", margin: 0,
  });
  s.addShape(pres.shapes.RECTANGLE, { x: 3.5, y: 4.3, w: 3.0, h: 0.65, fill: { color: C.gold }, line: { color: C.gold } });
  s.addText("골든타임은 2026년 지금이다", {
    x: 3.5, y: 4.3, w: 3.0, h: 0.65, fontSize: 16, bold: true, color: C.darkBg, align: "center", margin: 0,
  });
  addSlideNum(s, 50);
}

// ═══════════════════════════════════════════════════════════════
// SAVE
// ═══════════════════════════════════════════════════════════════
const outPath = `${process.env.HOME}/research-output/2026-기후-콘텐츠-소비자-동향/04_presentation_draft.pptx`;
pres.writeFile({ fileName: outPath })
  .then(() => console.log(`✅ PPTX saved: ${outPath}`))
  .catch(e => { console.error("❌ Error:", e); process.exit(1); });
