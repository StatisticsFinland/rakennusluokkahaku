def init_test_db(app):
    from src import building_data, classifier
    from src.models import db, Answer, AnswerQuestion, Attribute, BuildingClass, ClassAttribute, Session, QuestionGroup

    with app.app_context():
        # Clear all tables
        [db.session.remove(x) for x in Answer.query.all()]
        [db.session.remove(x) for x in AnswerQuestion.query.all()]
        [db.session.remove(x) for x in Attribute.query.all()]
        [db.session.remove(x) for x in BuildingClass.query.all()]
        [db.session.remove(x) for x in ClassAttribute.query.all()]
        [db.session.remove(x) for x in Session.query.all()]
        [db.session.remove(x) for x in QuestionGroup.query.all()]

        # Initialize question_group table
        db.session.add(QuestionGroup(grouping_key='1',
                                     group_name='WC:t',
                                     group_question='{"fi":"Minkälaisia WC-tiloja rakennuksessa on?", "sv":"[Svenska]Hurudana toaletter innehåller byggnaden?", "en":"[English]What kinds of restrooms does the space contain?"}'))
        db.session.commit()

        # Initialize attribute table
        group = QuestionGroup.query.first()
        attributes = [Attribute(id_='1',
                                name='{"fi":"Asunnot", "sv":"[Svenska]Asunnot", "en":"[English]Asunnot"}',
                                question='{"fi":"Onko rakennuksessa asunnot?", "sv":"[Svenska]Onko rakennuksessa asunnot?", "en":"[English]Onko rakennuksessa asunnot?"}',
                                active=True,
                                group=None,
                                tooltip='{"fi":"", "en":"", "sv":""}',
                                probability=0.1),
                      Attribute(id_='101',
                                name='{"fi":"Asuinhuone", "sv":"[Svenska]Asuinhuone", "en":"[English]Asuinhuone"}',
                                question='{"fi":"Onko rakennuksessa asuinhuone?", "sv":"[Svenska]Onko rakennuksessa asuinhuone?", "en":"[English]Onko rakennuksessa asuinhuone?"}',
                                active=True,
                                group=None,
                                tooltip='{"fi":"", "en":"", "sv":""}',
                                probability=0.2),
                      Attribute(id_='102',
                                name='{"fi":"Eteinen", "sv":"[Svenska]Eteinen", "en":"[English]Eteinen"}',
                                question='{"fi":"Onko rakennuksessa eteinen?", "sv":"[Svenska]Onko rakennuksessa eteinen?", "en":"[English]Onko rakennuksessa eteinen?"}',
                                active=True,
                                group=None,
                                tooltip='{"fi":"", "en":"", "sv":""}',
                                probability=0.3),
                      Attribute(id_='114',
                                name='{"fi":"WC", "sv":"[Svenska]WC", "en":"[English]WC"}',
                                question='{"fi":"Onko rakennuksessa wc?", "sv":"[Svenska]Onko rakennuksessa wc?", "en":"[English]Onko rakennuksessa wc?"}',
                                group=group,
                                active=False,
                                tooltip='{"fi":"", "en":"", "sv":""}',
                                probability=0.2),
                      Attribute(id_='116',
                                name='{"fi":"WC-pesuhuone", "sv":"[Svenska]WC-pesuhuone", "en":"[English]WC-pesuhuone"}',
                                question='{"fi":"Onko rakennuksessa wc-pesuhuone?", "sv":"[Svenska]Onko rakennuksessa wc-pesuhuone?", "en":"[English]Onko rakennuksessa wc-pesuhuone?"}',
                                group=group,
                                active=False,
                                tooltip='{"fi":"", "en":"", "sv":""}',
                                probability=0.2)]
        db.session.add_all(attributes)

        # Initialize building_classes table
        building_classes = [BuildingClass(class_id='0110',
                                          class_name='Omakotitalot',
                                          class_probability=1.0),
                            BuildingClass(class_id='0111',
                                          class_name='Paritalot',
                                          class_probability=1.0),
                            BuildingClass(class_id='0112',
                                          class_name='Rivitalot',
                                          class_probability=1.0)]
        db.session.add_all(building_classes)

        # Initialize answer table
        db.session.add(Answer(value='yes'))
        db.session.add(Answer(value='no'))
        db.session.add(Answer(value='skip'))

        db.session.commit()

        # Initialize class-attribute table
        db.session.add(ClassAttribute(attribute=attributes[0],
                                      building_class=building_classes[0],
                                      has_attribute=True))
        db.session.add(ClassAttribute(attribute=attributes[0],
                                      building_class=building_classes[1],
                                      has_attribute=True))
        db.session.add(ClassAttribute(attribute=attributes[0],
                                      building_class=building_classes[2],
                                      has_attribute=True))
        db.session.add(ClassAttribute(attribute=attributes[1],
                                      building_class=building_classes[0],
                                      has_attribute=True))
        db.session.add(ClassAttribute(attribute=attributes[1],
                                      building_class=building_classes[1],
                                      has_attribute=True))
        db.session.add(ClassAttribute(attribute=attributes[1],
                                      building_class=building_classes[2],
                                      has_attribute=False))
        db.session.add(ClassAttribute(attribute=attributes[2],
                                      building_class=building_classes[0],
                                      has_attribute=True))
        db.session.add(ClassAttribute(attribute=attributes[2],
                                      building_class=building_classes[1],
                                      has_attribute=False))
        db.session.add(ClassAttribute(attribute=attributes[2],
                                      building_class=building_classes[2],
                                      has_attribute=True))
        db.session.add(ClassAttribute(attribute=attributes[3],
                                      building_class=building_classes[0],
                                      has_attribute=True))
        db.session.add(ClassAttribute(attribute=attributes[3],
                                      building_class=building_classes[1],
                                      has_attribute=False))
        db.session.add(ClassAttribute(attribute=attributes[3],
                                      building_class=building_classes[2],
                                      has_attribute=False))
        db.session.add(ClassAttribute(attribute=attributes[4],
                                      building_class=building_classes[0],
                                      has_attribute=False))
        db.session.add(ClassAttribute(attribute=attributes[4],
                                      building_class=building_classes[1],
                                      has_attribute=True))
        db.session.add(ClassAttribute(attribute=attributes[4],
                                      building_class=building_classes[2],
                                      has_attribute=True))

        # Commit initialization
        db.session.commit()

        # Refresh building data cache
        building_data.load_from_db()

        # Refresh classifier
        classifier.load_from_db()
