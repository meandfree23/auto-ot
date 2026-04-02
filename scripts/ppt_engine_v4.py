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
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[[TITLE]]</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700;800;900&family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'mckinsey-blue': '#002855',
                        'apple-bg': '#fbfbfd',
                        'apple-text': '#1d1d1f',
                        'apple-sub': '#86868b'
                    },
                    fontFamily: {
                        sans: ['Inter', 'Noto Sans KR', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: var(--apple-bg);
            color: var(--apple-text);
            font-family: 'Inter', 'Noto Sans KR', sans-serif;
            -webkit-font-smoothing: antialiased;
            line-height: 1.5;
        }
        .hero-title {
            font-size: clamp(3.5rem, 6vw, 6rem);
            font-weight: 800;
            letter-spacing: -0.04em;
            line-height: 1.05;
            color: #111111;
        }
        .sub-title {
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.15em;
            color: var(--apple-sub);
            text-transform: uppercase;
            margin-bottom: 2rem;
        }
        .slide-section {
            min-height: 100vh;
            padding: 180px 8% 120px 8%;
            border-bottom: 1px solid #e5e5ea;
        }
        .minimal-card {
            background: #ffffff;
            border: 1px solid #e5e5ea;
            border-radius: 1.5rem;
            padding: 2.5rem;
            transition: transform 0.4s ease, box-shadow 0.4s ease;
        }
        .minimal-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px -10px rgba(0,0,0,0.05);
        }
        .nav-link {
            color: var(--apple-sub);
            transition: color 0.2s ease;
        }
        .nav-link:hover { color: #111111; }
        .bento-grid {
            display: grid; grid-template-columns: 1fr; gap: 2rem;
        }
        @media (min-width: 1024px) {
            .bento-grid { grid-template-columns: repeat(3, 1fr); }
            .span-2 { grid-column: span 2; }
            .span-3 { grid-column: span 3; }
        }
        .animated-entry {
            opacity: 0; transform: translateY(30px);
        }
    </style>
</head>
<body class="antialiased">
    <header class="fixed top-0 w-full p-8 flex justify-between items-center z-50 bg-white/80 backdrop-blur-xl border-b border-gray-100">
        <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-black rounded-lg flex items-center justify-center text-white">
                <i data-lucide="layers" class="w-5 h-5"></i>
            </div>
            <div class="flex flex-col">
                <span class="font-bold tracking-tight text-xl leading-none">Antigravity</span>
                <span class="text-[9px] font-semibold text-apple-sub tracking-widest mt-1 uppercase">Strategic Intelligence V25.0</span>
            </div>
        </div>
        <nav class="hidden md:flex items-center gap-8 text-xs font-semibold uppercase tracking-widest">
            <a href="#Market Intelligence" class="nav-link">Market</a>
            <a href="#Strategic Logic" class="nav-link">Logic</a>
            <a href="#Creative & Visual" class="nav-link">Creative</a>
        </nav>
    </header>

    <main id="slides-wrapper">
        [[SLIDES_HTML]]
    </main>

    <script>
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const children = entry.target.querySelectorAll('.animated-entry');
                    children.forEach((child, idx) => {
                        setTimeout(() => {
                            child.style.opacity = "1";
                            child.style.transform = "translateY(0)";
                            child.style.transition = "all 1.2s cubic-bezier(0.16, 1, 0.3, 1)";
                        }, idx * 100);
                    });
                }
            });
        }, { threshold: 0.1 });
        document.querySelectorAll('.slide-section').forEach(el => observer.observe(el));
        lucide.createIcons();
    </script>
</body>
</html>"""

def generate_html(data, output_dir, job_id):
    title = data.get("strategy_title", "Topic-First Intelligence")
    categories = data.get("categories", {})
    accent_color = "#4A6741"
    
    slides_html_list = []
    
    # 1. Main Title Slide
    slides_html_list.append(f'''
    <section class="slide-section flex items-center" id="slide-intro">
        <div class="max-w-5xl w-full">
            <div class="sub-title animated-entry">Intelligence Report</div>
            <h1 class="hero-title animated-entry">{title}</h1>
            <div class="h-1 w-24 bg-mckinsey-blue mt-8 mb-12 animated-entry"></div>
            <p class="text-2xl font-light text-apple-sub animated-entry max-w-4xl leading-relaxed tracking-tight">
                Global market trends, strategic benchmarks, and high-fidelity creative blueprints synthesized for high-impact decision making.
            </p>
        </div>
    </section>''')
    
    # 2. Categorical Slides
    for cat_name, sections in categories.items():
        if not sections: continue
        
        slides_html_list.append(f'''
        <section class="slide-section" id="{cat_name}">
            <div class="max-w-7xl mx-auto w-full">
                <div class="flex items-end justify-between mb-20 animated-entry">
                    <div>
                        <div class="sub-title">Category Focus</div>
                        <h2 class="text-5xl font-black tracking-tight text-[#111]">{cat_name}</h2>
                    </div>
                </div>
                
                <div class="bento-grid">''')
                
        for idx, sec in enumerate(sections):
            importance = str(sec.get('importance', 'normal'))
            grid_class = "span-2" if importance in ["critical", "high"] else ""
            if idx == 0 and len(sections) % 2 != 0: grid_class = "span-3"
            
            tag_bg = "bg-mckinsey-blue text-white" if importance == "critical" else "bg-[#f5f5f7] text-gray-500"
            
            content_lines = "".join([f'''
                <li class="flex items-start gap-4 mb-4 text-[15px] font-medium text-[#333] tracking-tight">
                    <span class="w-[3px] h-4 bg-gray-300 mt-1 shrink-0 rounded-full"></span>
                    <span class="leading-relaxed">{line.strip()}</span>
                </li>''' for line in sec.get('contents', [])])

            slides_html_list.append(f'''
                <div class="minimal-card {grid_class} animated-entry flex flex-col">
                    <div class="flex justify-between items-center mb-6">
                        <span class="{tag_bg} px-3 py-1 rounded-md text-[10px] font-bold tracking-widest uppercase">{sec['tag']}</span>
                    </div>
                    <h3 class="text-2xl font-black mb-6 leading-snug tracking-tight text-[#111]">{sec['title']}</h3>
                    <ul class="flex-1">{content_lines}</ul>
                </div>''')

        slides_html_list.append('''
                </div>
            </div>
        </section>''')
        
    final_html = HTML_TEMPLATE.replace('[[TITLE]]', title).replace('[[SLIDES_HTML]]', "".join(slides_html_list))
    
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
            
        items = [re.sub(r'^\s*[-*]\s*', '', l.strip()) for l in lines[1:] if l.strip().startswith('-') or l.strip().startswith('*')]
        
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
        
    prs = Presentation()
    title = data.get("strategy_title", "Topic-First Intelligence Report")
    
    # 1. Main Title Slide (Minimal, highly stark)
    slide_layout_title = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout_title)
    if slide.shapes.title:
        slide.shapes.title.text = title
        slide.shapes.title.text_frame.paragraphs[0].font.bold = True
        slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0) # Black
    if len(slide.placeholders) > 1:
        subtitle = slide.placeholders[1]
        subtitle.text = f"Job ID: {job_id}\nStrategic Intelligence V25.0"
        subtitle.text_frame.paragraphs[0].font.color.rgb = RGBColor(100, 100, 100)
    
    # 2. Category Slides
    categories = data.get("categories", {})
    slide_layout_content = prs.slide_layouts[1]
    
    for cat_name, sections in categories.items():
        if not sections: continue
        
        slide = prs.slides.add_slide(slide_layout_content)
        if slide.shapes.title:
            slide.shapes.title.text = f"{cat_name}"
            # McKinsey blue title
            slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 40, 85)
            slide.shapes.title.text_frame.paragraphs[0].font.bold = True
            
        if len(slide.placeholders) > 1:
            tf = slide.placeholders[1].text_frame
            tf.clear()
            
            for sec in sections:
                p = tf.add_paragraph()
                p.text = f"• {sec['title']}"
                p.font.bold = True
                p.font.size = Pt(16)
                p.font.color.rgb = RGBColor(30, 30, 30)
                
                for line in sec.get('contents', []):
                    p2 = tf.add_paragraph()
                    p2.text = f"  - {line}"
                    p2.font.size = Pt(12)
                    p2.font.color.rgb = RGBColor(80, 80, 90)
                    
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
