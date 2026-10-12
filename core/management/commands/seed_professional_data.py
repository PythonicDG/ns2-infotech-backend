from datetime import date
from pathlib import Path

from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from aboutus.models import PageSection as AboutSection
from aboutus.models import SectionContent as AboutContent
from announcements.models import Announcement as NewsItem
from announcements.models import AnnouncementCategory
from core.models import (
    Announcement,
    CompanyProfile,
    FooterItem,
    FooterSection,
    FooterSubscription,
    Menu,
    SiteStatistic,
    SocialLink,
    SubMenu,
)
from homepage.models import PageSection as HomeSection
from homepage.models import SectionContent as HomeContent
from modules.models import Module, PageSection as CourseSection
from modules.models import SectionContent as CourseContent


COMPANY_NAME = "Modern Institute of Automation"
PHONE = "093702 18408"
EMAIL = "dipak@gmail.com"
ADDRESS = (
    "Flat No. 5, Second Floor, Mayur Complex, Pavana Nagar, Bijli Nagar Road, "
    "Chinchwad, Pimpri-Chinchwad, Maharashtra 411033"
)


class Command(BaseCommand):
    help = "Seed complete, professional, frontend-ready website content."

    @transaction.atomic
    def handle(self, *args, **options):
        company = self.seed_core()
        self.seed_homepage(company)
        self.seed_about()
        self.seed_course_landing()
        self.seed_courses()
        self.seed_announcements()
        self.stdout.write(self.style.SUCCESS("Professional website data seeded successfully."))

    @staticmethod
    def fit(model, values):
        """Respect legacy CharField limits while keeping the seed command portable."""
        fitted = dict(values)
        for key, value in fitted.items():
            if not isinstance(value, str):
                continue
            try:
                max_length = model._meta.get_field(key).max_length
            except Exception:
                max_length = None
            if max_length and len(value) > max_length:
                fitted[key] = value[: max_length - 1].rstrip() + "…"
        return fitted

    def seed_core(self):
        company = CompanyProfile.objects.filter(is_active=True).first()
        if company is None:
            company = CompanyProfile()
        company.name = COMPANY_NAME
        company.tagline = "Automate your future."
        company.description = (
            "Practical industrial automation training for students, graduates, technicians, "
            "and working professionals, with a strong focus on real hardware and job-ready skills."
        )
        company.email = EMAIL
        company.phone = PHONE
        company.address = ADDRESS
        company.google_maps_url = (
            "https://www.google.com/maps?q=Modern+Institute+of+Automation+Chinchwad&output=embed"
        )
        company.copyright_text = "© 2026 Modern Institute of Automation. All rights reserved."
        company.credits_text = "Practical skills for modern industry."
        company.is_active = True
        # Local database backups can reference media that was not included with the
        # project.  Clear only those broken references so textual seeding remains
        # independent of optional image assets.
        for image_field_name in ("logo", "cover_image"):
            image_field = getattr(company, image_field_name)
            if image_field and not image_field.storage.exists(image_field.name):
                setattr(company, image_field_name, None)
        company.save()

        menu_data = [
            ("Home", "/", False, 1),
            ("About Us", "/aboutus", False, 2),
            ("Courses", "/modules", False, 3),
            ("Announcements", "/announcements", False, 4),
            ("Contact", "/contact", False, 5),
            ("Enroll Now", "/contact#enquiry-form", True, 6),
        ]
        Menu.objects.exclude(text__in=[item[0] for item in menu_data]).delete()
        menus = {}
        for text, url, is_button, order in menu_data:
            menu, _ = Menu.objects.update_or_create(
                text=text,
                defaults={"url": url, "is_button": is_button, "order": order, "is_active": True},
            )
            menus[text] = menu

        SubMenu.objects.all().delete()
        for order, (text, slug) in enumerate(
            [
                ("PLC & SCADA Training", "plc-scada-training"),
                ("EPLAN Electrical Design", "eplan-electrical-design"),
                ("Industrial Robotics", "industrial-robotics"),
            ],
            start=1,
        ):
            SubMenu.objects.create(
                menu=menus["Courses"], text=text, slug=slug,
                url=f"/modules/{slug}", order=order, is_active=True,
            )

        FooterSection.objects.all().delete()
        footer_groups = [
            ("Explore", [("Home", "/"), ("About Us", "/aboutus"), ("Courses", "/modules"), ("Contact", "/contact")]),
            ("Popular Courses", [("PLC & SCADA", "/modules/plc-scada-training"), ("EPLAN Electrical Design", "/modules/eplan-electrical-design"), ("Industrial Robotics", "/modules/industrial-robotics")]),
            ("Get in Touch", [(PHONE, f"tel:+91{PHONE.replace(' ', '')}"), (EMAIL, f"mailto:{EMAIL}"), ("Chinchwad, Pune", "/contact")]),
        ]
        for section_order, (title, items) in enumerate(footer_groups, start=1):
            section = FooterSection.objects.create(title=title, order=section_order, is_active=True)
            FooterItem.objects.bulk_create([
                FooterItem(section=section, text=text, url=url, order=order, is_active=True)
                for order, (text, url) in enumerate(items, start=1)
            ])
        FooterSubscription.objects.all().update(is_active=False)
        FooterSubscription.objects.create(
            placeholder_text="Enter your email address", button_text="Stay Updated", is_active=True
        )

        Announcement.objects.all().delete()
        Announcement.objects.bulk_create([
            Announcement(icon="📘", text="Admissions open for upcoming automation training batches", order=1),
            Announcement(icon="⚙️", text="Hands-on practice with industrial PLC, HMI, SCADA and drives", order=2),
            Announcement(icon="🎯", text="Interview preparation and placement assistance included", order=3),
        ])
        SiteStatistic.objects.all().delete()

        existing_instagram = SocialLink.objects.filter(platform__iexact="Instagram").first()
        instagram_url = (
            existing_instagram.social_link
            if existing_instagram and "instagram.com" in existing_instagram.social_link
            else "https://www.instagram.com/moderninstituteofautomation/"
        )
        SocialLink.objects.all().delete()
        SocialLink.objects.bulk_create([
            SocialLink(platform="Instagram", social_link=instagram_url, is_active=True),
            SocialLink(platform="WhatsApp", social_link=f"https://wa.me/91{PHONE.replace(' ', '')}", is_active=True),
        ])
        return company

    def replace_home_section(self, company, section_type, order, values, items=()):
        content_type = ContentType.objects.get_for_model(company)
        section = HomeSection.objects.filter(section_type=section_type).order_by("id").first()
        if section is None:
            section = HomeSection(section_type=section_type)
        section.content_type = content_type
        section.object_id = company.pk
        section.order = order
        section.is_active = True
        for key, value in self.fit(HomeSection, values).items():
            setattr(section, key, value)
        for image_field_name in ("background_image", "primary_image"):
            image_field = getattr(section, image_field_name)
            if image_field and not image_field.storage.exists(image_field.name):
                setattr(section, image_field_name, None)
        section.save()
        HomeSection.objects.filter(section_type=section_type).exclude(pk=section.pk).delete()
        # Remove managed homepage assets before replacing rows so repeated seed
        # runs do not leave orphaned files in MEDIA_ROOT.
        for existing_item in section.content_items.all():
            if existing_item.icon:
                existing_item.icon.delete(save=False)
        section.content_items.all().delete()
        asset_root = Path(__file__).resolve().parents[3] / "homepage" / "seed_assets"
        for index, raw_item in enumerate(items, start=1):
            item = dict(raw_item)
            asset_name = item.pop("_asset", None)
            content = HomeContent(
                section=section,
                order=index,
                is_active=True,
                **self.fit(HomeContent, item),
            )
            if asset_name:
                asset_path = asset_root / asset_name
                if asset_path.exists():
                    with asset_path.open("rb") as image_file:
                        # Keep the upload in memory so SectionContent.save()
                        # writes only the optimized WebP, not an orphaned JPEG.
                        content.icon = ContentFile(image_file.read(), name=asset_name)
            content.save()

    def seed_homepage(self, company):
        sections = [
            ("HERO", 1, {
                "super_heading": "INDUSTRIAL AUTOMATION TRAINING IN PUNE",
                "heading": "Build Job-Ready Skills in PLC, SCADA and Electrical Design",
                "subheading": "Learn through guided lab sessions on industrial controllers, HMI, SCADA, drives, sensors, control panels and engineering software.",
                "primary_button_text": "Explore Courses", "primary_button_url": "/modules",
                "secondary_button_text": "Book a Free Counselling Session", "secondary_button_url": "/contact",
            }, [
                {"label": "Hands-on", "title": "Industrial Hardware"},
                {"label": "Multi-brand", "title": "PLC Platforms"},
                {"label": "Career", "title": "Interview Preparation"},
                {"label": "Flexible", "title": "Batch Options"},
            ]),
            ("OVERVIEW", 2, {
                "super_heading": "ABOUT THE INSTITUTE",
                "heading": "Practical Training for Modern Automation Careers",
                "subheading": "A focused learning environment for building strong electrical, controls and automation fundamentals.",
                "overview_text": "Modern Institute of Automation combines concept clarity with structured practice on the tools used across manufacturing, process and machine-automation environments.",
                "primary_button_text": "Know More About Us", "primary_button_url": "/aboutus",
                "secondary_button_text": "View All Courses", "secondary_button_url": "/modules",
            }, [
                {"text": "Individual practice and guided lab exercises"},
                {"text": "Curriculum covering electrical basics through advanced automation"},
                {"text": "Application-oriented projects and troubleshooting"},
                {"text": "Resume, interview and career-readiness support"},
            ]),
            ("WHY_CHOOSE_US", 3, {
                "super_heading": "WHY CHOOSE MIA",
                "heading": "Training Designed Around Real Industrial Work",
                "subheading": "Build the confidence to understand, program, wire, commission and troubleshoot automation systems.",
            }, [
                {"title": "Practice-Oriented Learning", "description": "Reinforce every concept through wiring, programming, simulation and troubleshooting exercises."},
                {"title": "Multiple Automation Platforms", "description": "Work with commonly used PLC brands, engineering software, HMI, SCADA and drive technologies."},
                {"title": "Structured Learning Path", "description": "Progress from electrical fundamentals to integrated control-system applications."},
                {"title": "Career Preparation", "description": "Receive support for technical interviews, resumes and automation job roles."},
            ]),
            ("OUR_SERVICES", 4, {
                "super_heading": "SPECIALIZED",
                "heading": "Automation Training Programs",
                "subheading": "Choose a focused course or build a broader skill set across industrial automation and electrical design.",
            }, [
                {"label": "PLC & SCADA", "title": "Industrial Automation", "description": "Electrical controls, Allen-Bradley, Siemens, Mitsubishi and Delta PLCs, HMI, SCADA, VFD, servo and stepper applications.", "text": "/modules/plc-scada-training"},
                {"label": "EPLAN", "title": "Electrical Design", "description": "Schematics, symbols, macros, panel documentation, reports, calculations and engineering deliverables in EPLAN Electric P8.", "text": "/modules/eplan-electrical-design"},
                {"label": "ROBOTICS", "title": "Industrial Robotics", "description": "Robot safety, coordinate systems, motion programming, teach-pendant operation and cell-integration fundamentals.", "text": "/modules/industrial-robotics"},
            ]),
            ("OUR_PLACED_STUDENTS", 5, {
                "super_heading": "STUDENT OUTCOMES", "heading": "Our Placed Students",
                "subheading": "Celebrating learners who turned practical automation training into an engineering opportunity.",
            }, [
                {"title": "Abhijeet Gajanan Surve", "description": "Automation Engineer", "text": "Sandip Institute of Engineering & Management, Nashik", "_asset": "abhijeet-surve-placement.jpeg"},
                {"title": "Akash Dattatray Dhole", "description": "Junior Automation Engineer", "text": "Sahakar Maharshi Rajaram Bapu Patil Polytechnic Institute", "_asset": "akash-dhole-placement.jpeg"},
                {"title": "Chaitanya Kiranrao Lokhande", "description": "Automation Trainee Engineer", "text": "Jagdamba College of Engineering, Yavatmal", "_asset": "chaitanya-lokhande-placement.jpeg"},
                {"title": "Chetan Shivashankar Dahake", "description": "GET Engineer", "text": "D. Y. Patil College of Engineering, Talegaon", "_asset": "chetan-dahake-placement.jpeg"},
            ]),
            ("TESTIMONIALS", 6, {
                "super_heading": "LEARNING EXPERIENCE", "heading": "What Learners Value in Our Programs",
                "subheading": "A practical, step-by-step approach helps learners turn concepts into usable workplace skills.",
            }, [
                {"title": "Clear, practical instruction", "description": "Concepts are connected to wiring and programming exercises, making automation easier to understand.", "question": "Hands-on Learning", "answer": "Program experience"},
                {"title": "Confidence with industrial hardware", "description": "Regular lab practice builds familiarity with PLCs, panels, sensors, HMI and drives.", "question": "Lab Practice", "answer": "Program experience"},
                {"title": "Useful career preparation", "description": "Technical revision, project discussion and interview preparation support job readiness.", "question": "Career Support", "answer": "Program experience"},
            ]),
            ("FAQ", 7, {
                "super_heading": "FREQUENTLY ASKED QUESTIONS", "heading": "Plan Your Training with Confidence",
                "subheading": "Quick answers about eligibility, practical sessions, course coverage and career support.",
            }, [
                {"question": "Who can join the automation courses?", "answer": "Students, diploma holders, engineering graduates, technicians and working professionals from electrical, electronics, instrumentation, mechanical or related backgrounds can apply."},
                {"question": "Do I need prior PLC programming experience?", "answer": "No. The learning path starts with electrical control fundamentals and progresses to PLC programming, HMI, SCADA and system integration."},
                {"question": "Is the training practical?", "answer": "Yes. Programs include guided exercises using industrial hardware, engineering software, control wiring and troubleshooting scenarios."},
                {"question": "Which PLC platforms are covered?", "answer": "The PLC and SCADA program includes Allen-Bradley, Siemens, Mitsubishi and Delta platforms, with software selected for the respective hardware."},
                {"question": "Is placement support included?", "answer": "Learners receive career-readiness support such as resume guidance, technical interview preparation and assistance in identifying suitable opportunities. Employment is subject to individual performance and employer selection."},
                {"question": "Are weekday and weekend batches available?", "answer": "Batch schedules are planned according to current enrolments. Contact the institute for the latest weekday, weekend and fast-track options."},
            ]),
            ("CONTACT_US", 8, {
                "super_heading": "CONTACT US", "heading": "Speak with a Course Counsellor",
                "subheading": "Discuss your background, learning goals, suitable course and current batch options.",
                "overview_text": "Visit the institute for a counselling session and lab overview.",
                "primary_button_text": "Send Enquiry", "primary_button_url": "/contact#enquiry-form",
            }, [
                {"label": "Visit the Institute", "title": ADDRESS, "description": "Chinchwad, Pimpri-Chinchwad, Pune"},
                {"label": "Call or WhatsApp", "title": PHONE, "description": "Contact us for current counselling and batch timings."},
                {"label": "Email", "title": EMAIL, "description": "Send your course and admission questions."},
            ]),
            ("CTA", 9, {
                "super_heading": "START YOUR AUTOMATION JOURNEY", "heading": "Choose the Right Course for Your Career Goal",
                "subheading": "Book a counselling session to understand the curriculum, lab practice and current batch schedule.",
                "overview_text": f"Phone: {PHONE}", "primary_button_text": "Call Now", "primary_button_url": f"tel:+91{PHONE.replace(' ', '')}",
            }, []),
        ]
        HomeSection.objects.exclude(section_type__in=[row[0] for row in sections]).delete()
        for section_type, order, values, items in sections:
            self.replace_home_section(company, section_type, order, values, items)

    def replace_about_section(self, section_type, order, values, items=()):
        section, _ = AboutSection.objects.update_or_create(
            section_type=section_type,
            defaults={"order": order, "is_active": True, **self.fit(AboutSection, values)},
        )
        section.content_items.all().delete()
        AboutContent.objects.bulk_create([
            AboutContent(section=section, order=index, is_active=True, **self.fit(AboutContent, item))
            for index, item in enumerate(items, start=1)
        ])

    def seed_about(self):
        sections = [
            ("HERO", 1, {"super_heading": "MODERN INSTITUTE OF AUTOMATION", "heading": "Practical Skills for the Future of Industry", "subheading": "We help learners build strong foundations in electrical controls, automation programming and engineering design.", "primary_button_text": "Explore Courses", "primary_button_url": "/modules"}, []),
            ("WHO_WE_ARE", 2, {"super_heading": "WHO WE ARE", "heading": "An Industry-Focused Automation Training Institute", "subheading": "Modern Institute of Automation provides structured, application-oriented training for learners preparing for careers in manufacturing, machine automation, electrical design and control systems.", "overview_text": "Our approach combines explanation, demonstration, guided practice, project work and troubleshooting so that learners understand not only how a system works, but also how to apply that knowledge responsibly in the workplace.", "primary_button_text": "Speak with a Counsellor", "primary_button_url": "/contact"}, [
                {"label": "Practical", "title": "Lab-Based Learning", "description": "Practice on controllers, panels and software used in automation workflows."},
                {"label": "Structured", "title": "Progressive Curriculum", "description": "Move from core concepts to integrated industrial applications."},
                {"label": "Career", "title": "Professional Readiness", "description": "Develop technical communication, project and interview skills."},
            ]),
            ("DIRECTOR_MESSAGE", 3, {"super_heading": "A MESSAGE FROM THE INSTITUTE", "heading": "Learning That Builds Capability and Confidence", "subheading": "Automation is best learned by connecting theory with observation, wiring, programming and repeated problem-solving.", "overview_text": "Our purpose is to create a disciplined learning environment where every learner can build sound fundamentals, practise with care and grow into a dependable engineering professional.", "primary_button_text": "View Programs", "primary_button_url": "/modules"}, [
                {"label": "Institute Leadership", "title": "Director, Modern Institute of Automation", "description": "Committed to practical technical education and continuous learning."}
            ]),
            ("OUR_STORY", 4, {"super_heading": "OUR APPROACH", "heading": "From Classroom Concepts to Industrial Application", "subheading": "MIA was created around a simple need: learners require more than software demonstrations to become confident automation professionals.", "overview_text": "Every program is organised around clear concepts, hardware familiarisation, software practice, application exercises, documentation and troubleshooting. This creates a repeatable path from basic understanding to independent problem-solving."}, [
                {"label": "01", "title": "Understand", "description": "Build electrical, control and safety fundamentals."},
                {"label": "02", "title": "Practise", "description": "Apply concepts through guided lab exercises."},
                {"label": "03", "title": "Integrate", "description": "Connect PLC, HMI, SCADA, drives and field devices."},
                {"label": "04", "title": "Demonstrate", "description": "Present projects and prepare for technical discussions."},
            ]),
            ("VISION_MISSION", 5, {"super_heading": "VISION & MISSION", "heading": "Developing Capable Automation Professionals", "overview_text": "Our direction is guided by practical learning, professional responsibility and relevance to modern industry."}, [
                {"label": "Vision", "title": "Accessible, high-quality automation education", "description": "To help learners become confident, adaptable and responsible contributors to automated industry."},
                {"label": "Mission", "title": "Practical learning with strong fundamentals", "description": "To deliver structured training that connects core engineering principles with current industrial tools and workflows."},
                {"label": "Values", "title": "Clarity, practice and professionalism", "description": "To promote safe work, honest guidance, continuous improvement and respect for engineering standards."},
            ]),
            ("EXPERTISE", 6, {"super_heading": "OUR EXPERTISE", "heading": "Core Areas of Training", "subheading": "A balanced curriculum across controls, programming, visualisation, motion and electrical documentation."}, [
                {"label": "PLC Programming", "description": "Ladder logic, sequence control, interlocks, timers, counters, data handling and troubleshooting."},
                {"label": "HMI & SCADA", "description": "Operator screens, tags, alarms, trends, communication and supervisory monitoring."},
                {"label": "Industrial Drives", "description": "VFD configuration, motor-control applications, servo and stepper fundamentals."},
                {"label": "Electrical Controls", "description": "Relays, contactors, sensors, starters, wiring practices and control circuits."},
                {"label": "EPLAN Design", "description": "Schematics, symbols, macros, reports, calculations and panel documentation."},
                {"label": "Industrial Robotics", "description": "Robot operation, coordinate systems, motion instructions, safety and cell integration."},
            ]),
            ("ACCREDITATIONS", 7, {"super_heading": "TRAINING STANDARDS", "heading": "Professional Practices Built into Every Program", "subheading": "Our course delivery emphasises safe work, accurate documentation and disciplined troubleshooting.", "overview_text": "Specific software versions and hardware availability may vary by batch; the institute shares the current lab configuration during counselling."}, [
                {"label": "Application-Oriented Curriculum", "title": "Industry-relevant exercises and workflows"},
                {"label": "Structured Assessment", "title": "Practice tasks, project reviews and technical revision"},
                {"label": "Professional Documentation", "title": "Clear naming, drawing and reporting practices"},
                {"label": "Safety Awareness", "title": "Responsible handling of electrical and automation equipment"},
            ]),
            ("INFRASTRUCTURE", 8, {"super_heading": "LEARNING ENVIRONMENT", "heading": "A Lab Built for Active Practice", "subheading": "The training environment supports controller programming, panel wiring, simulation and engineering documentation."}, [
                {"label": "PLC Workstations", "description": "Practice with multiple controller families and programming environments."},
                {"label": "Control Components", "description": "Relays, contactors, push buttons, sensors, indicators and motor-control devices."},
                {"label": "HMI & SCADA Tools", "description": "Build monitoring screens, alarms, trends and operator workflows."},
                {"label": "Engineering Software", "description": "Use automation and electrical-design tools in guided exercises."},
            ]),
            ("GALLERY", 9, {"super_heading": "INSIDE MIA", "heading": "Learning in Action", "subheading": "Images from lab practice, demonstrations, projects and learner activities can be added here."}, []),
            ("OUR_TEAM", 10, {"super_heading": "OUR TRAINERS", "heading": "Learn with Practising Automation Mentors", "subheading": "Trainer profiles", "overview_text": "Our training approach combines subject knowledge, application guidance and patient, step-by-step mentoring."}, [
                {"label": "Automation Training Team", "title": "PLC, SCADA & Industrial Controls", "description": "Guides learners through programming, hardware integration, projects and troubleshooting."},
                {"label": "Electrical Design Team", "title": "EPLAN & Panel Documentation", "description": "Supports schematic design, calculations, component selection, reports and documentation workflows."},
            ]),
        ]
        AboutSection.objects.exclude(section_type__in=[row[0] for row in sections]).delete()
        for section_type, order, values, items in sections:
            self.replace_about_section(section_type, order, values, items)

    def replace_course_section(self, module, section_type, order, values, items=()):
        section, _ = CourseSection.objects.update_or_create(
            module=module, section_type=section_type,
            defaults={"order": order, "is_active": True, **self.fit(CourseSection, values)},
        )
        section.content_items.all().delete()
        CourseContent.objects.bulk_create([
            CourseContent(section=section, order=index, is_active=True, **self.fit(CourseContent, item))
            for index, item in enumerate(items, start=1)
        ])

    def seed_course_landing(self):
        CourseSection.objects.filter(module__isnull=True).delete()
        sections = [
            ("HERO", 1, {"super_heading": "INDUSTRIAL AUTOMATION COURSES", "heading": "Build Practical Skills for Modern Industry", "highlighted_heading": "Modern Industry", "subheading": "Explore focused training programs in PLC and SCADA, EPLAN electrical design and industrial robotics.", "primary_button_text": "View Programs", "primary_button_url": "#programs", "secondary_button_text": "Talk to a Counsellor", "secondary_button_url": "/contact"}, []),
            ("MODULE_OPPORTUNITIES", 2, {"heading": "Choose a Program That Matches Your Goal", "subheading": "Each program combines core concepts, guided practice and application-focused learning."}, [
                {"label": "01", "title": "PLC & SCADA Training", "description": "For automation, maintenance, commissioning and controls roles.", "primary_button_text": "View Course", "primary_button_url": "/modules/plc-scada-training"},
                {"label": "02", "title": "EPLAN Electrical Design", "description": "For electrical design, panel engineering and documentation roles.", "primary_button_text": "View Course", "primary_button_url": "/modules/eplan-electrical-design"},
                {"label": "03", "title": "Industrial Robotics", "description": "For robot operation, programming and integration fundamentals.", "primary_button_text": "View Course", "primary_button_url": "/modules/industrial-robotics"},
            ]),
            ("WHY_CHOOSE_US", 3, {"super_heading": "THE MIA ADVANTAGE", "heading": "Learn by Doing", "subheading": "Training designed to help you explain, demonstrate and troubleshoot what you learn."}, [
                {"title": "Guided Lab Practice", "description": "Complete structured exercises with trainer support."},
                {"title": "Current Engineering Tools", "description": "Learn using widely adopted automation and design software."},
                {"title": "Integrated Applications", "description": "Connect controllers, interfaces, drives and field devices."},
                {"title": "Career Readiness", "description": "Prepare for projects, technical interviews and workplace expectations."},
            ]),
            ("FEATURE_HIGHLIGHTS", 4, {"super_heading": "PROGRAM FEATURES", "heading": "What You Can Expect", "subheading": "A professional learning experience from foundation concepts to applied work."}, [
                {"label": "01", "title": "Concept-to-Lab Delivery", "description": "Every major topic is reinforced through application."},
                {"label": "02", "title": "Practice Assignments", "description": "Build confidence through progressive tasks."},
                {"label": "03", "title": "Project Discussion", "description": "Learn to explain design decisions and troubleshoot logically."},
                {"label": "04", "title": "Batch Flexibility", "description": "Ask about current weekday, weekend and fast-track schedules."},
            ]),
            ("PROGRAM_STRUCTURE", 5, {"super_heading": "HOW YOU LEARN", "heading": "A Clear Path from Fundamentals to Application", "subheading": "The exact sequence varies by program, while the learning method remains consistent."}, [
                {"label": "01", "title": "Foundation", "description": "Understand components, terminology, safety and core principles."},
                {"label": "02", "title": "Tool Familiarisation", "description": "Learn the relevant hardware and software environment."},
                {"label": "03", "title": "Guided Application", "description": "Complete wiring, programming or design exercises."},
                {"label": "04", "title": "Integration", "description": "Combine multiple topics in realistic scenarios."},
                {"label": "05", "title": "Career Preparation", "description": "Review projects, technical questions and professional presentation."},
            ]),
            ("FAQ", 6, {"heading": "Course Selection Questions", "subheading": "Contact our counsellor if you need help choosing between programs."}, [
                {"question": "Can freshers join?", "answer": "Yes. The programs begin with the required fundamentals and progress in a structured manner."},
                {"question": "Can working professionals enrol?", "answer": "Yes. Ask the institute about currently available weekday, weekend and fast-track batches."},
                {"question": "Will I receive a detailed syllabus?", "answer": "Yes. Available course syllabi can be viewed from the individual course pages."},
            ]),
        ]
        for section_type, order, values, items in sections:
            section = CourseSection.objects.create(
                module=None, section_type=section_type, order=order, is_active=True,
                **self.fit(CourseSection, values),
            )
            CourseContent.objects.bulk_create([
                CourseContent(section=section, order=index, is_active=True, **self.fit(CourseContent, item))
                for index, item in enumerate(items, start=1)
            ])

    def attach_syllabus(self, module, filename):
        source = Path(__file__).resolve().parents[4] / "client data" / filename
        if not source.exists():
            self.stdout.write(self.style.WARNING(f"Syllabus not found: {source}"))
            return
        if module.syllabus and Path(module.syllabus.path).exists():
            return
        with source.open("rb") as stream:
            module.syllabus.save(filename, File(stream), save=True)

    def seed_courses(self):
        course_data = [
            {
                "title": "PLC & SCADA Training", "slug": "plc-scada-training", "order": 1,
                "tagline": "Multi-brand PLC programming, HMI, SCADA, drives and industrial control practice.",
                "syllabus": "NEW PLC SCADA Syllabus Updated.pdf",
                "overview": "Build a complete foundation in industrial control systems through electrical basics, controller programming, visualisation, motion and drive applications.",
                "subjects": [
                    ("Electrical Control Fundamentals", "NO/NC devices, switches, indicators, relays, contactors, starters, timers, sensors, wiring methods, sinking/sourcing and PLC connections.", "Relays,Contactors,Sensors,Control circuits"),
                    ("Allen-Bradley PLC", "MicroLogix 1400 programming with RSLogix 500, RSLinx Classic and RSLogix Emulate 500.", "MicroLogix,RSLogix,RSLinx"),
                    ("Siemens PLC", "S7-1200 series hardware and programming in TIA Portal.", "S7-1200,TIA Portal"),
                    ("Mitsubishi PLC", "FX5U platform programming and diagnostics using GX Works3.", "FX5U,GX Works3"),
                    ("Delta PLC", "DVP series PLC programming using WPLSoft.", "Delta DVP,WPLSoft"),
                    ("SCADA", "Supervisory monitoring and visualisation using FactoryTalk View.", "FactoryTalk View,Tags,Alarms,Trends"),
                    ("HMI", "Operator-interface development for Siemens KTP700 Basic in TIA Portal.", "KTP700,HMI,TIA Portal"),
                    ("VFD Applications", "Configuration concepts for PowerFlex 525 and Modbus-enabled drive applications.", "PowerFlex 525,VFD,Modbus"),
                    ("Servo & Stepper Systems", "Motion-control fundamentals using Mitsubishi servo and stepper-drive applications.", "Servo,Stepper,Motion control"),
                    ("Advanced Platforms", "Introduction to Studio 5000 Logix Designer for Allen-Bradley systems.", "Studio 5000,Logix Designer"),
                ],
            },
            {
                "title": "EPLAN Electrical Design", "slug": "eplan-electrical-design", "order": 2,
                "tagline": "Professional electrical schematics, panel documentation, reports and calculations in EPLAN Electric P8.",
                "syllabus": "Eplan UPDATED Syllabus.pdf",
                "overview": "Learn a structured electrical-design workflow from project setup and schematics through component data, panel planning, reports and engineering calculations.",
                "subjects": [
                    ("Project Setup & Basic Commands", "Navigate the EPLAN environment and create organised engineering projects.", "EPLAN Electric P8,Projects"),
                    ("Schematics & Interruption Points", "Create readable power and control drawings with consistent cross-referencing.", "Schematics,Cross-references"),
                    ("Symbols, Libraries & Macros", "Use standard symbols, create custom symbols and build reusable symbol and page macros.", "Symbols,Libraries,Macros"),
                    ("Plot Frames & Templates", "Create and edit plot frames, templates and project text conventions.", "Plot frames,Templates"),
                    ("Wire & Device Data", "Manage wire colours, ferruling, identifiers, PLC boxes and component properties.", "Ferruling,Identifiers,PLC boxes"),
                    ("Parts & Data Portal", "Create, edit and assign part numbers, including data added through the EPLAN Data Portal.", "Parts,Data Portal"),
                    ("Data Exchange & Revision", "Convert between AutoCAD and EPLAN, create backups and manage revision markers.", "AutoCAD,Backup,Revision"),
                    ("Reports & Excel Output", "Generate reports and export relevant engineering data to Excel.", "Reports,Excel"),
                    ("Engineering Calculations", "Perform load and wire calculations, component selection and busbar selection.", "Load calculation,Wire calculation,Busbar"),
                    ("Panel Engineering", "Understand panel types, arrangement, power distribution, power circuits and control circuits.", "Panel design,Power circuits,Control circuits"),
                ],
            },
            {
                "title": "Industrial Robotics", "slug": "industrial-robotics", "order": 3,
                "tagline": "Core robot operation, programming, safety and cell-integration skills for automation environments.",
                "syllabus": None,
                "overview": "Develop a practical understanding of industrial robot systems, safe operation, coordinate frames, motion instructions, end effectors and basic cell integration.",
                "subjects": [
                    ("Robot Safety", "Understand operating zones, interlocks, safe states and responsible teach-mode practices.", "Safety,Interlocks"),
                    ("Robot Anatomy", "Identify axes, joints, controllers, teach pendants and common end effectors.", "Axes,Controller,Teach pendant"),
                    ("Coordinate Systems", "Work with joint, world, tool and user coordinate frames.", "Frames,TCP,Coordinates"),
                    ("Motion Programming", "Create and refine point-to-point and linear motion sequences.", "PTP,Linear motion"),
                    ("I/O Integration", "Use digital signals to coordinate robot actions with machines and fixtures.", "Digital I/O,Handshake"),
                    ("Cell Applications", "Study pick-and-place, machine tending and material-handling workflows.", "Pick and place,Machine tending"),
                ],
            },
        ]
        Module.objects.exclude(slug__in=[c["slug"] for c in course_data]).update(is_active=False)
        for course in course_data:
            module, _ = Module.objects.update_or_create(
                slug=course["slug"],
                defaults={"title": course["title"], "tagline": course["tagline"], "order": course["order"], "is_active": True},
            )
            if course["syllabus"]:
                self.attach_syllabus(module, course["syllabus"])
            CourseSection.objects.filter(module=module).delete()
            self.create_course_sections(module, course)

    def create_course_sections(self, module, course):
        title = course["title"]
        sections = [
            ("PAGE_BANNER", 1, {"super_heading": "PROFESSIONAL TRAINING PROGRAM", "heading": title, "subheading": module.tagline, "primary_button_text": "Enquire Now", "primary_button_url": "/contact#enquiry-form", "secondary_button_text": "View Curriculum", "secondary_button_url": "#module-subjects-covered"}, []),
            ("COURSE_OVERVIEW", 2, {"super_heading": "COURSE OVERVIEW", "heading": "Learn the Skills Behind", "highlighted_heading": title, "subheading": course["overview"], "overlay_title": "Application-focused training", "overlay_description": "Concepts, guided exercises and professional workflows."}, [
                {"title": "Understand", "description": "Build a clear foundation in the relevant systems and terminology."},
                {"title": "Practise", "description": "Complete progressive tasks with trainer guidance."},
                {"title": "Integrate", "description": "Connect individual skills in realistic applications."},
                {"title": "Present", "description": "Explain your work clearly in projects and interviews."},
            ]),
            ("KEY_HIGHLIGHTS", 3, {"super_heading": "PROGRAM HIGHLIGHTS", "heading": "A Practical Route to", "highlighted_heading": "Professional Capability", "subheading": "Designed for learners who want usable, demonstrable skills."}, [
                {"label": "01", "title": "Hands-on Lab Practice", "description": "Reinforce learning through structured exercises."},
                {"label": "02", "title": "Application Case Studies", "description": "Connect topics to industrial workflows and problems."},
                {"label": "03", "title": "Interview Preparation", "description": "Review concepts, projects and common technical questions."},
                {"label": "04", "title": "Resume Guidance", "description": "Present training, projects and skills professionally."},
                {"label": "05", "title": "Placement Assistance", "description": "Receive support in identifying suitable opportunities; selection depends on learner performance and employer requirements."},
            ]),
            ("SUBJECTS_COVERED", 4, {"super_heading": "DETAILED CURRICULUM", "heading": "Subjects and Tools", "highlighted_heading": "Covered", "subheading": "The current syllabus is organised into practical, progressive learning units."}, [
                {"title": name, "description": description, "tags": tags}
                for name, description, tags in course["subjects"]
            ]),
            ("ELIGIBILITY_CRITERIA", 5, {"super_heading": "WHO SHOULD JOIN", "heading": "Eligibility and", "highlighted_heading": "Recommended Background", "subheading": "The program is suitable for motivated learners who want to build or strengthen practical automation skills."}, [
                {"title": "Students and Fresh Graduates", "description": "Diploma, BE, BTech or equivalent learners from electrical, electronics, instrumentation, mechanical and related disciplines."},
                {"title": "Technicians and Maintenance Professionals", "description": "Professionals seeking structured automation, controls or design upskilling."},
                {"title": "Career Switchers", "description": "Learners with relevant technical fundamentals who are prepared for regular practice."},
                {"title": "No Prior Software Mastery Required", "description": "Training progresses from the required foundations to application-level work."},
            ]),
            ("FEES_BATCH_DETAILS", 6, {"super_heading": "ADMISSIONS", "heading": "Fees and", "highlighted_heading": "Batch Details", "subheading": "Course fees and schedules depend on the selected batch format and current admissions calendar.", "primary_button_text": "Request Current Details", "primary_button_url": "/contact#enquiry-form"}, [
                {"label": "Schedule", "title": "Weekday and Weekend Options", "description": "Contact the institute for the latest available timings."},
                {"label": "Format", "title": "Instructor-Led Practical Training", "description": "Classroom explanation supported by guided lab work."},
                {"label": "Fees", "title": "Shared During Counselling", "description": "Receive the current fee, payment and batch information directly from the institute."},
                {"label": "Support", "title": "Career-Readiness Assistance", "description": "Includes technical revision, resume guidance and interview preparation."},
            ]),
            ("FACULTY", 7, {"super_heading": "TRAINER SUPPORT", "heading": "Learn with", "highlighted_heading": "Practical Guidance", "subheading": "Trainers support concept clarity, correct practice and systematic troubleshooting."}, [
                {"label": "Program Mentor", "title": "Industrial Automation Trainer", "description": "Guidance across concepts, lab exercises, projects and technical preparation.", "tags": title},
            ]),
            ("PAST_RESULTS", 8, {"super_heading": "LEARNING OUTCOMES", "heading": "What You Should Be Able to", "highlighted_heading": "Demonstrate", "subheading": "Successful completion requires attendance, practice and satisfactory performance in assigned activities."}, [
                {"label": "01", "title": "Explain Core Concepts", "description": "Use correct terminology and sound engineering reasoning."},
                {"label": "02", "title": "Complete Practical Tasks", "description": "Follow a structured workflow with attention to safety and accuracy."},
                {"label": "03", "title": "Troubleshoot Systematically", "description": "Identify likely causes, verify observations and document corrective action."},
                {"label": "04", "title": "Discuss Project Work", "description": "Present objectives, design decisions, results and lessons clearly."},
            ]),
            ("TESTIMONIALS", 9, {"super_heading": "PROGRAM EXPERIENCE", "heading": "Learning Built Around", "highlighted_heading": "Practice", "subheading": "The course structure gives learners repeated opportunities to apply and explain what they learn."}, [
                {"title": "Step-by-step progression", "description": "Start with the required foundations and build toward integrated tasks.", "question": "Structured learning", "answer": "Course approach"},
                {"title": "Trainer-guided exercises", "description": "Receive feedback while developing correct technical habits.", "question": "Practical support", "answer": "Course approach"},
                {"title": "Career-focused revision", "description": "Connect course topics with projects and technical interview discussions.", "question": "Professional readiness", "answer": "Course approach"},
            ]),
            ("CTA", 10, {"super_heading": "READY TO BEGIN?", "heading": f"Enquire About {title}", "subheading": "Speak with the institute to review eligibility, the current syllabus, fees and available batch timings.", "primary_button_text": "Send an Enquiry", "primary_button_url": "/contact#enquiry-form", "secondary_button_text": "Call the Institute", "secondary_button_url": f"tel:+91{PHONE.replace(' ', '')}"}, []),
        ]
        for section_type, order, values, items in sections:
            self.replace_course_section(module, section_type, order, values, items)

    def seed_announcements(self):
        NewsItem.objects.all().delete()
        AnnouncementCategory.objects.all().delete()
        admissions = AnnouncementCategory.objects.create(name="Admissions", slug="admissions", is_active=True)
        courses = AnnouncementCategory.objects.create(name="Courses", slug="courses", is_active=True)
        updates = AnnouncementCategory.objects.create(name="Institute Updates", slug="institute-updates", is_active=True)
        NewsItem.objects.bulk_create([
            NewsItem(
                title="Admissions Open for Upcoming Automation Training Batches",
                slug="admissions-open-automation-training",
                short_description="Applications are open for upcoming PLC & SCADA, EPLAN and industrial robotics training batches.",
                full_description="Prospective learners can contact the institute for counselling, eligibility guidance, current fees and available weekday or weekend batch schedules. Seats are allocated according to lab capacity and confirmed enrolment.",
                category=admissions, publish_date=date(2026, 9, 29), is_active=True,
            ),
            NewsItem(
                title="Updated PLC & SCADA Curriculum Available",
                slug="updated-plc-scada-curriculum",
                short_description="The course curriculum covers electrical controls, four PLC platforms, HMI, SCADA, drives and motion fundamentals.",
                full_description="The PLC & SCADA course page now includes the detailed training scope for Allen-Bradley, Siemens, Mitsubishi and Delta platforms, together with HMI, FactoryTalk View SCADA, VFD, servo and stepper applications.",
                category=courses, publish_date=date(2026, 9, 29), is_active=True,
            ),
            NewsItem(
                title="EPLAN Electrical Design Syllabus Published",
                slug="eplan-electrical-design-syllabus",
                short_description="Review the updated EPLAN curriculum covering schematics, macros, reports, calculations and panel documentation.",
                full_description="The EPLAN program includes project setup, symbols and libraries, plot frames, templates, macros, parts data, revision workflows, report generation, calculations and panel engineering topics.",
                category=courses, publish_date=date(2026, 9, 29), is_active=True,
            ),
            NewsItem(
                title="Free Course Counselling and Lab Overview",
                slug="free-course-counselling-lab-overview",
                short_description="Book a conversation with the institute to choose the right program and understand the practical training approach.",
                full_description="Learners and parents may contact the institute to discuss course selection, prerequisites, lab practice, schedules and career-readiness support before enrolment.",
                category=updates, publish_date=date(2026, 9, 29), is_active=True,
            ),
        ])
