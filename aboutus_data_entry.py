import os
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ns2_infotech_backend.settings')
django.setup()

from aboutus.models import PageSection, SectionContent


def populate_aboutus():
    print('Deleting existing About Us sections...')
    PageSection.objects.all().delete()

    print('Creating About Us page data from provided JSON...')

    # HERO Section
    hero = PageSection.objects.create(
        section_type='HERO',
        order=1,
        is_active=True,
        super_heading='ABOUT US',
        heading='Empowering Future Automation Experts',
        subheading='NS-2 Infotech is committed to bridging the gap between industry demands and skilled professionals through cutting-edge automation training.',
        primary_button_text='Get In Touch',
        primary_button_url='#contact',
    )
    # Note: background_image='sections/about-hero-bg.webp' - file not found, skipping

    # WHO_WE_ARE Section
    who_we_are = PageSection.objects.create(
        section_type='WHO_WE_ARE',
        order=2,
        is_active=True,
        super_heading='WHO WE ARE',
        heading='About NS-2 Infotech',
        subheading='Modern Institute of Automation',
        overview_text='Founded in 2018, NS-2 Infotech has trained 5000+ students across PLC, SCADA, DCS, and Industrial Automation domains. We are dedicated to providing industry-aligned training with 100% placement support.',
    )
    # Note: primary_image='sections/who-we-are.webp' - file not found, skipping
    SectionContent.objects.create(section=who_we_are, order=1, label='Industry-Aligned Curriculum')
    SectionContent.objects.create(section=who_we_are, order=2, label='Hands-On Practical Training')
    SectionContent.objects.create(section=who_we_are, order=3, label='100% Placement Assistance')
    SectionContent.objects.create(section=who_we_are, order=4, label='Expert Faculty from Industry')

    # DIRECTOR_MESSAGE Section
    director_message = PageSection.objects.create(
        section_type='DIRECTOR_MESSAGE',
        order=3,
        is_active=True,
        super_heading='LEADERSHIP',
        heading='Message from the Director',
        subheading='Mr. John Doe',
        overview_text='Founder & Director, NS-2 Infotech',
    )
    # Note: primary_image='sections/director-photo.webp' - file not found, skipping
    SectionContent.objects.create(
        section=director_message,
        order=1,
        label='Director Message',
        description='When I founded NS-2 Infotech, my vision was clear — to create an institution that doesn\'t just teach, but transforms lives. Every student who walks through our doors carries a dream, and we take the responsibility of nurturing that dream very seriously.\n\nOur curriculum is designed in collaboration with industry leaders to ensure our students are job-ready from day one. We believe in learning by doing, and our state-of-the-art labs reflect that commitment.\n\nI invite you to be part of this journey. Together, let\'s build the future of automation.'
    )

    # OUR_STORY Section
    our_story = PageSection.objects.create(
        section_type='OUR_STORY',
        order=4,
        is_active=True,
        super_heading='OUR JOURNEY',
        heading='The NS-2 Infotech Story',
        subheading='From a small training center to a leading automation institute — here\'s how we grew.',
    )
    SectionContent.objects.create(section=our_story, order=1, label='2018', title='The Beginning', description='NS-2 Infotech was founded with a mission to provide quality automation training to aspiring engineers. Started with just 2 courses and 15 students.')
    SectionContent.objects.create(section=our_story, order=2, label='2019', title='First Placement Batch', description='Successfully placed our first batch of 30 students in top automation companies. Expanded our course catalog to 6 specialized programs.')
    SectionContent.objects.create(section=our_story, order=3, label='2021', title='Infrastructure Expansion', description='Moved to a larger campus with dedicated PLC & SCADA labs, a digital library, and modern classrooms to support growing student enrollment.')
    SectionContent.objects.create(section=our_story, order=4, label='2023', title='1000+ Students Placed', description='Crossed the milestone of 1000+ successful placements. Partnered with 50+ companies for campus recruitment drives.')
    SectionContent.objects.create(section=our_story, order=5, label='2025', title='National Recognition', description='Recognized as one of the top automation training institutes in India. Launched corporate training and internship programs.')

    # VISION_MISSION Section
    vision_mission = PageSection.objects.create(
        section_type='VISION_MISSION',
        order=5,
        is_active=True,
        heading='What drives us forward every single day',
    )
    SectionContent.objects.create(section=vision_mission, order=1, label='Our Vision', description='To be the most trusted and innovative automation training institute in India, producing industry-ready professionals who lead the future of industrial automation.')
    SectionContent.objects.create(section=vision_mission, order=2, label='Our Mission', description='To provide world-class, hands-on automation training with industry-aligned curriculum, state-of-the-art infrastructure, and guaranteed placement support — empowering every student to achieve their career goals.')
    SectionContent.objects.create(section=vision_mission, order=3, label='Core Values', description='Excellence in Education: We continuously update our curriculum to match industry standards.\n\nStudent-First Approach: Every decision we make puts our students\' success at the center.\n\nIntegrity & Transparency: We maintain honest communication with students and parents.\n\nInnovation: We embrace new technologies and teaching methods.')

    # EXPERTISE Section
    expertise = PageSection.objects.create(
        section_type='EXPERTISE',
        order=6,
        is_active=True,
        super_heading='WHY CHOOSE US',
        heading='What Makes Us Different',
        subheading='Our unique approach to automation training sets us apart from the rest.',
    )
    SectionContent.objects.create(section=expertise, order=1, label='Small Batch Sizes', description='Maximum 15 students per batch ensuring personalized attention and hands-on practice for every student.')
    SectionContent.objects.create(section=expertise, order=2, label='Industry Expert Faculty', description='All our trainers have 10+ years of industry experience in automation and are certified professionals.')
    SectionContent.objects.create(section=expertise, order=3, label='Live Project Training', description='Students work on real industrial projects during training, building a strong portfolio before placement.')
    SectionContent.objects.create(section=expertise, order=4, label='100% Placement Record', description='We have maintained a 100% placement record for the last 3 consecutive years with top MNCs.')
    SectionContent.objects.create(section=expertise, order=5, label='Lifetime Access to Resources', description='Students get lifetime access to course materials, recorded sessions, and alumni network support.')
    SectionContent.objects.create(section=expertise, order=6, label='Flexible Learning Options', description='Choose from weekday, weekend, and online batches to fit training around your schedule.')

    # ACCREDITATIONS Section
    accreditations = PageSection.objects.create(
        section_type='ACCREDITATIONS',
        order=7,
        is_active=True,
        super_heading='TRUST & RECOGNITION',
        heading='Accreditations & Affiliations',
        subheading='We are proudly recognized and affiliated with leading industry boards and organizations.',
    )
    SectionContent.objects.create(section=accreditations, order=1, label='ISO 9001:2015 Certified', title='Quality Management', description='Our institute is ISO certified, ensuring world-class quality standards in education and training delivery.')
    SectionContent.objects.create(section=accreditations, order=2, label='NSDC Partner', title='Skill Development', description='Affiliated with the National Skill Development Corporation for recognized skill certification programs.')
    SectionContent.objects.create(section=accreditations, order=3, label='Siemens Authorized Training Center', title='Technology Partner', description='Official Siemens training partner providing certified courses on Siemens PLC, HMI, and SCADA systems.')

    # INFRASTRUCTURE Section
    infrastructure = PageSection.objects.create(
        section_type='INFRASTRUCTURE',
        order=8,
        is_active=True,
        super_heading='OUR FACILITIES',
        heading='World-Class Infrastructure',
        subheading='Our state-of-the-art facilities are designed to provide the best learning experience.',
    )
    SectionContent.objects.create(section=infrastructure, order=1, label='Smart Classrooms', title='Air-Conditioned & Digital', description='Fully air-conditioned classrooms equipped with projectors, smart boards, and high-speed internet for interactive learning.')
    SectionContent.objects.create(section=infrastructure, order=2, label='PLC & SCADA Lab', title='Hands-On Practice', description='Dedicated automation lab with Siemens, Allen Bradley, and Mitsubishi PLCs for real-world hands-on training.')
    SectionContent.objects.create(section=infrastructure, order=3, label='Digital Library', title='24/7 Access', description='Extensive digital library with e-books, video lectures, technical papers, and reference manuals accessible anytime.')
    SectionContent.objects.create(section=infrastructure, order=4, label='Computer Lab', title='Latest Software & Tools', description='High-performance computers with licensed simulation software including TIA Portal, RSLogix, and MATLAB.')
    SectionContent.objects.create(section=infrastructure, order=5, label='Seminar Hall', title='Events & Workshops', description='200-seater seminar hall for guest lectures, industry workshops, and placement drives.')
    SectionContent.objects.create(section=infrastructure, order=6, label='Student Lounge', title='Relax & Collaborate', description='Comfortable lounge area for students to relax, collaborate on projects, and network with peers.')

    # GALLERY Section
    gallery = PageSection.objects.create(
        section_type='GALLERY',
        order=9,
        is_active=True,
        super_heading='LIFE AT NS-2',
        heading='Campus Gallery',
        subheading='Our vibrant campus in pictures',
        overview_text='Experience the energy and enthusiasm that defines life at NS-2 Infotech.',
    )
    # Note: primary_image='sections/campus-banner.webp' - file not found, skipping
    SectionContent.objects.create(section=gallery, order=1, label='Training Session')
    SectionContent.objects.create(section=gallery, order=2, label='Lab Practice')
    SectionContent.objects.create(section=gallery, order=3, label='Placement Drive')
    SectionContent.objects.create(section=gallery, order=4, label='Workshop')
    SectionContent.objects.create(section=gallery, order=5, label='Convocation')
    SectionContent.objects.create(section=gallery, order=6, label='Industrial Visit')

    # OUR_TEAM Section
    our_team = PageSection.objects.create(
        section_type='OUR_TEAM',
        order=10,
        is_active=True,
        heading='Meet Our',
        subheading='Expert Team',
        overview_text='Our team of experienced professionals is dedicated to shaping the future of automation education.',
    )
    SectionContent.objects.create(section=our_team, order=1, label='Mr. Rajesh Kumar', title='Senior PLC Trainer', description='12+ years of experience in Siemens and Allen Bradley PLC programming.', person_name='Rajesh Kumar', person_role='Senior PLC Trainer', linkedin_url='https://linkedin.com/in/example')
    SectionContent.objects.create(section=our_team, order=2, label='Ms. Priya Sharma', title='SCADA & HMI Expert', description='Specialized in Wonderware and WinCC SCADA systems with 8+ years of industrial experience.', person_name='Priya Sharma', person_role='SCADA & HMI Expert', linkedin_url='https://linkedin.com/in/example')
    SectionContent.objects.create(section=our_team, order=3, label='Mr. Amit Patel', title='DCS & Instrumentation', description='Former Honeywell engineer with deep expertise in DCS and process control systems.', person_name='Amit Patel', person_role='DCS & Instrumentation', linkedin_url='https://linkedin.com/in/example')

    print('✅ About Us data loaded successfully from provided JSON.')


if __name__ == '__main__':
    populate_aboutus()
