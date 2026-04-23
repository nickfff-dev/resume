from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

W, H = A4  # 595.27 x 841.89 pt

# ─── COLORS ───
C_BG       = HexColor('#0f0f0f')
C_SIDEBAR  = HexColor('#161616')
C_ACCENT   = HexColor('#c8ff3e')
C_WHITE    = HexColor('#f0ece4')
C_MUTED    = HexColor('#999999')
C_DIM      = HexColor('#555555')
C_RULE     = HexColor('#2a2a2a')
C_TAG_BG   = HexColor('#1e1e1e')

# ─── LAYOUT ───
SIDEBAR_W  = 175
MAIN_X     = SIDEBAR_W + 28
MAIN_W     = W - MAIN_X - 28
PAD        = 22

def draw_resume(filename):
    c = canvas.Canvas(filename, pagesize=A4)

    # ── Full background ──
    c.setFillColor(C_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ── Sidebar background ──
    c.setFillColor(C_SIDEBAR)
    c.rect(0, 0, SIDEBAR_W, H, fill=1, stroke=0)

    # ── Sidebar accent bar ──
    c.setFillColor(C_ACCENT)
    c.rect(0, 0, 3, H, fill=1, stroke=0)

    # ─────────────────────────────────
    #  HEADER BLOCK (spans full width)
    # ─────────────────────────────────
    header_h = 120
    c.setFillColor(C_SIDEBAR)
    c.rect(0, H - header_h, W, header_h, fill=1, stroke=0)

    # Accent bar on top of header
    c.setFillColor(C_ACCENT)
    c.rect(0, H - 3, W, 3, fill=1, stroke=0)

    # Name
    c.setFillColor(C_WHITE)
    c.setFont('Helvetica-Bold', 32)
    c.drawString(PAD + 3, H - 50, 'NICKSON')

    # Accent dot + last initial
    c.setFillColor(C_ACCENT)
    c.setFont('Helvetica-Bold', 32)
    name_w = c.stringWidth('NICKSON', 'Helvetica-Bold', 32)
    c.drawString(PAD + 3 + name_w + 6, H - 50, '.')

    # Title
    c.setFillColor(C_MUTED)
    c.setFont('Helvetica', 11)
    c.drawString(PAD + 3, H - 68, 'SOFTWARE ENGINEER  ·  FRONTEND, BACKEND & CLOUD SYSTEMS')

    # Thin rule
    c.setStrokeColor(C_RULE)
    c.setLineWidth(0.5)
    c.line(PAD, H - 80, W - PAD, H - 80)

    # Contact row
    contacts = [
        ('Email', 'qendev87@gmail.com'),
        ('GitHub', 'github.com/nickfff-dev'),
        ('Phone', '+254 11 322 3234'),
    ]
    cx = PAD + 3
    for label, val in contacts:
        c.setFillColor(C_DIM)
        c.setFont('Helvetica', 7.5)
        c.drawString(cx, H - 96, label.upper())
        c.setFillColor(C_MUTED)
        c.setFont('Helvetica', 9)
        c.drawString(cx, H - 107, val)
        cx += (W - PAD * 2) / 3

    # ─────────────────────────────────
    #  SIDEBAR CONTENT
    # ─────────────────────────────────
    sy = H - header_h - 28

    def sidebar_section(title, items, y, item_font=8.5):
        """Draw a sidebar section. Returns new y position."""
        # Section label
        c.setFillColor(C_ACCENT)
        c.setFont('Helvetica-Bold', 7.5)
        c.drawString(PAD, y, title.upper())
        y -= 10
        c.setStrokeColor(HexColor('#2d2d2d'))
        c.setLineWidth(0.4)
        c.line(PAD, y, SIDEBAR_W - PAD, y)
        y -= 13
        for item in items:
            if isinstance(item, tuple):
                # (bold_label, normal_text)
                c.setFillColor(C_WHITE)
                c.setFont('Helvetica-Bold', item_font)
                bw = c.stringWidth(item[0], 'Helvetica-Bold', item_font)
                c.drawString(PAD, y, item[0])
                c.setFillColor(C_MUTED)
                c.setFont('Helvetica', item_font - 0.5)
                c.drawString(PAD + bw + 3, y, item[1])
            elif item.startswith('__sub__'):
                text = item[7:]
                c.setFillColor(C_DIM)
                c.setFont('Helvetica', item_font - 1.5)
                c.drawString(PAD + 8, y, text)
            else:
                c.setFillColor(C_MUTED)
                c.setFont('Helvetica', item_font)
                c.drawString(PAD + 4, y, '–  ' + item)
            y -= 14
        return y - 6

    # Skills
    sy = sidebar_section('Core Skills', [
        'Node.js / Express',
        'Python / Flask',
        'Rust  ·  C',
        'React / TypeScript',
        'REST API Design',
        'System Architecture',
    ], sy)

    sy = sidebar_section('DevOps & Cloud', [
        'Docker / Kubernetes',
        'AWS  ·  GCP  ·  DigitalOcean',
        'GitHub Actions',
        'Jenkins / GitLab CI',
        'Ansible / Puppet / Chef',
        'Nginx / HAProxy',
    ], sy)

    sy = sidebar_section('Data & Storage', [
        'PostgreSQL / MySQL',
        'MongoDB / Redis',
        'SQLAlchemy',
    ], sy)

    sy = sidebar_section('Platforms', [
        'WordPress (advanced)',
        'Elementor / WooCommerce',
        'Custom PHP / CPTs',
    ], sy)

    sy = sidebar_section('Education', [
        ('ALX / Holberton', ''),
        '__sub__Software Engineering',
        '__sub__Backend Track',
        '__sub__Feb 2023 – Dec 2024',
    ], sy)

    # ─────────────────────────────────
    #  MAIN CONTENT
    # ─────────────────────────────────
    my = H - header_h - 22

    def draw_section_title(title, y):
        c.setFillColor(C_ACCENT)
        c.setFont('Helvetica-Bold', 7.5)
        c.drawString(MAIN_X, y, title.upper())
        y -= 9
        c.setStrokeColor(C_RULE)
        c.setLineWidth(0.5)
        c.line(MAIN_X, y, MAIN_X + MAIN_W, y)
        return y - 14

    def draw_exp(role, company, period, bullets, y, main_x=MAIN_X, main_w=MAIN_W):
        c.setFillColor(C_WHITE)
        c.setFont('Helvetica-Bold', 10.5)
        c.drawString(main_x, y, role)

        # Right-align period
        c.setFillColor(C_DIM)
        c.setFont('Helvetica', 8)
        pw = c.stringWidth(period, 'Helvetica', 8)
        c.drawString(main_x + main_w - pw, y, period)

        y -= 13
        c.setFillColor(C_MUTED)
        c.setFont('Helvetica-Bold', 8.5)
        c.drawString(main_x, y, company)
        y -= 14

        for bullet in bullets:
            # Bullet marker
            c.setFillColor(C_ACCENT)
            c.setFont('Helvetica-Bold', 8)
            c.drawString(main_x, y, '→')
            # Wrap long bullet text
            c.setFillColor(HexColor('#aaaaaa'))
            c.setFont('Helvetica', 8.5)
            max_w = main_w - 14
            words = bullet.split()
            line = ''
            first = True
            bx = main_x + 12
            for word in words:
                test = line + (' ' if line else '') + word
                if c.stringWidth(test, 'Helvetica', 8.5) > max_w:
                    c.drawString(bx, y, line)
                    y -= 11
                    line = word
                    if first:
                        first = False
                        bx = main_x + 12
                else:
                    line = test
            if line:
                c.drawString(bx, y, line)
                y -= 11
            y -= 3
        return y - 5

    def draw_project(name, tech, desc, links, y):
        c.setFillColor(C_WHITE)
        c.setFont('Helvetica-Bold', 9.5)
        c.drawString(MAIN_X, y, name)

        # Tech tags inline
        tx = MAIN_X + c.stringWidth(name, 'Helvetica-Bold', 9.5) + 8
        for t in tech:
            tw = c.stringWidth(t, 'Helvetica', 7) + 8
            c.setFillColor(C_TAG_BG)
            c.roundRect(tx - 1, y - 2, tw + 2, 11, 2, fill=1, stroke=0)
            c.setFillColor(C_DIM)
            c.setFont('Helvetica', 7)
            c.drawString(tx + 3, y + 1, t)
            tx += tw + 4

        y -= 12
        # Description — wrap
        c.setFillColor(HexColor('#aaaaaa'))
        c.setFont('Helvetica', 8.5)
        words = desc.split()
        line = ''
        for word in words:
            test = line + (' ' if line else '') + word
            if c.stringWidth(test, 'Helvetica', 8.5) > MAIN_W:
                c.drawString(MAIN_X, y, line)
                y -= 11
                line = word
            else:
                line = test
        if line:
            c.drawString(MAIN_X, y, line)
            y -= 11

        # Links
        if links:
            c.setFillColor(C_ACCENT)
            c.setFont('Helvetica', 7.5)
            lx = MAIN_X
            for ltext, _ in links:
                c.drawString(lx, y, ltext)
                lx += c.stringWidth(ltext, 'Helvetica', 7.5) + 14
            y -= 10
        return y - 5

    # ── Summary ──
    c.setFillColor(HexColor('#aaaaaa'))
    c.setFont('Helvetica', 9)
    summary = ('Backend-heavy full-stack engineer with 7+ years building production systems — from '
               'scalable APIs and cloud infrastructure to payment integrations and automation pipelines. '
               'Proven at reducing costs, shipping reliably, and owning systems end-to-end.')
    words = summary.split()
    line = ''
    for word in words:
        test = line + (' ' if line else '') + word
        if c.stringWidth(test, 'Helvetica', 9) > MAIN_W:
            c.drawString(MAIN_X, my, line)
            my -= 12
            line = word
        else:
            line = test
    if line:
        c.drawString(MAIN_X, my, line)
        my -= 20

    # ── Experience ──
    my = draw_section_title('Experience', my)

    my = draw_exp(
        'Lead Engineer', 'E.T. Technology Enterprises  ·  Remote', '2022 – 2025',
        [
            'Led development, deployment & maintenance of multiple production web apps and cloud servers.',
            'Integrated open-source tools into workflows, cutting software licensing costs by 50%.',
            'Architected CI/CD pipelines (GitHub Actions, Jenkins) enabling zero-downtime deployments.',
            'Managed Kubernetes clusters on AWS and DigitalOcean; containerised all core services with Docker.',
            'Mentored team members on system tooling, improving internal ICT adoption and efficiency.',
        ], my)

    my = draw_exp(
        'Freelance Full-Stack Developer', 'Independent', '2018 – Present',
        [
            'Shipped custom web apps, REST APIs, and WordPress solutions for clients across multiple industries.',
            'Delivered advanced WordPress builds: custom CPTs, WooCommerce, referral systems, and SEO.',
            'Collaborated with distributed teams to deploy cloud-based solutions on time and within scope.',
        ], my)

    my = draw_exp(
        'Senior Content Officer', 'Jumia Kenya / Uganda', '2016 – 2025',
        [
            'Managed product display across high-traffic e-commerce frontend; ensured accuracy at scale.',
            'Built advanced Excel KPI trackers used across departments for reporting and project progress.',
        ], my)

    my -= 4

    # ── Selected Projects ──
    my = draw_section_title('Selected Projects', my)

    my = draw_project(
        'Files Manager API',
        ['Node.js', 'Redis', 'MongoDB', 'Bull'],
        'Production file platform with background queues, token auth, thumbnail generation, and permissions.',
        [('github.com/nickfff-dev/alx-files_manager', '')], my)

    my = draw_project(
        'EasyBets',
        ['React', 'Node.js', 'Payments'],
        'Sports betting platform with real-time odds, user accounts, and secure transaction flows.',
        [('easybets.vercel.app', '')], my)

    my = draw_project(
        'Catcha Flight',
        ['Python', 'API integration', 'Caching'],
        'Flight price aggregator scanning multiple carriers for cheapest routes with smart date-range caching.',
        [('catcha-flight.vercel.app', '')], my)

    my = draw_project(
        'Grant Tracker',
        ['React', 'Node.js', 'PostgreSQL'],
        'Grant lifecycle management system replacing spreadsheet workflows for nonprofits and institutions.',
        [('granttrackerv1.vercel.app', '')], my)

    my = draw_project(
        'AirBnB Clone v2',
        ['Python', 'Flask', 'MySQL', 'HAProxy'],
        'Full-stack AirBnB replica with custom storage engine, RESTful API, and HAProxy load balancing.',
        [('github.com/nickfff-dev/AirBnB_clone_v2', '')], my)

    # ── Footer rule ──
    c.setStrokeColor(C_RULE)
    c.setLineWidth(0.4)
    c.line(MAIN_X, 28, MAIN_X + MAIN_W, 28)
    c.setFillColor(C_DIM)
    c.setFont('Helvetica', 7)
    c.drawString(MAIN_X, 18, 'github.com/nickfff-dev  ·  qendev87@gmail.com  ·  +254 11 322 3234')

    c.save()
    print(f"Resume saved to {filename}")

draw_resume('nickson_resume.pdf')