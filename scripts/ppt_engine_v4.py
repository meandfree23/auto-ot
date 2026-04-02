import os
import sys
import re
import json
import argparse
from pathlib import Path

# --- Path Injection for Internal Modules ---
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# --- HTML TEMPLATE (V17.0 Topic-First Intelligence - Premium Dashboard) ---
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="ko" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[[TITLE]]</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700;800;900&family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        'brand-accent': '[[BRAND_HEX]]',
                        'glass-bg': 'rgba(255, 255, 255, 0.05)',
                        'glass-border': 'rgba(255, 255, 255, 0.1)',
                    },
                    fontFamily: { sans: ['Inter', 'Noto Sans KR', 'sans-serif'] },
                    boxShadow: { 'glow': '0 0 40px -10px rgba([[BRAND_RGB]], 0.3)' }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #000000;
            color: #f5f5f7;
            background-image: radial-gradient(circle at 15% 50%, rgba([[BRAND_RGB]], 0.15), transparent 25%), radial-gradient(circle at 85% 30%, rgba(255, 255, 255, 0.05), transparent 25%);
            background-attachment: fixed;
            -webkit-font-smoothing: antialiased;
        }
        .glass-card {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 1.5rem;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .glass-card:hover {
            transform: translateY(-5px) scale(1.01);
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.2);
            box-shadow: var(--glow);
        }
        .hero-title {
            font-size: clamp(3rem, 6vw, 5.5rem);
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1.1;
            background: linear-gradient(180deg, #fff 0%, #a1a1a6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .bento-grid { display: grid; grid-template-columns: 1fr; gap: 1.5rem; }
        @media (min-width: 1024px) { .bento-grid { grid-template-columns: repeat(3, 1fr); } .span-2 { grid-column: span 2; } .span-3 { grid-column: span 3; } }
        .animated-entry { opacity: 0; transform: translateY(40px); filter: blur(10px); }
        .visible { opacity: 1; transform: translateY(0); filter: blur(0); transition: all 1s cubic-bezier(0.16, 1, 0.3, 1); }
    </style>
</head>
<body class="antialiased min-h-screen">
    <header class="fixed top-0 w-full p-6 flex justify-between items-center z-50 bg-black/50 backdrop-blur-xl border-b border-white/10">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-gradient-to-br from-gray-800 to-black rounded-xl border border-white/10 flex items-center justify-center text-white shadow-glow">
                <i data-lucide="cpu" class="w-5 h-5 text-brand-accent"></i>
            </div>
            <div class="flex flex-col">
                <span class="font-bold tracking-tight text-xl leading-none text-white">Antigravity</span>
                <span class="text-[9px] font-medium text-gray-400 tracking-[0.2em] mt-1 uppercase">Strategic Intelligence V26.0</span>
            </div>
        </div>
    </header>
    <main class="pt-32 pb-24 px-6 md:px-12 lg:px-24 max-w-[1600px] mx-auto">
        <section class="min-h-[70vh] flex flex-col justify-center mb-20">
            <div class="inline-block mb-6 animated-entry">
                <span class="px-3 py-1 rounded-full border border-brand-accent/30 bg-brand-accent/10 text-brand-accent text-xs font-bold tracking-widest uppercase">Job ID: [[JOB_ID]]</span>
            </div>
            <h1 class="hero-title animated-entry mb-8">[[TITLE]]</h1>
            <p class="text-xl md:text-2xl font-light text-gray-400 animated-entry max-w-4xl leading-relaxed tracking-tight">
                Global market trends, gap-check risks, and high-fidelity creative blueprints synthesized for high-impact decision making.
            </p>
        </section>
        [[SLIDES_HTML]]
    </main>
    <footer class="py-12 border-t border-white/10 text-center text-gray-500 text-sm font-medium tracking-widest uppercase animated-entry">
        CONFIDENTIAL & PROPRIETARY &copy; 2026 Antigravity Intelligence
    </footer>
    <script>
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); });
        }, { threshold: 0.1, rootMargin: "0px 0px -50px 0px" });
        document.querySelectorAll('.animated-entry').forEach((el, idx) => {
            el.style.transitionDelay = `${(idx % 4) * 100}ms`;
            observer.observe(el);
        });
        lucide.createIcons();
    </script>
</body>
</html>'''


def get_dynamic_theme(title):
    themes = [
        {"name": "Apple Blue", "hex": "#0071e3", "rgb": "0, 113, 227"},
        {"name": "McKinsey Navy", "hex": "#002855", "rgb": "0, 40, 85"},
        {"name": "Hermes Orange", "hex": "#F37021", "rgb": "243, 112, 33"},
        {"name": "Forest Green", "hex": "#2e4635", "rgb": "46, 70, 53"},
        {"name": "Rose Gold", "hex": "#b76e79", "rgb": "183, 110, 121"},
        {"name": "Electric Purple", "hex": "#8a2be2", "rgb": "138, 43, 226"},
        {"name": "Lush Red", "hex": "#e63946", "rgb": "230, 57, 70"}
    ]
    
    title_lower = title.lower()
    if any(k in title_lower for k in ["테크", "it", "플랫폼", "디지털", "앱"]): return themes[0]
    if any(k in title_lower for k in ["금융", "전략", "비즈니스", "b2b"]): return themes[1]
    if any(k in title_lower for k in ["커머스", "명품", "쇼핑", "프리미엄"]): return themes[2]
    if any(k in title_lower for k in ["친환경", "환경", "자연", "에너지", "esg"]): return themes[3]
    if any(k in title_lower for k in ["뷰티", "화장품", "여성", "코스메틱"]): return themes[4]
    if any(k in title_lower for k in ["게임", "메타버스", "web3", "ai"]): return themes[5]
    if any(k in title_lower for k in ["식품", "음식", "엔터테인먼트", "f&b"]): return themes[6]
    
    idx = sum(ord(c) for c in title) % len(themes)
    return themes[idx]

def generate_html(data, output_dir, job_id):
    title = data.get("strategy_title", "Topic-First Intelligence")
    categories = data.get("categories", {})
    
    slides_html_list = []
    
    for cat_name, sections in categories.items():
        if not sections: continue
        
        slides_html_list.append(f'''
        <section class="mb-32">
            <div class="flex items-center gap-4 mb-12 animated-entry">
                <div class="h-px bg-white/20 flex-1"></div>
                <h2 class="text-2xl font-medium tracking-widest uppercase text-gray-500">{cat_name}</h2>
                <div class="h-px bg-white/20 flex-1"></div>
            </div>
            <div class="bento-grid">''')
                
        for idx, sec in enumerate(sections):
            importance = str(sec.get('importance', 'normal'))
            
            grid_class = "span-2" if importance in ["critical", "high"] or "Gap" in cat_name else ""
            if idx == 0 and len(sections) % 2 != 0: grid_class = "span-3"
            
            tag_bg = "bg-red-500/20 text-red-400 border border-red-500/30" if "Gap" in cat_name else "bg-brand-accent/20 text-brand-accent border border-brand-accent/30"
            icon = "alert-triangle" if "Gap" in cat_name else "trending-up"
            tag_name = "CRITICAL RISK" if "Gap" in cat_name else "INSIGHT"
            
            content_lines = ""
            in_table = False
            for line in sec.get('contents', []):
                if line.startswith('|'):
                    if not in_table:
                        content_lines += '<div class="overflow-x-auto my-4 w-full rounded-lg border border-white/10 bg-black/20"><table class="w-full text-left border-collapse whitespace-nowrap">'
                        in_table = True
                    if '---' in line: continue
                    cells = [c.strip() for c in line.split('|') if c.strip()]
                    if not cells: continue
                    tds = "".join([f'<td class="px-4 py-3 border-b border-white/5 text-sm text-gray-300">{c}</td>' for c in cells])
                    content_lines += f'<tr class="hover:bg-white/5 transition-colors">{tds}</tr>'
                else:
                    if in_table:
                        content_lines += '</table></div>'
                        in_table = False
                        
                    if line.startswith('![') and '](' in line:
                        m = re.search(r'\((.*?)\)', line)
                        url = m.group(1) if m else ""
                        m_alt = re.search(r'\[(.*?)\]', line)
                        alt = m_alt.group(1) if m_alt else ""
                        content_lines += f'<div class="my-5 rounded-xl overflow-hidden border border-brand-accent/20 shadow-[0_0_20px_rgba(0,113,227,0.15)] cursor-pointer transform hover:scale-[1.01] transition-all duration-300"><img src="{url}" alt="{alt}" class="w-full object-cover max-h-56 opacity-90 hover:opacity-100 transition-opacity duration-500"></div>'
                    elif line.startswith('> '):
                        content_lines += f'<blockquote class="border-l-4 border-brand-accent/80 pl-5 py-3 my-5 bg-brand-accent/10 rounded-r-lg italic text-white text-sm font-semibold tracking-tight shadow-glow leading-relaxed">{line[2:]}</blockquote>'
                    elif line.startswith('- ') or line.startswith('* '):
                        content_lines += f'<li class="flex items-start gap-4 text-sm font-medium text-gray-200 mt-3"><span class="w-[3px] h-4 bg-brand-accent/50 mt-1 shrink-0 rounded-full"></span><span class="leading-relaxed">{line[2:]}</span></li>'
                    else:
                        content_lines += f'<p class="text-sm text-gray-400 mt-3 leading-relaxed">{line}</p>'
            if in_table:
                content_lines += '</table></div>'

            slides_html_list.append(f'''
                <div class="glass-card {grid_class} p-8 md:p-10 animated-entry flex flex-col">
                    <div class="flex justify-between items-center mb-6">
                        <span class="{tag_bg} px-3 py-1 rounded-md text-[10px] font-bold tracking-widest uppercase">{tag_name}</span>
                        <i data-lucide="{icon}" class="text-gray-400 w-5 h-5"></i>
                    </div>
                    <h3 class="text-2xl font-bold mb-6 tracking-tight text-white">{sec['title']}</h3>
                    <ul class="flex-1 space-y-4">{content_lines}</ul>
                </div>''')

        slides_html_list.append('''
            </div>
        </section>''')
        
    final_html = HTML_TEMPLATE.replace('[[TITLE]]', title).replace('[[SLIDES_HTML]]', "".join(slides_html_list)).replace('[[JOB_ID]]', job_id)
    
    theme = get_dynamic_theme(title)
    final_html = final_html.replace('[[BRAND_HEX]]', theme['hex']).replace('[[BRAND_RGB]]', theme['rgb'])

    
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{job_id}_precision_report.html")
    with open(out_path, 'w', encoding='utf-8') as f: f.write(final_html)
    return out_path

def generate_strategic_base_inline(job_id):
    import re
    try:
        from scripts.antigravity_bridge import load_markdown
        summary, deep, questions = load_markdown(job_id)
    except:
        summary, deep, questions = "", "", ""
    text = (summary or "") + "\n" + (deep or "") + "\n" + (questions or "")
    
    title = f"Topic-First Intelligence: {job_id}"
    m_title = re.search(r'# \[(.+?)\] (.+)', text)
    if m_title:
        title = m_title.group(2).strip()
        
    categories = {
        "Gap Check & Risks": [],
        "Strategic Logic": [],
        "Creative & Visual": [],
        "Market Intelligence": []
    }
    
    sections = re.split(r'\n(##|###) ', text)
    for i in range(1, len(sections), 2):
        if i+1 >= len(sections): break
        h_level = sections[i]
        sec_content = sections[i+1].strip()
        lines = sec_content.split('\n')
        h2 = lines[0].strip()
        
        cat = "Market Intelligence"
        if any(k in h2 for k in ["크리에이티브", "솔루션", "Creative"]): cat = "Creative & Visual"
        elif any(k in h2 for k in ["질문", "리스크", "가정", "확인", "Risk", "Gap"]): cat = "Gap Check & Risks"
        elif any(k in h2 for k in ["전략", "Insights", "목표", "과제", "OT"]): cat = "Strategic Logic"
            
        items = [l.strip() for l in lines[1:] if l.strip()]
        
        if items:
            categories[cat].append({
                "title": h2,
                "tag": "INSIGHT",
                "contents": items[:4],
                "importance": "high" if "핵심" in h2 or "뉴스" in h2 else "normal"
            })
            
    return {"strategy_title": title, "categories": categories}

def generate_pptx(data, output_dir, job_id):
    try:
        from pptx import Presentation
        from pptx.util import Pt
        from pptx.dml.color import RGBColor
    except ImportError:
        print("[PPT Engine Error] python-pptx not installed.")
        return None
        
    master_path = os.path.join(ROOT, "templates", "premium_master.pptx")
    has_master = os.path.exists(master_path)
    try:
        if has_master:
            print(f"[PPT Engine] Loading premium custom master template: {master_path}")
            prs = Presentation(master_path)
        else:
            print("[PPT Engine] Warning: No premium_master.pptx found. Using fallback blank template.")
            prs = Presentation()
    except Exception as e:
        print(f"[PPT Engine Error] Failed to load template: {e}. Using fallback blank template.")
        prs = Presentation()
        has_master = False

    title = data.get("strategy_title", "Topic-First Intelligence Report")
    
    # 1. Main Title Slide
    layout_title = prs.slide_layouts[0] if len(prs.slide_layouts) > 0 else None
    if layout_title:
        slide = prs.slides.add_slide(layout_title)
        if slide.shapes.title:
            slide.shapes.title.text = title
            try:
                slide.shapes.title.text_frame.paragraphs[0].font.bold = True
                if not has_master:
                    slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
            except: pass
        if len(slide.placeholders) > 1:
            try:
                subtitle = slide.placeholders[1]
                subtitle.text = f"Job ID: {job_id}\nStrategic Intelligence V26.0"
                if not has_master:
                    subtitle.text_frame.paragraphs[0].font.color.rgb = RGBColor(100, 100, 100)
            except: pass
    
    # 2. Category Slides
    categories = data.get("categories", {})
    layout_content_idx = 1 if len(prs.slide_layouts) > 1 else 0
    layout_content = prs.slide_layouts[layout_content_idx] if len(prs.slide_layouts) > 0 else None
    
    if layout_content:
        for cat_name, sections in categories.items():
            if not sections: continue
            
            slide = prs.slides.add_slide(layout_content)
            if slide.shapes.title:
                slide.shapes.title.text = f"{cat_name}"
                try:
                    if not has_master:
                        slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 40, 85)
                        slide.shapes.title.text_frame.paragraphs[0].font.bold = True
                except: pass
                
            if len(slide.placeholders) > 1:
                tf = slide.placeholders[1].text_frame
                tf.clear()
                
                for sec in sections:
                    p = tf.add_paragraph()
                    p.text = f"• {sec['title']}"
                    try:
                        p.font.bold = True
                        if not has_master:
                            p.font.size = Pt(16)
                            p.font.color.rgb = RGBColor(30, 30, 30)
                    except: pass
                    
                    for line in sec.get('contents', []):
                        if line.startswith('![') and '](' in line:
                            continue # skip images for PPT layout safety
                            
                        p2 = tf.add_paragraph()
                        if line.startswith('|') and '---' not in line:
                            cells = [c.strip() for c in line.split('|') if c.strip()]
                            p2.text = "   [데이터 표] " + " | ".join(cells)
                            try:
                                if not has_master:
                                    p2.font.size = Pt(11)
                                    p2.font.color.rgb = RGBColor(100, 100, 120)
                            except: pass
                        elif line.startswith('> '):
                            p2.text = f"   (인용) {line[2:]}"
                            try:
                                if not has_master:
                                    p2.font.size = Pt(12)
                                    p2.font.bold = True
                                    p2.font.color.rgb = RGBColor(40, 40, 80)
                            except: pass
                        elif line.startswith('- ') or line.startswith('* '):
                            p2.text = f"  - {line[2:]}"
                            try:
                                if not has_master:
                                    p2.font.size = Pt(12)
                                    p2.font.color.rgb = RGBColor(80, 80, 90)
                            except: pass
                        elif '---' in line and line.startswith('|'):
                            pass
                        else:
                            p2.text = f"    {line}"
                            try:
                                if not has_master: p2.font.size = Pt(12)
                            except: pass
                    
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"{job_id}_strategic_deck.pptx")
    prs.save(out_path)
    return out_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--mode", default="standard")
    parser.add_argument("-o", "--output", default="./outputs/03_final_reports")
    args = parser.parse_args()
    
    try:
        data = generate_strategic_base_inline(args.job_id)
        
        print(f"[V25.0 Engine] Generating Premium HTML & PPTX Dashboards for {args.job_id}...")
        html_out = generate_html(data, args.output, args.job_id)
        pptx_out = generate_pptx(data, args.output, args.job_id)
        
        print(f"DONE (HTML): {html_out}")
        if pptx_out: print(f"DONE (PPTX): {pptx_out}")
        
    except Exception as e:
        print(f"[V25.0 Error] Failed: {e}")
        import traceback; traceback.print_exc()
        sys.exit(1)
