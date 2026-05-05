import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ns2_infotech_backend.settings')
django.setup()

from internships.models import Module, PageSection, SectionContent


def populate_modules():
    print("🚀 Starting Module Detail Page Data Entry...")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MODULE 1: PLC & SCADA Training
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print("📦 Creating Module: PLC & SCADA Training...")
    plc = Module.objects.create(
        title="PLC & SCADA Training",
        tagline="Master PLC Programming and SCADA Systems from basics to advanced industrial applications.",
        slug="plc-scada-training",
        order=1,
    )

    # PAGE_BANNER
    PageSection.objects.create(
        module=plc, section_type='PAGE_BANNER', order=1,
        heading="PLC & SCADA Training",
        highlighted_heading="Master Course",
        subheading="Become a certified automation engineer with hands-on training on Siemens, Allen Bradley, and Mitsubishi hardware. Industry-ready curriculum designed by experts.",
        primary_button_text="Enroll Now", primary_button_url="/contact",
        secondary_button_text="Download Brochure", secondary_button_url="#brochure",
    )

    # COURSE_OVERVIEW
    overview = PageSection.objects.create(
        module=plc, section_type='COURSE_OVERVIEW', order=2,
        super_heading="COURSE OVERVIEW",
        heading="What You Will Learn in",
        highlighted_heading="PLC Programming",
        subheading="This comprehensive course covers ladder logic, structured text, function block diagrams, and real-world industrial automation scenarios. You will gain hands-on experience with multiple PLC brands used in the industry.",
        primary_button_text="View Full Syllabus", primary_button_url="#syllabus",
        overlay_title="100% Practical Training",
        overlay_description="Every student gets individual PLC hardware for practice sessions.",
    )
    SectionContent.objects.create(section=overview, order=1, title="Ladder Logic Programming", description="Master relay logic, timers, counters, and sequencing.")
    SectionContent.objects.create(section=overview, order=2, title="Structured Text & FBD", description="Learn IEC 61131-3 programming standards.")
    SectionContent.objects.create(section=overview, order=3, title="HMI Integration", description="Connect PLCs with touchscreen HMI panels.")
    SectionContent.objects.create(section=overview, order=4, title="Industrial Communication", description="Profinet, Modbus, and Ethernet/IP protocols.")

    # KEY_HIGHLIGHTS
    highlights = PageSection.objects.create(
        module=plc, section_type='KEY_HIGHLIGHTS', order=3,
        super_heading="KEY HIGHLIGHTS",
        heading="Why This Course Stands Out",
        subheading="Industry-leading features that make our PLC course the best choice for aspiring automation engineers.",
    )
    SectionContent.objects.create(section=highlights, order=1, label="1", title="5 PLC Brands Covered", description="Siemens, Allen Bradley, Mitsubishi, Delta, and Schneider.")
    SectionContent.objects.create(section=highlights, order=2, label="2", title="100% Hands-On Training", description="Individual hardware and software setup for every student.")
    SectionContent.objects.create(section=highlights, order=3, label="3", title="Industry Projects", description="Work on 3 real-world industrial automation projects.")
    SectionContent.objects.create(section=highlights, order=4, label="4", title="Placement Guarantee", description="100% placement assistance with top automation companies.")
    SectionContent.objects.create(section=highlights, order=5, label="5", title="Certified Course", description="Receive an industry-recognized certification upon completion.")
    SectionContent.objects.create(section=highlights, order=6, label="6", title="Expert Faculty", description="Learn from trainers with 10+ years of industrial experience.")

    # SUBJECTS_COVERED
    subjects = PageSection.objects.create(
        module=plc, section_type='SUBJECTS_COVERED', order=4,
        super_heading="CURRICULUM",
        heading="Subjects Covered",
        subheading="A detailed breakdown of all the topics you will master during this course.",
    )
    for i, (title, desc) in enumerate([
        ("PLC Hardware & Architecture", "Understanding CPU, I/O modules, power supply, and rack configuration."),
        ("Ladder Logic Programming", "Contacts, coils, timers, counters, comparators, and math operations."),
        ("Structured Text (ST)", "IEC 61131-3 compliant text-based programming for complex logic."),
        ("Function Block Diagram", "Graphical programming for reusable function blocks."),
        ("Analog Signal Processing", "4-20mA, 0-10V signal scaling, PID control loops."),
        ("Industrial Communication", "Profinet, Modbus TCP/RTU, Ethernet/IP, and PROFIBUS."),
        ("HMI Design & Integration", "Creating operator screens, alarms, trends, and recipe management."),
        ("Siemens TIA Portal", "Complete project development using Siemens S7-1200/1500."),
        ("Allen Bradley RSLogix", "Programming and commissioning with CompactLogix & MicroLogix."),
    ], 1):
        SectionContent.objects.create(section=subjects, order=i, title=title, description=desc)

    # ELIGIBILITY_CRITERIA
    eligibility = PageSection.objects.create(
        module=plc, section_type='ELIGIBILITY_CRITERIA', order=5,
        super_heading="ELIGIBILITY",
        heading="Who Can Enroll",
        subheading="This course is designed for a wide range of learners.",
    )
    for i, (title, desc) in enumerate([
        ("Engineering Graduates", "B.E./B.Tech in Electrical, Electronics, Instrumentation, or Mechanical."),
        ("Diploma Holders", "Diploma in Electrical, Electronics, or Instrumentation Engineering."),
        ("Working Professionals", "Engineers looking to upskill in industrial automation."),
        ("Final Year Students", "Students in their final year of engineering can also apply."),
    ], 1):
        SectionContent.objects.create(section=eligibility, order=i, title=title, description=desc)

    # FEES_BATCH_DETAILS
    fees = PageSection.objects.create(
        module=plc, section_type='FEES_BATCH_DETAILS', order=6,
        super_heading="INVESTMENT",
        heading="Fees & Batch Details",
        subheading="Flexible payment options and convenient batch timings.",
        primary_button_text="Reserve Your Seat", primary_button_url="/contact",
    )
    SectionContent.objects.create(section=fees, order=1, label="Fee", title="₹45,000", description="One-time payment with EMI options available.")
    SectionContent.objects.create(section=fees, order=2, label="Duration", title="3 Months", description="Weekday and weekend batches available.")
    SectionContent.objects.create(section=fees, order=3, label="Next Batch", title="15th June 2026", description="Limited to 15 students per batch.")
    SectionContent.objects.create(section=fees, order=4, label="Seats", title="8 Left", description="Early bird discount of 10% available.")

    # FACULTY
    faculty = PageSection.objects.create(
        module=plc, section_type='FACULTY', order=7,
        super_heading="MEET YOUR TRAINERS",
        heading="Expert Faculty",
        subheading="Learn from industry veterans with decades of real-world automation experience.",
    )
    SectionContent.objects.create(section=faculty, order=1, title="Mr. Rajesh Kumar", label="Senior PLC Trainer", description="12+ years at Siemens India. Expert in S7-1500 and TIA Portal.", tags="Siemens,TIA Portal,S7-1500")
    SectionContent.objects.create(section=faculty, order=2, title="Ms. Sneha Patil", label="Allen Bradley Specialist", description="10+ years with Rockwell Automation. CompactLogix & ControlLogix expert.", tags="Allen Bradley,RSLogix,ControlLogix")
    SectionContent.objects.create(section=faculty, order=3, title="Mr. Amit Deshmukh", label="Automation Consultant", description="15+ years in process automation. Expertise in PLC-SCADA integration.", tags="SCADA,DCS,Process Control")

    # PAST_RESULTS
    results = PageSection.objects.create(
        module=plc, section_type='PAST_RESULTS', order=8,
        super_heading="TRACK RECORD",
        heading="Our Results Speak",
        highlighted_heading="For Themselves",
        subheading="Proven track record of student success and industry placements.",
    )
    SectionContent.objects.create(section=results, order=1, label="500+", title="Students Placed", description="In the last 2 years alone.")
    SectionContent.objects.create(section=results, order=2, label="95%", title="Placement Rate", description="Consistently above industry average.")
    SectionContent.objects.create(section=results, order=3, label="₹4.5L", title="Avg. Starting Salary", description="For freshers after completing the course.")
    SectionContent.objects.create(section=results, order=4, label="50+", title="Hiring Partners", description="Including Siemens, ABB, L&T, and Honeywell.")

    # TESTIMONIALS
    testimonials = PageSection.objects.create(
        module=plc, section_type='TESTIMONIALS', order=9,
        super_heading="STUDENT REVIEWS",
        heading="What Our Students Say",
        subheading="Real feedback from students who transformed their careers with us.",
    )
    SectionContent.objects.create(section=testimonials, order=1, title="Best PLC Training in Nashik", description="The hands-on approach with real PLCs made all the difference. I got placed at Siemens within 2 weeks of completing the course.", question="Aditya Deshmukh", answer="Placed at Siemens Ltd.")
    SectionContent.objects.create(section=testimonials, order=2, title="Career Changing Experience", description="I was a mechanical engineer with no automation knowledge. This course gave me the confidence and skills to switch to automation.", question="Priya Sharma", answer="Placed at ABB Global")
    SectionContent.objects.create(section=testimonials, order=3, title="Worth Every Rupee", description="Individual PLC hardware, expert faculty, and placement support — everything was top-notch. Highly recommended!", question="Rohit Kulkarni", answer="Placed at L&T Automation")
    SectionContent.objects.create(section=testimonials, order=4, title="Exceeded Expectations", description="The TIA Portal training was incredibly detailed. I could handle real projects from day one at my new job.", question="Snehal Wagh", answer="Placed at Honeywell")

    # CTA
    PageSection.objects.create(
        module=plc, section_type='CTA', order=10,
        heading="Ready to Start Your PLC Career?",
        subheading="Join the next batch and become a certified PLC programmer in just 3 months.",
        primary_button_text="CALL NOW", primary_button_url="tel:+919075102234",
        secondary_button_text="Book Free Demo", secondary_button_url="/contact",
        overlay_title="Phone", overlay_description="+91 90751 02234",
    )

    # FAQ
    faq = PageSection.objects.create(
        module=plc, section_type='FAQ', order=11,
        heading="Frequently Asked Questions",
        subheading="Common questions about our PLC Programming course.",
    )
    for i, (q, a) in enumerate([
        ("Do I need prior programming knowledge?", "No, we start from absolute basics. Even students with no coding background can join."),
        ("Will I get hands-on practice with real PLCs?", "Yes, every student gets individual PLC hardware (Siemens, AB, Mitsubishi) for practice."),
        ("What is the batch size?", "We keep batches small — maximum 15 students — to ensure personalized attention."),
        ("Is placement guaranteed?", "We provide 100% placement assistance. Our placement rate has been 95%+ consistently."),
        ("Are EMI payment options available?", "Yes, we offer 3-month and 6-month EMI options with zero interest."),
        ("Can working professionals join?", "Absolutely! We have dedicated weekend and evening batches for working professionals."),
    ], 1):
        SectionContent.objects.create(section=faq, order=i, question=q, answer=a)

    print(f"  ✅ PLC Programming module created with {plc.sections.count()} sections")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MODULE 2: SCADA Systems
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print("📦 Creating Module: SCADA Systems...")
    scada = Module.objects.create(
        title="SCADA Systems",
        tagline="Learn Supervisory Control and Data Acquisition from industry experts.",
        slug="scada-systems",
        order=2,
    )

    PageSection.objects.create(
        module=scada, section_type='PAGE_BANNER', order=1,
        heading="SCADA Systems",
        highlighted_heading="Professional Course",
        subheading="Gain expertise in WinCC, Wonderware, and FactoryTalk SCADA platforms with real-time project experience.",
        primary_button_text="Enroll Now", primary_button_url="/contact",
    )

    ov2 = PageSection.objects.create(
        module=scada, section_type='COURSE_OVERVIEW', order=2,
        super_heading="COURSE OVERVIEW",
        heading="Comprehensive SCADA Training",
        subheading="From tag configuration to alarm management, learn everything required to design, deploy, and maintain industrial SCADA systems. Includes multi-brand training on WinCC, Wonderware InTouch, and FactoryTalk View.",
        overlay_title="Live Industrial Projects",
        overlay_description="Students work on simulated plant SCADA systems during training.",
    )
    SectionContent.objects.create(section=ov2, order=1, title="SCADA Architecture", description="Client-server, web-based, and cloud SCADA architectures.")
    SectionContent.objects.create(section=ov2, order=2, title="Tag & Database Management", description="Internal/external tags, scaling, and historian configuration.")
    SectionContent.objects.create(section=ov2, order=3, title="Graphics & HMI Design", description="Building operator screens, animations, and navigation flows.")
    SectionContent.objects.create(section=ov2, order=4, title="Alarm & Event Management", description="Alarm priorities, logging, acknowledgment, and historical trends.")

    h2 = PageSection.objects.create(
        module=scada, section_type='KEY_HIGHLIGHTS', order=3,
        super_heading="KEY HIGHLIGHTS",
        heading="Course Highlights",
        subheading="What makes our SCADA course the industry's preferred training program.",
    )
    SectionContent.objects.create(section=h2, order=1, title="3 SCADA Platforms", description="WinCC, Wonderware InTouch, FactoryTalk View.")
    SectionContent.objects.create(section=h2, order=2, title="Live Plant Simulation", description="Practice on simulated water treatment and power plant SCADA systems.")
    SectionContent.objects.create(section=h2, order=3, title="PLC-SCADA Integration", description="End-to-end integration with Siemens and AB PLCs.")
    SectionContent.objects.create(section=h2, order=4, title="Report Generation", description="Crystal Reports integration and automated PDF reporting.")

    s2 = PageSection.objects.create(
        module=scada, section_type='SUBJECTS_COVERED', order=4,
        super_heading="CURRICULUM",
        heading="Topics Covered",
    )
    for i, (t, d) in enumerate([
        ("SCADA Fundamentals", "Architecture, protocols, and communication standards."),
        ("Siemens WinCC", "Project creation, tag management, graphics, scripts, and archiving."),
        ("Wonderware InTouch", "Tag configuration, animations, alarms, and trend displays."),
        ("FactoryTalk View SE", "Rockwell's SCADA platform configuration and deployment."),
        ("OPC Communication", "OPC DA and OPC UA client-server communication setup."),
        ("SQL Database Integration", "Connecting SCADA to SQL Server for data logging and reporting."),
    ], 1):
        SectionContent.objects.create(section=s2, order=i, title=t, description=d)

    e2 = PageSection.objects.create(
        module=scada, section_type='ELIGIBILITY_CRITERIA', order=5,
        super_heading="ELIGIBILITY",
        heading="Who Should Enroll",
    )
    SectionContent.objects.create(section=e2, order=1, title="Engineering Graduates", description="Electrical, Electronics, Instrumentation, or Computer Science.")
    SectionContent.objects.create(section=e2, order=2, title="PLC Trained Professionals", description="Those who have completed basic PLC training and want to advance.")
    SectionContent.objects.create(section=e2, order=3, title="Working Engineers", description="Professionals in automation looking to add SCADA expertise.")

    f2 = PageSection.objects.create(
        module=scada, section_type='FEES_BATCH_DETAILS', order=6,
        super_heading="PRICING",
        heading="Fees & Schedule",
        primary_button_text="Enroll Now", primary_button_url="/contact",
    )
    SectionContent.objects.create(section=f2, order=1, label="Fee", title="₹35,000", description="Inclusive of all lab and certification charges.")
    SectionContent.objects.create(section=f2, order=2, label="Duration", title="2 Months", description="Intensive weekend and weekday batches.")
    SectionContent.objects.create(section=f2, order=3, label="Next Batch", title="1st July 2026", description="Register early for the best seats.")
    SectionContent.objects.create(section=f2, order=4, label="Seats", title="12 Left", description="Filling fast — limited seats per batch.")

    fac2 = PageSection.objects.create(
        module=scada, section_type='FACULTY', order=7,
        super_heading="YOUR MENTORS",
        heading="Industry Expert Faculty",
    )
    SectionContent.objects.create(section=fac2, order=1, title="Mr. Sanjay Joshi", label="SCADA Specialist", description="14+ years at Schneider Electric. WinCC & Wonderware certified.", tags="WinCC,Wonderware,OPC")
    SectionContent.objects.create(section=fac2, order=2, title="Ms. Kavita Rao", label="Control Systems Engineer", description="11+ years in process automation with SCADA deployment experience.", tags="FactoryTalk,SQL,Reporting")

    r2 = PageSection.objects.create(
        module=scada, section_type='PAST_RESULTS', order=8,
        super_heading="ACHIEVEMENTS",
        heading="Proven Track Record",
    )
    SectionContent.objects.create(section=r2, order=1, label="300+", title="SCADA Engineers Trained")
    SectionContent.objects.create(section=r2, order=2, label="92%", title="Placement Rate")
    SectionContent.objects.create(section=r2, order=3, label="₹5L", title="Avg. Package")
    SectionContent.objects.create(section=r2, order=4, label="40+", title="Partner Companies")

    t2 = PageSection.objects.create(
        module=scada, section_type='TESTIMONIALS', order=9,
        heading="Student Experiences",
    )
    SectionContent.objects.create(section=t2, order=1, title="Excellent SCADA Training", description="The multi-platform approach is the best part. I learned WinCC, Wonderware, and FactoryTalk in one course.", question="Vishal Mane", answer="Placed at Schneider Electric")
    SectionContent.objects.create(section=t2, order=2, title="From Zero to SCADA Expert", description="I had no SCADA knowledge before joining. The trainers made complex topics easy to understand.", question="Neha Kulkarni", answer="Placed at Emerson")
    SectionContent.objects.create(section=t2, order=3, title="Industry-Ready Training", description="The live plant simulation projects gave me confidence to handle real SCADA systems from day one.", question="Rahul Desai", answer="Placed at Yokogawa")

    PageSection.objects.create(
        module=scada, section_type='CTA', order=10,
        heading="Launch Your SCADA Career Today",
        subheading="Become a certified SCADA professional with our industry-leading training program.",
        primary_button_text="CALL NOW", primary_button_url="tel:+919075102234",
        secondary_button_text="Enquire Online", secondary_button_url="/contact",
        overlay_title="Phone", overlay_description="+91 90751 02234",
    )

    faq2 = PageSection.objects.create(
        module=scada, section_type='FAQ', order=11,
        heading="Frequently Asked Questions",
        subheading="Common questions about the SCADA Systems course.",
    )
    for i, (q, a) in enumerate([
        ("Is PLC knowledge required before SCADA training?", "Basic PLC knowledge is recommended but not mandatory. We cover PLC-SCADA integration from scratch."),
        ("Which SCADA software will I learn?", "You will learn Siemens WinCC, Wonderware InTouch, and Rockwell FactoryTalk View SE."),
        ("Do I get a certificate?", "Yes, you receive an industry-recognized certification from NS-2 Infotech upon completion."),
        ("What are the job roles after this course?", "SCADA Engineer, Control Room Operator, SCADA Developer, Automation Engineer."),
    ], 1):
        SectionContent.objects.create(section=faq2, order=i, question=q, answer=a)

    print(f"  ✅ SCADA Systems module created with {scada.sections.count()} sections")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MODULE 3: Industrial Robotics
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print("📦 Creating Module: Industrial Robotics...")
    robotics = Module.objects.create(
        title="Industrial Robotics",
        tagline="Program and operate industrial robots for manufacturing automation.",
        slug="industrial-robotics",
        order=3,
    )

    PageSection.objects.create(
        module=robotics, section_type='PAGE_BANNER', order=1,
        heading="Industrial Robotics",
        highlighted_heading="Certification Program",
        subheading="Learn to program, simulate, and deploy industrial robots with training on FANUC, ABB, and KUKA platforms.",
        primary_button_text="Join Next Batch", primary_button_url="/contact",
    )

    ov3 = PageSection.objects.create(
        module=robotics, section_type='COURSE_OVERVIEW', order=2,
        super_heading="PROGRAM OVERVIEW",
        heading="Industrial Robotics",
        highlighted_heading="Training Program",
        subheading="Comprehensive training covering robot programming, path planning, welding applications, pick-and-place operations, and Industry 4.0 integration with cobots and vision systems.",
    )
    SectionContent.objects.create(section=ov3, order=1, title="Robot Programming", description="Teach pendant programming, offline programming, and simulation.")
    SectionContent.objects.create(section=ov3, order=2, title="Path Planning & Motion", description="Joint interpolation, linear motion, and circular motion paths.")
    SectionContent.objects.create(section=ov3, order=3, title="Vision Systems", description="Camera integration for quality inspection and guided pick-place.")
    SectionContent.objects.create(section=ov3, order=4, title="Safety & Compliance", description="ISO 10218 safety standards and risk assessment for robotic cells.")

    h3 = PageSection.objects.create(
        module=robotics, section_type='KEY_HIGHLIGHTS', order=3,
        super_heading="HIGHLIGHTS",
        heading="Program Features",
    )
    SectionContent.objects.create(section=h3, order=1, title="Multi-Brand Training", description="FANUC, ABB, KUKA, and Universal Robots (cobots).")
    SectionContent.objects.create(section=h3, order=2, title="Robot Simulation Lab", description="RobotStudio, ROBOGUIDE, and KUKA.Sim access for offline programming.")
    SectionContent.objects.create(section=h3, order=3, title="Live Robot Practice", description="Hands-on sessions with actual industrial robot arms.")
    SectionContent.objects.create(section=h3, order=4, title="Industry 4.0 Ready", description="IoT integration, digital twins, and smart factory concepts.")

    f3 = PageSection.objects.create(
        module=robotics, section_type='FEES_BATCH_DETAILS', order=4,
        super_heading="PRICING",
        heading="Course Fees & Schedule",
        primary_button_text="Reserve Your Spot", primary_button_url="/contact",
    )
    SectionContent.objects.create(section=f3, order=1, label="Fee", title="₹55,000", description="Includes lab access and certification.")
    SectionContent.objects.create(section=f3, order=2, label="Duration", title="4 Months", description="Comprehensive weekend and weekday batches.")
    SectionContent.objects.create(section=f3, order=3, label="Next Batch", title="10th July 2026", description="Early registration recommended.")
    SectionContent.objects.create(section=f3, order=4, label="Seats", title="6 Left", description="Small batch for maximum learning.")

    t3 = PageSection.objects.create(
        module=robotics, section_type='TESTIMONIALS', order=5,
        heading="What Our Graduates Say",
    )
    SectionContent.objects.create(section=t3, order=1, title="Dream Job in Robotics", description="This course opened doors to my dream career. Working with real robots was an incredible experience.", question="Mayur Patil", answer="Placed at FANUC India")
    SectionContent.objects.create(section=t3, order=2, title="Industry-Level Training", description="The simulation software and hands-on robot sessions made me job-ready from day one.", question="Ananya Singh", answer="Placed at ABB Robotics")

    PageSection.objects.create(
        module=robotics, section_type='CTA', order=6,
        heading="Step Into the Future of Manufacturing",
        subheading="Industrial robotics is the fastest-growing field in automation. Start your journey today.",
        primary_button_text="CALL NOW", primary_button_url="tel:+919075102234",
        secondary_button_text="Free Career Counseling", secondary_button_url="/contact",
    )

    faq3 = PageSection.objects.create(
        module=robotics, section_type='FAQ', order=7,
        heading="Frequently Asked Questions",
    )
    for i, (q, a) in enumerate([
        ("Do I need mechanical engineering background?", "No, students from Electrical, Electronics, Mechanical, and Computer Science can all enroll."),
        ("Will I get to work with real robots?", "Yes, we have FANUC and ABB robot arms in our lab for hands-on practice."),
        ("What job roles can I get after this course?", "Robot Programmer, Automation Engineer, Robotics Application Engineer, Integration Specialist."),
    ], 1):
        SectionContent.objects.create(section=faq3, order=i, question=q, answer=a)

    print(f"  ✅ Industrial Robotics module created with {robotics.sections.count()} sections")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # MODULE 4: EPLAN Designing
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    print("📦 Creating Module: EPLAN Designing...")
    eplan = Module.objects.create(
        title='EPLAN Designing',
        tagline='Learn professional electrical panel designing with EPLAN software.',
        slug='eplan-designing',
        order=4,
    )

    # PAGE_BANNER
    PageSection.objects.create(
        module=eplan, section_type='PAGE_BANNER', order=1,
        heading='EPLAN Designing',
        highlighted_heading='Professional Course',
        subheading='Master industrial electrical panel design, schematic creation, and documentation using EPLAN Electric P8 — the global standard in electrical engineering.',
        primary_button_text='Enroll Now', primary_button_url='/contact',
        secondary_button_text='Download Brochure', secondary_button_url='#brochure',
    )

    # COURSE_OVERVIEW
    ov = PageSection.objects.create(
        module=eplan, section_type='COURSE_OVERVIEW', order=2,
        super_heading='COURSE OVERVIEW',
        heading='Learn Professional',
        highlighted_heading='Electrical Design',
        subheading='EPLAN Electric P8 is the industry standard for electrical engineering design. This course covers schematic creation, panel layout, cable planning, PLC assignment, and automated report generation.',
        overlay_title='Industry-Standard Software',
        overlay_description='Train on licensed EPLAN Electric P8 software.',
    )
    SectionContent.objects.create(section=ov, order=1, title='Schematic Design', description='Create single-line and multi-line circuit diagrams.')
    SectionContent.objects.create(section=ov, order=2, title='Panel Layout Design', description='2D and 3D panel layouts with copper bar routing.')
    SectionContent.objects.create(section=ov, order=3, title='PLC Auto-Connection', description='Automated PLC I/O assignment and wiring.')
    SectionContent.objects.create(section=ov, order=4, title='Report Generation', description='BOMs, cable lists, terminal diagrams, and wire labels.')

    # KEY_HIGHLIGHTS
    h = PageSection.objects.create(
        module=eplan, section_type='KEY_HIGHLIGHTS', order=3,
        super_heading='KEY HIGHLIGHTS',
        heading='Course Highlights',
        subheading='What makes our EPLAN course the preferred choice.',
    )
    SectionContent.objects.create(section=h, order=1, title='Licensed Software', description='Train on genuine EPLAN Electric P8 licenses.')
    SectionContent.objects.create(section=h, order=2, title='Real Project Work', description='Design actual industrial panel projects.')
    SectionContent.objects.create(section=h, order=3, title='Industry Standards', description='Learn IEC 61346 and EN 81346 standards.')
    SectionContent.objects.create(section=h, order=4, title='Placement Support', description='100% placement assistance for EPLAN designers.')

    # SUBJECTS_COVERED
    s = PageSection.objects.create(
        module=eplan, section_type='SUBJECTS_COVERED', order=4,
        super_heading='CURRICULUM',
        heading='Topics Covered',
    )
    for i, (t, d) in enumerate([
        ('EPLAN Interface & Project Setup', 'Workspace configuration, project structure, and navigation.'),
        ('Symbol Library & Macros', 'Standard symbols, custom macros, and component libraries.'),
        ('Schematic Drawing', 'Circuit diagrams, cross-references, and connection points.'),
        ('PLC Configuration', 'PLC cards, addressing, and automatic connection generation.'),
        ('Panel Layout (2D)', 'Component placement, mounting rails, and cable ducts.'),
        ('3D Panel Design', 'EPLAN Pro Panel for 3D visualization and copper routing.'),
        ('Cable & Wire Planning', 'Cable routing, wire numbering, and harness design.'),
        ('Report Generation', 'BOM, terminal diagrams, cable lists, and label printing.'),
    ], 1):
        SectionContent.objects.create(section=s, order=i, title=t, description=d)

    # FEES_BATCH_DETAILS
    f = PageSection.objects.create(
        module=eplan, section_type='FEES_BATCH_DETAILS', order=5,
        super_heading='PRICING',
        heading='Fees & Schedule',
        primary_button_text='Reserve Your Seat', primary_button_url='/contact',
    )
    SectionContent.objects.create(section=f, order=1, label='Fee', title='Rs 30,000', description='Inclusive of software access and certification.')
    SectionContent.objects.create(section=f, order=2, label='Duration', title='2 Months', description='Weekday and weekend batches available.')
    SectionContent.objects.create(section=f, order=3, label='Next Batch', title='20th June 2026', description='Limited seats — register early.')
    SectionContent.objects.create(section=f, order=4, label='Seats', title='10 Left', description='Small batch for individual attention.')

    # TESTIMONIALS
    t = PageSection.objects.create(
        module=eplan, section_type='TESTIMONIALS', order=6,
        heading='Student Reviews',
    )
    SectionContent.objects.create(section=t, order=1, title='Excellent EPLAN Training', description='The project-based approach helped me land a job as an EPLAN designer at a German MNC.', question='Saurabh More', answer='Placed at Rittal India')
    SectionContent.objects.create(section=t, order=2, title='Industry Ready Skills', description='I learned not just the software but also industrial standards and best practices.', question='Pooja Jadhav', answer='Placed at Schneider Electric')

    # CTA
    PageSection.objects.create(
        module=eplan, section_type='CTA', order=7,
        heading='Start Your EPLAN Design Career',
        subheading='Become a certified EPLAN designer and unlock opportunities in electrical engineering.',
        primary_button_text='CALL NOW', primary_button_url='tel:+919075102234',
        secondary_button_text='Enquire Online', secondary_button_url='/contact',
        overlay_title='Phone', overlay_description='+91 90751 02234',
    )

    # FAQ
    faq = PageSection.objects.create(
        module=eplan, section_type='FAQ', order=8,
        heading='Frequently Asked Questions',
    )
    SectionContent.objects.create(section=faq, order=1, question='Do I need prior CAD experience?', answer='No, we start from basics. Knowledge of electrical circuits is helpful but not mandatory.')
    SectionContent.objects.create(section=faq, order=2, question='Which version of EPLAN is used?', answer='We use the latest EPLAN Electric P8 version with genuine licenses.')
    SectionContent.objects.create(section=faq, order=3, question='What job roles can I get?', answer='EPLAN Designer, Electrical Design Engineer, Panel Design Engineer, Control Panel Designer.')

    print(f"  ✅ EPLAN Designing module created with {eplan.sections.count()} sections")

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # SUMMARY
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    total_modules = Module.objects.count()
    total_sections = PageSection.objects.filter(module__isnull=False).count()
    total_content = SectionContent.objects.filter(section__module__isnull=False).count()

    print(f"\n{'='*50}")
    print(f"✅ Data Entry Complete!")
    print(f"   📦 Modules Created: {total_modules}")
    print(f"   📄 Sections Created: {total_sections}")
    print(f"   📝 Content Items Created: {total_content}")
    print(f"{'='*50}")
    print(f"\n🌐 Access your modules at:")
    print(f"   /modules/plc-programming/")
    print(f"   /modules/scada-systems/")
    print(f"   /modules/industrial-robotics/")
    print(f"\n🔗 API Endpoints:")
    print(f"   GET /api/internships/modules/")
    print(f"   GET /api/internships/modules/plc-programming/")
    print(f"   GET /api/internships/modules/scada-systems/")
    print(f"   GET /api/internships/modules/industrial-robotics/")


if __name__ == '__main__':
    populate_modules()
