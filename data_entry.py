import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ns2_infotech_backend.settings')
django.setup()

from django.contrib.contenttypes.models import ContentType
from core.models import Menu, SubMenu, FooterSection, FooterItem, CompanyProfile, SiteStatistic, Announcement, SocialLink
from homepage.models import PageSection, SectionContent

def populate():
    print("🚀 Starting Professional MIA Data Entry...")

    # 1. Company Profile (The base content object)
    company, _ = CompanyProfile.objects.get_or_create(
        name="Modern Institute of Automation",
        defaults={
            'tagline': "Excellence in Industrial Training",
            'description': "MIA is India's leading training center for PLC, SCADA, Robotics, and IoT. We bridge the gap between engineering theory and industrial practice.",
            'email': "info@miaautomation.com",
            'phone': "+91 90751 02234",
            'address': "MIA Tower, College Road, Nashik, Maharashtra 422005",
            'copyright_text': "© 2026 MIA. All rights reserved.",
        }
    )
    company_ct = ContentType.objects.get_for_model(CompanyProfile)

    # 2. Navbar Structure
    print("📍 Populating Professional Navbar...")
    Menu.objects.all().delete()
    m_home = Menu.objects.create(text="Home", url="/", order=1)
    m_about = Menu.objects.create(text="Who We Are", url="/about", order=2)
    m_courses = Menu.objects.create(text="Specialized Courses", url="/courses", order=3)
    SubMenu.objects.create(menu=m_courses, text="PLC & SCADA Training", url="/courses/plc-scada", order=1)
    SubMenu.objects.create(menu=m_courses, text="Industrial Robotics", url="/courses/robotics", order=2)
    SubMenu.objects.create(menu=m_courses, text="EPLAN Designing", url="/courses/eplan", order=3)
    m_placement = Menu.objects.create(text="Placement Cell", url="/placements", order=4)
    m_contact = Menu.objects.create(text="Enroll Now", url="/contact", order=5, is_button=True)

    # 3. Footer Structure
    print("📂 Populating Professional Footer...")
    FooterSection.objects.all().delete()
    fs_explore = FooterSection.objects.create(title="Explore MIA", order=1)
    FooterItem.objects.create(section=fs_explore, text="Our Story", url="/about", order=1)
    FooterItem.objects.create(section=fs_explore, text="Student Success", url="/placements", order=2)
    FooterItem.objects.create(section=fs_explore, text="News & Updates", url="/news", order=3)

    fs_courses = FooterSection.objects.create(title="Top Modules", order=2)
    FooterItem.objects.create(section=fs_courses, text="Siemens TIA Portal", url="/courses/siemens", order=1)
    FooterItem.objects.create(section=fs_courses, text="Allen Bradley PLC", url="/courses/ab", order=2)
    FooterItem.objects.create(section=fs_courses, text="Industry 4.0", url="/courses/iot", order=3)

    # 4. Hero & Stats
    print("🌟 Populating Hero Content & Statistics...")
    Announcement.objects.all().delete()
    Announcement.objects.create(icon="🎓", text="New Batch for PLC SCADA starting from 1st May - Limited Seats!", order=1)
    Announcement.objects.create(icon="🚀", text="MIA Students placed in Siemens and ABB last week! Check Placements.", order=2)

    SiteStatistic.objects.all().delete()
    SiteStatistic.objects.create(icon="⭐", value="4.9/5", label="Rated by", sub_label="5K+ Engineers", order=1)
    SiteStatistic.objects.create(icon="🏢", value="150+", label="Corporate", sub_label="Hiring Partners", order=2)

    # 5. Homepage Sections
    print("🏠 Populating Full Homepage Content...")
    PageSection.objects.all().delete()
    
    # 1. HERO
    hero = PageSection.objects.create(
        section_type='HERO', order=1, content_type=company_ct, object_id=company.id,
        label="Homepage Hero Header",
        super_heading="NEXT-GEN INDUSTRIAL TRAINING",
        heading="Master Industrial Automation with Industry Experts",
        subheading="Learn PLC, SCADA, HMI, and Robotics with 100% hands-on practicals on industrial hardware. Join the 5,000+ engineers who transformed their careers with MIA.",
        primary_button_text="Explore Our Courses", primary_button_url="/courses",
        secondary_button_text="Watch Free Demo", secondary_button_url="/demo"
    )
    # Floating Stats for Hero (if used in components)
    SectionContent.objects.create(section=hero, label="5000+", title="Engineers Trained", order=1)
    SectionContent.objects.create(section=hero, label="100%", title="Practical Approach", order=2)

    # 2. OVERVIEW
    overview = PageSection.objects.create(
        section_type='OVERVIEW', order=2, content_type=company_ct, object_id=company.id,
        super_heading="WHY MIA?",
        heading="Bridging the Gap Between College and Industry",
        overview_text="Hands-on training with Siemens, Delta, and Allen Bradley hardware.",
        primary_button_text="Learn More About Us", primary_button_url="/about"
    )
    SectionContent.objects.create(section=overview, text="Authorized Certification Provider", order=1)
    SectionContent.objects.create(section=overview, text="Individual PC and Hardware per Student", order=2)
    SectionContent.objects.create(section=overview, text="Lifetime Placement Assistance", order=3)

    # 3. WHY CHOOSE US
    why_us = PageSection.objects.create(
        section_type='WHY_CHOOSE_US', order=3, content_type=company_ct, object_id=company.id,
        heading="Why Aspiring Automation Engineers Trust Us"
    )
    SectionContent.objects.create(section=why_us, title="Expert Mentors", description="Learn from veterans with 15+ years of industrial experience.", order=1)
    SectionContent.objects.create(section=why_us, title="Job Guarantee", description="Access to premium placement cell with top MNC tie-ups.", order=2)
    SectionContent.objects.create(section=why_us, title="Flexible Timing", description="Evening and weekend batches optimized for working professionals.", order=3)

    # 4. SERVICES (Courses)
    services = PageSection.objects.create(
        section_type='OUR_SERVICES', order=4, content_type=company_ct, object_id=company.id,
        heading="Our Specialized Training Programs",
        subheading="Industry-standard modules designed to make you a complete automation engineer."
    )
    SectionContent.objects.create(section=services, title="PLC-SCADA Mastery", description="Covers 5 brands of PLC and 3 SCADA systems.", order=1)
    SectionContent.objects.create(section=services, title="Electrical Design (EPLAN)", description="Learn professional industrial panel designing.", order=2)
    SectionContent.objects.create(section=services, title="Robotics & IIoT", description="Master Fanuc and KUKA programming with IoT integration.", order=3)

    # 5. PLACED STUDENTS
    placed = PageSection.objects.create(
        section_type='OUR_PLACED_STUDENTS', order=5, content_type=company_ct, object_id=company.id,
        heading="MIA Pride: Recent Placements",
        subheading="Our students are currently working in some of the world's leading engineering firms."
    )
    SectionContent.objects.create(section=placed, title="Aditya Deshmukh", text="Siemens Ltd.", description="MIA is the best place to gain hardware confidence.", order=1)
    SectionContent.objects.create(section=placed, title="Priya Sharma", text="ABB Global", description="The SCADA training helped me crack the toughest technical rounds.", order=2)

    # 6. TESTIMONIALS
    testimonials = PageSection.objects.create(
        section_type='TESTIMONIALS', order=6, content_type=company_ct, object_id=company.id,
        heading="Voices of Success"
    )
    SectionContent.objects.create(section=testimonials, question="Wade Warren", answer="MIA changed my career path. I went from unemployed to a Senior Automation Engineer in 6 months.", order=1)

    # 7. FAQ
    faq = PageSection.objects.create(
        section_type='FAQ', order=7, content_type=company_ct, object_id=company.id,
        heading="Common Questions", subheading="Everything you need to know about our courses."
    )
    SectionContent.objects.create(section=faq, question="Do I need a strong coding background?", answer="No, we start from basic electrical relay logic and build up to advanced programming.", order=1)
    SectionContent.objects.create(section=faq, question="Is the certificate valid globally?", answer="Yes, MIA certificates are industry-recognized across the globe.", order=2)

    # 8. CONTACT CTA
    PageSection.objects.create(
        section_type='CONTACT_US', order=8, content_type=company_ct, object_id=company.id,
        heading="Speak with Our Career Experts",
        subheading="Ready to visit our lab? Book a free walk-through session today."
    )

    # 9. FINAL CTA
    PageSection.objects.create(
        section_type='CTA', order=9, content_type=company_ct, object_id=company.id,
        heading="Kickstart Your Automation Career",
        subheading="Join the next batch and secure your future in Industry 4.0.",
        primary_button_text="Get Started Now", primary_button_url="/enroll"
    )

    print("✅ Full industry-level data populated successfully!")

if __name__ == '__main__':
    populate()
